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

def send_sms_to_turbozaim(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://lk.turbozaim.ru/registration'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        surname = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Фамилия' and @class='labeled-input']")))
        name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Имя' and @class='labeled-input']")))
        patronymic = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Отчество' and @class='labeled-input']")))
        date = wait.until(EC.presence_of_element_located((By.NAME, "birthDate")))
        phone = wait.until(EC.presence_of_element_located((By.NAME, "phone")))
        email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Example@gmail.com' and @class='labeled-input']")))
        cheakbox = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Соглашению об использовании аналога')]")))
        # Вводим данные
        surname.send_keys('Иванов')
        name.send_keys('Иван')
        patronymic.send_keys('Сергеевич')
        date.send_keys('15.02.2001')
        phone.send_keys(phone_number[2::1])
        email.send_keys(f'testebde{random_chars}dbwidb@mail.ru')
        cheakbox.click()
        time.sleep(5)
        # Ждем, пока кнопка "Войти или зарегистрироваться" станет доступной
        login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_primary")))

        # Нажимаем на кнопку
        login_button.click()
        time.sleep(6)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}