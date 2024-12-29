import requests
from config import Proxy, Services
import json
from utils.anti_captcha import main, create_task, get_task_result
from bs4 import BeautifulSoup
from utils.response_utils import get_cookies_and_headers

def send_sms_to_yasm(phone_number: str):
    url = Services.YSAM
    cookie = get_cookies_and_headers('https://insneaker.ru').get('Cookie')
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "host": "insneaker.ru",
        "Cookie": cookie,
        "origin": "https://insneaker.ru",
        "referer": "https://insneaker.ru/client_account/session/new",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-csrf-token": "",
        "x-requested-with": "XMLHttpRequest"
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    session = requests.session()

    # Получаем куки и CSRF-токен
    cooki = session.get('https://insneaker.ru/', proxies=proxies)

    soup = BeautifulSoup(cooki.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'authenticity_token'})

    if csrf_input and 'value' in csrf_input.attrs:
        csrf_token = csrf_input['value']
        headers['x-csrf-token'] = csrf_token

    data = {
        'login': phone_number,
        'type': 'phone',
        'g-recaptcha-response': main(url='https://insneaker.ru/', site_key='6LcZi0EmAAAAAPNov8uGBKSHCvBArp9oO15qAhXa')
    }

    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:
            response = session.post(url, headers=headers, proxies=proxies, data=data)
            print("YSAM: ", response, response.text)
            with open('ysam.log', "w") as file:
                file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
            response.raise_for_status()

            try:
                response_json = response.json()  # Изменено для правильного получения JSON
                return {"status_code": response.status_code, "response": response_json}
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}, Response: {response.text}")
                return {"status_code": response.status_code, "response": response.text}

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 443:  # Обрабатываем ошибку 443
                print("Proxy error occurred, retrying...")
                attempt += 1
                continue  # Переходим к следующей попытке
            else:
                print(f"HTTP error occurred: {http_err}")
                return {"status_code": response.status_code, "response": str(http_err)}

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return {"status_code": None, "response": str(e)}

        except Exception as e:
            print(f"Unhandled error: {e}")
            return {"status_code": None, "response": str(e)}

    print("Max attempts reached, giving up.")
    return {"status_code": None, "response": "Max attempts reached"}
