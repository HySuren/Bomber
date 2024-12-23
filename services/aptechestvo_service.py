import requests
from config import Proxy, Services


def send_sms_to_aptech(phone_number: str):
    try:
        url = Services.APTECH

        headers = {
            "accept": "text/plain, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",  # Изменено: Убрал content-length
            "origin": "https://aptechestvo.ru",
            "priority": "u=1, i",
            "referer": "https://aptechestvo.ru/",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        data2 = {
            "phone": phone_number
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        URL2 = 'https://aptechestvo.ru/ajax/new_app/sms/send_sms_code.php'

        try:
            session = requests.session()
            cooki = session.get('https://aptechestvo.ru/')
            session.cookies.update(cooki.cookies)
            response = session.post(url, headers=headers, proxies=proxies, data=data2)
            response.raise_for_status()
            print("APTECH: ", {"status_code": response.status_code, "response": response.text})
            with open('logs\\aptech.log', 'w') as file:
                file.write(f"Статус код: {str(response.status_code)}\nОтвет: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
        except Exception as e:
            print(f"Произошла неизвестная ошибка: {e}")
    except Exception as e:
        print(e)
