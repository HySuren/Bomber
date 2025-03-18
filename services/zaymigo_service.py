import requests
from config import Proxy, Services
from utils.email_generate import generate_random_string
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def send_sms_to_zaymigo(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://borrow.zaymigo.ru/'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        surname = wait.until(EC.presence_of_element_located((By.NAME, "surname")))
        name = wait.until(EC.presence_of_element_located((By.NAME, "name")))
        patronymic = wait.until(EC.presence_of_element_located((By.NAME, "patronymic")))
        phone = wait.until(EC.presence_of_element_located((By.NAME, "phone")))
        email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        cheakbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "links__item")))
        # Вводим данные
        surname.send_keys('Иванов')
        name.send_keys('Иван')
        patronymic.send_keys('Сергеевич')
        phone.send_keys(phone_number[2::1])
        email.send_keys(f'testebde{random_chars}dbwidb@mail.ru')
        cheakbox.click()
        time.sleep(5)
        # Ждем, пока кнопка "Войти или зарегистрироваться" станет доступной
        login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "loan-step__action")))

        # Нажимаем на кнопку
        login_button.click()
        time.sleep(5)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}
