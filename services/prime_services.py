import requests
from config import Proxy, Services

def send_sms_to_prime(phone_number: str):
    try:
        url = Services.PRIME

        payload = {
        "phone": phone_number[1::1],
        "password": "d0407153e",
        "password_confirmation": "d0407153e",
        "device_name": "samsung  SM-N975F",
        "additionally": {}
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        headers = {
            "accept": "application/json, text/plain, */*",
            "app-version": "2.8.0",
            "Content-Type": "application/json",
            "Content-Length": "132",
            "Host": "prim3.clmedical.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.2"
        }

        session = requests.session()

        response = session.post(url, json=payload, proxies=proxies, headers=headers)
        print(f'PRIME: {response.status_code}, {response.text}')
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(e)