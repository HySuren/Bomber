import requests
from config import Proxy, Services
from utils.anti_captcha import main,get_task_result,create_task

def send_sms_to_rsb_bank(phone_number: str):
    try:
        url = Services.SPARC_FOOD

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }
        captcha = main(url='https://ds1.info/', site_key='6LcvFJskAAAAAEQ2Z9iuecjKZigx9rb6q9KacBKd')
        payload = {
            "phone": "+79309233611",
            "captcha_token": captcha
        }

        headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "45",
        "Content-Type": "application/json",
        "Host": "ds1.info",
        "Origin": "https://ds1.info",
        "Referer": "https://ds1.info/c/catalog",
        "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        session = requests.session()

        response = session.post('https://ds1.info/api/auth/sovremennik-delivery/phone/send-code', json=payload, headers=headers)
        print(f'sparc_food: {response.status_code}, {response.text}')

        with open('sparc_food.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}\n")

        return {"status_code": 200, "response": response.text}

    except Exception as e:
        print(f'Error occurred: {e}')
