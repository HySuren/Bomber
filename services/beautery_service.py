import tls_client
import json
from config import Proxy, Services

def send_sms_to_beautery(phone_number: str):
    try:
        url = Services.BEAUTERY

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        data = {
            "full_name": "ghjkl;ljhb",
            "user_phone": phone_number,
            "email": "teru@mail.ru",
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
            json=data
        )

        # Логирование ответа
        with open('beautery.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")

        response.raise_for_status()

        try:
            response_json = response.json()
            return {"status_code": response.status_code, "response": response_json}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Response: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
    except tls_client.exceptions.TLSClientError as e:
        print(f"TLS Client error: {e}")
        return {"status_code": None, "response": str(e)}
    except Exception as e:
        print(f"Unhandled error: {e}")
        return {"status_code": None, "response": str(e)}
