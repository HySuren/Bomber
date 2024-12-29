import requests
from config import Proxy, Services

def send_sms_to_svoi(phone_number: str):
    url = Services.SVOI

    headers = {
      "accept": "*/*",
      "accept-encoding": "gzip, deflate, br, zstd",
      "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
      "connection": "keep-alive",
      "content-length": "360",
      "content-type": "application/json",
      "host": "svoi.ru",
      "origin": "https://svoi.ru",
      "referer": "https://svoi.ru/online/login",
      "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"Windows\"",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Ap"
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    session = requests.session()
    cooki = session.get('https://svoi.ru/online/login')
    session.cookies.update(cooki.cookies)

    data = {
        "operationName": "sendCode",
        "variables": {
            "sendCodeInput": {
                "phone": phone_number,
                "captchaToken": None
            }
        },
        "query": "mutation sendCode($sendCodeInput: SendCodeInput!) {\n  sendCode(input: $sendCodeInput) {\n    status\n    errors {\n      code\n      subject\n      systemMessage\n      userMessage\n      params\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:
            response = session.post(url, json=data, headers=headers, proxies=proxies)
            response.raise_for_status()
            print("YSAM: ", response, response.text)
            with open('ysam.log', "w") as file:
                file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
            response.raise_for_status()

            try:
                response_json = response.json()  # Изменено для правильного получения JSON
                return {"status_code": response.status_code, "response": response_json}
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}, Response: {response.text}")
                return {"status_code": response.status_code, "response": response.text}

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 443:
                print("Proxy error occurred, retrying...")
                attempt += 1
                continue
            else:
                print(f"HTTP error occurred: {http_err}")
                return {"status_code": response.status_code, "response": str(http_err)}

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return {"status_code": None, "response": str(e)}

        except Exception as e:
            print(f"Unhandled error: {e}")
            return {"status_code": None, "response": str(e)}

    print("Max attempts reached, giving up.")
    return {"status_code": None, "response": "Max attempts reached"}

