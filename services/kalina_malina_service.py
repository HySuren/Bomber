import requests
from config import Proxy, Services
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



def send_sms_to_kalina_malina(phone_number: str):
    try:
        # Инициализируем драйвер
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # Открываем окно в полном экране
        driver.maximize_window()

        # Открываем нужный URL
        url = 'https://kalina-malina.ru/'
        driver.get(url)

        time.sleep(3.5)

        wait = WebDriverWait(driver, 10)
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'flex') and contains(., 'Войти')]"))
        )
        time.sleep(0.5)
        login_button.click()
        time.sleep(3)

        phone_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='tel' and @placeholder='+7']"))
        )

        phone_number = phone_number[2::1]
        phone_input.send_keys(phone_number)

        time.sleep(2)
        submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'bg-red') and contains(., 'Получить код')]"))
        )
        submit_button.click()
        time.sleep(1.5)
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'good'}
