from utils.email_generate import generate_random_string
from utils.anti_captcha import main, create_task, get_task_result
from utils.response_utils import get_cookies_and_headers
from config import Services, Proxy
import requests
import re
import json

def send_sms_to_fudziyama(phone_number: str):
    url = 'https://epilas.ru/appointment_Add.h?fName=_appointment._result&r=879265721'
    cookie = get_cookies_and_headers('https://epilas.ru/')
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": cookie,
        "origin": "https://darkshaurma.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    data = {
    "editAppointmentId": None,
    "name": "LARISA",
    "phone": "9309233612",
    "gender": 2,
    "medcenterId": 4,
    "desiredEmployeeId": 0,
    "dt": "090220250900",
    "serviceIds": None,
    "promoComboIds": 1,
    "addSource": 2,
    "s": 4130
    }



    response = requests.post(url, headers=headers, data=data)
    print({'status_code': response.status_code, 'response': response.text})
    return {'status_code': response.status_code, 'response': 'good'}



