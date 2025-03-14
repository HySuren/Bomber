import requests
from config import Proxy, Services
import time
import json

def send_sms_to_nfapteka(phone_number: str, proxy: str = Proxy.PROXY_URL):
    print("NFAPTEKA запущена")
    url = Services.NFAPTEKA

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://nfapteka.ru",
        "priority": "u=1, i",
        "referer": "https://nfapteka.ru/registration/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    data = {
        "component": "bxmaker.authuserphone.login",
        "sessid": "7e7739d52a7461de94728bc36bbab8e9",
        "method": "callCode",
        "phone": phone_number,
        "registration": "Y"
    }

    proxies = {
        "http": proxy,
        "https": proxy
    }

    session = requests.session()
    cooki = session.get('https://nfapteka.ru/registration/')
    session.cookies.update(cooki.cookies)

    response = session.post(url, headers=headers, data=data, proxies=proxies)
    session.cookies.update(response.cookies)
    print(response.text)
    print("Звонок сделан, ждемс 50 сек")

    time.sleep(50)

    data = {
        "component": "bxmaker.authuserphone.login",
        "sessid": "7e7739d52a7461de94728bc36bbab8e9",
        "method": "sendCode",
        "phone": phone_number,
        "registration": "Y"
    }

    max_attempts = 5
    attempt = 0


    print("NFAPTEKA: ",response, response.text)
    while attempt < max_attempts:
        try:
            response = session.post(url, headers=headers, data=data)
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
            if response.status_code == 443:
                print("Proxy error occurred, retrying...")
                attempt += 1
                continue
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
