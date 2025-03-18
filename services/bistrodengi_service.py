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
def send_sms_to_bistrodengi(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://bistrodengi.ru/get/?utm_source=bankiru&wmid=1&utm_content=c4c55596f3eb54f07f5918670f9bfe83'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        time.sleep(1)
        phone = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="online_phone"]')))
        brithday = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="online_birthdate"]')))
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="formBlock"]/div[2]/form/div/div[2]/div[1]/div/label')))
        phone.send_keys(phone_number[2::1])
        brithday.send_keys('12.04.2000')
        driver.execute_script("arguments[0].click();", checkbox)
        phone.submit()


        time.sleep(5)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}