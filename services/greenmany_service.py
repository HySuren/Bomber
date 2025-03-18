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
def send_sms_to_vivadenqi(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://online-ui.vivadengi.ru/phone-number'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        start_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/main/a')))
        driver.execute_script("arguments[0].click();", start_btn)
        time.sleep(1)
        phone = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="phone_number"]')))
        phone.send_keys(phone_number[2::1])
        phone.submit()

        lastname = wait.until(EC.presence_of_element_located((By.XPATH,
                                                              '//*[@id="lastname"]'
                                                              )))
        lastname.send_keys('Степанов')
        firstname = wait.until(EC.presence_of_element_located((By.XPATH,
                                                               '//*[@id="firstname"]'
                                                               )))
        firstname.send_keys('Олег')
        patronymic = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="patronymic"]')))
        patronymic.send_keys('Юрьевич')
        birthday = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '//*[@id="birthday"]')))
        birthday.send_keys('12.03.2000')
        birthday.send_keys(Keys.ENTER)

        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[4]/div/div/main/div[2]/div/div/form/div/div[1]/div/div/div/div/label')))
        driver.execute_script("arguments[0].click();", checkbox)
        end_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[4]/div/div/main/div[2]/div/div/form/div/div[2]/button')))
        end_btn.click()
        time.sleep(5)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}
