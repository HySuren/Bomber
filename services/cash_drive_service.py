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
def send_sms_to_cash_drive(phone_number: str):

    # Установка драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(executable_path='C:\\Users\\Danya\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'))
    random_chars = generate_random_string()
    try:
        # Открываем нужный URL
        url = 'https://cashdrive.ru/'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        start_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/section[1]/div/div[1]/div[4]/a')))
        start_btn.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        reg_step_1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout"]/div[3]/div/div[1]/button')))
        reg_step_1.click()

        time.sleep(2)
        phone = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/html/body/div[1]/div/main/form/div[2]/div[2]/div/div[1]/div/input')))
        phone.send_keys(phone_number[2::1])
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="agreePersonal"]/label')))
        end_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/form/div[3]/div/div/button[2]')))
        driver.execute_script("arguments[0].click();", end_btn)
        time.sleep(5)
    except Exception as error:
        print(type(error), error)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'гуд'}