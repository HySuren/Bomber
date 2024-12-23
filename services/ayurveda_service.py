import requests
from config import Proxy, Services


def send_sms_to_ayurveda(phone_number: str):
    try:
        url = Services.AYURVEDA_URL

        form_data = {
            "data[firstname]": "sssss",
            "data[lastname]": "dddddd",
            "data[phone]": phone_number,
            "data[email]": "examplesssw@mail.ru",
            "wa_json_mode": "1",
            "need_redirects": "1",
            "contact_type": "person"
        }

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "referer=https%3A%2F%2Fyandex.ru%2F; _ga=GA1.1.1396994314.1733611678; cityselect__kladr_id=3601900000800; cityselect__fias_id=3237ad6b-7bd7-42ba-840e-7f98442b4785; cityselect__constraints_street=3601900000800; cityselect__country=rus; cityselect__city=%D0%9A%D0%BE%D0%BF%D0%B0%D0%BD%D0%B0%D1%8F%201-%D1%8F; cityselect__region=36; cityselect__zip=396675; cityselect__show_notifier=1733611692; seoyandexmetrika__FirstViewedPageType=%D0%A1%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%20%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8; _ym_uid=1733611691383579359; _ym_d=1733611691; landing=%2F; PHPSESSID=hnuakbdrsoodet3suvt4mkhova; dp_plugin_country=rus; dp_plugin_region=77; dp_plugin_city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; is_mobile=false; SL_G_WPT_TO=ru; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _ym_isad=1; _ga_VKW134GWGR=GS1.1.1734785004.12.1.1734785017.47.0.0",
            "origin": "https://www.ayurveda-shop.ru",
            "priority": "u=1, i",
            "referer": "https://www.ayurveda-shop.ru/signup/",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        session = requests.session()
        cooki = session.get('https://www.ayurveda-shop.ru/')
        session.cookies.update(cooki.cookies)
        response = session.post(url, data=form_data, proxies=proxies, headers=headers)
        with open('logs\\ayurveda.log', "w") as file:
            file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
        print('AURUVEDA: ', {"status_code": response.status_code, "response": response.text})
        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)
