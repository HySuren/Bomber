import requests
from config import Proxy, Services


def send_sms_to_rsb_bank(phone_number: str):
    try:
        url = Services.RSB_BANK

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        payload = {
            "phoneNumber": phone_number[2::1],
            "password": None,
            "token": None,
            "sysName": "mobilebank",
            "device": "8c89d52b-49f3-39c9-b9a6-6c2866c57a20",
            "location": None,
            "clientIp": "192.168.232.2",
            "statistics": {
                "device": {
                    "type": "mobile",
                    "model": "Samsung SM-N975F",
                    "screen": "900x1600"
                },
                "operationSystem": {
                    "name": "Android",
                    "version": "9"
                },
                "location": {
                    "language": "ru_RU"
                },
                "connection": {
                    "type": "WIFI"
                }
            }
        }

        headers = {
            "User-Agent": "MobBankSwift / 1.0.3.10493 Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI) ru.rsb.mobbank",
            "Content-Type": "application/json; charset=UTF-8",
        }

        session = requests.session()

        response = session.post(url, json=payload,headers=headers)
        print(f'RSB_BANK: {response.status_code}, {response.text}')

        with open('RSB_BANK.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}\n")

        return {"status_code": 200, "response": response.text}

    except Exception as e:
        print(f'Error occurred: {e}')