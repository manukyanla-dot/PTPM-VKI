import unittest

from src.password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):
    # --- Позитивные ---
    def test_valid_latin(self):
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_cyrillic(self):
        self.assertTrue(validate_password("ПарольТест9#"))

    # --- Границы длины ---
    def test_boundary_length_7(self):
        self.assertFalse(validate_password("Passw1!"))

    def test_boundary_length_8(self):
        self.assertTrue(validate_password("Passwo1!"))

    def test_boundary_length_20(self):
        self.assertTrue(validate_password("A" * 17 + "a1!"))

    def test_boundary_length_21(self):
        self.assertFalse(validate_password("A" * 17 + "a1!b"))

    def test_empty_string(self):
        self.assertFalse(validate_password(""))

    # --- Классы эквивалентности ---
    def test_missing_uppercase(self):
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lowercase(self):
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special(self):
        self.assertFalse(validate_password("SecurePassword1"))

    def test_underscore_not_special(self):
        self.assertFalse(validate_password("SecurePass1_"))

    def test_question_mark_not_special(self):
        self.assertFalse(validate_password("SecurePass1?"))

    # --- Исключения ---
    def test_space_inside(self):
        with self.assertRaises(ValueError):
            validate_password("Pass 1234!")

    def test_space_leading(self):
        with self.assertRaises(ValueError):
            validate_password(" Pass1234!")

    def test_space_trailing(self):
        with self.assertRaises(ValueError):
            validate_password("Pass1234! ")

    def test_type_none(self):
        with self.assertRaises(TypeError):
            validate_password(None)

    def test_type_int(self):
        with self.assertRaises(TypeError):
            validate_password(12345678)

    def test_type_list(self):
        with self.assertRaises(TypeError):
            validate_password(["P", "a", "s", "s", "1", "!"])


if __name__ == "__main__":
    unittest.main()
