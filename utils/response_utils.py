from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_cookies_and_headers(url):
    # Настройка опций для headless режима
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

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
        return cookie_string
    finally:
        pass
