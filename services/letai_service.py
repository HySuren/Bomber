import requests
import random
import string
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers

def generate_device_id(length=9):
    """Генерирует случайный device_id заданной длины."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def send_sms_to_letai(phone_number: str):
    url = Services.LETAI
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "connection": "keep-alive",
        "content-type": "application/json",
        "host": "newlk.letai.ru",
        "origin": "https://cabinet.letai.ru",
        "referer": "https://cabinet.letai.ru/",
        "Cookie": get_cookies_and_headers('https://letai.ru'),
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "version": "300"
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    session = requests.session()

    device_id = generate_device_id()

    data = {
        "phone": phone_number,
        "device_id": device_id
    }

    response = session.post(url, json=data, headers=headers, proxies=proxies)
    response.raise_for_status()
    print("LETAI: ", response, response.text)
    with open('LETAI.log', "w") as file:
        file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
    response.raise_for_status()
    return {"status_code": response.status_code, "response": response.text}
