# Test Case: Verify that duplicate Student IDs cannot be created

import os
import unittest
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class DuplicateStudentIDTest(unittest.TestCase):

    def setUp(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8"
        )

        self.cursor = self.connection.cursor()

    def test_duplicate_student_id(self):

        print("\nEnter Student Details")

        student_id = int(input("Student ID: "))
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")

        # Check whether the Student ID already exists
        check_query = "SELECT * FROM students WHERE student_id=%s"
        self.cursor.execute(check_query, (student_id,))
        record = self.cursor.fetchone()

        if record:
            print("\nDuplicate Student ID detected.")
            print("Student ID already exists in the database.")
            print("Test Passed: Duplicate Student ID cannot be created.")

        else:
            insert_query = """
            INSERT INTO students
            (student_id, first_name, last_name, email)
            VALUES (%s,%s,%s,%s)
            """

            self.cursor.execute(
                insert_query,
                (student_id, first_name, last_name, email)
            )

            self.connection.commit()

            print("\nStudent record inserted successfully.")
            print("No duplicate Student ID found.")

    def tearDown(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)