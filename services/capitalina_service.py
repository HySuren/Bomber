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
from selenium.webdriver.chrome.options import Options

def send_sms_to_capitalina(phone_number: str, proxy: str = Proxy.PROXY_URL):
    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Открываем нужный URL
        url = 'https://finters-zaem.ru/anketa'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        last_n = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="lastname"]')))
        first_n = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="firstname"]')))
        surname = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="middlename"]')))
        phone = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="phone"]')))
        phone.click()
        phone.send_keys(phone_number[2])
        time.sleep(0.2)
        phone.send_keys(phone_number[3])
        time.sleep(0.2)
        phone.send_keys(phone_number[4])
        time.sleep(0.2)
        phone.send_keys(phone_number[5])
        time.sleep(0.2)
        phone.send_keys(phone_number[6])
        time.sleep(0.2)
        phone.send_keys(phone_number[7])
        time.sleep(0.2)
        phone.send_keys(phone_number[8])
        time.sleep(0.2)
        phone.send_keys(phone_number[9])
        time.sleep(0.2)
        phone.send_keys(phone_number[10])
        time.sleep(0.2)
        phone.send_keys(phone_number[10])
        last_n.send_keys('Михаилович')
        surname.send_keys('Прохоров')
        first_n.send_keys('Андрей')
        checkbox1 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="accept-personal-data"]')))
        checkbox1.click()
        phone.submit()

        time.sleep(8)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}