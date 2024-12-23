import requests
from config import Proxy, Services
import json
from capmonster_python import RecaptchaV2Task

def send_sms_to_begemot(phone_number: str):

    url = Services.BEGEMOT
    headers = {
  "accept": "*/*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
  "content-length": "62",
  "content-type": "application/vnd.api+json",
  "cookie": "ab-test-user-id=486b5ea3ced0869588d86b0620af24bf; fuser_id=4dfa15118abc8f1eace3ab46ff14481f596e87b87551fc7f8dcf3ae1d0c73547a%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22fuser_id%22%3Bi%3A1%3Bs%3A32%3A%228b443e760c554219ebd723eae142749a%22%3B%7D; guid_city=0c5b2444-70a0-4932-980c-b4dc0d3f02b5; name_city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; guid_region=0c5b2444-70a0-4932-980c-b4dc0d3f02b5; guid_country=8aa15da9-92a4-4530-ab74-1992c973c539; region_timezone=UTC%2B3%3A00; _userGUID=0:m4eo6n0k:CcTuWKpnrlUYV7WZlnFCgcuZ7hanpjzQ; _userGUID=0:m4eo6n0k:CcTuWKpnrlUYV7WZlnFCgcuZ7hanpjzQ; digi_uc=|; _gcl_au=1.1.1454214024.1733605897; _ga=GA1.1.708661259.1733605897; tmr_lvid=442833925b69c9368fa6cc217c755c53; tmr_lvidTS=1733605896800; flocktory-uuid=75aae902-454a-4044-bf0a-c3451bf7a220-8; _ym_uid=1733605897445463143; _ym_d=1733605897; syte_uuid=d866b0d0-b4df-11ef-8f05-11cad59f26b7; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; uxs_uid=d9cd1ea0-b4df-11ef-a498-d14599b191f3; qrator_jsr=v2.0.1734643441.305.2ebc784a20qwIe9i|0j9D6Y6v2CvEwllP|+msgSj/qOSjPabCLIzdlvCIimBSazpYalg01aWWVa2CUKPakjT+0PEvdayNtfzOvt5eB5qh+hwwNCq4aIsfOvQ==-5sceFn3i58Z0ceFXWHfrvHc+2fE=-00; SL_G_WPT_TO=ru; qrator_jsid2=v2.0.1734643441.305.2ebc784a20qwIe9i|AWzgsQEza9KZ7NC2|pgIXwaqkiU5egc121u+jDMdP5Wr4CPtm+EBbd/5vzMUa+/W40DlPl0Q49nS6Zyot2edRrTNLkmjYgEJlwl4GCr7Pv4YWfiqWYjlJkpLk95EKVfKNMq7zog/fr8OA0QvdWmeNmEj/iHcrveR9zdFltw==-H1KWs8/2rvoa+HVhHhC/x+vTumM=; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; PHPSESSID=5jvcdjhah9mj8pp0bvivckqcle; _csrf=1476875ce8a2207df0f5616a8d170482246d60f91bb7db2684adb8d67ee53885a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22dnAoOKcU0rPhwcwum-WvbcNEKnf6jg1T%22%3B%7D; dSesn=ed8bcf8f-279e-f2a2-cad1-094240355dae; _dvs=0:m4vtwqr2:Tf6vndEZ1mWk3_f6DpbR_aNGZDqVaLk2; iso_cookie=RU; UX_utm_medium=undefined; UX_utm_source=undefined; stimgs={%22sessionId%22:38440014%2C%22didReportCameraImpression%22:false%2C%22newUser%22:false}; _ym_isad=1; _ym_visorc=b; domain_sid=xPt7aDYlc46an9vTX5jm7%3A1734643438465; _qz_sess=f9d8d347-54d6-41ac-98ff-141827bd1b9a; tmr_detect=0%7C1734643440662; mindboxDeviceUUID=1c1829c6-d889-4258-81e3-add9ae321938; directCrm-session=%7B%22deviceGuid%22%3A%221c1829c6-d889-4258-81e3-add9ae321938%22%7D; _ga_MZNG6JMV9K=GS1.1.1734643437.3.0.1734643446.51.0.0; coupon=22112024-50,12092024-40,2CHJXIXI,12092024-30,2CUFEIX4,2C4VUZF6,12092024-20,12092024-10,2CPW5AUR",
  "origin": "https://sokolov.ru",
  "priority": "u=1, i",
  "referer": "https://sokolov.ru/",
  "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
  "x-city-uuid": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
  "x-country-code": "RU",
  "x-country-uuid": "8aa15da9-92a4-4530-ab74-1992c973c539",
  "x-promocodes": "22112024-50,12092024-40,2CHJXIXI,12092024-30,2CUFEIX4,2C4VUZF6,12092024-20,12092024-10,2CPW5AUR",
  "x-region-uuid": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
  "x-site": "sokolov.ru",
  "x-source": "site"
}

    #print(1)
    #capmonster = RecaptchaV2Task("2b34ab1ed18543953dd6c4751bebd58e")
    #print(2)
    #task_id = capmonster.create_task("https://tashirpizza.ru/", "6LeiJSgTAAAAADhuLNywY--H2_D0f8XSY_Oql-B2")
    #print(3)
    #result = capmonster.join_task_result(task_id)
    #print(4)
    #capcha = result.get("gRecaptchaResponse")
    #print(capcha)
    payload = {
    "data": {
        "type": "login",
        "attributes": {
            "phone": "79309233611"
        }
    }
}

    r = requests.post('https://sokolov.ru/api/v4/profile/user/send-code/', data=payload)
    print(r)
    print(r.text)
