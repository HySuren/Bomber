import requests
def send_sms_to_ayurveda(phone_number: str):
    try:
        url = 'https://www.ayurveda-shop.ru/signup/'
        form_data = {
            "data[firstname]": "Манга",
            "data[lastname]": "Live",
            "data[phone]": phone_number,
            "data[email]": "example@mail.ru",
            "wa_json_mode": "1",
            "need_redirects": "1",
            "contact_type": "person"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.post(url, data=form_data, headers=headers)

        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)