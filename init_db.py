import sqlite3, os

os.makedirs('database', exist_ok=True)
conn = sqlite3.connect('database/products.db')
c = conn.cursor()

# Drop old table if exists
c.execute('DROP TABLE IF EXISTS products')

# Create new table with category column
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    description TEXT,
    category TEXT
)
''')

# Insert products by category
c.executemany('INSERT INTO products (name, price, description, category) VALUES (?, ?, ?, ?)', [
    ('Laptop', 899.99, 'High performance laptop', 'Electronics'),
    ('Smartphone', 499.99, 'Latest Android phone', 'Electronics'),
    ('Headphones', 89.99, 'Noise cancelling headphones', 'Accessories'),
    ('Office Chair', 149.99, 'Ergonomic comfort chair', 'Furniture'),
    ('Desk Lamp', 39.99, 'LED study lamp', 'Home')
])

conn.commit()
conn.close()
print("✅ Database re-initialized with categories.")
