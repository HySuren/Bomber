import requests
from config import Proxy, Services


def send_sms_to_dragon(phone_number: str):
    try:
        url = Services.DRAGON

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        payload = {
            "method": "login",
            "type": "auth",
            "phone": phone_number[1::1]
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
            "Host": "zabic.ru"
        }
        session = requests.session()

        response = session.post(url, data=payload,headers=headers, proxies=proxies)

        return {"status_code": 200, "response": response.text}

    except Exception as e:
        print(f'Error occurred: {e}')
