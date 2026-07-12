from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/process", methods=["POST"])
def process():

    card = request.form["card"]

    # Any card number except 1234567890123456 will fail
    if card == "1234567890123456":
        return redirect("/success")

    return redirect("/failed")


@app.route("/failed")
def failed():
    return render_template("failed.html")


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)