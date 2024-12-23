import requests
import re
import json
import requests
from bs4 import BeautifulSoup

from config import Proxy, Services


def send_sms_to_thai_traditions(phone_number: str):
    try:
        url = Services.TTRADITIONS_URL

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://thai-traditions.ru",
            "priority": "u=1, i",
            "referer": "https://thai-traditions.ru/",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        session = requests.Session()
        response = session.get('https://thai-traditions.ru/ajax/form.php?backurl=%2Fcatalog%2F&type=auth&auth=Y')
        cookies = session.cookies.get_dict()
        cookies_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])

        headers['cookie'] = cookies_str
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'})

        if csrf_input and 'value' in csrf_input.attrs:
            csrf_token = csrf_input['value']

        data = {
            "AUTH_FORM": "Y",
            "TYPE": "AUTH",
            "backurl": "",
            "csrf_token": csrf_token,
            "USER_TEL": phone_number,
            "USER_FIO_NAME": "",
            "USER_TEL_CODE": ""
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = session.post(url, data=data, headers=headers, proxies=proxies)

        with open('logs\\TTraditions.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        print('TTraditions: ', {"status_code": response.status_code, "response": response.text})
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(e)
