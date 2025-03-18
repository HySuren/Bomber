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
from selenium.webdriver.common.keys import Keys  # импорт Keys


def send_sms_to_prostoy_vopros(phone_number: str):
    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://prostoyvopros.ru/vzyat-v-dolg'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        time.sleep(1)
        f = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="__nuxt"]/div/div[2]/div[2]/div/div/div[3]/label[1]/input')))
        n = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/label[2]/input')))
        o = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/label[3]/input')))
        city = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/label[4]/input')))
        phone = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="__nuxt"]/div/div[2]/div[2]/div/div/div[3]/label[5]/input')))
        email = wait.until(EC.presence_of_element_located((By.XPATH,
                                                              '/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/label[6]/input')))
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH,
                                                              '/html/body/div[1]/div/div[2]/div[2]/div/div/div[4]/div[1]/label')))
        f.send_keys('Иванов')
        n.send_keys('Иван')
        o.send_keys('Иванович')
        phone.send_keys(phone_number[2::1])
        driver.execute_script("arguments[0].click();", checkbox)
        email.send_keys(f'idnwiodoiw{random_chars}dwnw@mail.ru')
        city.send_keys('г Москв')
        time.sleep(1)
        city.send_keys(Keys.TAB)

        end_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div[4]/div[2]/button')))
        end_btn.click()
        time.sleep(50)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}
