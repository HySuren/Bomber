import logging
import psycopg2
import threading
import sqlite3
import time
import requests
import gspread
import json
from datetime import datetime, timedelta
from config import PhoneAgregator, Databases, services, service_names,DB_CONFIG
from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from utils.validators import validate_and_format_number
from oauth2client.service_account import ServiceAccountCredentials

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
from services.akbars_service import send_sms_to_akbars
from services.aptechestvo_service import send_sms_to_aptech
from services.winelab_service import send_sms_to_winelab
from services.letai_service import send_sms_to_letai
from services.svoi_bank_service import send_sms_to_svoi
from services.raifaisen_bank_service import send_sms_to_raiffeisen
from services.superapteka_service import send_sms_to_superapteka
from services.nfapteka_service import send_sms_to_nfapteka
from services.spacesuhi_service import send_sms_to_spacesuhi
from services.express_china_service import send_sms_to_china
from services.vipavenue_service import send_sms_to_vipavenue
from services.poizonshop_service import send_sms_to_poizonshop
from services.yasm_service import send_sms_to_yasm
from services.creddy_service import send_sms_to_creddy
from services.nahosa_service import send_sms_to_nahosa
from services.brandshop_service import send_sms_to_brandshop
from services.sportpoint_service import send_sms_to_sportpoint
from services.street_beat_service import send_sms_to_street_beat
from services.happywear_service import send_sms_to_happywear
from services.prime_services import send_sms_to_prime
from services.pulse_insure_service import send_sms_to_pluse_insure
from services.rsb_bank_service import send_sms_to_rsb_bank
from services.dragon_service import send_sms_to_dragon
from services.katana_sushi_service import send_sms_to_ninjafood
from services.eda11_service import send_sms_to_eda11
from services.asscon import send_sms_to_chibbis
from services.sushitut71_service import send_sms_to_mybox
from services.nadodeneg_service import send_sms_to_nadodeneg
from services.eco_vspishka_service import send_sms_to_eco_vspishka
from services.pm_ru_service import send_sms_to_pm_ru
from services.secret_service import send_sms_to_localkitchen
from services.trend_reality_service import send_sms_to_trend_reality
from services.webbankir_service import send_sms_to_webbankir
from services.srochno_dengi_service import send_sms_to_srochno_dengi
from services.zaymigo_service import send_sms_to_zaymigo

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Constants ---
DB_PATH = "sms_stats.db"
DELIVERY_CHECK_ATTEMPTS = 10
DELIVERY_CHECK_INTERVAL = 3


