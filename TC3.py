import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTest(unittest.TestCase):

    def setUp(self):
        service = Service()
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.get("https://practicetestautomation.com/practice-test-login/")

    def test_invalid_login(self):
        driver = self.driver

        # Pause for manual entry
        input("Enter the username and password manually, then press Enter here...")

        # Click the Login button
        driver.find_element(By.ID, "submit").click()

        # Wait for the error message
        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "error"))
        )

        # Display and verify the error message
        print("Error Message:", error.text)

        self.assertTrue(error.is_displayed(), "Error message is not displayed")

        print("Test Passed: Error message is displayed.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()