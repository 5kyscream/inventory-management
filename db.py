# The correct db.py for MySQL
import mysql.connector
from datetime import datetime
import os

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    return conn

def add_user(username, password, role):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_db_connection()
    c = conn.cursor(buffered=True) # Use buffered cursor for reads
    c.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_item(sku, name, description, category, expiration_date):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO items (sku, name, description, category, expiration_date) VALUES (%s, %s, %s, %s, %s)',
              (sku, name, description, category, expiration_date))
    conn.commit()
    conn.close()

def update_item(sku, name, description, category, expiration_date):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE items SET name = %s, description = %s, category = %s, expiration_date = %s WHERE sku = %s',
              (name, description, category, expiration_date, sku))
    conn.commit()
    conn.close()

def get_items():
    conn = get_db_connection()
    c = conn.cursor(buffered=True)
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return items

def add_stock(sku, quantity, location):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO stock (sku, quantity, location) VALUES (%s, %s, %s)', (sku, quantity, location))
    conn.commit()
    conn.close()

def update_stock(sku, quantity, location):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE stock SET quantity = %s, location = %s WHERE sku = %s', (quantity, location, sku))
    conn.commit()
    conn.close()

def get_stock():
    conn = get_db_connection()
    c = conn.cursor(buffered=True)
    c.execute('SELECT items.sku, items.name, stock.quantity, stock.location FROM stock JOIN items ON stock.sku = items.sku')
    stock = c.fetchall()
    conn.close()
    return stock

def add_order(type, sku, quantity, status, user_id):
    conn = get_db_connection()
    c = conn.cursor()
    created_at = datetime.now().isoformat()
    c.execute('INSERT INTO orders (type, sku, quantity, status, created_at, user_id) VALUES (%s, %s, %s, %s, %s, %s)',
              (type, sku, quantity, status, created_at, user_id))
    conn.commit()
    conn.close()

def update_order(order_id, status, sku, quantity):
    conn = get_db_connection()
    c = conn.cursor()
    modified_at = datetime.now().isoformat()
    c.execute('UPDATE orders SET status = %s, sku = %s, quantity = %s, modified_at = %s WHERE id = %s',
              (status, sku, quantity, modified_at, order_id))
    conn.commit()
    conn.close()

def get_orders():
    conn = get_db_connection()
    c = conn.cursor(buffered=True)
    c.execute('SELECT orders.id, orders.type, orders.sku, items.name, orders.quantity, orders.status, orders.created_at, orders.user_id, users.username '
              'FROM orders JOIN items ON orders.sku = items.sku JOIN users ON orders.user_id = users.id')
    orders = c.fetchall()
    conn.close()
    return orders

def get_stock_report():
    conn = get_db_connection()
    c = conn.cursor(buffered=True)
    c.execute('SELECT items.sku, items.name, SUM(stock.quantity) as total_quantity, stock.location '
              'FROM stock JOIN items ON stock.sku = items.sku GROUP BY items.sku, stock.location')
    report = c.fetchall()
    conn.close()
    return report