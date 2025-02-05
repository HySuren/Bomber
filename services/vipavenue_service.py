import requests
from config import Proxy, Services
from utils.anti_captcha import main, create_task, get_task_result
import random
import json
import time
from utils.anti_captcha import main, create_task, get_task_result
from utils.email_generate import generate_random_string

def send_sms_to_vipavenue(phone_number: str):
    url = 'https://users.vipavenue.ru/api/auth/send-code'
    random_char = generate_random_string()
    captcha = main(url='https://vipavenue.ru', captcha_type='RecaptchaV3TaskProxyless',site_key='6LdSHqweAAAAAFT7yAWHIHxRQJDGk910UMU9Kqq7')
    print(captcha)
    payload = {
    "phone": "79302933612",
    "code_type": "login",
    "recaptcha_token": captcha,
    "referral_code": None,
    "utm_source": None,
    "utm_medium": None,
    "utm_campaign": None,
    "platform_type": "desktop_site",
    "site_gender_id": '36361',
    "site_location_id": '36810',
    "device_uuid": f"4{random_char}bf-02cc-46b2-9e58-7763016185c1"
}

    headers_dict = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "cookie": (
            "session=ovtjzB61RMStevrvett8mpZ2rZRUkfkXXavIH9rUFG4kE85V; "
            "_ga=GA1.1.510590463.1738725493; "
            "tmr_lvid=c80b201f22731cae9dbb263b5cf76f6d; "
            "tmr_lvidTS=1738725492984; "
            "adspire_uid=AS.2049200890.1738725493; "
            "mindboxDeviceUUID=424a84bf-02cc-46b2-9e58-7763016185c1; "
            "directCrm-session=%7B%22deviceGuid%22%3A%22424a84bf-02cc-46b2-9e58-7763016185c1%22%7D; "
            "_userGUID=0:m6rc9lhv:DrpBlBhor6FosKCeUiswEbZpudWk8aK_; "
            "dSesn=b759de03-17ec-df73-4e66-f6f7c7aa84fb; "
            "adtech_uid=6885e13d-5c33-4f90-b180-47733ff29d98%3Avipavenue.ru; "
            "top100_id=t1.7729791.1813690112.1738725494410; "
            "_ym_uid=1738725494552015489; "
            "_ym_d=1738725494; "
            "ab_id=2ebc784ae1da5b99534c997521b435f33e89bfde; "
            "_ym_isad=1; "
            "_ym_visorc=b; "
            "t3_sid_7729791=s1.393783710.1738725494412.1738725509437.1.10; "
            "_ga_KXB8Z0CNHS=GS1.1.1738725492.1.1.1738725511.41.0.0"
        ),
        "origin": "https://vipavenue.ru",
        "priority": "u=1, i",
        "referer": "https://vipavenue.ru/",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        ),
        "x-trace-frontend-request-side": "browser",
        "x-trace-path": "/"
    }
    session = requests.Session()

    responce = session.post(url, json=payload, headers=headers_dict)