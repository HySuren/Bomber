import requests
from config import Proxy, Services


def send_sms_to_dommalera(phone_number: str):
    try:
        url = f'{Services.DOMMALERA_URL}{phone_number}'

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, headers=headers, proxies=proxies)

        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(f"Ошибка при отправке SMS через Dommalera: {e}")
        return {"error": str(e)}
