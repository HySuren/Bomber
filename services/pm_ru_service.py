import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import unquote
from utils.response_utils import save_logs
from utils.anti_captcha import main, get_task_result, create_task
from config import Services, Proxy
from utils.response_utils import get_cookies_and_headers


def send_sms_to_pm_ru(phone_number: str):
    url = Services.PM_RU

    session = requests.Session()
    captcha = main(url='https://pm.ru', site_key='6Ld29rUqAAAAAGrJgIJiBpDnt35tVhIn-2mE9tF0')

    # Удаляем пробелы и скобки из номера телефона
    clean_phone_number = phone_number.replace(" ", "").replace("(", "").replace(")", "")

    data = {
        "g-recaptcha-response": captcha,
        "lk-phone": clean_phone_number,
        "users-agreement": "on",
        "lk-code": "",
        "phone": clean_phone_number
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://pm.ru",
        "referer": "https://pm.ru/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    response = session.post(url, json=data, headers=headers, proxies=proxies)

    return {"status_code": response.status_code, "response": 'good'}