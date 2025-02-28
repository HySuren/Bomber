import requests
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers

def send_sms_to_trend_reality(phone_number: str):
    try:
        url = Services.TRENDREALITY

        payload = {
            'phone': phone_number
        }

        headers = {
            'Accept': 'application/json',
            'Accept-Charset': 'UTF-8',
            'User-Agent': 'Ktor client',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '20',
            'Host': 'auth.trendrealty.ru',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, data=payload, headers=headers, proxies=proxies)
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(e)