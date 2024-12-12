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
            "USER_TEL_CODE": ""
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, data=payload, proxies=proxies)

        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)