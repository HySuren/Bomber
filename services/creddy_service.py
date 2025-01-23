import requests
from config import Proxy, Services

def send_sms_to_creddy(phone_number: str):

    url = Services.CREDDY
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://client.creddy.ru",
        "priority": "u=1, i",
        "referer": "https://client.creddy.ru/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    data = {
        "phone_number": phone_number[1::1]
    }

    session = requests.session()

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        try:
            response = session.post(f'https://api-auth.creddy.ru/api/v1/user',json=data, headers=headers, proxies=proxies)
            print("creddy: ", response, response.text)
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
