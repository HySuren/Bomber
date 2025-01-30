import requests
from utils.response_utils import get_cookies_and_headers
from utils.anti_captcha import main, create_task, get_task_result
from config import Services

def send_sms_to_chibbis(phone_number: str):
    url = Services.CHIBBIS

    session = requests.Session()
    cookie = get_cookies_and_headers(url='https://chibbis.ru/tula')
    captcha = main(url='https://chibbis.ru/', captcha_type='RecaptchaV2TaskProxyless', site_key='6Lc92QoUAAAAANkFHHIwmosiM1E3k9JI88fyxVDf')

    data = {
        "phone": phone_number[1::1]
    }

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://chibbis.ru",
        "cookie": cookie,
        "grecaptchatoken": captcha,
        "priority": "u=1, i",
        "referer": "https://chibbis.ru/tula",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }


    response = session.post('https://chibbis.ru/webapi/auth/verification-code', json=data, headers=headers)
    return {"status_code": response.status_code, "response": response.text}

