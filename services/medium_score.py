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

def send_sms_to_medium(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://mscore.ru/registration'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        surname = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="site_registration"]/div/div[3]/div[1]/label/span[1]/span/input')))
        name = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="site_registration"]/div/div[3]/div[2]/label/span[1]/span/input')))
        patronymic = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="site_registration"]/div/div[3]/div[3]/label/span[1]/span/input')))
        email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="site_registration"]/div/div[7]/label/span[1]/span/input')))
        phone = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="site_registration"]/div/div[10]/label/span[1]/span/input')))
        cheakbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="site_registration"]/div/div[4]/label[1]')))
        cheakbox1 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="site_registration"]/div/div[11]/label/div[1]')))
        # Вводим данные
        surname.send_keys('Иванов')
        name.send_keys('Иван')
        patronymic.send_keys('Сергеевич')
        email.send_keys(f'idnwiodoiw{random_chars}dwnw@mail.ru')
        phone.send_keys(phone_number[2::1])
        driver.execute_script("arguments[0].click();", cheakbox)
        driver.execute_script("arguments[0].click();", cheakbox1)
        time.sleep(2)
        phone.submit()
        time.sleep(6)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}