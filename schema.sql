CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK( role IN ('admin', 'manager', 'staff', 'sales') ) NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    expiration_date DATE
);

CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    location TEXT NOT NULL,
    FOREIGN KEY(sku) REFERENCES items(sku)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT CHECK( type IN ('purchase', 'sales') ) NOT NULL,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT CHECK( status IN ('pending', 'received', 'shipped') ) NOT NULL,
    created_at DATETIME NOT NULL,
    modified_at DATETIME,
    user_id INTEGER,
    FOREIGN KEY(sku) REFERENCES items(sku),
    FOREIGN KEY(user_id) REFERENCES users(id)
);