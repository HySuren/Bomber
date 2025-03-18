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
def send_sms_to_caranqa(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://cabinet.caranga.ru/registration'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        f = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="lastName"]')))
        n = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="firstName"]')))
        o = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="fatherName"]')))
        phone = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="tel"]')))
        email = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="email"]')))
        p = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="password"]')))
        rp = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="password-repeat"]')))
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/app-root/div/div/registration-view/div/div/reg-step1/form/div/div/div[3]/reg-agreement-conditions/lcg-checkbox/div/div[1]')))
        phone.send_keys(phone_number[2::1])
        f.send_keys('Иванов')
        n.send_keys('Иван')
        o.send_keys('Иванович')
        email.send_keys(f'idnwiodoiw{random_chars}dwnw@mail.ru')
        p.send_keys('CTcjdztq8cYrM')
        rp.send_keys('CTcjdztq8cYrM')
        driver.execute_script("arguments[0].click();", checkbox)
        phone.submit()


        time.sleep(5)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}
