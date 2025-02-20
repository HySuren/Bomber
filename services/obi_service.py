import requests
from config import Proxy, Services
import json
from utils.response_utils import get_cookies_and_headers

def send_sms_to_obi(phone_number: str):
    try:
        url = Services.OBI
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        data = {
            "query": "mutation($phone_1:String!){startLogin(phone:$phone_1){exists,error{type}}}",
            "variables": {
                "phone_1": phone_number[1::1]
            }
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.session()
        response = session.post(url, headers=headers, proxies=proxies, json=data)
        print("OBI: ", response, response.text)
        with open('logs\\obi.log', "w") as file:
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
