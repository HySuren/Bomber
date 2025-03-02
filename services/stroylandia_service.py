import requests
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers

def send_sms_to_trend_reality(phone_number: str):
    try:
        url = 'https://mobileapi.neftm.ru/api/Auth/Register'

        payload = {
            "phone": "+79309233611",
            "promocode": "",
            "theme": 1
        }

        headers = {
            'x-deviceid': '9a572c06ceea4cc38b21e918c37a1be14',
            'user-agent': 'centrida.neftmagistral/8.1.0 (SM-S9210; Android 9)',
            'content-type': 'application/json',
            'accept-encoding': 'gzip'
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, json=payload, headers=headers, proxies=proxies)
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(e)

print(send_sms_to_trend_reality(''))