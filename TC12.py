# Test Case: Verify retry mechanism for failed payment transaction

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PaymentRetryTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000")

    def test_retry_payment(self):

        driver = self.driver

        input(
            "Click 'Proceed to Payment'.\n"
            "Enter an INVALID card number.\n"
            "Click 'Pay Now'.\n"
            "Press Enter here after Payment Failed appears..."
        )

        retry = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "retry-payment")
            )
        )

        self.assertTrue(retry.is_displayed())

        print("Retry Button Found")
        print("Test Passed")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)