from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_cookies_and_headers(url, mode='default'):
    # Настройка опций для headless режима
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Открываем указанный URL
        driver.get(url)

        # Получаем куки
        cookies = driver.get_cookies()

        # Преобразуем куки в строку формата key=value
        cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        driver.quit()
        if mode == 'default':
            return cookie_string
        elif mode == 'sessid':
            return driver.session_id
    finally:
        pass
