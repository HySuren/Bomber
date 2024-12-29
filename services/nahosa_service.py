import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



def send_sms_to_nahosa(phone_number: str):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Открываем окно в полном экране
        driver.maximize_window()

        # Открываем нужный URL
        url = 'https://naohasa.ru/login?redirectTo=%2F%3F%3Futm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3D115849262%26utm_content%3D16693431967%26utm_term%3D---autotargeting%26desktop%26%25D0%259C%25D0%25BE%25D1%2581%25D0%25BA%25D0%25B2%25D0%25B0%26yclid%3D18011288710375538687'
        driver.get(url)

        # Ждем 1 секунду после загрузки страницы
        time.sleep(2)

        # Явное ожидание: ждем, пока кнопка "Войти" станет кликабельной и кликаем по ней
        wait = WebDriverWait(driver, 10)

        # Ждем, пока поле для ввода номера телефона станет доступным
        phone_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='tel' and @placeholder='+7 (999) 000-00-00']"))
        )

        # Вводим номер телефона (замените 'YOUR_PHONE_NUMBER' на нужный номер)
        phone_input.send_keys(phone_number)

        # Ждем, пока кнопка "Получить код" станет кликабельной и нажимаем на нее
        time.sleep(2)
        submit_button = wait.until(
            EC.element_to_be_clickable(

                (By.XPATH, "//button[contains(@class, 'inline-flex items-center') and contains(., 'Продолжить')]"))
        )
        submit_button.click()
        time.sleep(3)

    finally:
        driver.quit()
        return {"status_code": 200, "response": 'good'}
