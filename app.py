from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'secret-key-123'

def get_db_connection():
    conn = sqlite3.connect('database/products.db')
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Home Page (Search + Category)
# -----------------------------
@app.route('/')
def index():
    conn = get_db_connection()
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    if search_query:
        query += ' AND name LIKE ?'
        params.append(f'%{search_query}%')
    if category_filter:
        query += ' AND category = ?'
        params.append(category_filter)

    products = conn.execute(query, params).fetchall()
    categories = conn.execute('SELECT DISTINCT category FROM products').fetchall()
    conn.close()

    return render_template('index.html', products=products, categories=categories,
                           search_query=search_query, category_filter=category_filter)


# -----------------------------
# Add to Cart
# -----------------------------
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if 'cart' not in session:
        session['cart'] = []

    # Check if product already in cart
    for item in session['cart']:
        if item['id'] == product['id']:
            item['quantity'] += 1
            break
    else:
        session['cart'].append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': 1
        })

    return redirect(url_for('index'))


# -----------------------------
# Update Quantity
# -----------------------------
@app.route('/update_quantity/<int:product_id>/<action>')
def update_quantity(product_id, action):
    if 'cart' in session:
        for item in session['cart']:
            if item['id'] == product_id:
                if action == 'increase':
                    item['quantity'] += 1
                elif action == 'decrease' and item['quantity'] > 1:
                    item['quantity'] -= 1
                break
    return redirect(url_for('cart'))


# -----------------------------
# Cart Page
# -----------------------------
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)


# -----------------------------
# Checkout (Payment Type)
# -----------------------------
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        payment_type = request.form.get('payment_type')
        total = request.form.get('total')
        # Here you can save order/payment info into a DB
        session.pop('cart', None)
        return render_template('checkout.html', payment_type=payment_type, total=total)
    else:
        cart_items = session.get('cart', [])
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        return render_template('checkout.html', cart=cart_items, total=total)


if __name__ == '__main__':
    app.run(debug=True)
