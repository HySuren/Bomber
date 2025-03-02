import requests
from config import Proxy, Services
from utils.email_generate import generate_random_string
import json


def send_sms_to_webbankir(phone_number: str):
    try:
        url = Services.WEBBANKIR
        random_char = generate_random_string(length=2)
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

        payload = {
            "data": {
                "type": "PhoneVerification",
                "attributes": {
                    "phone": phone_number[1::1],
                    "webbankirCrossId": f"abc{random_char}c155-5e37-4aa7-8351-030c7c487565"
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        return {
            'status_code': response.status_code,
            'response': response.text
        }
    except Exception as error:
        print(error)
        return {
            'status_code': 400
        }
