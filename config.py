import os
from dotenv import load_dotenv

load_dotenv()


services = ["1", "2", "3"]

service_names = {
    "1": "Ayurveda",
    "2": "Thai Traditions",
    "3": "Dommalera"
}

class PhoneAgregator:
    API_TOKEN = os.getenv("API_TOKEN")
    GET_PHONE_NUMBER_URL = os.getenv("GET_PHONE_NUMBER_URL")
    CHECK_SMS_URL = os.getenv("CHECK_SMS_URL")

class Services:
    AYURVEDA_URL = os.getenv("AYURVEDA")
    TTRADITIONS_URL = os.getenv("TTRADITIONS")
    DOMMALERA_URL = os.getenv("DOMMALERA")

class Proxy:
    PROXY_URL = os.getenv("PROXY")
