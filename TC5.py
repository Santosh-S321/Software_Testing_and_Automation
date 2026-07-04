# Test Case: Verify that a newly added student record appears correctly in a Dynamic Web Table

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DynamicWebTableTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://demoqa.com/webtables")

    def test_add_student_record(self):
        driver = self.driver

        input(
            "Manually add a new student record and click Submit.\n"
            "When the record appears in the table, press Enter here..."
        )

        student_name = input("Enter the student's First Name exactly as entered: ")

        # Wait until the student's name appears anywhere in the table
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{student_name}')]")
            )
        )

        record = driver.find_element(
            By.XPATH,
            f"//*[contains(text(), '{student_name}')]"
        )

        self.assertTrue(record.is_displayed())

        print(f"Student Record Found: {student_name}")
        print("Test Passed: Newly added student record appears correctly.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)