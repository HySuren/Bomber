import requests
from config import Proxy, Services
import json

def send_sms_to_beautery(phone_number: str):
    try:
        url = Services.BEAUTERY

        headers = {
  "accept": "application/json, text/plain, */*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
  "content-length": "104",
  "content-type": "application/json",
  "cookie": "viewed_products=%5B35751%5D; _ym_uid=1734009414507603540; _ym_d=1734009414; _ga=GA1.1.21568723.1734009414; klcid=510; searchbooster_v2_user_id=PpXMSryE_3d7qNpHVy9U4_ddUWh41Zn1xdTwBiwlf4A%7C11.19.19.24; ageCheckPopupRedirectUrl=%2Fv2-mount-input; SL_G_WPT_TO=ru; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _ym_isad=1; _ym_visorc=w; _ga_YDSJPTSP1G=GS1.1.1734718749.3.1.1734718763.0.0.0; PHPSESSID=m5l2tg1ho123u0p7nibqjp4go0",
  "origin": "https://beautery.ru",
  "priority": "u=1, i",
  "referer": "https://beautery.ru/api/user/",
  "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


        data = {
        "user_phone": phone_number,

    }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, headers=headers, json=data, proxies=proxies)
        with open('logs\\beautery.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        response.raise_for_status()

        try:
            response_json = response.json()
            return {"status_code": response.status_code, "response": response_json}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Response: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {"status_code": response.status_code, "response": str(e)}
    except Exception as e:
        print(f"Unhandled error: {e}")
        return {"status_code": None, "response": str(e)}