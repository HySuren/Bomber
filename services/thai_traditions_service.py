import requests
import tls_client
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

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': str(len(payload)),
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://thai-traditions.ru',
            'priority': 'u=1, i',
            'referer': 'https://thai-traditions.ru/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-kl-kfa-ajax-request': 'Ajax_Request',
            'x-requested-with': 'XMLHttpRequest'
        }

        session = tls_client.Session(
            client_identifier="chrome_131",
            proxies={
                "http": Proxy.PROXY_URL,
                "https": Proxy.PROXY_URL,
            }
        )

        response = session.post(
            url=url,
            headers=headers,
            json=payload
        )
        with open('TTraditions.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        print(e)