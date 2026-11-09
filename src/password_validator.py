SPECIAL_CHARS = frozenset("!@#$%^&*")


def validate_password(password: str) -> bool:
    """
    Выполняет валидацию строки пароля на соответствие политикам безопасности.

    :param password: Проверяемый пароль
    :return: True, если пароль удовлетворяет всем условиям, иначе False
    :raises TypeError: Если входной параметр не является строкой
    :raises ValueError: Если входная строка содержит символы пробела
    """
    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строкой")
    if " " in password:
        raise ValueError("Пароль не должен содержать пробелы")

    if not 8 <= len(password) <= 20:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return any(c in SPECIAL_CHARS for c in password)
