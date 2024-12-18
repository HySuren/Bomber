import logging
import threading
import sqlite3
import time
import requests
import gspread
from datetime import datetime, timedelta
from config import PhoneAgregator, services, service_names
from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from utils.validators import validate_and_format_number
from oauth2client.service_account import ServiceAccountCredentials

# Импортируем сервисы
from services.ayurveda_service import send_sms_to_ayurveda
from services.thai_traditions_service import send_sms_to_thai_traditions
from services.dommalera_service import send_sms_to_dommalera
from services.obi_service import send_sms_to_obi
from services.four_lapy_service import send_sms_to_4lapy
from services.beautery_service import send_sms_to_beautery
from services.banki_ru_service import send_sms_to_thai_banki_ru
from services.gazprom_bonus_service import send_sms_to_gazprombonus
from services.kalina_malina_service import send_sms_to_kalina_malina
from services.bykdabaran_service import send_sms_to_bykdabaran

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Constants ---
DB_PATH = "sms_stats.db"
DELIVERY_CHECK_ATTEMPTS = 10
DELIVERY_CHECK_INTERVAL = 6  # seconds


# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print('addadad')
    # Таблица для статистики
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS sms_stats (
            id INTEGER PRIMARY KEY,
            service_name TEXT,
            delivered INTEGER,
            not_delivered INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    # Таблица для конфигурации сервисов
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS config (
            service_name TEXT PRIMARY KEY,
            enabled BOOLEAN NOT NULL CHECK (enabled IN (0, 1))
        )"""
    )

    # Инициализация таблицы config
    for service_id, service_name in service_names.items():
        cursor.execute(
            "INSERT OR IGNORE INTO config (service_name, enabled) VALUES (?, ?)",
            (service_name, 1)
        )

    # Таблица для заблокированных сервисов
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS banned (
            service_name TEXT,
            banned_date DATETIME,
            comment TEXT DEFAULT "Менее 20% дошедших за последние 100 попыток"
        )"""
    )

    conn.commit()
    conn.close()


init_db()


