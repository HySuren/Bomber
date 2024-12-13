import logging
import requests
import  time
from config import PhoneAgregator, services, service_names
from fastapi import FastAPI, HTTPException, Body
from fastapi_utils.tasks import repeat_every

from services.ayurveda_service import send_sms_to_ayurveda
from services.thai_traditions_service import send_sms_to_thai_traditions
from services.dommalera_service import send_sms_to_dommalera
from services.obi_service import send_sms_to_obi
from services.four_lapy_service import send_sms_to_4lapy
from services.beautery_service import send_sms_to_beautery
from services.banki_ru_service import send_sms_to_thai_banki_ru
from services.gazprom_bonus_service import send_sms_to_gazprombonus
from utils.validators import validate_and_format_number
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime



def initialize_google_sheet(sheet):
    """Инициализация таблицы: добавление заголовков, если их нет."""
    try:
        headers = ["Service", "Delivered", "Not Delivered", "Timestamp"]
        existing_data = sheet.get_all_values()
        if not existing_data:  # Если таблица пуста
            sheet.append_row(headers)
            logger.info("Заголовки добавлены в таблицу.")
        elif existing_data[0] != headers:  # Проверяем, что заголовки корректны
            sheet.update('A1:D1', [headers])  # Обновляем первую строку
            logger.info("Заголовки обновлены в таблице.")
    except Exception as e:
        logger.error(f"Ошибка инициализации Google Sheets: {e}")

