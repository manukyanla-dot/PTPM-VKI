import pytest
from src.validator import validate_registration, mask_password


# ---------- Успешные кейсы ----------
@pytest.mark.parametrize("login", [
    "user_01",                 # строка
    "+7-999-123-4567",         # телефон
    "user@example.com",        # email
])
def test_success(login):
    ok, msg = validate_registration(login, "Пароль1!", "Пароль1!")
    assert ok is True
    assert msg == ""


# ---------- Логин ----------
def test_login_empty():
    ok, msg = validate_registration("", "Пароль1!", "Пароль1!")
    assert ok is False and "пустой" in msg.lower()

def test_login_blacklist():
    ok, msg = validate_registration("admin", "Пароль1!", "Пароль1!")
    assert ok is False and "чёрном списке" in msg

def test_login_short():
    ok, msg = validate_registration("ab", "Пароль1!", "Пароль1!")
    assert ok is False and "формат" in msg


# ---------- Пароль ----------
def test_password_short():
    ok, msg = validate_registration("user_01", "Пар1!", "Пар1!")
    assert ok is False and "короче 7" in msg

def test_password_no_upper():
    ok, msg = validate_registration("user_01", "пароль1!", "пароль1!")
    assert ok is False and "заглавной" in msg

def test_password_no_lower():
    ok, msg = validate_registration("user_01", "ПАРОЛЬ1!", "ПАРОЛЬ1!")
    assert ok is False and "строчной" in msg

def test_password_no_digit():
    ok, msg = validate_registration("user_01", "Пароль!!", "Пароль!!")
    assert ok is False and "цифры" in msg

def test_password_no_special():
    ok, msg = validate_registration("user_01", "Пароль11", "Пароль11")
    assert ok is False and "спецсимвола" in msg

def test_password_latin_invalid():
    ok, msg = validate_registration("user_01", "Password1!", "Password1!")
    assert ok is False


# ---------- Совпадение ----------
def test_mismatch():
    ok, msg = validate_registration("user_01", "Пароль1!", "Пароль2!")
    assert ok is False and "не совпадают" in msg


# ---------- Маскирование ----------
def test_mask_same():
    assert mask_password("Пароль1!") == mask_password("Пароль1!")

def test_mask_diff():
    assert mask_password("Пароль1!") != mask_password("Пароль2!")

def test_mask_no_plaintext():
    assert "Пароль1!" not in mask_password("Пароль1!")