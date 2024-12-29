import requests
from config import Proxy, Services
from utils.response_utils import get_cookies_and_headers

def send_sms_to_street_beat(phone_number: str):
    url = Services.STREET_BEAT
    cookie = get_cookies_and_headers('https://street-beat.ru/')
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryKmuDTrkxhgJaUP23",
        "Cookie": cookie,
        "origin": "https://street-beat.ru",
        "priority": "u=1, i",
        "referer": "https://street-beat.ru/cat/obuv/krossovki/new_balance/530/?utm_campaign=hand-search-brand-streetbeat-msk-45711237&utm_source=yandex&utm_medium=cpc&utm_term=%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%20%D1%81%D1%82%D1%80%D0%B8%D1%82%20%D0%B1%D0%B8%D1%82&utm_content=4387435697_0_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0_213_desktop_23942048340__23942048340__v3%7C%7C14949185209%7C%7C23942048340%7C%7C%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%20%D1%81%D1%82%D1%80%D0%B8%D1%82%20%D0%B1%D0%B8%D1%82%7C%7C1%7C%7Cpremium%7C%7Cnone%7C%7Csearch%7C%7Cno%7C%7C0&utm_id=45711237&yclid=7649501396109623295",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    data = {
        "phone": phone_number[1::1]
    }
    print(data)
    session = requests.session()

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    max_attempts = 5
    attempt = 0
    response = session.post(url, data=data, headers=headers, proxies=proxies)
    print("street_beat: ", response, response.text)
    with open('street_beat.log', 'a') as file:
        file.write(f"Ответ {response.status_code}, {response.text}\n")
    return {"status_code": response.status_code, "response": response.json()}