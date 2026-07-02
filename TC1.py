import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ManualLoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_manual_login(self):
        driver = self.driver

        # Open the dummy login page
        driver.get("https://the-internet.herokuapp.com/login")

        print("\nEnter the credentials manually:")
        print("Username: tomsmith")
        print("Password: SuperSecretPassword!")
        input("After logging in successfully, press Enter to continue...")

        # Verify successful login
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )

        self.assertIn(
            "You logged into a secure area!",
            success_message.text
        )

        print("✅ Test Passed: User logged in successfully.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()