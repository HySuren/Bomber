import requests
from config import Proxy, Services


def send_sms_to_dommalera(phone_number: str):
    try:
        url = f'{Services.DOMMALERA_URL}{phone_number[1::1]}'

        headers = {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, headers=headers, proxies=proxies)

        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(f"Ошибка при отправке SMS через Dommalera: {e}")
        return {"error": str(e)}
