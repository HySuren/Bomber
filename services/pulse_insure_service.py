import requests
from config import Proxy, Services

def send_sms_to_pluse_insure(phone_number: str):
    try:
        url = Services.PLUSE

        payload = {
            "authenticationUser": {
                "phoneNumber": phone_number
            }
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        headers = {
            "X-Process-ID": "6f63116e-d224-4a41-a5ad-0e528b9eac65",
            "X-Platform-Type": "RuStore",
            "X-Application-Version": "4.26.0",
            "X-Publisher": "PUB_01",
            "X-Store": "RUSTORE",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "api-prod.app.pulse.insure",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.12.0"
        }

        session = requests.session()

        response = session.post(url, json=payload, headers=headers)
        print(f'PLUSE: {response.status_code}, {response.text}')
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(e)
