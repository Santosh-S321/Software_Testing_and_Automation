"""
Generate an employee dataset of 200 employees using Faker.

Writes employee_dataset.csv with columns:
    emp_id, name, department, experience, salary, status

Run:  python create_employee_dataset.py
"""

import csv
import random
from pathlib import Path

from faker import Faker

fake = Faker("en_IN")
fake.seed_instance(2026)
random.seed(2026)

NUM_RECORDS = 200
OUTPUT_FILE = Path("employee_dataset.csv")

DEPARTMENTS = ["IT", "HR", "Finance", "Marketing", "Operations", "Sales"]


def main():
    records = []
    for i in range(1, NUM_RECORDS + 1):
        records.append({
            "emp_id": i,
            "name": fake.name(),
            "department": random.choice(DEPARTMENTS),
            "experience": random.randint(0, 15),
            "salary": random.randint(30000, 150000),
            "status": random.choice(["active", "inactive"]),
        })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["emp_id", "name", "department", "experience", "salary", "status"]
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"{NUM_RECORDS} employee records written to {OUTPUT_FILE.name}")
    sample = [r for r in records
              if r["experience"] >= 5 and r["department"] == "IT" and r["status"] == "active"]
    print(f"IT & active & experience>=5 candidates in dataset: {len(sample)}")


if __name__ == "__main__":
    main()