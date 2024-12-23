import requests
from config import Proxy, Services


def send_sms_to_poizonshop(phone_number: str):
    try:
        url = Services.POIZONSHOP

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "baggage": "sentry-environment=production,sentry-release=tDQA0vcu_ZA2wVggYFs5f,sentry-public_key=6ab658e3aabef9ba3a1ed978eac97393,sentry-trace_id=1dc13d6d2bb74ad48b283acaa2822854,sentry-sample_rate=1,sentry-sampled=true",
            "connection": "keep-alive",
            "content-length": "23",
            "content-type": "application/json",
            "host": "poizonshop.ru",
            "origin": "https://poizonshop.ru",
            "referer": "https://poizonshop.ru/sneakers",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sentry-trace": "1dc13d6d2bb74ad48b283acaa2822854-901b170d05a3de69-1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        session = requests.Session()
        response = session.get('https://poizonshop.ru/')
        cookies = session.cookies.get_dict()
        cookies_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])

        headers['cookie'] = cookies_str
        data = {
            "phone": phone_number[1::1]
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = session.post(url, json=data, headers=headers, proxies=proxies)
        print("POIZONSHOP: ", {"status_code": response.status_code, "response": response.text})
        with open("logs\\poizonshop.log", "w") as file:
            file.write(f"poizonshop responce status_code: {response}, text: {response.text}")
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(f'poizonshop ERROR: {e}')
