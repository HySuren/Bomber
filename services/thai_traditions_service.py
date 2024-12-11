import requests

def send_sms_to_thai_traditions(phone_number: str):
    try:
        payload = {
            "AUTH_FORM": "Y",
            "TYPE": "AUTH",
            "backurl": "",
            "USER_TEL": phone_number,
            "USER_TEL_CODE": ""
        }
        response = requests.post('https://thai-traditions.ru/auth/ajax_registration.php', data=payload)
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)