import requests
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers

def send_sms_to_thai_banki_ru(phone_number: str):
    try:
        url = Services.BANKI_RU

        payload = {
            "phoneNumber": phone_number[1::1],
            "consent": {
                "personalDataConsent": True,
                "advertisingConsent": True,
                "marketConsent": True
            },
            "regSource": "authform"
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, json=payload, headers=headers, proxies=proxies)
        with open('logs\\banki_ru.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)
