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
from selenium.webdriver.common.keys import Keys # импорт Keys
def send_sms_to_adengi(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://adengi.ru/registration/personal?amount=15000&type=smart_limit'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        f = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="last-name"]')))
        n = wait.until(EC.presence_of_element_located((By.XPATH,
                                                       '//*[@id="first-name"]')))
        o = wait.until(EC.presence_of_element_located((By.XPATH,
                                                       '//*[@id="middle-name"]')))
        email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
        f.send_keys('Иванов')
        f.submit()
        n.send_keys('Саша')
        n.submit()
        o.send_keys('Сергеевич')
        o.submit()
        email.send_keys(f'idnwiodoiw{random_chars}dwnw@mail.ru')
        phone = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="phone"]')))
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagePersonalRoot"]/div/div/div[2]/form/div/div[3]/div/div/input')))
        phone.send_keys(phone_number[2::1])
        driver.execute_script("arguments[0].click();", checkbox)

        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagePersonalRoot"]/div/div/div[2]/form/div/div[2]/div[1]/button')))
        send_btn.click()
        n.send_keys(Keys.ENTER)

        n.send_keys(Keys.ENTER)
        email.send_keys(Keys.ENTER)
        time.sleep(50)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}