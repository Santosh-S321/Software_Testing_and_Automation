# Test Case: Verify that the submitted student information is stored correctly in the Database

import os
import unittest
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class StudentDatabaseTest(unittest.TestCase):

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

    def test_student_record(self):

        print("\nEnter Student Details")

        student_id = int(input("Student ID: "))
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")

        # Remove existing record if the ID already exists
        self.cursor.execute(
            "DELETE FROM students WHERE student_id=%s",
            (student_id,)
        )

        # Insert student record
        insert_query = """
        INSERT INTO students
        (student_id, first_name, last_name, email)
        VALUES (%s, %s, %s, %s)
        """

        self.cursor.execute(
            insert_query,
            (student_id, first_name, last_name, email)
        )

        self.connection.commit()

        # Verify the stored record
        select_query = """
        SELECT student_id, first_name, last_name, email
        FROM students
        WHERE student_id=%s
        """

        self.cursor.execute(select_query, (student_id,))
        record = self.cursor.fetchone()

        self.assertIsNotNone(record)

        self.assertEqual(record[0], student_id)
        self.assertEqual(record[1], first_name)
        self.assertEqual(record[2], last_name)
        self.assertEqual(record[3], email)

        print("\nStudent Record Stored Successfully")
        print("-----------------------------------")
        print("Student ID :", record[0])
        print("First Name :", record[1])
        print("Last Name  :", record[2])
        print("Email      :", record[3])

        print("\nTest Passed: Student information stored correctly in the database.")

    def tearDown(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)