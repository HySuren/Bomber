
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
def send_sms_to_sms_finance(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://www.smsfinance.ru/registration/1?utm_source=ydirect&utm_medium=cpc&utm_campaign=master_kampanij&yclid=2453163080323170303'
        time.sleep(1)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        f = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/app-root/div/app-first-registration-step/div/div/div/div/form/div/div[1]/app-autocomplete-fio[1]/span/p-autocomplete/span/input')))
        n = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/app-root/div/app-first-registration-step/div/div/div/div/form/div/div[1]/app-autocomplete-fio[2]/span/p-autocomplete/span/input')))
        o = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/app-root/div/app-first-registration-step/div/div/div/div/form/div/div[1]/app-autocomplete-fio[3]/span/p-autocomplete/span/input')))
        phone = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="float-input__mainPhone"]')))
        email = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/app-root/div/app-first-registration-step/div/div/div/div/form/div/div[1]/app-autocomplete-email/span/p-autocomplete/span/input')))
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="gender-checkbox MALE"]')))
        checkbox1 = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/app-root/div/app-first-registration-step/div/div/div/div/form/div/div[1]/app-checkbox/div/label')))
        phone.send_keys(phone_number[2::1])
        f.send_keys('Иванов')
        n.send_keys('Иван')
        o.send_keys('Иванович')
        email.send_keys(f'idnwiodoiw{random_chars}dwnw@mail.ru')
        driver.execute_script("arguments[0].click();", checkbox)
        driver.execute_script("arguments[0].click();", checkbox)
        driver.execute_script("arguments[0].click();", checkbox1)

        end_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-first-registration-step/div/div/div/div/form/div/div[2]/p-button/button')))
        end_btn.click()
        time.sleep(594)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}
