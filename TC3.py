# Test Case: Verify that error message is displayed for invalid credentials

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://practicetestautomation.com/practice-test-login/")

    def test_invalid_login(self):
        driver = self.driver

        input(
            "Enter INVALID credentials, click Login manually, "
            "then press Enter here..."
        )

        # Wait until the error message is visible
        error = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "error"))
        )

        print("Error Message:", error.text)

        # Verify the error is displayed
        self.assertTrue(error.is_displayed())

        # Verify either invalid username or invalid password message
        self.assertTrue(
            "Your username is invalid!" in error.text or
            "Your password is invalid!" in error.text
        )

        print("Test Passed: Error message displayed.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)