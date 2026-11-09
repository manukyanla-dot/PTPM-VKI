import hashlib
import re
from typing import Tuple

from src.logger_setup import setup_logger

log = setup_logger()

# ---------- Константы ----------
BLACKLIST = {
    "admin", "root", "user", "test", "qwerty",
    "guest", "moderator", "support", "login", "password",
}

PHONE_RE = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
STR_RE   = re.compile(r"^[A-Za-z0-9_]{5,}$")
PWD_RE   = re.compile(r"^[А-Яа-яЁё0-9!@#$%^&*()_\-+=]{7,}$")

SPECIALS = r"!@#$%^&*()_\-+="

# ---------- Маскирование пароля ----------
def mask_password(pwd: str) -> str:
    """
    Маскирует пароль: одинаковый пароль → одинаковый результат,
    разный → разный. Реальные символы не раскрываются.
    """
    digest = hashlib.sha256(pwd.encode("utf-8")).hexdigest()[:10]
    return f"***{digest}"


# ---------- Вспомогательные проверки ----------
def _validate_login(login: str) -> str | None:
    """Возвращает текст ошибки или None, если логин валиден."""
    if not login:
        return "Логин пустой"

    if PHONE_RE.match(login) or EMAIL_RE.match(login):
        return None

    if STR_RE.match(login):
        if login.lower() in BLACKLIST:
            return "Логин в чёрном списке"
        return None

    return "Некорректный формат логина (телефон/email/строка)"


def _validate_password(pwd: str) -> list[str]:
    """Возвращает список ошибок пароля (может быть пустым)."""
    errors: list[str] = []

    if len(pwd) < 7:
        errors.append("Пароль короче 7 символов")
    if not PWD_RE.match(pwd):
        errors.append("Пароль содержит недопустимые символы")
    if not re.search(r"[А-ЯЁ]", pwd):
        errors.append("Нет заглавной кириллической буквы")
    if not re.search(r"[а-яё]", pwd):
        errors.append("Нет строчной кириллической буквы")
    if not re.search(r"\d", pwd):
        errors.append("Нет цифры")
    if not re.search(f"[{re.escape(SPECIALS)}]", pwd):
        errors.append("Нет спецсимвола")

    return errors


# ---------- Основная функция ----------
def validate_registration(login: str, pwd: str, confirm: str) -> Tuple[bool, str]:
    """
    Комплексная валидация регистрационных данных.

    :return: (True, "") при успехе; (False, "причина") при ошибке.
    """
    masked_pwd     = mask_password(pwd)
    masked_confirm = mask_password(confirm)

    log.info(
        "Запрос регистрации: login=%r, pwd=%s, confirm=%s",
        login, masked_pwd, masked_confirm,
    )

    try:
        # --- Логин ---
        login_err = _validate_login(login)
        if login_err:
            log.error("Отказ: %s | login=%r", login_err, login)
            return False, login_err

        # --- Пароль ---
        pwd_errors = _validate_password(pwd)
        if pwd_errors:
            msg = "; ".join(pwd_errors)
            log.error("Отказ: %s | login=%r", msg, login)
            return False, msg

        # --- Совпадение ---
        if pwd != confirm:
            msg = "Пароль и подтверждение не совпадают"
            log.error("Отказ: %s | login=%r", msg, login)
            return False, msg

        log.info("Успех: login=%r", login)
        return True, ""

    except Exception as e:
        # трассировка стека в лог
        log.exception("Непредвиденная ошибка при валидации: %s", e)
        return False, "Внутренняя ошибка сервера"