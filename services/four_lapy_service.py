import requests
from config import Proxy, Services
import json


def send_sms_to_4lapy(phone_number: str):
    url = Services.FOUR_LAPY
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    data = {
        "phone": phone_number[1:]
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }
    response = requests.post(url, headers=headers, data=data, proxies=proxies)
    try:
        response_json = response.json()
        return {"status_code": response.status_code, "response": response_json}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}, Response: {response.text}")
        return {"status_code": response.status_code, "response": response.text}
