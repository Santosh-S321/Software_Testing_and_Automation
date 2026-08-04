"""
Data-Driven Login Testing using Selenium.

For each record in login_input.csv:
    i)   Open the login page, enter username and password, click Login.
    ii)  Determine whether login succeeds or fails, and store the result
         (PASS/FAIL) in a new CSV file (login_results.csv).

The demo app (AutoLogoutDemo, a Flask login page, valid creds: admin/admin123)
is started automatically on port 5051 so the test runs out of the box.

Run:  python login_data_driven_test.py
"""

import csv
import threading
import time
from pathlib import Path
from urllib import request as url_request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AutoLogoutDemo.app import app as flask_app

BASE_URL = "http://127.0.0.1:5051"
PORT = 5051

INPUT_FILE = Path("login_input.csv")
OUTPUT_FILE = Path("login_results.csv")


def start_server():
    flask_app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)


def wait_for_server(timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with url_request.urlopen(BASE_URL + "/", timeout=2):
                return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("Flask server did not start in time.")


def read_test_data(path):
    records = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            records.append({
                "username": row.get("username", ""),
                "password": row.get("password", ""),
                "expected": row.get("expected", "").strip().upper(),
            })
    return records


def perform_login(driver, username, password):
    """Submit credentials and return True if login succeeded, else False."""
    driver.get(BASE_URL + "/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)

    driver.find_element(By.TAG_NAME, "button").click()

    # Success redirects to /dashboard ("Welcome Admin"); failure returns
    # the login page with an "Invalid Credentials" body.
    time.sleep(1)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
    except Exception:
        return False
    heading = driver.find_element(By.TAG_NAME, "h1").text
    return "Welcome" in heading


def main():
    records = read_test_data(INPUT_FILE)
    if not records:
        print(f"No test records found in {INPUT_FILE.name}")
        return 1

    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    wait_for_server()

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(options=options)

    results = []
    try:
        for i, rec in enumerate(records, 1):
            actual = "PASS" if perform_login(driver, rec["username"], rec["password"]) else "FAIL"
            status = "PASS" if actual == rec["expected"] else "FAIL"
            print(f"[{i}/{len(records)}] user={rec['username']!r} "
                  f"expected={rec['expected']} actual={actual} -> {status}")
            results.append({
                "username": rec["username"],
                "password": rec["password"],
                "expected": rec["expected"],
                "actual": actual,
                "result": status,
            })
    finally:
        driver.quit()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password", "expected", "actual", "result"])
        writer.writeheader()
        writer.writerows(results)

    passed = sum(1 for r in results if r["result"] == "PASS")
    print(f"\nResults written to {OUTPUT_FILE.name} "
          f"({passed}/{len(results)} tests passed).")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())