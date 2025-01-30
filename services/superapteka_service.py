import requests
from config import Proxy, Services
import json
from capmonster_python import RecaptchaV2Task
from utils.anti_captcha import main, create_task, get_task_result

def send_sms_to_superapteka(phone_number: str):

    url = Services.SUPERAPTEKA

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    capcha = main(url='https://superapteka.ru/', captcha_type='RecaptchaV2TaskProxyless',site_key='6LfuiY8aAAAAAHlIASGG4el8o7Y2zUEjnIXX7bkb')
    data = {
        "phоne": phone_number,
        "g-recaptcha-response": capcha
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }




    response = requests.post(url, headers=headers, proxies=proxies, json=data)
    print("YSAM: ", response, response.text)
    with open('ysam.log', "w") as file:
        file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
    response.raise_for_status()


    return {"status_code": response.status_code, "response": response.text}
