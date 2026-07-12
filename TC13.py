# Test Case: Verify email notification verification after failed transaction

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EmailNotificationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Replace with your application's URL
        self.driver.get("http://127.0.0.1:5000")

    def test_email_notification(self):

        driver = self.driver

        input(
            "Perform the following manually:\n"
            "1. Proceed to the payment page.\n"
            "2. Enter INVALID payment details.\n"
            "3. Submit the payment.\n"
            "4. Wait until the failure page appears.\n"
            "5. Press Enter here..."
        )

        # Wait for the email notification message
        notification = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "email-notification")
            )
        )

        self.assertTrue(notification.is_displayed())

        print("Notification Message:")
        print(notification.text)

        self.assertIn("email", notification.text.lower())

        print("\nTest Passed: Email notification displayed after failed transaction.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)