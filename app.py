import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi_utils.tasks import repeat_every
import requests
import  time

from services.ayurveda_service import send_sms_to_ayurveda
from services.thai_traditions_service import send_sms_to_thai_traditions
from services.dommalera_service import send_sms_to_dommalera
from utils.validators import validate_and_format_number

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

API_URL = "http://c4ke.fun:1706/api/drop/getPhoneNumber"
API_TOKEN = "Dancer_Pu"
CHECK_SMS_URL = f"http://c4ke.fun:1706/api/drop/getCode"
SMS_RATE_LIMIT = 2
DELIVERY_CHECK_ATTEMPTS = 10
DELIVERY_CHECK_INTERVAL = 5

services = ["1", "2", "3"]
service_names = {
    "1": "Ayurveda",
    "2": "Thai Traditions",
    "3": "Dommalera"
}
service_index = 0

# Хранилище статистики
service_stats = {service: {"taken": 0, "delivered": 0} for service in services}
last_sent_timestamps = {service: [] for service in services}


def fetch_phone_number():
    """Получить номер телефона из API."""
    try:
        response = requests.get(f"{API_URL}?token={API_TOKEN}")
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
            try:
                response = requests.get(f"{CHECK_SMS_URL}?token={API_TOKEN}&uid={uid}")
                logger.debug(f"Проверка доставки SMS, попытка {attempt + 1}: {response.text}")
                response.raise_for_status()
                data = response.json()
                if data.get("success"):
                    print(data)
                    return True
                elif data.get("status") == "STATUS_WAIT_CODE":
                    time.sleep(DELIVERY_CHECK_INTERVAL)
            except requests.HTTPError as e:
                logger.error(f"Ошибка проверки доставки SMS: {e}")
        return False
    except Exception as e:
        logger.error(f"Ошибка в процессе проверки доставки: {e}")
        return False


def send_sms_with_rate_limit(service: str, phone_number: str, uid: str = None):
    try:
        now = time.time()
        last_sent_timestamps[service] = [
            ts for ts in last_sent_timestamps[service] if now - ts < 60
        ]

        if len(last_sent_timestamps[service]) < SMS_RATE_LIMIT:
            try:
                # Передаём имя сервиса для форматирования
                formatted_number = validate_and_format_number(phone_number, service_names[service])
            except ValueError as e:
                logger.error(f"Ошибка валидации номера {phone_number}: {e}")
                return

            service_stats[service]["taken"] += 1
            logger.info(f"Отправка через сервис {service}: {formatted_number}")

            match service:
                case "1":
                    send_sms_to_ayurveda(formatted_number)
                case "2":
                    send_sms_to_thai_traditions(formatted_number)
                case "3":
                    send_sms_to_dommalera(formatted_number)
                case _:
                    logger.error(f"Неизвестный сервис: {service}")
                    return

            if uid and check_delivery_status(uid):
                service_stats[service]["delivered"] += 1

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
