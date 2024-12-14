import requests
from config import Proxy, Services

def send_sms_to_thai_traditions(phone_number: str):
    try:
        url = Services.TTRADITIONS_URL

        payload = {
            "AUTH_FORM": "Y",
            "TYPE": "AUTH",
            "backurl": "",
            "USER_TEL": phone_number,
            "USER_FIO_NAME": "",
            "USER_TEL_CODE": ""
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        response = requests.post(url, data=payload, headers=headers, proxies=proxies)

        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)