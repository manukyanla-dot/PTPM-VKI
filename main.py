import hashlib
import logging
import os
import re
import sys
from typing import Tuple


os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("registration")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler("logs/app.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)



BLACKLIST = {
    "admin", "root", "user", "test", "qwerty",
    "guest", "moderator", "support", "login", "password",
}

PHONE_RE = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
STR_RE   = re.compile(r"^[A-Za-z0-9_]{5,}$")
PWD_RE   = re.compile(r"^[А-Яа-яЁё0-9!@#$%^&*()_\-+=]{7,}$")
SPECIALS = r"!@#$%^&*()_\-+="


def mask_password(pwd: str) -> str:
    """Одинаковый пароль → одинаковый результат; разный → разный."""
    digest = hashlib.sha256(pwd.encode("utf-8")).hexdigest()[:10]
    return f"***{digest}"



def _validate_login(login: str) -> str | None:
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
    errors = []
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


def validate_registration(login: str, pwd: str, confirm: str) -> Tuple[bool, str]:

    logger.info(
        "Запрос: login=%r, pwd=%s, confirm=%s",
        login, mask_password(pwd), mask_password(confirm),
    )

    try:
        login_err = _validate_login(login)
        if login_err:
            logger.error("Отказ: %s | login=%r", login_err, login)
            return False, login_err

        pwd_errors = _validate_password(pwd)
        if pwd_errors:
            msg = "; ".join(pwd_errors)
            logger.error("Отказ: %s | login=%r", msg, login)
            return False, msg

        if pwd != confirm:
            msg = "Пароль и подтверждение не совпадают"
            logger.error("Отказ: %s | login=%r", msg, login)
            return False, msg

        logger.info("Успех: login=%r", login)
        return True, ""

    except Exception as e:
        logger.exception("Непредвиденная ошибка: %s", e)
        return False, "Внутренняя ошибка сервера"



def main() -> None:
    try:
        login   = input("Логин: ").strip()
        pwd     = input("Пароль: ").strip()
        confirm = input("Подтверждение пароля: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nПрервано пользователем")
        return

    ok, msg = validate_registration(login, pwd, confirm)
    print(ok)
    print(msg)


if __name__ == "__main__":
    main()