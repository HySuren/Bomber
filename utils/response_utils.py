from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import DB_CONFIG
import psycopg2
import json


def get_cookies_and_headers(url, mode='default'):
    # Настройка опций для headless режима
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)

        cookies = driver.get_cookies()

        cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        if mode == 'default':
            return cookie_string
        elif mode == 'sessid':
            return driver.session_id
        elif mode == 'dicts':

            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            return {"cookie": cookie_dict}
    finally:
        driver.quit()


def remove_null_bytes(s):
    if isinstance(s, str):
        return s.replace('x00', '')
    elif isinstance(s, dict):
        return {k: remove_null_bytes(v) for k, v in s.items()}
    return s


def save_logs(service_name: str, status_code: str, response: str, domain: str, weight: int, headers: dict,
              body: dict = None):
    try:
        service_name = remove_null_bytes(service_name)
        status_code = remove_null_bytes(status_code)
        response = remove_null_bytes(response)
        headers = remove_null_bytes(headers)
        body = remove_null_bytes(body)

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        response_info = {
            "domain": domain,
            "weight": weight,
            "headers": headers,
            "body": body if body else {}
        }

        cursor.execute(
            """INSERT INTO logs (service_name, status_code, response, response_info)
               VALUES (%s, %s, %s, %s)""",
            (service_name, status_code, response, json.dumps(response_info))
        )

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Лог успешно сохранен для сервиса {service_name}")

    except Exception as error:
        print(f"Ошибка при сохранении лога: {error}, {type(error)}")