import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def send_sms_to_sportpoint(phone_number: str):
    # Инициализируем драйвер
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        driver.maximize_window()

        # Открываем нужный URL
        url = 'https://sportpoint.ru/?showAuth&authRedirect=/favorites/'
        driver.get(url)

        # Ждем 1 секунду после загрузки страницы
        time.sleep(2)

        # Явное ожидание: ждем, пока кнопка "Войти" станет кликабельной и кликаем по ней
        wait = WebDriverWait(driver, 9)

        time.sleep(2)
        phone_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Телефон']"))
        )
        if phone_field.is_displayed():
            phone_field.send_keys(phone_number)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='sp-button' and text()='Получить код']"))
            )
            button.click()

            lastname_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Фамилия']"))
            )

            lastname_field.send_keys("Ермаков")

            name_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Имя']"))
            )
            name_field.send_keys("Виталий")

            email_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='E-mail']"))
            )
            email_field.send_keys("dbawyudbiuaid@mail.ru")

            date_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Дата рождения']"))
            )
            date_field.send_keys('12.05.2000')

            button = WebDriverWait(driver, 9).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='sp-button' and text()='Зарегестрироваться']"))
                # Точное совпадение текста
            )
            button.click()

        time.sleep(2)

    finally:
        driver.quit()
        return {"status_code": 200, "response": 'good'}
