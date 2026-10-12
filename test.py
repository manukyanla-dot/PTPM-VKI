from main import validate_registration, mask_password


def run():
    cases = [
        # (login, pwd, confirm, ожидаемый_ok)
        ("user_01", "Пароль1!", "Пароль1!", True),
        ("+7-999-123-4567", "Пароль1!", "Пароль1!", True),
        ("user@example.com", "Пароль1!", "Пароль1!", True),

        ("", "Пароль1!", "Пароль1!", False),
        ("admin", "Пароль1!", "Пароль1!", False),
        ("ab", "Пароль1!", "Пароль1!", False),

        ("user_01", "Пар1!", "Пар1!", False),
        ("user_01", "пароль1!", "пароль1!", False),
        ("user_01", "ПАРОЛЬ1!", "ПАРОЛЬ1!", False),
        ("user_01", "Пароль!!", "Пароль!!", False),
        ("user_01", "Пароль11", "Пароль11", False),
        ("user_01", "Password1!", "Password1!", False),

        ("user_01", "Пароль1!", "Пароль2!", False),
    ]

    for i, (l, p, c, exp) in enumerate(cases, 1):
        ok, msg = validate_registration(l, p, c)
        status = "OK " if ok == exp else "FAIL"
        print(f"[{status}] #{i:02d} login={l!r:20} -> {ok} | {msg}")

    assert mask_password("Пароль1!") == mask_password("Пароль1!")
    assert mask_password("Пароль1!") != mask_password("Пароль2!")
    print("Маскирование — OK")


if __name__ == "__main__":
    run()