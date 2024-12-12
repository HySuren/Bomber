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

        if service_name == "Thai Traditions":
            phone_number = f"+7 ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        elif service_name == "Dommalera":
            pass
        elif service_name == "Ayurveda":
            pass

        return phone_number
    except Exception as e:
        print(f"Ошибка валидации: {e}")
        raise
