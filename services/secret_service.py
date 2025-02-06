from config import Proxy, Services
import requests
import uuid


def generate_headers():
    return {
        "platform": "android",
        "app-version": "10.37.3",
        "accept": "application/json",
        "accept-charset": "UTF-8",
        "user-agent": "Ktor client",
        "content-type": "application/json",
        "content-length": str(456),  # Длина контента можно оставить статической, если она известна заранее
        "accept-encoding": "gzip"
    }


def send_sms_to_localkitchen(phone_number: str):
    url = Services.LOCALCITHCEN

    headers = generate_headers()
    data = {
        "phone": phone_number[2::1],
        "ad_access": True,
        "personal_data_access": True,
        "vendor_id": str(uuid.uuid4()),  # Генерация нового vendor_id
        "platform": "android",
        "keychain_token": "4f28574cea2556ea",
        "osname": "Android 9",
        "appv": "10.37.3",
        "delivery_guy": False,
        "dev": False,
        "devn": "SM-S9210",
        "mcc": "250",
        "app": "com.fastrunkitchen",
        "process": "com.fastrunkitchen",
        "app_dir": "/data/user/0/com.fastrunkitchen/files",
        "emulator": False,
        "devm": "samsung",
        "sign": "UmWKY1GEt+00yn6h8hXDE97dtao="
    }

    proxies = {
        "http": Proxy.PROXY_URL,
        "https": Proxy.PROXY_URL
    }

    response = requests.post(url, headers=headers, json=data, proxies=proxies)

    return {"status_code": response.status_code, "response": response.text}
