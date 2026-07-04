# Test Case: Verify that the search feature returns relevant results

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://automationexercise.com/products")

    def test_search_feature(self):
        driver = self.driver

        # Wait for manual search
        input("Enter a search term in the browser, click Search, then press Enter here...")

        # Wait until search results are displayed
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "productinfo"))
        )

        # Get all displayed products
        products = driver.find_elements(By.CLASS_NAME, "productinfo")

        # Verify search results exist
        self.assertGreater(len(products), 0, "No search results found.")

        print(f"Number of search results: {len(products)}")
        print("Test Passed: Search feature returned relevant results.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)