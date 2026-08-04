"""
Employee Record Analysis using Selenium.

Steps:
    i)   Read all the employee records from the webpage.
    ii)  Find employees with experience >= 5 years, department == IT and
         status = active.
    iii) Verify that every selected employee has a salary > 60k.
    iv)  Store all matching (validated) records in a list of dictionaries.
    v)   Print number of matching employees, average salary and the highest
         salary employee.
    vi)  Generate a CSV report containing all matching employees.

Run:  python employee_test.py
"""

import csv
import re
import threading
import time
from pathlib import Path
from urllib import request as url_request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from EmployeeDemo.app import app as emp_app, EMPLOYEES

BASE_URL = "http://127.0.0.1:5052"
PORT = 5052

MIN_EXPERIENCE = 5
REQUIRED_DEPARTMENT = "IT"
REQUIRED_STATUS = "active"
MIN_SALARY = 60000

DATASET_FILE = Path("employee_dataset.csv")
REPORT_FILE = Path("employee_report.csv")


def start_server():
    emp_app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)


def wait_for_server(timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with url_request.urlopen(BASE_URL + "/", timeout=2):
                return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("Flask server did not start in time.")


def parse_salary(text):
    return float(re.sub(r"[^\d]", "", text))


def read_all_employees(driver):
    """(i) Read every employee record from the webpage table."""
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#employees tbody tr")))

    employees = []
    for row in driver.find_elements(By.CSS_SELECTOR, "table#employees tbody tr.employee"):
        emps = {
            "emp_id": int(row.find_element(By.CLASS_NAME, "emp-id").text),
            "name": row.find_element(By.CLASS_NAME, "name").text,
            "department": row.find_element(By.CLASS_NAME, "department").text,
            "experience": int(row.find_element(By.CLASS_NAME, "experience").text),
            "salary": parse_salary(row.find_element(By.CLASS_NAME, "salary").text),
            "status": row.find_element(By.CLASS_NAME, "status").text,
        }
        employees.append(emps)
    return employees


def main():
    # Load dataset into the Flask app before starting the server.
    with open(DATASET_FILE, newline="", encoding="utf-8") as f:
        EMPLOYEES[:] = list(csv.DictReader(f))

    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    wait_for_server()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(BASE_URL + "/")

        # (i) Read all employee records from the webpage.
        all_employees = read_all_employees(driver)
        print(f"(i)   Total employee records read from webpage: {len(all_employees)}")

        # (ii) Filter: experience >= 5, department == IT, status == active.
        selected = [
            e for e in all_employees
            if e["experience"] >= MIN_EXPERIENCE
            and e["department"] == REQUIRED_DEPARTMENT
            and e["status"] == REQUIRED_STATUS
        ]
        print(f"(ii)  Selected (exp>=5, IT, active): {len(selected)}")

        # (iii) Verify every selected employee has salary > 60k.
        #       (iv) Keep only matching (validated) records.
        matching = []
        for e in selected:
            if e["salary"] > MIN_SALARY:
                matching.append(e)
            else:
                print(f"(iii) EXCLUDED (salary <= {MIN_SALARY}): "
                      f"emp_id={e['emp_id']} salary=Rs.{e['salary']}")

        print(f"(iii) Verified salary > {MIN_SALARY}: "
              f"{len(matching)} of {len(selected)} selected employees pass.")
        print(f"(iv)  Matching records stored in list of dicts: {len(matching)}")

        # (v) Print number of matching employees, average salary, highest salary employee.
        if matching:
            salaries = [e["salary"] for e in matching]
            avg_salary = round(sum(salaries) / len(salaries), 2)
            highest = max(matching, key=lambda e: e["salary"])
            print(f"(v)   Number of matching employees: {len(matching)}")
            print(f"      Average salary           : Rs.{avg_salary}")
            print(f"      Highest salary employee  : {highest['name']} "
                  f"(emp_id={highest['emp_id']}, Rs.{highest['salary']})")
        else:
            avg_salary = 0.0
            print("(v)   No matching employees.")

        # (vi) Generate a CSV report of all matching employees.
        with open(REPORT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["emp_id", "name", "department", "experience", "salary", "status"]
            )
            writer.writeheader()
            writer.writerows(matching)
        print(f"(vi)  CSV report generated: {REPORT_FILE.name} ({len(matching)} rows)")

        return 0 if matching else 1

    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())