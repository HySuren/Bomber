import requests
from config import Proxy, Services
import string
import random
from utils.response_utils import get_cookies_and_headers

def generate_hex_string(length=32):
  """Генерирует случайную шестнадцатеричную строку указанной длины."""
  hex_chars = string.hexdigits # '0123456789abcdefABCDEF'
  return ''.join(random.choice(hex_chars) for i in range(length)).lower()



def send_sms_to_boostra(phone_number: str, proxy: str = Proxy.PROXY_URL):
    try:
        url = 'https://boostra.ru/ajax/send_sms.php'
        cookie = get_cookies_and_headers('https://boostra.ru/init_user?amount=30000&period=16')
        phone_number = f"+7 ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        random_chars = generate_hex_string()
        payload = {
            "hui": random_chars,
            "code": '', # Значение 'code' отсутствует в исходном примере, поэтому ставим None
            "flag": "LOGIN",
            "phone": phone_number
        }


        headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'connection': 'keep-alive',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'host': 'boostra.ru',
    'cookie': cookie,
    'origin': 'https://boostra.ru',
    'referer': 'https://boostra.ru/init_user?amount=30000&period=16',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-kl-kfa-ajax-request': 'Ajax_Request',
    'x-requested-with': 'XMLHttpRequest'
}


        proxies = {
            "http": proxy,
            "https": proxy
        }

        session = requests.session()

        response = session.post(url, data=payload, proxies=proxies, headers=headers)
        return {"status_code": response.status_code, "response": response.json()}
    except Exception as e:
        print(e)