import requests
from config import Proxy, Services
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def send_sms_to_beautery(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Открываем нужный URL
        url = 'https://user.beautery.ru'
        driver.get(url)

        # Явное ожидание: ждем, пока элемент для ввода номера телефона будет доступен
        wait = WebDriverWait(driver, 10)
        phone_input = wait.until(EC.presence_of_element_located((By.ID, "modal-signup-phone-login")))

        # Вводим номер телефона
        phone_number = phone_number[2::1]
        phone_input.send_keys(phone_number)

        # Ждем, пока кнопка "Войти или зарегистрироваться" станет доступной
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))

        # Нажимаем на кнопку
        login_button.click()
        time.sleep(5)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}