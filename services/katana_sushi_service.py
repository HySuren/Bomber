import time

import requests
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def send_sms_to_ninjafood(phone_number: str):
    try:
        url = Services.NINJAFOOD

        payload = {
            "phone": phone_number
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.session()


        response = session.post('https://app.ninjafood.su/api/user/login', json=payload, proxies=proxies)

        print(f'NINJAFOOD: {response.status_code}, {response.text}')
        with open('NINJAFOOD.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)
