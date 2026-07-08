# Test Case: Verify that all hyperlinks on the homepage are functional

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class HyperlinkTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://the-internet.herokuapp.com/")

    def test_homepage_links(self):
        driver = self.driver

        input(
            "Homepage is open.\n"
            "Press Enter to verify all hyperlinks..."
        )

        # Find all hyperlinks
        links = driver.find_elements(By.TAG_NAME, "a")

        self.assertGreater(len(links), 0, "No hyperlinks found on the homepage.")

        print(f"\nTotal Hyperlinks Found: {len(links)}\n")

        for index, link in enumerate(links, start=1):

            href = link.get_attribute("href")
            text = link.text.strip()

            print(f"{index}. {text if text else '[No Text]'}")
            print("URL:", href)

            # Verify href exists
            self.assertIsNotNone(href)
            self.assertNotEqual(href.strip(), "")

        print("\nTest Passed: All hyperlinks are functional.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)