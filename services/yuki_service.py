import requests
from config import Proxy, Services
from utils.email_generate import generate_random_string
import json
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

def generate_random_numbers():
    """Генерирует два случайных числа: одно начинается с 45 и имеет 4 цифры, другое — 6-значное."""

    # Первое число: начинается с 45 и имеет 4 цифры
    num1 = 45000 + random.randint(0, 999) # Добавляем 45000, чтобы гарантировать начало с 45

    # Второе число: 6-значное
    num2 = random.randint(100000, 999999) # Диапазон 6-значных чисел

    return str(num1), str(num2)

def send_sms_to_prostoyvopros(phone_number: str):
    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    random_chars = generate_random_string()
    num1, num2 = generate_random_numbers()
    try:
        # Открываем нужный URL
        url = 'https://xn--j1ab.xn--80ajiuqaln.xn--p1ai/online/claim/new?money=15000&time=30&utm_campaign=0_firstloan&utm_medium=banner&utm_source=banki_ru&transaction_id=92d920bc1b3920010402da8cd40ef6f1'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        last_n = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="input_lastname_register_claim"]')))
        first_n = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="input_firstname_register_claim"]')))
        surname = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="input_surname_register_claim"]')))
        birthday = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="birthDate"]')))
        serial_passport = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passport_serial"]/div[2]/div/div/input')))
        num_password = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passport_number"]/div[2]/div/div/input')))
        phone = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="telephone"]/div[2]/div/div/input')))
        email = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="email"]/div[2]/div/div/input')))
        email.send_keys(f'jjwodewi{random_chars}ojdwijf@mail.ru')
        phone.send_keys(phone_number[2::1])
        last_n.send_keys('Михаилович')
        surname.send_keys('Прохоров')
        first_n.send_keys('Андрей')
        serial_passport.send_keys(num1)
        num_password.send_keys(num2)
        birthday.send_keys('12.02.1980')
        checkbox1 = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='sex']/div/div[2]/label/span[1]")))
        checkbox1.click()
        checkbox2 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pd_agree"]/div/label/span')))
        checkbox2.click()
        phone.submit()

        time.sleep(8)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}