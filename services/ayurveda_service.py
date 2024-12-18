import requests
from config import Proxy, Services

def send_sms_to_ayurveda(phone_number: str):
    try:
        url = Services.AYURVEDA_URL

        form_data = {
            "data[firstname]": "sssss",
            "data[lastname]": "dddddd",
            "data[phone]": phone_number,
            "data[email]": "examplesssw@mail.ru",
            "wa_json_mode": "1",
            "need_redirects": "1",
            "contact_type": "person"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, data=form_data, headers=headers)
        with open('ayurveda.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)