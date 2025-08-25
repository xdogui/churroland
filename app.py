from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Productos disponibles
PRODUCTS = [
    {"id": 1, "name": "ChurroParty", "price": 2000, "image": "/static/images/VasodChurro.jpg"},
#   {"id": 1, "name": "Churro Arcoiris", "price": 2000, "image": "/static/churro_arcoiris.jpg"}
    {"id": 2, "name": "Churro Chocolate", "price": 1800, "image": "/static/images/ChurroChoco.png"},
    {"id": 3, "name": "Churro Fresa", "price": 1500, "image": "/static/images/ChurroFresa.png"}
]

# Página principal
@app.route("/")
def home():
    return render_template("home.html", products=PRODUCTS)

# Agregar producto al carrito
@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        cart = session.get("cart", [])
        for item in cart:
            if item["id"] == product_id:
                item["quantity"] += 1
                break
        else:
            cart.append({"id": product["id"], "name": product["name"], "price": product["price"], "quantity": 1})
        session["cart"] = cart
    return redirect(url_for("home"))

# Ver carrito
@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

# Quitar producto
@app.route("/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != product_id]
    session["cart"] = cart
    return redirect(url_for("cart"))

# Checkout (solo ejemplo)
@app.route("/checkout")
def checkout():
    session.pop("cart", None)  # Vacía el carrito
    return "<h1>✅ ¡Gracias por tu compra!</h1><a href='/'>Volver a la tienda</a>"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)