def connect_to_google_sheets(sheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("testwork-370710-d0dec9b47b1b.json", scope)
        client = gspread.authorize(creds)
        print(client.open(sheet_name).sheet1)
        return client.open(sheet_name).sheet1
    except Exception as e:
        print(f"Google: {e}")


app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SMS_RATE_LIMIT = 2
DELIVERY_CHECK_ATTEMPTS = 10
DELIVERY_CHECK_INTERVAL = 5

service_index = 0

service_stats = {service: {"taken": 0, "delivered": 0} for service in services}
last_sent_timestamps = {service: [] for service in services}


def send_stats_to_google_sheets(sheet, stats, timestamp, time_interval: str):
    """
    Отправка статистики в Google Sheets:
    1. Данные по сервисам.
    2. Сводка Summary в конце с выделением.
    """
    try:
        initialize_google_sheet(sheet)  # Убедимся, что заголовки есть

        # Формируем строки для текущего отчета
        rows = []
        for service, data in stats.items():
            delivered = data["delivered"]
            not_delivered = data.get("not_delivered", 0)
            rows.append([service_names[service], delivered, not_delivered, timestamp])

        # Подсчет итогов (Summary)
        total_delivered = sum(data["delivered"] for data in stats.values())
        total_not_delivered = sum(data.get("not_delivered", 0) for data in stats.values())
        summary_row = ["Summary", total_delivered, total_not_delivered, timestamp, time_interval]

        # Добавляем строки отчета в таблицу
        sheet.append_rows(rows + [summary_row])

        # Определяем диапазон заливки для Summary
        start_row = len(sheet.get_all_values()) - len(rows)
        summary_row_index = start_row + len(rows)

        # Заливка только строки Summary
        sheet.format(f"A{summary_row_index}:D{summary_row_index}", {
            "backgroundColor": {"red": 1, "green": 0.9, "blue": 0.9}  # Светло-красный цвет
        })

    except Exception as e:
        logger.error(f"Ошибка записи статистики в Google Sheets: {e}")

def fetch_phone_number():
    """Получить номер телефона из API."""
    try:
        response = requests.get(f"{PhoneAgregator.GET_PHONE_NUMBER_URL}?token={PhoneAgregator.API_TOKEN}")
        logger.info(f"Получен ответ API: {response.text}")
        response.raise_for_status()
        data = response.json()
        return str(data.get('number')), data.get('activationId')
    except Exception as e:
        logger.error(f"Ошибка при запросе номера: {e}")
        return None, None


def check_delivery_status(uid):
    """Проверяет статус доставки SMS."""
    try:
        for attempt in range(DELIVERY_CHECK_ATTEMPTS):
            response = requests.get(f"{PhoneAgregator.CHECK_SMS_URL}?token={PhoneAgregator.API_TOKEN}&uid={uid}")
            logger.info(f"Проверка доставки SMS, попытка {attempt + 1}: {response.text}")
            response.raise_for_status()
            data = response.json()
            if data.get("success") and data.get("status") == "OK":
                return True
            elif data.get("status") == "STATUS_WAIT_CODE":
                time.sleep(DELIVERY_CHECK_INTERVAL)
        return False
    except Exception as e:
        logger.error(f"Ошибка проверки доставки: {e}")
        return False


def send_sms_with_rate_limit(service: str, phone_number: str, uid: str = None):
    try:
        now = time.time()
        last_sent_timestamps[service] = [
            ts for ts in last_sent_timestamps[service] if now - ts < 60
        ]

        if len(last_sent_timestamps[service]) < SMS_RATE_LIMIT:
            formatted_number = validate_and_format_number(phone_number, service_names[service])
            service_stats[service]["taken"] += 1
            logger.info(f"Отправка через сервис {service}: {formatted_number}")

            # Вызов конкретного сервиса
            result = None
            match service:
                case "1":
                    result = send_sms_to_ayurveda(formatted_number)
                case "2":
                    result = send_sms_to_thai_traditions(formatted_number)
                case "3":
                    result = send_sms_to_dommalera(formatted_number)
                case "4":
                    result = send_sms_to_obi(formatted_number)
                case "5":
                    result = send_sms_to_4lapy(formatted_number)
                case "6":
                    result = send_sms_to_beautery(formatted_number)
                case "7":
                    result = send_sms_to_thai_banki_ru(formatted_number)
                case "8":
                    result = send_sms_to_gazprombonus(formatted_number)
                case _:
                    logger.error(f"Неизвестный сервис: {service}")
                    return

            if uid:
                if check_delivery_status(uid):
                    service_stats[service]["delivered"] += 1
                else:
                    service_stats[service]["not_delivered"] = service_stats[service].get("not_delivered", 0) + 1

            last_sent_timestamps[service].append(now)
            logger.info(f"SMS отправлено через {service_names[service]} на номер {formatted_number}")
        else:
            logger.warning(f"Превышен лимит отправки SMS для сервиса {service_names[service]}. Ожидание...")
    except Exception as e:
        logger.error(f"Ошибка при отправке SMS через {service_names[service]}: {e}")


@app.post("/sms/send")
def receive_phone_number(phone_number: str = Body(..., embed=True)):
    global service_index

    if not phone_number:
        raise HTTPException(status_code=400, detail="Номер телефона обязателен.")

    service = services[service_index]
    service_index = (service_index + 1) % len(services)

    send_sms_with_rate_limit(service, phone_number, u)
    stats = service_stats[service]
    return {
        "message": f"SMS отправлено через сервис {service_names[service]}",
        "stats": {
            "taken": stats["taken"],
            "delivered": stats["delivered"]
        }
    }


@app.on_event("startup")
@repeat_every(seconds=20)
def periodic_sms_sender():
    try:
        phone_number, activation_id = fetch_phone_number()
        if phone_number:
            global service_index
            service = services[service_index]
            service_index = (service_index + 1) % len(services)
            send_sms_with_rate_limit(service, phone_number, activation_id)
        else:
            logger.warning("Номер телефона не получен или ошибка API.")
    except Exception as e:
        logger.error(f"Ошибка при периодической отправке SMS: {e}")



@app.on_event("startup")
@repeat_every(seconds=600)  # Каждые 10 минут
def record_stats_every_10_minutes():
    try:
        sheet = connect_to_google_sheets("ServicesData")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_stats_to_google_sheets(sheet, service_stats, timestamp, 'За 10 минуту')
        logger.info("Статистика за 1 минут записана в Google Sheets.")
    except Exception as e:
        logger.error(f"Ошибка записи статистики за 10 минут: {e}")

@app.on_event("startup")
@repeat_every(seconds=3600)
def record_hourly_summary():
    try:
        sheet = connect_to_google_sheets("ServicesData")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_stats_to_google_sheets(sheet, service_stats, timestamp, 'За 1 час')
        logger.info("Сводная статистика за час записана в Google Sheets.")
    except Exception as e:
        logger.error(f"Ошибка записи сводной статистики за час: {e}")

