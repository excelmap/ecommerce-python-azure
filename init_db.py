import sqlite3, os

# make sure database folder exists
os.makedirs('database', exist_ok=True)

# create database connection
conn = sqlite3.connect('database/products.db')
c = conn.cursor()

# create products table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    description TEXT
)
''')

# insert sample products
c.executemany('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', [
    ('Laptop', 899.99, 'High performance laptop'),
    ('Smartphone', 499.99, 'Latest Android phone'),
    ('Headphones', 89.99, 'Noise cancelling headphones')
])

conn.commit()
conn.close()
print("✅ Database initialized successfully.")
