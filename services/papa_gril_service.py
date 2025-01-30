import requests
from config import Proxy, Services
from utils.anti_captcha import main, get_task_result, create_task, API_URL

def send_sms_to_prime(phone_number: str):
    try:
        url = Services.PRIME

        print('Решение капчи начать')
        captcha = main(captcha_type='RecaptchaV2TaskProxyless',site_key='ysc1_Pb7vIqqZq88WiSoGuhDToLoeoiCbIDBDI0bcPTLq7a6e6f9a', url='https://askino.papagril.ru' )
        print(f'Решение капчи закончено: {captcha}')

        payload = {
        "country": 'RU',
        "y-smart-captcha-response": captcha,
        "phone": "+79309233611",
        "ignorephonecheck": "true",
        "additionally": {}
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        headers = {
            "accept": "application/json, text/plain, */*",
            "app-version": "2.8.0",
            "Content-Type": "application/json",
            "Content-Length": "132",
            "Host": "prim3.clmedical.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.2"
        }

        session = requests.session()

        response = session.post(url, data=payload, proxies=proxies, headers=headers)
        print(f'PRIME: {response.status_code}, {response.text}')
        with open('PRIME.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)