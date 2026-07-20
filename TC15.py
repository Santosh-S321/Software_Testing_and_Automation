# Test Case: Test whether the password is Case-sensitive

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PasswordCaseSensitiveTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://practicetestautomation.com/practice-test-login/")

    def test_password_case_sensitive(self):

        driver = self.driver

        input(
            "\nManual Steps:\n"
            "1. Enter the correct Username manually.\n"
            "2. Enter the Password with incorrect letter case (e.g., password123 instead of Password123).\n"
            "3. Click the Login button.\n"
            "4. After the error message appears, press Enter here..."
        )

        # Wait for the error message
        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "error"))
        )

        print("\nError Message:")
        print(error.text)

        # Verify login failed because of incorrect password case
        self.assertIn("Your password is invalid!", error.text)

        print("\n Test Passed: Password is case-sensitive.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)