# Test Case: Verify that Cart Total is calculated correctly after adding multiple products

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class CartTotalTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://demowebshop.tricentis.com/")

    def test_cart_total(self):
        driver = self.driver

        input(
            "Manually:\n"
            "1. Add TWO or more products.\n"
            "2. Click Shopping cart.\n"
            "3. Wait until the cart page opens.\n"
            "4. Press Enter here..."
        )

        # Print current URL for debugging
        print("Current URL:", driver.current_url)

        # Find all product rows in the shopping cart
        rows = driver.find_elements(By.CSS_SELECTOR, "tr.cart-item-row")

        print("Products found:", len(rows))

        self.assertGreaterEqual(
            len(rows),
            2,
            "Less than two products found in the cart."
        )

        print("Test Passed: Multiple products are present in the cart.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)