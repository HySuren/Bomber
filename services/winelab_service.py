import requests
import random
import string
from config import Proxy, Services
import json


def generate_char():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))


def send_sms_to_winelab(phone_number: str):
    try:
        url = Services.WINELAB
        char_generate = generate_char()
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "priority": "u=1, i",
            "referer": f"https://www.winelab.ru/?ysclid=m4xzfngek5{char_generate}",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-dtpc": "62$173641443_960h26vLIOFAPTSAGQBJGDTUGGVCQDBJAOWVMBN-0e0",
            "x-requested-with": "XMLHttpRequest"
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.session()
        response = session.get(url, headers=headers, params={'number': phone_number}, proxies=proxies)
        print("WINELAB: ", response, response.text)
        with open('logs\\winelab.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
            file.write('-----------------------------------------------------------------------')
        response.raise_for_status()
        try:
            response_json = response.json()
            return {"status_code": response.status_code, "response": response_json}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Response: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {"status_code": None, "response": str(e)}
    except Exception as e:
        print(f"Unhandled error: {e}")
        return {"status_code": None, "response": str(e)}
