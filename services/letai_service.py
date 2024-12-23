import requests
import random
import string
from config import Proxy, Services


def generate_device_id(length=9):
    """Генерирует случайный device_id заданной длины."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def send_sms_to_letai(phone_number: str):
    try:
        url = Services.LETAI

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "connection": "keep-alive",
            "content-length": "58",
            "content-type": "application/json",
            "host": "newlk.letai.ru",
            "origin": "https://cabinet.letai.ru",
            "referer": "https://cabinet.letai.ru/",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "version": "300"
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.session()
        cooki = session.get('https://cabinet.letai.ru/')
        session.cookies.update(cooki.cookies)

        device_id = generate_device_id()
        data = {
            "phone": phone_number,
            "device_id": device_id
        }
        response = session.post(url, json=data, headers=headers, proxies=proxies)
        response.raise_for_status()

        print("LETAI: ", response, response.text)
        with open('logs\\litai.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        response.raise_for_status()
        try:
            response_json = response
            return {"status_code": response.status_code, "response": response_json.text}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Response: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {"status_code": response.status_code, "response": str(e)}
    except Exception as e:
        print(f"Unhandled error: {e}")
        return {"status_code": None, "response": str(e)}
