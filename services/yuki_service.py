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
from selenium.webdriver import ActionChains


def send_sms_to_prostoyvopros(phone_number: str):
    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://prostoyvopros.ru/vzyat-v-dolg'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        surname = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите фамилию']")))
        name = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите имя']")))
        last_name = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите отчество']")))
        city = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder=' ']")))
        phone = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='+7 (912) 345 67-89']")))
        email = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите Email']")))
        checkhost = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div/div[2]/div[2]/div/div/div[4]/div[1]/label/input")))
        surname.send_keys('Сизоненко')
        btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step1-btn-next']")))
        name.send_keys('Андрей')
        last_name.send_keys('Викторович')
        city.send_keys('г Москва')
        city.click()
        time.sleep(5)
        phone.send_keys(phone_number[2::1])
        email.send_keys('eiugfaohievsru@mail.ru')
        checkhost.click()
        time.sleep(2)
        # Ждем, пока кнопка "Войти или зарегистрироваться" станет доступной
        btn.click()
        time.sleep(10)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}
