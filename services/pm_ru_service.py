import requests
import re
from utils.anti_captcha import main
from utils.response_utils import get_cookies_and_headers
from config import Services, Proxy

def send_sms_to_pm_ru(phone_number: str):
    url = 'https://msk.mebelbor.ru/bitrix/components/bxmaker/authuserphone.simple/ajax.php'
    cookie = get_cookies_and_headers('https://msk.mebelbor.ru')
    session = requests.Session()
    captcha = main(url='https://msk.mebelbor.ru', site_key='6LeSHNoaAAAAAJ8gRt5H5847DB3idlBfuWaniLYp')
    data = {
        "sessid": "856bb67e2422f9f5f715fc842a4f6f29f6",
        "siteId": "s1",
        "template": ".cceb2f662b33e69fd10458411ba5725b6ffb6086b1d1b41a47b46519c2511d74",
        "parameters": "YToyOntzOjE33OiJSRUxPQURfQUZURVJfQVVUSCI7czoxOiJZIjtzOjEwOiJDQUNIRV9UWVBFIjtzOjE6IkEiO30=.2bb8ab613c7bac419310727b25742aff12f26feaeb62393e8d218155aee84f46",
        "rand": "bM0U6t",
        "confirmType": "1",
        "confirmValue": "",
        "captchaId": "false",
        "captchaCode": captcha,
        "method": "authByPhone",
        "phone": "+7 930 923-36-12"
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://pm.ru",
        "cookie": cookie,
        "priority": "u=1, i",
        "referer": "https://pm.ru/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    response = session.post(url, json=data, headers=headers)

    return {"status_code": response.status_code, "response": response.text}

