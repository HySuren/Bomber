import requests
from config import Proxy, Services
import json

def send_sms_to_kalina_malina(phone_number: str):
    try:
        url = Services.FOUR_LAPY
        headers = {
            'Content-type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        data = {
            "phone": phone_number[2:]
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, headers=headers, data=data, proxies=proxies)

        response.raise_for_status()

        try:
            response_json = response.json()
            return {"status_code": response.status_code, "response": response_json}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Response: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(f"Unhandled error: {e}\n{response.text}")
        return {"status_code": None, "response": str(e)}