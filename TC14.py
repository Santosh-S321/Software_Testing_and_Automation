# Test Case: Verify drag and drop functionality verification

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class DragAndDropTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://the-internet.herokuapp.com/drag_and_drop")

    def test_drag_and_drop(self):
        driver = self.driver

        input(
            "Manually drag Column A onto Column B.\n"
            "After the columns are swapped, press Enter here..."
        )

        # Read the headings after drag and drop
        column_a = driver.find_element(By.ID, "column-a").text
        column_b = driver.find_element(By.ID, "column-b").text

        print("\nColumn A Heading:", column_a)
        print("Column B Heading:", column_b)

        # Verify the headings have swapped
        self.assertEqual(column_a, "B")
        self.assertEqual(column_b, "A")

        print("\nTest Passed: Drag and Drop functionality verified successfully.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)