# --- Utility Functions ---
def is_service_enabled(service_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT enabled FROM config WHERE service_name = ?", (service_name,))
        result = cursor.fetchone()
        conn.close()
        return result and result[0] == 1
    except Exception as e:
        logger.error(f"Error checking service status: {e}")
        return False


def check_and_ban_services():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Проверяем каждый сервис
        for service_name in service_names.values():
            cursor.execute(
                """SELECT SUM(delivered), SUM(not_delivered) 
                FROM (
                    SELECT delivered, not_delivered 
                    FROM sms_stats 
                    WHERE service_name = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 100
                )""",
                (service_name,)
            )
            result = cursor.fetchone()
            if result:
                delivered, not_delivered = result
                total_attempts = (delivered or 0) + (not_delivered or 0)

                if total_attempts >= 100:
                    delivery_rate = (delivered or 0) / total_attempts
                    if delivery_rate <= 0.2:
                        # Выключаем сервис
                        cursor.execute("UPDATE config SET enabled = 0 WHERE service_name = ?", (service_name,))
                        # Добавляем запись в banned
                        cursor.execute(
                            "INSERT INTO banned (service_name, banned_date) VALUES (?, ?)",
                            (service_name, datetime.now())
                        )
                        logger.info(f"Service {service_name} has been banned due to low delivery rate.")

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error in check_and_ban_services: {e}")


def reenable_services():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Проверяем сервисы, которые были заблокированы более 12 часов назад
        cursor.execute(
            """SELECT service_name FROM banned 
            WHERE banned_date <= ?""",
            (datetime.now() - timedelta(hours=12),)
        )
        services_to_enable = cursor.fetchall()

        for service_name, in services_to_enable:
            # Включаем сервис обратно
            cursor.execute("UPDATE config SET enabled = 1 WHERE service_name = ?", (service_name,))
            logger.info(f"Service {service_name} has been re-enabled after 12 hours.")

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error in reenable_services: {e}")


# --- Google Sheets Setup ---
def connect_to_google_sheets(sheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("testwork-370710-d0dec9b47b1b.json", scope)
        client = gspread.authorize(creds)
        return client.open(sheet_name).sheet1
    except Exception as e:
        logger.error(f"Google Sheets error: {e}")
        return None


# --- SMS Sending Logic ---
class SmsServiceThread(threading.Thread):
    def __init__(self, service_id, rate_limit, db_path):
        super().__init__()
        self.service_id = str(service_id)
        self.rate_limit = rate_limit
        self.db_path = db_path
        self.last_sent_timestamps = []
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            try:
                now = time.time()
                self.last_sent_timestamps = [ts for ts in self.last_sent_timestamps if now - ts < 60]
                print(1)
                if len(self.last_sent_timestamps) < self.rate_limit:
                    service_name = service_names[self.service_id]
                    if not is_service_enabled(service_name):
                        logger.info(f"Service {service_name} is disabled. Skipping.")
                        time.sleep(5)
                        continue

                    phone_number, activation_id = self.fetch_phone_number()
                    if phone_number:
                        delivered = self.send_sms(phone_number, activation_id)
                        self.update_stats(delivered)
                        self.last_sent_timestamps.append(now)
                else:
                    time.sleep(5)  # Wait before next check
            except Exception as e:
                logger.error(f"Error in service {self.service_id}: {e}")

    def stop(self):
        self.stop_event.set()

    def fetch_phone_number(self):
        """Получение номера телефона и activationId."""
        try:
            response = requests.get(f"{PhoneAgregator.GET_PHONE_NUMBER_URL}?token={PhoneAgregator.API_TOKEN}")
            response.raise_for_status()
            data = response.json()
            return str(data.get('number')), data.get('activationId')
        except Exception as e:
            logger.error(f"Error fetching phone number for service {self.service_id}: {e}")
            return None, None

    def send_sms(self, phone_number, activation_id):
        """Отправка SMS через соответствующий сервис и проверка доставки."""
        try:
            formatted_number = validate_and_format_number(phone_number, service_names[self.service_id])
            logger.info(f"Sending SMS via service {self.service_id} to {formatted_number}, activation_id: {activation_id}")

            # Отправляем SMS через нужный сервис
            if self.service_id == "1":
                result = send_sms_to_dommalera(formatted_number)
            elif self.service_id == "2":
                result = send_sms_to_4lapy(formatted_number)
            elif self.service_id == "3":
                result = send_sms_to_beautery(formatted_number)
            elif self.service_id == "4":
                result = send_sms_to_thai_banki_ru(formatted_number)
            elif self.service_id == "5":
                result = send_sms_to_kalina_malina(formatted_number)
            elif self.service_id == "6":
                result = send_sms_to_thai_traditions(formatted_number)
            elif self.service_id == "7":
                result = send_sms_to_ayurveda(formatted_number)
            elif self.service_id == "8":
                result = send_sms_to_bykdabaran(formatted_number)
            elif self.service_id == "9":
                result = send_sms_to_obi(formatted_number)
            else:
                logger.error(f"Service ID {self.service_id} is not supported.")
                return False

            if result.get("status_code") != 200:
                logger.warning(
                    f"SMS delivery failed during sending phase via service {service_names[str(self.service_id)]}: {result.get('status_code')}")
                return False

            # Проверяем доставку SMS
            return self.check_delivery_status(activation_id)
        except Exception as e:
            logger.error(f"Error sending SMS via service {self.service_id}: {e}")
            return False

    def check_delivery_status(self, activation_id):
        """Проверка доставки SMS по activationId."""
        try:
            for attempt in range(DELIVERY_CHECK_ATTEMPTS):
                response = requests.get(
                    f"{PhoneAgregator.CHECK_SMS_URL}?token={PhoneAgregator.API_TOKEN}&uid={activation_id}")
                logger.info(
                    f"Checking delivery status for activationId {activation_id}, attempt {attempt + 1}: {response.text}")
                response.raise_for_status()
                data = response.json()

                # Если SMS доставлено
                if data.get("success"):
                    return True

                # Если статус "STATUS_WAIT_CODE", ждем перед следующей попыткой
                if data.get("status") == "STATUS_WAIT_CODE":
                    time.sleep(DELIVERY_CHECK_INTERVAL)
            return False  # После 10 попыток считаем SMS недоставленным
        except Exception as e:
            logger.error(f"Error checking delivery status for activationId {activation_id}: {e}")
            return False

    def update_stats(self, delivered):
        """Обновление статистики в базе данных сразу после получения ответа о доставке."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            service_name = service_names.get(self.service_id, "Unknown Service")
            delivered_status = 1 if delivered else 0
            not_delivered_status = 0 if delivered else 1

            # Записываем статистику немедленно после каждого сообщения
            print(service_name)
            print(delivered_status)
            print(not_delivered_status)
            cursor.execute(
                "INSERT INTO sms_stats (service_name, delivered, not_delivered, timestamp) VALUES (?, ?, ?, ?)",
                (service_name, delivered_status, not_delivered_status, datetime.now()),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error updating stats in database: {e}")


# --- Report Generation ---
def generate_report(sheet, interval_minutes):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=interval_minutes)
        cursor.execute(
            """SELECT service_name, SUM(delivered), SUM(not_delivered)
            FROM sms_stats WHERE timestamp BETWEEN ? AND ? GROUP BY service_name""",
            (start_time, end_time)
        )
        rows = cursor.fetchall()
        if not rows:
            logger.warning(f"Нет данных для отчёта за последние {interval_minutes} минут.")
            return
        logger.info(f"Данные для отчёта: {rows}")
        timestamp = end_time.strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row(
            ["Service", "Delivered", "Not Delivered", "Timestamp", f"Отчет за последние {interval_minutes}"])

        for row in rows:
            sheet.append_row([row[0], row[1], row[2], timestamp])

        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при генерации отчёта: {e}")


# --- FastAPI App ---
app = FastAPI()

service_threads = []


@app.on_event("startup")
def startup():
    global service_threads

    # Определяем настройки для сервисов с ограничением по частоте
    high_priority_services = [("1", 4), ("2", 5), ("3", 4), ("4", 4), ("5", 4), ("6", 4), ("8", 4)]
    low_priority_services = [("7", 4), ("9", 2)]

    for service_id, rate_limit in high_priority_services + low_priority_services:
        thread = SmsServiceThread(service_id, rate_limit, DB_PATH)
        thread.start()
        service_threads.append(thread)


@app.on_event("shutdown")
def shutdown():
    for thread in service_threads:
        thread.stop()
        thread.join()


@app.get("/generate_report/{interval_minutes}")
def api_generate_report(interval_minutes: int):
    sheet = connect_to_google_sheets("ServicesData")
    if not sheet:
        raise HTTPException(status_code=500, detail="Unable to connect to Google Sheets")

    generate_report(sheet, interval_minutes)
    return {"message": "Report generated successfully"}


@app.on_event("startup")
@repeat_every(seconds=1800)  # Каждые 30 минут
def periodic_service_check():
    check_and_ban_services()


@app.on_event("startup")
@repeat_every(seconds=1800)  # Каждые 30 минут
def periodic_reenable_services():
    reenable_services()


@app.on_event("startup")
@repeat_every(seconds=600)  # Интервал в секундах
def generate_report_task():
    try:
        logger.info("Запуск задачи генерации отчёта каждые 10 секунд.")
        sheet = connect_to_google_sheets("ServicesData")
        if not sheet:
            logger.error("Не удалось подключиться к Google Sheets")
            return
        generate_report(sheet, 10)
        logger.info("Отчёт успешно сгенерирован.")
    except Exception as e:
        logger.error(f"Ошибка в generate_report_task: {e}")


@app.on_event("startup")
@repeat_every(seconds=3600)  # каждый час
def generate_hourly_report_task():
    sheet = connect_to_google_sheets("ServicesData")
    if not sheet:
        logger.error("Unable to connect to Google Sheets")
        return
    generate_report(sheet, 60)
