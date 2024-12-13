import os
from dotenv import load_dotenv

load_dotenv()


services = ["1", "2", "3", "4", "5", "6", "7", "8"]

service_names = {
    "1": "Ayurveda",
    "2": "Thai Traditions",
    "3": "Dommalera",
    "4": "OBI",
    "5": "4LAPY",
    "6": "BEAUTERY",
    "7": "BANKI_RU",
    "8": "GAZPROMBONUS"
}

class PhoneAgregator:
    API_TOKEN = os.getenv("API_TOKEN")
    GET_PHONE_NUMBER_URL = os.getenv("GET_PHONE_NUMBER_URL")
    CHECK_SMS_URL = os.getenv("CHECK_SMS_URL")

class Services:
    AYURVEDA_URL = os.getenv("AYURVEDA")
    TTRADITIONS_URL = os.getenv("TTRADITIONS")
    DOMMALERA_URL = os.getenv("DOMMALERA")
    OBI = os.getenv("OBI")
    FOUR_LAPY = os.getenv("4LAPY")
    BEAUTERY = os.getenv("BEAUTERY")
    BANKI_RU = os.getenv("BANKI_RU")
    GAZPROMBONUS = os.getenv("GAZPROMBONUS")

class Proxy:
    PROXY_URL = os.getenv("PROXY")
