import time
import requests
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.anti_captcha import main, get_task_result, create_task
from utils.email_generate import generate_random_string

def send_sms_to_eda11(phone_number: str):
    try:
        url = Services.EDA11
        random_chars = generate_random_string()
        payload = device_info = {
            "device_id": f"89d2e60e-2c07-48cc-9d85-{random_chars}",
            "device_platform": "desktop",
            "merchant_keys": "720618dfb469503bfccd297bef310fbc",
            "transaction_type": "delivery",
            "json": True,
            "lang": "ru",
            "frontend": "modern",
            "phone": phone_number
        }

        captcha = main(url='https://eda11.ru', site_key='6LfkWr4dAAAAAKcwem5IKSiGMOcV13MppbsuHbfj')

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": captcha,
            "origin": "https://eda11.ru",
            "priority": "u=1, i",
            "referer": "https://eda11.ru/",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.session()


        response = session.get(url, headers=headers, params=payload)

        print(f'EDA11: {response.status_code}, {response.text}')
        with open('EDA11.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)
