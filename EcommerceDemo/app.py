from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "ecommerce-demo-2026"

PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "price": 799.00},
    {"id": 2, "name": "Mechanical Keyboard", "price": 2499.00},
    {"id": 3, "name": "USB-C Hub", "price": 1299.00},
    {"id": 4, "name": "Laptop Stand", "price": 1499.00},
    {"id": 5, "name": "HD Webcam", "price": 1999.00},
    {"id": 6, "name": "USB Cable (2m)", "price": 199.00},
]

GST_RATE = 0.18
DISCOUNT_RATE = 0.10
DISCOUNT_THRESHOLD = 1000
SHIPPING_FLAT = 49.00
FREE_SHIPPING_THRESHOLD = 2000


def compute_bill(subtotal):
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


def cart_items():
    items = []
    for product_id, qty in session.get("cart", {}).items():
        product = next(p for p in PRODUCTS if p["id"] == int(product_id))
        items.append((product["name"], product["price"], qty))
    return items


@app.route("/")
def home():
    return render_template("products.html", products=PRODUCTS)


@app.route("/add", methods=["POST"])
def add_to_cart():
    cart = session.get("cart", {})
    product_id = request.form["product_id"]
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart
    return redirect("/")


@app.route("/cart")
def cart():
    items = cart_items()
    subtotal = round(sum(price * qty for _, price, qty in items), 2)
    bill = compute_bill(subtotal)
    return render_template("cart.html", items=items, bill=bill, empty=not items)


@app.route("/clear")
def clear_cart():
    session["cart"] = {}
    return redirect("/cart")


if __name__ == "__main__":
    app.run(debug=True, port=5050)