-- Categories Table
CREATE TABLE categories(
	category_id SERIAL PRIMARY KEY,
	category_name VARCHAR(50) NOT NULL
);

-- Products Table
CREATE TABLE products (
	product_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	brand VARCHAR(50),
	price DECIMAL (10, 2) NOT NULL,
	stock_quantity INT DEFAULT 0,
	category_id INT REFERENCES categories(category_id)
);

-- Customers Table
CREATE TABLE customers(
	customer_id SERIAL PRIMARY KEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(100) UNIQUE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE orders(
	order_id SERIAL PRIMARY KEY,
	customer_id INT REFERENCES customers(customer_id),
	product_id INT REFERENCES products(product_id),
	order_date DATE DEFAULT CURRENT_DATE,
	total_amount DECIMAL(10, 2)
);

-- Suppliers Table
CREATE TABLE suppliers(
	supplier_id SERIAL PRIMARY KEY,
	company_name VARCHAR(100) NOT NULL,
	contact_name VARCHAR(100) NOT NULL,
	phone VARCHAR(20),
	country VARCHAR(50)
);

-- Location Table
CREATE TABLE locations(
	location_id SERIAL PRIMARY KEY,
	location_name VARCHAR(100) NOT NULL,
	city VARCHAR(50)
);

-- Order Items Table
CREATE TABLE order_items(
	item_id SERIAL PRIMARY KEY,
	order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
	product_id INT REFERENCES products(product_id),
	quantity INT NOT NULL DEFAULT 1,
	unit_price_at_sale DECIMAL(10, 2) NOT NULL -- Event Sale Price at the moment (if have)
);