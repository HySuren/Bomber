import requests
from config import Proxy, Services

def send_sms_to_akbars(phone_number: str):
    try:
        url = Services.BANKI_RU

        payload = {
        "phone": phone_number[2::1]
        }

        headers = headers = {
          "accept": "application/json, text/plain, */*",
          "accept-encoding": "gzip, deflate, br, zstd",
          "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
          "access-control-allow-headers": "*",
          "connection": "keep-alive",
          "content-length": "22",
          "content-type": "application/json",
          "devicetoken": '',
          "host": "bankok.akbars.ru",
          "origin": "https://online.akbars.ru",
          "referer": "https://online.akbars.ru/",
          "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-site",
          "sessiontoken": '',
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
          "x-protoobp-origin": "rum",
          "x-protoobp-parent-id": '297100131609950256',
          "x-protoobp-sampling-priority": '1',
          "x-protoobp-trace-id": '5999873919299026104'
        }


        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, json=payload, proxies=proxies, headers=headers)
        with open('banki_ru.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)