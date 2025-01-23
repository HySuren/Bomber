import requests
from config import Proxy, Services
import json
from utils.anti_captcha import main, create_task, get_task_result
from bs4 import BeautifulSoup

def send_sms_to_yasm(phone_number: str):
    url = Services.YSAM

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    session = requests.session()

    # Получаем куки и CSRF-токен
    cooki = session.get('https://insneaker.ru/', proxies=proxies)

    soup = BeautifulSoup(cooki.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'authenticity_token'})

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "host": "insneaker.ru",
        "Cookie": 'ins_myshop-cas393=a37rkt-aa8173341d7bdb69e5e907400378a70a; first_current_location=%2F; first_referer=; referer=; current_location=%2F; ins_order_version=1737637942.31506; visit=t; pnn_status_check=good; _ym_uid=1737637842505426854; _ym_d=1737637842; _ym_isad=1; SL_G_WPT_TO=ru; _ym_visorc=w; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; cart=%7B%22comment%22%3Anull%2C%22payment_title%22%3Anull%2C%22payment_description%22%3Anull%2C%22delivery_description%22%3Anull%2C%22delivery_price%22%3A0.0%2C%22number%22%3Anull%2C%22delivery_date%22%3Anull%2C%22delivery_from_hour%22%3Anull%2C%22delivery_to_hour%22%3Anull%2C%22delivery_title%22%3Anull%2C%22delivery_from_minutes%22%3Anull%2C%22delivery_to_minutes%22%3Anull%2C%22items_count%22%3A0%2C%22items_price%22%3A0.0%2C%22order_lines%22%3A%5B%5D%2C%22discounts%22%3A%5B%5D%2C%22total_price%22%3A0.0%7D; x_csrf_token=wcrfvuooJI55qV2SzE918C9QZ_iEki0sJLu96kgA7tij5_-jgirIHy2R5fK_-PM7GneZXts-nfqQDMtw_RhBFQ',
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

    if csrf_input and 'value' in csrf_input.attrs:
        csrf_token = csrf_input['value']
        headers['x-csrf-token'] = csrf_token
        headers['Cookie'] = f'ins_myshop-cas393=a37rkt-aa8173341d7bdb69e5e907400378a70a; first_current_location=%2F; first_referer=; referer=; current_location=%2F; ins_order_version=1737637942.31506; visit=t; pnn_status_check=good; _ym_uid=1737637842505426854; _ym_d=1737637842; _ym_isad=1; SL_G_WPT_TO=ru; _ym_visorc=w; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; cart=%7B%22comment%22%3Anull%2C%22payment_title%22%3Anull%2C%22payment_description%22%3Anull%2C%22delivery_description%22%3Anull%2C%22delivery_price%22%3A0.0%2C%22number%22%3Anull%2C%22delivery_date%22%3Anull%2C%22delivery_from_hour%22%3Anull%2C%22delivery_to_hour%22%3Anull%2C%22delivery_title%22%3Anull%2C%22delivery_from_minutes%22%3Anull%2C%22delivery_to_minutes%22%3Anull%2C%22items_count%22%3A0%2C%22items_price%22%3A0.0%2C%22order_lines%22%3A%5B%5D%2C%22discounts%22%3A%5B%5D%2C%22total_price%22%3A0.0%7D; x_csrf_token={csrf_token}',

    data = {
        'login': phone_number,
        'type': 'phone',
        'g-recaptcha-response': main(url='https://insneaker.ru/', site_key='6LcZi0EmAAAAAPNov8uGBKSHCvBArp9oO15qAhXa'),
        'recaptcha_type': 'invisible'
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
