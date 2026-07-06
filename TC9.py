# Test Case: Verify automatic logout after inactivity

import unittest
from selenium import webdriver


class AutoLogoutTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_auto_logout(self):

        driver = self.driver

        driver.get("http://127.0.0.1:5000")

        input(
            "Login manually using:\n"
            "Username : admin\n"
            "Password : admin123\n"
            "Press Enter after login..."
        )

        print("Waiting 35 seconds...")

        input(
            "Do NOT touch the browser.\n"
            "Wait for automatic logout.\n"
            "Press Enter after you are redirected..."
        )

        self.assertEqual(driver.title, "Login")

        print("✅ Test Passed")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()