from flask import Flask, render_template

app = Flask(__name__)

EMPLOYEES = []


def load_employees(path="employee_dataset.csv"):
    import csv
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


@app.route("/")
def employees():
    return render_template("employees.html", employees=EMPLOYEES)


if __name__ == "__main__":
    app.run(port=5052, debug=True)