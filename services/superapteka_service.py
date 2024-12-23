import requests
from config import Proxy, Services
import json
from capmonster_python import RecaptchaV2Task


def send_sms_to_superapteka(phone_number: str):
    try:
        url = Services.SUPERAPTEKA

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        capmonster = RecaptchaV2Task("2b34ab1ed18543953dd6c4751bebd58e")
        task_id = capmonster.create_task("https://superapteka.ru/", "6LfuiY8aAAAAAHlIASGG4el8o7Y2zUEjnIXX7bkb")
        result = capmonster.join_task_result(task_id)
        capcha = result.get("gRecaptchaResponse")

        data = {
            "phоne": phone_number,
            "g-recaptcha-response": capcha
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, headers=headers, json=data, proxies=proxies)
        print("SUPERAPTEKA: ", response, response.text)
        with open('logs\\superapteka.log', "w") as file:
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
