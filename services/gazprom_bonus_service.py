import requests
from config import Proxy, Services

def send_sms_to_gazprombonus(phone_number: str):
    try:
        url = Services.GAZPROMBONUS

        payload = {
            "phone_number": phone_number[1::1],
            "group_id": "USER_GROUP_CUSTOMER",
            "referrer_id": None,
            "type": "USER_AUTH_TYPE_PHONE_NUMBER"
        }


        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Cookie": "tmr_lvid=80595b63ea5274bb500fcae1e622126d; tmr_lvidTS=1734078479527; _ym_uid=1734078480561837476; _ym_d=1734078480; _ym_isad=1; _ym_visorc=b; SL_G_WPT_TO=ru; qrator_jsid2=v2.0.1734078493.743.4d4abbb2gGMlVHdO|aDHQ9OTkCYemFPbQ|iZyffd9BoDaLTcqEFv09pKI/BOewiXNEBLxgsswDPCQpYzxGxp91UgTiSUA+Tw+CwOwqtTasUxjgYL6GJKzJYnU7Z76tdS4vPHCd+g06ItvUBtb2EZG01E6tB2dzL4Ysj3voP861ezcMi8cSth6Edg==-HNF+1AiLstRlDp1zrAsSSs+b6hs=; flocktory-uuid=07c63c72-3997-48eb-96db-e7a2d1cda91e-1; domain_sid=f2t48aNJ5H7cLmcYYEypE%3A1734078482189; uxs_uid=2b1068d0-b92c-11ef-b57e-73faa8f8b70c; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; tmr_detect=0%7C1734078484479",
            "x-app-name": "Site",
            "x-app-version": "1.63.48",
            "x-client-os": "Windows",
            "x-client-os-version": "10",
            "x-correlation-id": "581761c7-122f-40c0-91a3-0382376d6717",
            "x-domain": "https://gazprombonus.ru",
            "x-fingerprint": "14cfc8fbf6d5c7a4e9f90a72786a89b7",
            "x-instance-id": "4c40458a-aa69-4a70-b173-8ce2f72669b8",
            "x-kl-kfa-ajax-request": "Ajax_Request",
            "x-project-id": "PROJECT_ID_OGON",
            "x-support-sdk": "false",
            "x-uuid": "5536fd6a-7e2a-45d7-9a0d-5a89902edac1",
            "x-ym-id": "1734078480561837476",
            "referer": "https://gazprombonus.ru/purchase",
            "origin": "https://gazprombonus.ru",
        }

        proxies = {
            "http": Proxy.PROXY_URL,
            "https": Proxy.PROXY_URL
        }

        response = requests.post(url, data=payload, proxies=proxies, headers=headers)

        return {"status_code": response.status_code, "response": response}
    except Exception as e:
        print(e)