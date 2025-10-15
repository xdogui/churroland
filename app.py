from flask import Flask, render_template, session, redirect, url_for, flash, request
import urllib.parse
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Productos disponibles
PRODUCTS = [
    {"id": 1, "name": "ChurroParty", "price": 2000, "image": "/static/images/VasodChurro.jpg"},
    {"id": 2, "name": "Churro Chocolate", "price": 1800, "image": "/static/images/ChurroChoco.png"},
    {"id": 3, "name": "Churro Caramelo", "price": 1700, "image": "/static/images/ChurroCaramelo.png"},
    {"id": 4, "name": "Churro Fresa", "price": 1500, "image": "/static/images/ChurroFresa.png"}
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
                flash(f"➕ Se agregó otra unidad de {product['name']} al carrito 🛒", "info")
                break
        else:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1
            })
            flash(f"✅ {product['name']} agregado al carrito 🛒", "success")
        session["cart"] = cart
    return redirect(url_for("home"))

# Ver carrito
@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

# Quitar producto del carrito
@app.route("/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != product_id]
    session["cart"] = cart
    return redirect(url_for("cart"))

# Página de checkout con formulario
@app.route("/checkout")
def checkout():
    cart = session.get("cart", [])
    if not cart:
        flash("Tu carrito está vacío 🛒", "info")
        return redirect(url_for("cart"))
    return render_template("checkout.html")

# Enviar pedido por WhatsApp
@app.route("/send_order", methods=["POST"])
def send_order():
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    telefono = request.form.get("telefono")
    direccion = request.form.get("direccion")

    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)

    # Crear mensaje de WhatsApp
    mensaje = f"🧾 *Nuevo Pedido de ChurroLand* 🧾\n"
    mensaje += f"👤 Cliente: {nombre} {apellido}\n"
    mensaje += f"📞 Teléfono: {telefono}\n"
    if direccion:
        mensaje += f"📍 Dirección: {direccion}\n"
    mensaje += "\n🛍️ *Productos:*\n"
    for item in cart:
        mensaje += f"- {item['name']} x{item['quantity']} = ₡{item['price'] * item['quantity']}\n"
    mensaje += f"\n💰 *Total:* ₡{total}\n"

    # Número de WhatsApp (formato internacional sin + ni espacios)
    numero_whatsapp = "50687368883"  # 👈 Cambia por tu número

    # Generar link de WhatsApp
    mensaje_encoded = urllib.parse.quote(mensaje)
    whatsapp_url = f"https://wa.me/{numero_whatsapp}?text={mensaje_encoded}"

    # Vaciar el carrito
    session.pop("cart", None)

    # Redirigir a WhatsApp
    return redirect(whatsapp_url)

# Páginas adicionales
@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/sabores")
def sabores():
    return render_template("sabores.html")

@app.route("/eventos")
def eventos():
    return render_template("eventos.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

# Ejecutar aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
