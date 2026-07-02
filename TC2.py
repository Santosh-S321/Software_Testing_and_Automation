from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_valid_login(self):
        driver = self.driver

        # Open the login page
        driver.get("https://example.com/login")

        # Enter valid username
        driver.find_element(By.ID, "username").send_keys("testuser")

        # Enter valid password
        driver.find_element(By.ID, "password").send_keys("password123")

        # Click the Login button
        driver.find_element(By.ID, "loginButton").click()

        # Wait for the page to load
        time.sleep(3)

        # Verify successful login
        expected_title = "Dashboard"
        self.assertEqual(driver.title, expected_title)

        print("✅ Login Test Passed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()