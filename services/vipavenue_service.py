import requests
from config import Proxy, Services
from utils.anti_captcha import main, create_task, get_task_result
import random
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def send_sms_to_vipavenue(phone_number: str):
    # Инициализируем драйвер
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Открываем окно в полном экране
        driver.maximize_window()

        # Открываем нужный URL
        url = 'https://vipavenue.ru/'
        driver.get(url)

        # Ждем 1 секунду после загрузки страницы
        time.sleep(11)
        # Явное ожидание: ждем, пока кнопка "Войти" станет кликабельной и кликаем по ней
        wait = WebDriverWait(driver, 5)


        user_icon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'header__icons-user')]"))
        )
        time.sleep(1)
        user_icon.click()
        time.sleep(1.2)
        input_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='+7 ___ _______']"))
        )

        phone_number = phone_number[1::1]
        with open('tests.log', 'a') as file:
            file.write(phone_number)
        # Вставляем текст в поле ввода
        input_field.send_keys(phone_number)  # Замените на нужный вам текст

        # Ждем, пока кнопка "Получить код" станет кликабельной и нажимаем на нее
        time.sleep(2)
        submit_button = wait.until(
            EC.element_to_be_clickable(

                (By.XPATH, "//button[contains(@class, 'modal__login-btn') and contains(., 'Получить код в SMS')]"))
        )
        submit_button.click()
        time.sleep(3)
    except Exception as e:
        return {"status_code": 400, "response": f"{e}"}
    finally:
        driver.quit()
        return {"status_code": 200, "response": 'good'}
