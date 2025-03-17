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

def send_sms_to_dengi_na_dom(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://denginadom.ru/?from2=bankiru&utm_source=affiliate&utm_medium=bankiru&utm_content=1&utm_campaign=cpa&wm_id=1&utm_term=75e2c89d4d4d99fffb1883a64ec1598d&offer=1&need_postback=1&goal_id=1&click_id=75e2c89d4d4d99fffb1883a64ec1598d'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        second_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[1]/section/div[3]/div[2]/div[2]/div/div[2]/button')))
        second_btn.click()
        time.sleep(5)
        fio = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="myCanvas"]')))
        email = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[1]/section/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[4]/div/div/input')))
        city = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[1]/section/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[3]/div/div/div/input')))
        phone = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[1]/section/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/input')))
        cheakbox = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[1]/section/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[5]/div/label')))
        # Вводим данные
        fio.send_keys('Иванов Иванов Иванов')
        email.send_keys(f'idnwiodoiw{random_chars}dwnw@mail.ru')
        phone.send_keys(phone_number[2::1])

        driver.execute_script("arguments[0].click();", cheakbox)
        time.sleep(1)
        city.send_keys('Москва')
        time.sleep(2)
        reg_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/main/div/div[1]/section/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[7]/button')))
        reg_btn.click()
        time.sleep(6)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}
