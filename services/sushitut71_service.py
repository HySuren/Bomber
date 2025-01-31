import requests
from utils.email_generate import generate_random_string
from config import Services, Proxy

def send_sms_to_mybox(phone_number: str):
    url = Services.MYBOX

    session = requests.Session()
    data = {
        "phone": "9309233671",
        "type": "auth",
        "apiKey": "2249e53bebea8fd7aeb90cf61583111a36f81a6e258795eb467ad685bf40118a8"
    }
    random_str = generate_random_string()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "connection": "keep-alive",
        "content-length": "112",
        "content-type": "application/json",
        "deviceid": f"424a84bf-02cc-46b2-9e58-77{random_str}63016185c1",
        "devicetype": "Desktop",
        "host": "mybile.mybox.ru",
        "origin": "https://mybox.ru",
        "platformid": "site",
        "referer": "https://mybox.ru/",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    response = session.post(url, proxies=proxies, json=data, headers=headers)
    print(response.url)
    return {"status_code": response.status_code, "response": response.text}