# --- Database Initialization ---
import psycopg2

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Таблица для статистики
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS sms_stats (
            id SERIAL PRIMARY KEY,
            service_name TEXT,
            delivered INTEGER,
            not_delivered INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS config (
            service_name TEXT PRIMARY KEY,
            enabled BOOLEAN NOT NULL CHECK (enabled IN (true, false))
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS banned (
            service_name TEXT,
            banned_date TIMESTAMP,
            comment TEXT DEFAULT 'Менее 20% дошедших за последние 100 попыток'
        )"""
    )

    for service_id, service_name in service_names.items():
        cursor.execute(
            "INSERT INTO config (service_name, enabled) VALUES (%s, %s) ON CONFLICT (service_name) DO NOTHING",
            (service_name, True)
        )

    conn.commit()
    cursor.close()
    conn.close()



init_db()


# --- Utility Functions ---
def is_service_enabled(service_name):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT enabled FROM config WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result and result[0]
    except Exception as e:
        logger.error(f"Error checking service status: {e}")
        return False



def check_and_ban_services():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for service_name in service_names.values():
            cursor.execute(
                """SELECT SUM(delivered), SUM(not_delivered) 
                FROM (
                    SELECT delivered, not_delivered 
                    FROM sms_stats 
                    WHERE service_name = %s
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
                        cursor.execute("UPDATE config SET enabled = FALSE WHERE service_name = %s", (service_name,))
                        cursor.execute(
                            "INSERT INTO banned (service_name, banned_date) VALUES (%s, %s)",
                            (service_name, datetime.now())
                        )
                        logger.info(f"Service {service_name} has been banned due to low delivery rate.")

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error in check_and_ban_services: {e}")


def reenable_services():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(
            """SELECT service_name FROM banned 
            WHERE banned_date <= %s""",
            (datetime.now() - timedelta(hours=12),)
        )
        services_to_enable = cursor.fetchall()

        for service_name, in services_to_enable:
            cursor.execute("UPDATE config SET enabled = TRUE WHERE service_name = %s", (service_name,))
            logger.info(f"Service {service_name} has been re-enabled after 12 hours.")

        #conn.commit()
        #conn.close()
    except Exception as e:
        logger.error(f"Error in reenable_services: {e}")


def get_sms_per_min(service_name):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT sms_per_min FROM config WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        else:
            logger.warning(f"No sms_per_min found for service {service_name}. Using default value.")
            return 5  # Default value if not found
    except Exception as e:
        logger.error(f"Error fetching sms_per_min for service {service_name}: {e}")
        return 5  # Default value in case of error


# --- SMS Sending Logic ---
class SmsServiceThread(threading.Thread):
    def __init__(self, service_id, db_path):
        super().__init__()
        self.service_id = str(service_id)
        self.db_path = db_path
        self.stop_event = threading.Event()
        self.sms_per_min = self.get_sms_per_min()  # Получаем количество смс в минуту для этого сервиса
        self.last_sent_timestamp = 0  # Время последней отправки

    def get_sms_per_min(self):
        """Получаем лимит отправки SMS для текущего сервиса."""
        service_name = service_names.get(self.service_id, "Unknown Service")
        return get_sms_per_min(service_name)

    def run(self):
        while not self.stop_event.is_set():
            try:
                now = time.time()
                time_since_last_sent = now - self.last_sent_timestamp

                if time_since_last_sent >= (60 / self.sms_per_min):  # Проверяем, прошло ли достаточно времени
                    service_name = service_names[self.service_id]
                    if not is_service_enabled(service_name):
                        logger.info(f"Service {service_name} is disabled. Skipping.")
                        time.sleep(5)
                        continue

                    phone_number, activation_id = self.fetch_phone_number()
                    if phone_number:
                        response_data = self.send_sms(phone_number, activation_id)

                        self.update_stats(delivered=response_data.get('delivered'), response_data=response_data.get('response'))  # Записываем статистику с ответом от сервиса
                        self.last_sent_timestamp = time.time()
                else:
                    time_to_wait = (60 / self.sms_per_min) - time_since_last_sent
                    logger.info(f"Waiting for {time_to_wait} seconds before next SMS...")
                    time.sleep(time_to_wait)
            except Exception as e:
                logger.error(f"Error in service {self.service_id}: {e}")

    def stop(self):
        self.stop_event.set()

    def fetch_phone_number(self):
        """Получение номера телефона и activationId в зависимости от страны."""
        try:
            # Извлекаем страну из конфигурации
            service_name = service_names[self.service_id]
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT country FROM config WHERE service_name = %s", (service_name,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                country = result[0]
            else:
                country = 'RU'

            if country == 'RU':
                response = requests.get(
                    f"{PhoneAgregator.GET_PHONE_NUMBER_URL}?token={PhoneAgregator.API_TOKEN}&country={PhoneAgregator.RU_COUNTRY}&carrier={PhoneAgregator.RU_CARRIER}")
                response.raise_for_status()
                data = response.json()
                return str(data.get('number')), data.get('activationId')
            else:
                logger.info(f"Fetching phone number for country {country} is not supported yet.")
                return None, None
        except Exception as e:
            logger.error(f"Error fetching phone number for service {self.service_id}: {e}")
            return None, None

    def send_sms(self, phone_number, activation_id):
        """Отправка SMS через соответствующий сервис и проверка доставки."""
        try:
            formatted_number = validate_and_format_number(phone_number, service_names[self.service_id])
            logger.info(f"Sending SMS via service {self.service_id} to {formatted_number}, activation_id: {activation_id}")
            match self.service_id:
                case "1":
                    result = send_sms_to_dommalera(formatted_number)
                case "2":
                    result = send_sms_to_4lapy(formatted_number)
                case "6":
                    result = send_sms_to_beautery(formatted_number)
                case "4":
                    result = send_sms_to_thai_banki_ru(formatted_number)
                case "7":
                    result = send_sms_to_thai_banki_ru(formatted_number)
                case "8":
                    result = send_sms_to_4lapy(formatted_number)
                case "9":
                    result = send_sms_to_obi(formatted_number)
                case "10":
                    result = send_sms_to_akbars(formatted_number)
                case "11":
                    result = send_sms_to_aptech(formatted_number)
                case "12":
                    result = send_sms_to_winelab(formatted_number)
                case "13":
                    result = send_sms_to_letai(formatted_number)
                case "14":
                    result = send_sms_to_svoi(formatted_number)
                case "15":
                    result = send_sms_to_gazprombonus(formatted_number)
                case "16":
                    result = send_sms_to_ayurveda(formatted_number)
                case "17":
                    result = send_sms_to_raiffeisen(formatted_number)
                case "18":
                    result = send_sms_to_superapteka(formatted_number)
                case "19":
                    result = send_sms_to_nfapteka(formatted_number)
                case "20":
                    result = send_sms_to_spacesuhi(formatted_number)
                case "21":
                    result = send_sms_to_china(formatted_number)
                case "22":
                    result = send_sms_to_thai_traditions(formatted_number)
                case "23":
                    result = send_sms_to_vipavenue(formatted_number)
                case "24":
                    result = send_sms_to_poizonshop(formatted_number)
                case "25":
                    result = send_sms_to_yasm(formatted_number)
                case "26":
                    result = send_sms_to_creddy(formatted_number)
                case "27":
                    result = send_sms_to_kalina_malina(formatted_number)
                case "28":
                    result = send_sms_to_nahosa(formatted_number)
                case "29":
                    result = send_sms_to_brandshop(formatted_number)
                case "30":
                    result = send_sms_to_sportpoint(formatted_number)
                case "31":
                    result = send_sms_to_street_beat(formatted_number)
                case "32":
                    result = send_sms_to_happywear(formatted_number)
                case "33":
                    result = send_sms_to_prime(formatted_number)
                case "34":
                    result = send_sms_to_pluse_insure(formatted_number)
                case "35":
                    result = send_sms_to_rsb_bank(formatted_number)
                case "36":
                    result = send_sms_to_dragon(formatted_number)
                case "37":
                    result = send_sms_to_ninjafood(formatted_number)
                case "38":
                    result = send_sms_to_eda11(formatted_number)
                case "40":
                    result = send_sms_to_chibbis(formatted_number)
                case "42":
                    result = send_sms_to_nadodeneg(formatted_number)
                case "43":
                    result = send_sms_to_eco_vspishka(formatted_number)
                case "44":
                    result = send_sms_to_pm_ru(formatted_number)
                case "45":
                    result = send_sms_to_localkitchen(formatted_number)
                case "46":
                    result = send_sms_to_trend_reality(formatted_number)
                case "47":
                    result = send_sms_to_webbankir(formatted_number)
                case "48":
                    result = send_sms_to_srochno_dengi(formatted_number)
                case "49":
                    result = send_sms_to_4lapy(formatted_number)
                case "50":
                    result = send_sms_to_akbars(formatted_number)
                case "51":
                    result = send_sms_to_aptech(formatted_number)
                case "52":
                    result = send_sms_to_thai_banki_ru(formatted_number)
                case "53":
                    result = send_sms_to_beautery(formatted_number)
                case "54":
                    result = send_sms_to_letai(formatted_number)
                case "55":
                    result = send_sms_to_prime(formatted_number)
                case "56":
                    result = send_sms_to_raiffeisen(formatted_number)
                case "57":
                    result = send_sms_to_trend_reality(formatted_number)
                case "59":
                    result = send_sms_to_nfapteka(formatted_number)
                case "60":
                    result = send_sms_to_zaymigo(formatted_number)
                case "61":
                    result = send_sms_to_zaymigo(formatted_number)
                case "62":
                    result = send_sms_to_zaymigo(formatted_number)
                case _:
                    logger.error(f"Service ID {self.service_id} is not supported.")
                    return {'delivered': False, 'response': 'нет такого сервиса'}

            if self.service_id == "11":
                if result.get("response") in ["Error", "Error в черном списке2", "Error ITTIME2"]:
                    logger.info(
                        f"SMS failed for service {service_names[str(self.service_id)]} due to error response: {result.get('response')}")
                    return {'delivered': False, 'response': {'status_code':result.get('status_code'),'response':result.get('response')}}

                if result.get("response") == "success":
                    return {'delivered': self.check_delivery_status(activation_id), 'response': {'status_code':result.get('status_code'),'response':result.get('response')}}

            if result.get("status_code") != 200 and result.get("status_code") != 201 and result.get('status_code') != 202:
                logger.warning(
                    f"SMS delivery failed during sending phase via service {service_names[str(self.service_id)]}: {result.get('status_code')}")
                return {'delivered': False, 'response': {'status_code':result.get('status_code'),'response':result.get('response')}}

            return {'delivered': self.check_delivery_status(activation_id), 'response': {'status_code':result.get('status_code'),'response':result.get('response')}}
        except Exception as e:
            logger.error(f"Error sending SMS via service {self.service_id}: {e}")
            return {'delivered': False, 'response': {'status_code':result.get('status_code'),'response':result.get('response')}}

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

                if data.get("success"):
                    return True

                if data.get("status") == "STATUS_WAIT_CODE":
                    time.sleep(DELIVERY_CHECK_INTERVAL)
            return False
        except Exception as e:
            logger.error(f"Error checking delivery status for activationId {activation_id}: {e}")
            return False

    def update_stats(self, delivered, response_data):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            service_name = service_names.get(self.service_id, "Unknown Service")
            delivered_status = 1 if delivered else 0
            not_delivered_status = 0 if delivered else 1
            print("IIO: ",json.dumps(response_data))
            # Записываем в таблицу sms_stats с полем response_data
            cursor.execute(
                """INSERT INTO public.sms_stats (service_name, delivered, not_delivered, response_data, timestamp) 
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)""",
                (service_name, delivered_status, not_delivered_status, json.dumps(response_data))
            )
            conn.commit()
            cursor.close()
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

    high_priority_services = [("21", 1), ("25", 1), ("26", 1), ("6", 1), ("19", 1), ("10", 1),
                              ("17", 1), ("8", 1), ("9", 1), ("18", 1), ("27", 1), ("28", 1), ("29", 1), ("30", 1)]
    low_priority_services = [("22", 1), ("23", 1), ("24", 1), ("20", 1), ("7", 1),
                             ("14", 1), ("11", 1), ("13", 1), ("31", 1), ("32", 1),
                             ("33", 1), ("34", 1), ("35", 1), ("36", 1), ("37", 1),
                             ("38", 1), ("40", 1), ("42", 1), ("43", 1), ("44", 1),
                             ("45", 1), ("46", 1), ("47", 1), ("48", 1), ("49", 1),
                             ("50", 1), ("51", 1), ("52", 1), ("53", 1), ("54", 1),
                             ("55", 1), ("56", 1), ("57", 1), ("58", 1), ("59", 1)
                             ]

    for service_id, rate_limit in high_priority_services + low_priority_services:
        thread = SmsServiceThread(service_id, DB_PATH)
        thread.start()
        service_threads.append(thread)


@app.on_event("shutdown")
def shutdown():
    for thread in service_threads:
        thread.stop()
        thread.join()


@app.on_event("startup")
@repeat_every(seconds=1800)
def periodic_service_check():
    check_and_ban_services()


@app.on_event("startup")
@repeat_every(seconds=1800)
def periodic_reenable_services():
    reenable_services()
