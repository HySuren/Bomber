import requests
from config import Proxy, Services
import json


def send_sms_to_4lapy(phone_number: str):
    url = Services.FOUR_LAPY
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    data = {
        "phone": phone_number[1:]
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.post(url, headers=headers, data=data, proxies=proxies)
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
