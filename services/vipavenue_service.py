import requests
from config import Proxy, Services
import random


def generate_random_ip():
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


def send_sms_to_vipavenue(phone_number: str):
    try:
        url = Services.VIPAVENUE
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://vipavenue.ru",
            "priority": "u=1, i",
            "referer": "https://vipavenue.ru/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-trace-frontend-request-side": "browser",
            "x-trace-path": "/product/1388035-krossovki-kombinirovannye-seand-premiata/"
        }

        session = requests.Session()
        response = session.get('https://users.vipavenue.ru/api/auth/send-code')  # Получение cookies
        cookies = session.cookies.get_dict()
        cookies_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])
        random_ip = generate_random_ip()
        headers['cookie'] = cookies_str

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        data = {
            "token": "",
            "captcha_is_verified": True,
            "phone_number": phone_number,
            "ip": random_ip
        }

        response = session.post(url, json=data, headers=headers, proxies=proxies)
        print("VIPAVENUE: ", {"status_code": response.status_code, "response": response.text})
        with open("logs\\VIPAVENUE.log", "w") as file:
            file.write(f"RAIFFEISEN responce status_code: {response}, text: {response.text}")
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(f'RAIFFEISEN ERROR: {e}')
