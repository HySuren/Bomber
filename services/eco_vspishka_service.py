import requests
from bs4 import BeautifulSoup
import json
from utils.response_utils import save_logs
from config import Services, Proxy


def send_sms_to_eco_vspishka(phone_number: str):
    url = Services.ECO_VPISKA

    session = requests.Session()

    response = session.get('https://ecopishka.ru/sign-in')

    if response.status_code != 200:
        print("Ошибка при получении страницы:", response.status_code)
        return {"status_code": response.status_code, "response": 'error'}

    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

    data = {
        "_csrf": csrf_token,
        "LoginSmsForm[check]": 14,
        "LoginSmsForm[phone]": phone_number
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://ecopishka.ru",
        "referer": "https://ecopishka.ru/sign-in",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/132.0.0.0 Safari/537.36"
        ),
        "x-csrf-token": csrf_token,
        "x-requested-with": "XMLHttpRequest"
    }

    # Отправляем POST-запрос с данными и заголовками
    response = session.post(url, data=data, headers=headers)

    # Логируем ответ
    response_size = len(response.content) + len(json.dumps(dict(response.headers)))
    print(response.status_code, response.text)
    save_logs(
        service_name="ECO_PISHKA",
        status_code=str(response.status_code),
        response=response.content[:500],
        domain="https://ecopishka.ru",
        weight=response_size,
        headers=dict(response.headers),
        body=response.json() if response.headers.get("Content-Type") == "application/json" else None
    )

    return {"status_code": response.status_code, "response": 'good'}