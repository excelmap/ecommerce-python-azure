from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret-key-123"

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------
def get_db_connection():
    conn = sqlite3.connect("database/products.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------
# HOME PAGE – DISPLAY PRODUCTS
# ---------------------------------
@app.route("/")
def index():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("index.html", products=products)

# ---------------------------------
# ADD TO CART – FIXED VERSION
# ---------------------------------
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    # Get product info
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()

    if not product:
        return redirect(url_for("index"))

    # Retrieve or initialize cart
    cart = session.get("cart", [])

    # Check if product exists in cart
    found = False
    for item in cart:
        if item["id"] == product["id"]:
            item["quantity"] += 1
            found = True
            break

    # Add new product if not found
    if not found:
        cart.append({
            "id": product["id"],
            "name": product["name"],
            "price": float(product["price"]),
            "quantity": 1
        })

    # Save cart back to session
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

# ---------------------------------
# VIEW CART
# ---------------------------------
@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

# ---------------------------------
# UPDATE QUANTITY
# ---------------------------------
@app.route("/update_quantity/<int:product_id>/<action>")
def update_quantity(product_id, action):
    cart = session.get("cart", [])
    for item in cart:
        if item["id"] == product_id:
            if action == "increase":
                item["quantity"] += 1
            elif action == "decrease" and item["quantity"] > 1:
                item["quantity"] -= 1
            break
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

# ---------------------------------
# REMOVE FROM CART
# ---------------------------------
@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != product_id]
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

# ---------------------------------
# CHECKOUT
# ---------------------------------
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        payment_type = request.form.get("payment_type")
        total = float(request.form.get("total", 0))
        session.pop("cart", None)  # clear cart after purchase
        return render_template("checkout.html", total=total, payment_type=payment_type)
    else:
        cart = session.get("cart", [])
        total = sum(item["price"] * item["quantity"] for item in cart)
        return render_template("checkout.html", total=total, payment_type=None)

# ---------------------------------
# START APP
# ---------------------------------
if __name__ == "__main__":
    os.makedirs("database", exist_ok=True)
    app.run(debug=True)


