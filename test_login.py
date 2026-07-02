import unittest
from login import validate_login


class TestLogin(unittest.TestCase):

    def test_valid_login(self):
        self.assertTrue(validate_login("admin", "1234"))

    def test_invalid_username(self):
        self.assertFalse(validate_login("user", "1234"))

    def test_invalid_password(self):
        self.assertFalse(validate_login("admin", "0000"))

    def test_invalid_both(self):
        self.assertFalse(validate_login("user", "0000"))


if __name__ == "__main__":
    unittest.main()