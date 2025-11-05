from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'secret-key-123'  # for session management

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database/products.db')
    conn.row_factory = sqlite3.Row
    return conn


# Home page – show all products
@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)


# Add a product to cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({
        'id': product['id'],
        'name': product['name'],
        'price': product['price']
    })
    return redirect(url_for('index'))


# Cart page
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)


# Checkout (clears the cart)
@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')


if __name__ == '__main__':
    app.run(debug=True)
