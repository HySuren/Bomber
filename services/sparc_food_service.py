import requests
from config import Proxy, Services
from utils.anti_captcha import main,get_task_result,create_task
from utils.email_generate import generate_random_string
def send_sms_to_sparc_food(phone_number: str):
    try:
        url = Services.SPARC_FOOD

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }
        sessid = generate_random_string()
        payload = {
            "sessid": f"94d8bcdaa0{sessid}ed72846a32ee4938",
            "AUTH_FORM": "Y",
            "TYPE": "REGISTRATION",
            "USER_NAME": "fefefe",
            "USER_LAST_NAME": "Daniel",
            "USER_LOGIN": "fefefefe4",
            "USER_PASSWORD": "d040715e",
            "USER_CONFIRM_PASSWORD": "d040715e",
            "USER_PHONE_NUMBER": "+7 (930) 923-36-11",
            "Register": "Зарегистрироваться"
        }

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-length": "344",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "__ddg9_=77.74.187.178; __ddg1_=q3AY2IlQ7A0iu0BaErHu; PHPSESSID=OOQBkZadCC762c0QkxPHMSJwGWybiGeZ; BITRIX_SM_SALE_UID=8897677; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1738270740%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ym_uid=1738220597240199637; _ym_d=1738220597; _ym_isad=1; BX_USER_ID=37d1bc3254a41ebb7b447d12bbe77a7b; _ym_visorc=w; SL_GWPT_Show_Hide_tmp=0; SL_G_WPT_TO=ru; SL_wptGlobTipTmp=1; __ddg10_=1738220742; __ddg8_=sUHlpffa7FMkcfiS",
            "origin": "https://sparc-food.com",
            "priority": "u=0, i",
            "referer": "https://sparc-food.com/personal/profile/?register=yes",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }

        session = requests.session()

        response = session.post(url, data=payload, headers=headers)
        print(f'sparc_food: {response.status_code}, {response.text}')

        with open('sparc_food.log', "a") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}\n")

        return {"status_code": 200, "response": response.text}

    except Exception as e:
        print(f'Error occurred: {e}')

send_sms_to_sparc_food('9')