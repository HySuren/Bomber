import requests

def send_sms_to_nadodeneg(phone_number: str):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-length": "287",
        "content-type": "application/json",
        "origin": "https://nadodeneg.ru",
        "priority": "u=1, i",
        "referer": "https://nadodeneg.ru/application/registration/phone",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "user-agent-data": "Windows 15.0.0 / fullVersionBrowser: 132.0.6834.111",
        "x-frontend": "prod-ru-nd-wp2_prod_develop"
    }
    print(f'NADODENEG: {phone_number}')

    payload = {
    "mobile_phone": phone_number,
    "step": "Step1",
    "target_url": "https://nadodeneg.ru/?utm_source=bankiru&utm_medium=affiliate&utm_campaign=bankiru_cps&click_id=24b94b045612a46bda614a1eff8d83a9&utm_term=bankiru&ndl",
    "requested_amount": 10000,
    "requested_days": 7,
    "ga_cid": "1903338519.1738292500"
    }

    response = requests.post('https://nadodeneg-api-gateway.srv.mendep.ru/user', json=payload, headers=headers)
    token = response.json()['token']
    user_id = response.json()['id']
    headers['x-authorization'] = f'Bearer {token}'

    payload = {
    "step": "Step2"
    }

    response = requests.patch(f'https://nadodeneg-api-gateway.srv.mendep.ru/user/{user_id}', json=payload, headers=headers)
    return {"status_code": response.status_code, "response": response.text}