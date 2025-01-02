import requests
from config import Proxy, Services
from utils.email_generate import generate_random_string

def send_sms_to_happywear(phone_number: str):
    try:
        url = Services.HAPPYWEAR
        email = generate_random_string()
        payload = {
        'phone': f'%2B7+({phone_number[2:5:1]})+{phone_number[5:8:1]}-{phone_number[8::1]}',
        'fullName': 'Daniel+Vorin',
        'firstName': 'Daniel',
        'lastName': 'Vorin',
        'email': f'{email}@mail.ru',
        'allowEmail': True,
        'referralName': None,
        'segmentIds': 'unfinished_onboarding',
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }
        session = requests.session()

        response = session.get(url, params=payload, proxies=proxies)
        print(response.text)
        with open('happywear_service.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)
