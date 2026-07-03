# Test Case: Verify that a user can login with valid credentials

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_valid_login(self):
        driver = self.driver

        # Open the login page
        driver.get("https://the-internet.herokuapp.com/login")

        # Enter valid username
        driver.find_element(By.ID, "username").send_keys("tomsmith")

        # Enter valid password
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

        # Click the Login button
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait until the success message is visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )

        # Verify successful login
        success_message = driver.find_element(By.ID, "flash").text
        self.assertIn("You logged into a secure area!", success_message)

        print("Login Test Passed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)