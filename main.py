from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt
from db import init_db, add_user, get_user, add_item, update_item, get_items, add_stock, update_stock, get_stock, add_order, update_order, get_orders, get_stock_report

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key

# Initialize database
init_db()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        role = 'staff' #default
        try:
            add_user(username, hashed, role)
            flash('user registered successfully', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = get_user(username)
        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('base.html', username=session['username'], role=session['role'])

@app.route('/items', methods=['GET', 'POST'])
def items():
    if 'user_id' not in session or session['role'] not in ['admin', 'manager']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        sku = request.form['sku']
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        expiration_date = request.form['expiration_date']
        if request.form['action'] == 'add':
            add_item(sku, name, description, category, expiration_date)
        elif request.form['action'] == 'update':
            update_item(sku, name, description, category, expiration_date)
        flash('Item saved successfully', 'success')
    items_list = get_items()
    return render_template('items.html', items=items_list)

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if 'user_id' not in session or session['role'] not in ['admin', 'manager', 'staff']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        sku = request.form['sku']
        quantity = int(request.form['quantity'])
        location = request.form['location']
        if request.form['action'] == 'add':
            add_stock(sku, quantity, location)
        elif request.form['action'] == 'update':
            update_stock(sku, quantity, location)
        flash('Stock updated successfully', 'success')
    stock_list = get_stock()
    items = get_items()
    return render_template('stock.html', stock=stock_list, items=items)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'user_id' not in session or session['role'] not in ['admin', 'manager', 'staff', 'sales']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        type = request.form['type']
        sku = request.form['sku']
        quantity = int(request.form['quantity'])
        status = request.form['status']
        user_id = session['user_id']
        if request.form['action'] == 'add':
            add_order(type, sku, quantity, status, user_id)
        elif request.form['action'] == 'update':
            order_id = request.form['order_id']
            update_order(order_id, status, sku, quantity)
        flash('Order processed successfully', 'success')
    orders_list = get_orders()
    items = get_items()
    return render_template('orders.html', orders=orders_list, items=items)

@app.route('/reports')
def reports():
    if 'user_id' not in session or session['role'] not in ['admin', 'manager']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    report = get_stock_report()
    return render_template('reports.html', report=report)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        role = request.form['role']
        add_user(username, password, role)
        flash('User added successfully', 'success')
    users_list = [get_user(u[1]) for u in get_user('')]  # Simplified for demo
    return render_template('users.html', users=users_list)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)