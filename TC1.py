# Test Case: Open a Website and verify the Title
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class WebsiteTitleTest(unittest.TestCase):

    def setUp(self):
        # Launch Chrome browser
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_website_title(self):
        driver = self.driver

        # Open the website
        driver.get("https://the-internet.herokuapp.com")

        # Wait until the page title is loaded
        WebDriverWait(driver, 10).until(
            lambda d: d.title != ""
        )

        # Expected title
        expected_title = "The Internet"

        # Verify the title
        self.assertEqual(driver.title, expected_title)

        print("Expected Title:", expected_title)
        print("Actual Title:", driver.title)
        print("Test Passed: Website title is correct.")

    def tearDown(self):
        # Close the browser
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)