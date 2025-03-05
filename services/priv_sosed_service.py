import requests
from config import Proxy, Services
from utils.email_generate import generate_random_string
from utils.response_utils import get_cookies_and_headers
import uuid
import json
import time


def send_sms_to_priv_sosed(phone_number: str):
    try:
        url = 'https://api.privsosed.ru/anketa/api/send-sms/'
        random_char = generate_random_string()
        cookie = get_cookies_and_headers('https://privsosed.ru/anketa/acceptmobile')
        print(cookie)
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': cookie + '; session_id=99744adb-eebe-47b3-b87e-e0cc5f1b6440;',
            'origin': 'https://privsosed.ru',
            'priority': 'u=1, i',
            'referer': 'https://privsosed.ru/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-request-id': str(uuid.uuid4())
        }

        payload = {
            "phone": phone_number
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, headers=headers, proxies=proxies, json=payload)
        return {
            'status_code': response.status_code,
            'response': response.text
        }
    except Exception as error:
        print(error)
        return {
            'status_code': 400
        }
print(send_sms_to_priv_sosed('+7 (930) 923-36-11'))