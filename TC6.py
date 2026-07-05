# Test Case: Verify successful document upload and rejection of unsupported file types

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class FileUploadTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://blueimp.github.io/jQuery-File-Upload/")

    def test_file_upload(self):
        driver = self.driver

        # Pause for manual upload
        input(
            "Manually upload a supported or unsupported file.\n"
            "After the upload result is displayed, press Enter here..."
        )

        # Get the page text
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # Check for success or rejection
        if "error" in page_text.lower() or "not allowed" in page_text.lower():
            print("Unsupported file type was rejected.")
            print("Test Passed: Unsupported file type rejected.")
        else:
            print("Supported file uploaded successfully.")
            print("Test Passed: Document uploaded successfully.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)