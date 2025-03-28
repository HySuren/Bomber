import os
from dotenv import load_dotenv

load_dotenv()

services = ["6", "7", "8", "9", "10", "11", "12", "13", "14",
            "16", "17", "18", "19", "20", "21", "22", "23", "24",
            "25", "26", "27", "28", "29", "30", "31", "32", "33",
            "34", "35", "36", "37", "38", "39", "40", "42", "43",
            "44", "45", "46", "47", "48","59", "60", "61",  "62",
            "63", "64", "65", "66", "67", "68", "69", "70", "71",
            "72", "73", "74", "75", "76", "77", "78", "79",
            "80", "81", "82", "83", "84", "85", "86", "87",
            "88","89","90","91","92","93","94","95","96","97",
            "98", "99", "100", "101", "102", "103", "104", "105", "106"]

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
    "40": "CHIBBIS",
    "42": "NADODENEG",
    "43": "ECO_VPISKA",
    "44": "PM_RU",
    "45": "LOCALCITHCEN",
    "46": 'TRENDREALITY',
    "47": 'WEBBANKIR',
    "48": 'SROCHNODENGI',
    "49": 'MIKROZAIM',
    "50": 'VEGANEDA',
    "51": 'DOSTUPNODENGI',
    "52": 'FASTMANY',
    "53": 'SANIAN',
    "54": 'BARBARROSA',
    "55": 'UTIMADENGI',
    "56": 'SUPERCASH',
    "57": 'FASTZAIM',
    "58": 'VANILINA',
    "59": 'SUPERPRAIM',
    "60": 'ZAYMIGO',
    "61": 'PAPAMANY',
    "62": 'SNEKCASH',
    "63": 'TURBOZAIM',
    "64": 'IXO',
    "65": 'FUNCASHFAST',
    "66": 'PROSTOYVOPROS',
    "67": 'YUKI',
    "68": 'KERESI',
    "69": 'BOOSTRA',
    "70": 'LOSTRA',
    "71": 'EXSTRA',
    "72": 'LAIMMANI',
    "73": 'MONEZZACASE',
    "74": 'GEBUS',
    "75": 'REDMANY',
    "76": 'A.DENGI',
    "77": 'POCETMANY',
    "78": 'MOJENY',
    "79": 'CAPITALINA',
    "80": 'SIKORSKY',
    "81": 'APPMANY',
    "82": 'CRESARRY',
    "83": 'FARMNET',
    "84": 'SUPERDROP',
    "85": 'FASTCASE',
    "86": 'SUPERINETNET',
    "87": 'LAKYMANY',
    "88": 'IZIMANY',
    "89": 'MEGASCORE',
    "90": 'DUBLEDUCK',
    "91": 'EZFACTMANY',
    "92": 'SNAKECASH',
    "93": 'EDAUDOMA',
    "94": 'KUHNAGRUZII',
    "95": 'CAFE11',
    "96": 'MEETCOFFI',
    "97": 'UGORINICHA',
    "98": 'MIRVKUSOV',
    "99": 'DENGINADOM',
    "100": 'sms_finance',
    "101": 'prostoi_vopros',
    "102": 'mig_credit',
    "103": 'greenmany',
    "104": 'centro_finance',
    "105": 'cash_drive',
    "106": 'bistrodengi'
}


class Databases:
    DBNAME = os.getenv("DBNAME")
    DBUSER = os.getenv("DBUSER")
    DBPASSWORD = os.getenv("DBPASSWORD")
    DBHOST = os.getenv("DBHOST")
    DBPORT = os.getenv("DBPORT")


DB_CONFIG = {
    "dbname": Databases.DBNAME,
    "user": Databases.DBUSER,
    "password": Databases.DBPASSWORD,
    "host": Databases.DBHOST,
    "port": Databases.DBPORT
}


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
    MYBOX = os.getenv('MYBOX')
    ECO_VPISKA = os.getenv('ECO_VPISKA')
    PM_RU = os.getenv('PM_RU')
    LOCALCITHCEN = os.getenv('LOCALKITCHEN')
    TRENDREALITY = os.getenv('TRENDREALITY')
    WEBBANKIR = os.getenv('WEBBANKIR')
    SROCHNODENGI = os.getenv('SROCHNODENGI')

class Proxy:
    PROXY_URL = os.getenv("PROXY")
