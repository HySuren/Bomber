import requests
import tls_client
from config import Proxy, Services
import json

def send_sms_to_bykdabaran(phone_number: str):
    try:
        url = Services.BYKDABARAN

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        payload = {
            "phone": phone_number[1::1],
            "g-recaptcha-version": 3
        }

        session = tls_client.Session(
            client_identifier="chrome_131"
        )

        response = session.post(
            url=url,
            headers=headers,
            json=payload
        )

        with open('bykdabaran.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        response.raise_for_status()

        try:
            response_json = response
            return {"status_code": response.status_code, "response": response_json.text}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Response: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {"status_code": response.status_code, "response": str(e)}
    except Exception as e:
        print(f"Unhandled error: {e}")
        return {"status_code": None, "response": str(e)}
