import requests

def send_sms_to_dommalera(phone_number: str):
    try:
        url = f'https://www.dommalera.ru/ajax/sms_login.php?&phoneauth={phone_number}'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.post(url, headers=headers)
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)