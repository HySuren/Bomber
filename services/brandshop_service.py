import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def send_sms_to_brandshop(phone_number: str):

    # Инициализируем драйвер
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Открываем окно в полном экране
        driver.maximize_window()

        # Открываем нужный URL
        url = 'https://brandshop.ru/new/obuv/krossovki/'
        driver.get(url)

        # Ждем 1 секунду после загрузки страницы
        time.sleep(5)

        # Явное ожидание: ждем, пока кнопка "Войти" станет кликабельной и кликаем по ней
        wait = WebDriverWait(driver, 9)

        profile_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='profile' and contains(@class, 'profile-header__icon')]"))
        )

        # Нажимаем на кнопку
        profile_button.click()
        time.sleep(2)
        input_field = wait.until(
            EC.visibility_of_element_located((By.ID, "login__input-tel"))
        )

        phone_number = phone_number[2::1]
        input_field.send_keys(phone_number)

        # Ждем, пока кнопка "Получить код" станет кликабельной и нажимаем на нее
        time.sleep(1)
        button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "login__btn"))
        )

        button.click()
        time.sleep(5)

    finally:
        driver.quit()
        return {"status_code": 200, "response": 'good'}
