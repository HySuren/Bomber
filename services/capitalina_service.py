import requests
import uuid
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers

def send_sms_to_capitalina(phone_number: str, proxy: str = Proxy.PROXY_URL):
    try:
        url = 'https://api.finters-zaem.ru/anketa/api/send-sms/'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '30',
            'content-type': 'application/json',
            'origin': 'https://finters-zaem.ru',
            'cookie': '_ga=GA1.1.1057073382.1741235903; session_id=df46718a-3bef-4225-bfb9-7704d3ce8bfb; track_id=420878462; webmaster_id=18954; affiliate_id=bankiru; _ym_uid=1741235903622393947; _ym_d=1741235903; _ym_isad=1; _ym_visorc=w; _ga_W7TK0EQZ03=GS1.1.1741235902.1.1.1741235918.0.0.0',
            'priority': 'u=1, i',
            'referer': 'https://finters-zaem.ru/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-request-id': str(uuid.uuid4())
        }
        phone_number = f"+7 ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        payload = {
        "phone": phone_number
        }

        proxies = {
            "http": proxy,
            "https": proxy
        }
        session = requests.session()

        response = session.post(url, json=payload, proxies=proxies, headers=headers)
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(e)