import os
from dotenv import load_dotenv

load_dotenv()


services = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "`10"]

service_names = {
    "1": "Dommalera",
    "2": "4LAPY",
    "3": "BEAUTERY",
    "4": "BANKI_RU",
    "5": "KALINA_MALINA",
    "6": "TTraditions",
    "7": "AYURVEDA",
    "8": "BYKDABARAN",
    "9": "OBI",
    "10": "AKBARS"
}


class Databases:
    DBNAME = os.getenv("DBNAME")
    DBUSER = os.getenv("DBUSER")
    DBPASSWORD = os.getenv("DBPASSWORD")
    DBHOST = os.getenv("DBHOST")
    DBPORT = os.getenv("DBPORT")


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
    KALINA_MALINA = os.getenv("KALINA_MALINA")
    BYKDABARAN = os.getenv("BYKDABARAN")
    AKBARS = os.getenv('AKBARS')

class Proxy:
    PROXY_URL = os.getenv("PROXY")
