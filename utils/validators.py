def validate_and_format_number(phone_number: str, service_name: str = None) -> str:
    """
    Проверяет и форматирует номер телефона в зависимости от сервиса.
    Ожидаемый формат входящего номера: начинается с +7, 8, или 7.
    Формат возвращаемого номера зависит от переданного сервиса.
    """
    print(f"Проверяем номер телефона: {phone_number} для сервиса {service_name}")

    try:
        # Убедимся, что номер начинается с +7, 8, или 7
        if not phone_number.startswith("+7") and not phone_number.startswith("8") and not phone_number.startswith("7"):
            raise ValueError("Invalid phone number format. Must start with +7, 8, or 7.")

        # Заменяем 8 или 7 на +7
        if phone_number.startswith("8"):
            phone_number = "+7" + phone_number[1:]
        elif phone_number.startswith("7") and not phone_number.startswith("+7"):
            phone_number = "+7" + phone_number[1:]

        # Проверяем, что номер корректной длины
        if len(phone_number) != 12 or not phone_number[2:].isdigit():
            raise ValueError("Invalid phone number length or non-digit characters found.")

        # Форматируем номер для конкретного сервиса
        if service_name == "Thai Traditions":
            # Формат для Thai Traditions: +7 (XXX) XXX-XX-XX
            phone_number = f"+7 ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}"
        elif service_name == "Dommalera":
            # Пример: добавить другое форматирование при необходимости
            pass  # Нет изменений
        elif service_name == "Ayurveda":
            # Для Ayurveda возвращаем номер без изменений
            pass

        return phone_number
    except Exception as e:
        print(f"Ошибка валидации: {e}")
        raise
