"""
E-Commerce Cart Bill Verification Test (Selenium + Flask demo)

Steps covered:
    i)   Add the specified products to the cart
    ii)  Read the price of each selected product dynamically from the webpage
    iii) Calculate the expected bill using python
    iv)  Read the displayed bill amount from the webpage
    v)   Verify that the calculated amount matches the displayed amount
    vi)  Capture a screenshot if the verification fails and generate a
         report showing total price, discount, GST, shipping, final amount
         and test status

Run:  python ecommerce_cart_test.py
"""

import re
import threading
import time
from pathlib import Path
from urllib import request as url_request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from EcommerceDemo.app import app as flask_app
from EcommerceDemo.app import (
    GST_RATE,
    DISCOUNT_RATE,
    DISCOUNT_THRESHOLD,
    SHIPPING_FLAT,
    FREE_SHIPPING_THRESHOLD,
)

BASE_URL = "http://127.0.0.1:5050"
PORT = 5050

PRODUCTS_TO_ADD = ["Wireless Mouse", "Mechanical Keyboard", "USB-C Hub"]

REPORT_FILE = Path("ecommerce_cart_test_report.html")
SCREENSHOT_FILE = Path("cart_verification_failed.png")


def parse_amount(text):
    return round(float(re.sub(r"[^\d.]", "", text)), 2)


def calculate_expected_bill(prices):
    """Mirror of EcommerceDemo.app.compute_bill using python."""
    subtotal = round(sum(prices), 2)
    discount = round(subtotal * DISCOUNT_RATE, 2) if subtotal >= DISCOUNT_THRESHOLD else 0.00
    taxable = subtotal - discount
    gst = round(taxable * GST_RATE, 2)
    shipping = 0.00 if taxable >= FREE_SHIPPING_THRESHOLD else SHIPPING_FLAT
    final_amount = round(subtotal - discount + gst + shipping, 2)
    return {
        "subtotal": subtotal,
        "discount": discount,
        "gst": gst,
        "shipping": shipping,
        "final_amount": final_amount,
    }


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


def read_displayed_bill(driver):
    html_ids = {
        "subtotal": "subtotal",
        "discount": "discount",
        "gst": "gst",
        "shipping": "shipping",
        "final_amount": "final-amount",
    }
    return {field: parse_amount(driver.find_element(By.ID, html_id).text)
            for field, html_id in html_ids.items()}


def generate_report(products, expected, displayed, test_status, screenshot_taken):
    mismatch = expected["final_amount"] != displayed["final_amount"]

    rows = [
        ("Total Price (Subtotal)", expected["subtotal"], displayed["subtotal"]),
        ("Discount", expected["discount"], displayed["discount"]),
        ("GST", expected["gst"], displayed["gst"]),
        ("Shipping", expected["shipping"], displayed["shipping"]),
        ("Final Amount", expected["final_amount"], displayed["final_amount"]),
    ]

    product_rows = "".join(
        f"<tr><td>{name}</td><td>&#8377;{'%.2f' % price}</td></tr>"
        for name, price in products.items()
    )

    table_rows = ""
    for label, expected_value, displayed_value in rows:
        match = expected_value == displayed_value
        result = "<span style='color:green'>PASS</span>" if match else "<span style='color:red'>FAIL</span>"
        table_rows += (
            f"<tr><td>{label}</td>"
            f"<td>&#8377;{'%.2f' % expected_value}</td>"
            f"<td>&#8377;{'%.2f' % displayed_value}</td>"
            f"<td>{result}</td></tr>"
        )

    status_color = "green" if test_status == "PASS" else "red"
    screenshot_note = (
        f"Screenshot saved: <code>{SCREENSHOT_FILE.name}</code>"
        if screenshot_taken
        else "No screenshot taken"
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>E-Commerce Cart Test Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 30px; background: #f7f7f7; }}
h1, h2 {{ color: #2c3e50; }}
table {{ border-collapse: collapse; background: #fff; }}
th, td {{ border: 1px solid #ddd; padding: 8px 14px; text-align: left; }}
th {{ background: #f0f0f0; }}
.banner {{ padding: 12px 16px; border-radius: 6px; font-weight: bold; color: #fff; width: 400px; }}
.pass {{ background: #27ae60; }}
.fail {{ background: #e74c3c; }}
</style>
</head>
<body>
<h1>E-Commerce Cart Bill Verification Report</h1>
<div class="banner {test_status.lower()}">TEST STATUS: {test_status}</div>

<h2>Products Added to Cart</h2>
<table>
<tr><th>Product</th><th>Price (read from webpage)</th></tr>
{product_rows}
</table>

<h2>Bill Breakdown</h2>
<table>
<tr><th>Field</th><th>Calculated (python)</th><th>Displayed (webpage)</th><th>Result</th></tr>
{table_rows}
</table>

<p>{screenshot_note}</p>
</body>
</html>
"""
    REPORT_FILE.write_text(html, encoding="utf-8")


def main():
    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    wait_for_server()

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    test_status = "PASS"
    screenshot_taken = False
    try:
        # (i) Add the specified products to the cart and
        # (ii) read each product price dynamically from the webpage
        products_prices = {}
        for name in PRODUCTS_TO_ADD:
            driver.get(BASE_URL + "/")
            card = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f"//div[contains(@class,'product')]"
                     f"[.//h3[contains(text(),'{name}')]]")
                )
            )
            products_prices[name] = parse_amount(card.find_element(By.CLASS_NAME, "price").text)
            card.find_element(By.TAG_NAME, "button").click()  # Add to Cart

            # Wait for the redirect back to the products page so the next
            # navigation never races with the pending form-submit redirect
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product"))
            )

        print("\nProducts added and prices read from the webpage:")
        for name, price in products_prices.items():
            print(f"  {name}: Rs.{price:.2f}")

        # (iii) Calculate the expected bill using python
        expected = calculate_expected_bill(list(products_prices.values()))
        print("\nExpected bill (calculated by python):")
        for field, value in expected.items():
            print(f"  {field:>13}: Rs.{value:.2f}")

        # (iv) Read the displayed bill amount from the webpage
        driver.get(BASE_URL + "/cart")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "final-amount"))
        )
        displayed = read_displayed_bill(driver)
        print("\nDisplayed bill (read from the webpage):")
        for field, value in displayed.items():
            print(f"  {field:>13}: Rs.{value:.2f}")

        # (v) Verify that the calculated amount matches the displayed amount
        for field in expected:
            if abs(expected[field] - displayed[field]) > 0.01:
                test_status = "FAIL"

        if test_status == "PASS":
            print(f"\nTest PASSED: Calculated final amount "
                  f"(Rs.{expected['final_amount']:.2f}) matches displayed amount "
                  f"(Rs.{displayed['final_amount']:.2f}).")
        else:
            print(f"\nTest FAILED: Calculated final amount "
                  f"(Rs.{expected['final_amount']:.2f}) does NOT match displayed amount "
                  f"(Rs.{displayed['final_amount']:.2f}).")

            # (vi) Capture a screenshot if the verification fails
            driver.save_screenshot(str(SCREENSHOT_FILE))
            screenshot_taken = True
            print(f"Screenshot saved as {SCREENSHOT_FILE.name}")

        generate_report(products_prices, expected, displayed, test_status, screenshot_taken)
        print(f"Report generated: {REPORT_FILE.name}")
        return 0 if test_status == "PASS" else 1

    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())
