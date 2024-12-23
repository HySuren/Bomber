import requests
from config import Proxy, Services
import json


def send_sms_to_china(phone_number: str):
    try:
        url = Services.CHINA

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "baggage": "sentry-environment=production,sentry-release=bf033780d2fc2f8b105b3e3187e5a2959cf8e11f,sentry-public_key=13b192a73bcc4c86b5b76d1dcac387db,sentry-trace_id=156be00f2e4e421da08c7cb61b838742",
            "content-type": "application/json",
            "origin": "https://my.express-today.ru",
            "priority": "u=1, i",
            "referer": "https://my.express-today.ru/registration?utm_source=yandex&utm_medium=cpl&utm_campaign=v_Novye_kreativy_MSK_SPB_161024&utm_content=cid%3A114970355_gid%3A5502992503_aid%3A1856942321745560758_st%3Asearch_pt%3Apremium_pos%3A2_src%3Anone_dvc%3Adesktop_reg%3A%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0_regid%3A213&utm_term=---autotargeting&utm_referrer=china&retpath=%2F%3Futm_source%3Dyandex%26utm_medium%3Dcpl%26utm_campaign%3Dv_Novye_kreativy_MSK_SPB_161024%26utm_content%3Dcid%253A114970355_gid%253A5502992503_aid%253A1856942321745560758_st%253Asearch_pt%253Apremium_pos%253A2_src%253Anone_dvc%253Adesktop_reg%253A%25D0%259C%25D0%25BE%25D1%2581%25D0%25BA%25D0%25B2%25D0%25B0_regid%253A213%26utm_term%3D---autotargeting%26yclid%3D14129684676723605503%26utm_referrer%3Dchina",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sentry-trace": "156be00f2e4e421da08c7cb61b838742",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        data = {
            "phone": phone_number,
            "ref": None,
            "utm": {
                "utm_source": "yandex",
                "utm_medium": "cpl",
                "utm_campaign": "v_Novye_kreativy_MSK_SPB_161024",
                "utm_content": "cid:114970355_gid:5502992503_aid:1856942321745560758_st:search_pt:premium_pos:2_src:none_dvc:desktop_reg:Москва_regid:213",
                "utm_term": "---autotargeting",
                "utm_referrer": "china"
            },
            "serviceMailing": True,
            "promotionMailing": True,
            "otherParams": {
                "yclid": "14129684676723605504"
            }
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.Session()
        session.post('https://my.express-today.ru/api/init-registration')  # Получение cookies
        cookies = session.cookies.get_dict()
        cookies_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])

        headers['cookie'] = cookies_str

        response = session.post(url, headers=headers, json=data, proxies=proxies)
        print("CHINA: ", response, response.text)
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
