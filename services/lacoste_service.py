from config import Proxy
from utils.anti_captcha import main, create_task, get_task_result
from utils.response_utils import get_cookies_and_headers
import requests

def send_sms_to_lacosta(phone_number: str):

    #cookie = get_cookies_and_headers('https://ls.net.ru/products/3107686-krossovki-fargoni/?utm_source=yandex&utm_medium=cpc&utm_campaign=114569386_%D0%95%D0%9F%D0%9A%20%2F%20%D0%9E%D0%BF%D0%BB%D0%B0%D1%82%D0%B0%20%D0%B7%D0%B0%20%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8%20%28%D0%BE%D1%82%2026.09.2024%29&utm_term=---autotargeting&utm_content=id_53201419705%7Crid_53201419705%7Ccid_114569386%7Cgid_5497056892%7Caid_1854755198770255821%7Cpos_other_1%7Csrc_search_yandex.ru%7Cdvc_desktop%7Creg_213_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&referrer=reattribution%3D1&etext=2202.1l0bEio1SZqeye_raWnQEEPbEie6IYEX7__0L__vVPjMi1k2GdkgSlaEd1qwBXbSZHpnenFndXZvY216YmRkag.61e5ce4618fbfc861975aed163a98838854b90a5&yclid=17772083705906200575')
    #print('cookie: ', cookie)
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "",
        "Cookie": 'mgo_sb_migrations=1418474375998%253D1; mgo_sb_first=typ%253Dutm%257C%252A%257Csrc%253Dyandex%257C%252A%257Cmdm%253Dcpc%257C%252A%257Ccmp%253D114569386_%2525D0%252595%2525D0%25259F%2525D0%25259A%252520%25252F%252520%2525D0%25259E%2525D0%2525BF%2525D0%2525BB%2525D0%2525B0%2525D1%252582%2525D0%2525B0%252520%2525D0%2525B7%2525D0%2525B0%252520%2525D0%2525BA%2525D0%2525BE%2525D0%2525BD%2525D0%2525B2%2525D0%2525B5%2525D1%252580%2525D1%252581%2525D0%2525B8%2525D0%2525B8%252520%2528%2525D0%2525BE%2525D1%252582%25252026.09.2024%2529%257C%252A%257Ccnt%253Did_53201419705%257Crid_53201419705%257Ccid_114569386%257Cgid_5497056892%257Caid_1854755198770255821%257Cpos_premium_2%257Csrc_search_none%257Cdvc_desktop%257Creg_213_%2525D0%25259C%2525D0%2525BE%2525D1%252581%2525D0%2525BA%2525D0%2525B2%2525D0%2525B0%257C%252A%257Ctrm%253D---autotargeting%257C%252A%257Cmango%253D%2528none%2529; mgo_uid=82xNEz94doEtFEkGmckM; tmr_lvid=92a46fd35cc72f28841c6ed1075526b3; tmr_lvidTS=1734898353951; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ym_uid=1734898357966299730; _ym_d=1734898357; utmLabels=utm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3D114569386_%25D0%2595%25D0%259F%25D0%259A%2520%252F%2520%25D0%259E%25D0%25BF%25D0%25BB%25D0%25B0%25D1%2582%25D0%25B0%2520%25D0%25B7%25D0%25B0%2520%25D0%25BA%25D0%25BE%25D0%25BD%25D0%25B2%25D0%25B5%25D1%2580%25D1%2581%25D0%25B8%25D0%25B8%2520%2528%25D0%25BE%25D1%2582%252026.09.2024%2529%26utm_term%3D---autotargeting%26utm_content%3Did_53201419705%7Crid_53201419705%7Ccid_114569386%7Cgid_5497056892%7Caid_1854755198770255821%7Cpos_other_1%7Csrc_search_yandex.ru%7Cdvc_desktop%7Creg_213_%25D0%259C%25D0%25BE%25D1%2581%25D0%25BA%25D0%25B2%25D0%25B0; _ym_isad=1; mgo_sb_current=typ%253Dutm%257C%252A%257Csrc%253Dyandex%257C%252A%257Cmdm%253Dcpc%257C%252A%257Ccmp%253D114569386_%2525D0%252595%2525D0%25259F%2525D0%25259A%252520%25252F%252520%2525D0%25259E%2525D0%2525BF%2525D0%2525BB%2525D0%2525B0%2525D1%252582%2525D0%2525B0%252520%2525D0%2525B7%2525D0%2525B0%252520%2525D0%2525BA%2525D0%2525BE%2525D0%2525BD%2525D0%2525B2%2525D0%2525B5%2525D1%252580%2525D1%252581%2525D0%2525B8%2525D0%2525B8%252520%252528%2525D0%2525BE%2525D1%252582%25252026.09.2024%252529%257C%252A%257Ccnt%253Did_53201419705%257Crid_53201419705%257Ccid_114569386%257Cgid_5497056892%257Caid_1854755198770255821%257Cpos_other_1%257Csrc_search_yandex.ru%257Cdvc_desktop%257Creg_213_%2525D0%25259C%2525D0%2525BE%2525D1%252581%2525D0%2525BA%2525D0%2525B2%2525D0%2525B0%257C%252A%257Ctrm%253D---autotargeting%257C%252A%257Cmango%253D%2528none%2529; mgo_sb_session=pgs%253D1%257C%252A%257Ccpg%253Dhttps%253A%252F%252Fls.net.ru%252Fproducts%252F3107686-krossovki-fargoni%252F%253Futm_source%253Dyandex%2526utm_medium%253Dcpc%2526utm_campaign%253D114569386_%2525D0%252595%2525D0%25259F%2525D0%25259A%252520%25252F%252520%2525D0%25259E%2525D0%2525BF%2525D0%2525BB%2525D0%2525B0%2525D1%252582%2525D0%2525B0%252520%2525D0%2525B7%2525D0%2525B0%252520%2525D0%2525BA%2525D0%2525BE%2525D0%2525BD%2525D0%2525B2%2525D0%2525B5%2525D1%252580%2525D1%252581%2525D0%2525B8%2525D0%2525B8%252520%252528%2525D0%2525BE%2525D1%252582%25252026.09.2024%252529%2526utm_term%253D---autotargeting%2526utm_content%253Did_53201419705%257Crid_53201419705%257Ccid_114569386%257Cgid_5497056892%257Caid_1854755198770255821%257Cpos_other_1%257Csrc_search_yandex.ru%257Cdvc_desktop%257Creg_213_%2525D0%25259C%2525D0%2525BE%2525D1%252581%2525D0%2525BA%2525D0%2525B2%2525D0%2525B0%2526referrer%253Dreattribution%25253D1%2526etext%253D2202.1l0bEio1SZqeye_raWnQEEPbEie6IYEX7__0L__vVPjMi1k2GdkgSlaEd1qwBXbSZHpnenFndXZvY216YmRkag.61e5ce4618fbfc861975aed163a98838854b90a5%2526yclid%253D17772083705906200575; mgo_cnt=2; mgo_sid=77o4spa0bw11002p481o; _ym_visorc=b; mindboxDeviceUUID=1c1829c6-d889-4258-81e3-add9ae321938; directCrm-session=%7B%22deviceGuid%22%3A%221c1829c6-d889-4258-81e3-add9ae321938%22%7D',
        "content-type": "application/json",
        "origin": "https://ls.net.ru",
        "priority": "u=1, i",
        "referer": "https://ls.net.ru/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-platform": "web",
        "x-support-webp": "1"
    }

    session = requests.session()
    response = session.get('https://ls.net.ru/')

    data = {
    "phone_number": "79847079831"
    }

    response = session.post('https://api2.ls.net.ru/apix/v2/auth/register', json=data, headers=headers)
    print(response)
    print(response.text)
