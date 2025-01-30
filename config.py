import os
from dotenv import load_dotenv

load_dotenv()

services = ["6","7", "8", "9", "10", "11", "12", "13", "14",
            "16", "17", "18", "19","20", "21", "22", "23", "24",
            "25", "26", "27","28", "29", "30", "31", "32", "33",
            "34", "35", "36", "37", "38", "39", "40"]

service_names = {
    "6": "BEAUTERY",
    "7": "BANKI_RU",
    "8": "4LAPY",
    "9": "OBI",
    "10": "AKBARS",
    "11": "APTECH",
    "12": "WINELAB",
    "13": "LETAI",
    "14": "SVOI",
    "16": "AYURVEDA",
    "17": "RAIFFEISEN",
    "18": "SUPERAPTEKA",
    "19": "NFAPTEKA",
    "20": "SPACESUHI",
    "21": "CHINA",
    "22": "TTraditions",
    "23": "VIPAVENUE",
    "24": "POIZONSHOP",
    "25": "YSAM",
    "26": "CREDDY",
    "27": "KALINA-MALINA",
    "28": "NAHOSA",
    "29": "BRANDSHOP",
    "30": "SPORTPOINT",
    "31": "STREET_BEAT",
    "32": "HAPPYWEAR",
    "33": "PRIME",
    "34": "PLUSE",
    "35": "RSB_BANK",
    "36": "DRAGON",
    "37": "NINJAFOOD",
    "38": "EDA11",
    "39": "SPARC_FOOD",
    "40": "CHIBBIS"
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
    RU_COUNTRY = os.getenv('RU_COUNTRY')
    RU_CARRIER = os.getenv('RU_CARRIER')

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
    APTECH = os.getenv('APTECH')
    WINELAB = os.getenv('WINELAB')
    LETAI = os.getenv('LETAI')
    SVOI = os.getenv('SVOI')
    RAIFFEISEN = os.getenv('RAIFFEISEN')
    SUPERAPTEKA = os.getenv('SUPERAPTEKA')
    NFAPTEKA = os.getenv('NFAPTEKA')
    SPACESUHI = os.getenv('SPACESUHI')
    CHINA = os.getenv('CHINA')
    POIZONSHOP = os.getenv('POIZONSHOP')
    VIPAVENUE = os.getenv('VIPAVENUE')
    YSAM = os.getenv('YSAM')
    CREDDY = os.getenv('CREDDY')
    STREET_BEAT = os.getenv('STREET_BEAT')
    HAPPYWEAR = os.getenv('HAPPYWEAR')
    PRIME = os.getenv('PRIME')
    PLUSE = os.getenv('PLUSE')
    RSB_BANK = os.getenv('RSB_BANK')
    DRAGON = os.getenv('DRAGON')
    NINJAFOOD = os.getenv('NINJAFOOD')
    EDA11 = os.getenv('EDA11')
    SPARC_FOOD = os.getenv('SPARC_FOOD')
    CHIBBIS = os.getenv('CHIBBIS')

class Proxy:
    PROXY_URL = os.getenv("PROXY")
