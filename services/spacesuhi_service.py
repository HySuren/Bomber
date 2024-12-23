import requests
from config import Proxy, Services
import json
from capmonster_python import RecaptchaV2Task

def send_sms_to_spacesuhi(phone_number: str):
    try:
        url = Services.SPACESUHI

        headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-length": "30",
        "content-type": "application/json",
        "origin": "https://spacesushi.moscow",
        "priority": "u=1, i",
        "referer": "https://spacesushi.moscow/auth/phone?ref=profile",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

        data = {
        "phoneNumber": phone_number
    }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.session()
        cooki = session.post(url)
        headers_cooki = cooki.cookies.get_dict()
        session.cookies.update(cooki.cookies)
        cookies_str = "; ".join([f"{key}={value}" for key, value in headers_cooki.items()])
        headers['cookie'] = cookies_str
        response = session.post(url,json=data,headers=headers)

        print("SPACESUHI: ",response, response.text)
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
