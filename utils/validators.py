def validate_and_format_number(phone_number: str, service_name: str = None) -> str:
    """
    Проверяет и форматирует номер телефона в зависимости от сервиса.
    Ожидаемый формат входящего номера: начинается с +7, 8, или 7.
    Формат возвращаемого номера зависит от переданного сервиса.
    """
    print(f"Проверяем номер телефона: {phone_number} для сервиса {service_name}")

    try:
        if not phone_number.startswith("+7") and not phone_number.startswith("8") and not phone_number.startswith("7"):
            raise ValueError("Invalid phone number format. Must start with +7, 8, or 7.")

        if phone_number.startswith("8"):
            phone_number = "+7" + phone_number[1:]
        elif phone_number.startswith("7") and not phone_number.startswith("+7"):
            phone_number = "+7" + phone_number[1:]

        if len(phone_number) != 12 or not phone_number[2:].isdigit():
            raise ValueError("Invalid phone number length or non-digit characters found.")

        if service_name == "TTraditions":
            phone_number = f"+7 ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        elif service_name == "Dommalera":
            pass
        elif service_name == "Ayurveda":
            pass
        elif service_name == "OBI":
            pass
        elif service_name == "4LAPY":
            pass
        elif service_name == "BEAUTERY":
            pass
        elif service_name == "BANKI_RU":
            pass
        elif service_name == "GAZPROMBONUS":
            pass
        elif service_name == "KALINA-MALINA":
            pass
        elif service_name == "BYKDABARAN":
            pass
        elif service_name == "AKBARS":
            pass
        elif service_name == "WINELAB":
            pass
        elif service_name == "LETAI":
            phone_number = phone_number[2::1]
        elif service_name == "SVOI":
            pass
        elif service_name == "RAIFFEISEN":
            phone_number = phone_number[1::1]
        elif service_name == "SUPERAPTEKA":
            phone_number = phone_number[1::1]
        elif service_name == "NFAPTEKA":
            phone_number = f"+7 ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        elif service_name == "SPACESUHI":
            pass
        elif service_name == "CHINA":
            phone_number = f"+7 {phone_number[2:5]} {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        elif service_name == "VIPAVENUE":
            phone_number = phone_number[1::1]
        elif service_name == "POIZONSHOP":
            pass
        elif service_name == "CREDDY":
            pass
        elif service_name == "NAHOSA":
            phone_number = phone_number[2::1]
        elif service_name == "BRANDSHOP":
            pass
        elif service_name == "SPORTPOINT":
            phone_number = phone_number[2::1]
        elif service_name == "STREET_BEAT":
            pass
        elif service_name == "HAPPYWEAR":
            pass
        elif service_name == 'PRIME':
            pass
        elif service_name == 'PLUS':
            pass
        elif service_name == "RSB_BANK":
            pass
        elif service_name == "DRAGON":
            pass
        elif service_name == 'NINJAFOOD':
            pass
        elif service_name == 'EDA11':
            pass
        elif service_name == 'CHIBBIS':
            pass
        elif service_name == 'NADODENEG':
            pass
        elif service_name == 'ECO_VPISKA':
            phone_number = f"+7 {phone_number[2:5]} {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        elif service_name == 'PM_RU':
            phone_number = f"+7 ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        elif service_name == "LOCALCITHCEN":
            pass
        elif service_name == "TRENDREALITY":
            pass
        elif service_name == "WEBBANKIR":
            pass
        elif service_name == "SROCHNODENGI":
            pass
        elif service_name == "MIKROZAIM":
            pass
        elif service_name == "VEGANEDA":
            pass
        elif service_name == "DOSTUPNODENGI":
            pass
        elif service_name == "FASTMANY":
            pass
        elif service_name == "SANIAN":
            pass
        elif service_name == "BARBARROSA":
            phone_number = phone_number[2::1]
        elif service_name == "UTIMADENGI":
            pass
        elif service_name == "SUPERCASH":
            phone_number = phone_number[1::1]
        elif service_name == "FASTZAIM":
            pass
        elif service_name == "VANILINA":
            pass
        elif service_name == "SUPERPRAIM":
            pass
        elif service_name == "ZAYMIGO":
            pass
        elif service_name == "PAPAMANY":
            pass
        elif service_name == "SNEKCASH":
            pass
        elif service_name == "TURBOZAIM":
            pass
        elif service_name == "IXO":
            pass
        elif service_name == "FUNCASHFAST":
            pass
        elif service_name == "PROSTOYVOPROS":
            pass
        elif service_name == "YUKI":
            pass
        elif service_name == "KERESI":
            pass
        elif service_name == "BOOSTRA":
            pass
        elif service_name == "LOSTRA":
            pass
        elif service_name == "EXSTRA":
            pass
        elif service_name == "LAIMMANI":
            pass
        elif service_name == "MONEZZACASE":
            pass
        elif service_name == "GEBUS":
            pass
        elif service_name == "REDMANY":
            pass
        elif service_name == "A.DENGI":
            pass
        elif service_name == "POCETMANY":
            pass
        elif service_name == "MOJENY":
            pass
        return phone_number
    except Exception as e:
        print(f"Ошибка валидации: {e}")
        raise
