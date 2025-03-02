import requests
from config import Proxy, Services
from utils.email_generate import generate_random_string
from utils.response_utils import get_cookies_and_headers
import uuid
import json


def send_sms_to_webbankir(phone_number: str, proxy: str = Proxy.PROXY_URL):
    try:
        url = Services.WEBBANKIR
        random_char = generate_random_string(length=2)
        new_uuid = uuid.uuid4()
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Baggage': 'sentry-environment=production,sentry-release=lk-ng%40WEBDEV-7499-2,sentry-public_key=084f946843e956474ccd29a65cadf572,sentry-trace_id=3c2598a99c374f1fb20f8e2fa0260eb4,sentry-sample_rate=0.2,sentry-transaction=%2Faccount%2Fregistration%2Fconfirmation%2F,sentry-sampled=false',
            'Content-Type': 'application/json',
            'Referer': 'https://webbankir.com/',
            'Sec-Ch-Ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sentry-Trace': '3c2598a99c374f1fb20f8e2fa0260eb4-9352b40edcb42eb3-0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }
        cookie = get_cookies_and_headers('https://webbankir.com/lk2/account/registration/confirmation', mode='dicts')
        payload = {
            "data": {
                "type": "PhoneVerification",
                "attributes": {
                    "phone": phone_number[1::1],
                    "webbankirCrossId": str(new_uuid)
                }
            }
        }

        proxies = {
            "http": proxy,
            "https": proxy
        }

        response = requests.post(url, headers=headers, proxies=proxies, json=payload)
        return {
            'status_code': response.status_code,
            'response': response.text
        }
    except Exception as error:
        print(error)
        return {
            'status_code': 400
        }