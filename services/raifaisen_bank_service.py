import requests
from config import Proxy, Services


def send_sms_to_raiffeisen(phone_number: str):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru",
        "authorization": "Basic cHJvZC1jbGllbnQtaWQ6eHh+Yjd9ZU8yUSR7eVkqe3ROTDRTZTBhaiR5KkA0Uks=",
        "connection": "keep-alive",
        "content-type": "application/json;charset=UTF-8",
        "host": "online.raiffeisen.ru",
        "origin": "https://online.raiffeisen.ru",
        "rc-device": "web",
        "referer": "https://online.raiffeisen.ru/login/main",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-device-id": "ba69b503-9edf-47d9-a47a-4a9299b44b18",
        "x-gib-fgsscgib-w-raiffeisen": "Lw8Bcf6dfb749eefb7891c7b0053e1067aad0c02",
        "x-gib-gsscgib-w-raiffeisen": "jEclLpV86n6z+BfEmwXu/ukpNqksVCzQsZ7DXzh7sK6sKPYyuOwkhHgG9vhU9FEDE3pF5ZR3Vspkgl14whYLyCqk9X238U1LXEzVdITWH+ICs16naZ6S3S6KsMhOu8Ghc2Tl3JvhwNtVvqtlMxqAIk6Tq6z7IuUD/L1/u/Pwjk6amStwipdqJvxBpVroBbfv9sP+4FRNXkIDwLj08YZCc2hj8IVwXuxUAKunIryYDEkILs/tugLA2mxU6sWR+0jo7g==",
        "x-platform": "web",
        "x-request-id": "18afb32e-8528-43cf-8690-1b19b490886a",
        "x-session-id": "25a7b203-735a-4231-aba8-6854595c33a3"
    }

    get_token = {
        "grant_type": "phone",
        "phone": phone_number,
        "platform": "web",
        "version": "58815",
        "device_install_id": "ba69b503-9edf-47d9-a47a-4a9299b44b18"
    }

    session = requests.session()
    cooki = session.get('https://online.raiffeisen.ru/')
    session.cookies.update(cooki.cookies)
    get_req_token = session.post('https://online.raiffeisen.ru/id/oauth/id/token', headers=headers, json=get_token)
    access_token = get_req_token.json()['access_token']

    payload = {
        "mfa_token": access_token
    }


    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:
            responce = session.post(Services.RAIFFEISEN, json=payload, headers=headers)
            print("RAIFAISEN: ", response, response.text)
            with open('RAIFAISEN.log', "w") as file:
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
