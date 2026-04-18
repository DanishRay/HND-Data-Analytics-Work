CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock_quantity INT
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    transaction_date DATE,
    status VARCHAR(20),
    total_amount DECIMAL(10, 2)
);

CREATE TABLE transaction_items (
    transaction_item_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES transactions(transaction_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    price DECIMAL(10, 2)
);


INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES
('David', 'Clark', 'david.clark@example.com', '555-1239', '12 Ocean Drive', 'San Diego', 'USA'),
('Emily', 'Jones', 'emily.jones@example.com', '555-7745', '89 River Road', 'Orlando', 'USA'),
('Michael', 'Brown', 'michael.brown@example.com', '555-2390', '45 Pine Grove', 'Austin', 'USA'),
('Sarah', 'Taylor', 'sarah.taylor@example.com', '555-4938', '567 Elm Ave', 'Dallas', 'USA'),
('Lily', 'Green', 'lily.green@example.com', '555-2391', '789 Maple Ave', 'Denver', 'USA'),
('James', 'Miller', 'james.miller@example.com', '555-9438', '123 Oak Street', 'San Antonio', 'USA'),
('Sophia', 'Walker', 'sophia.walker@example.com', '555-4729', '456 Cedar Lane', 'Chicago', 'USA'),
('Daniel', 'Wilson', 'daniel.wilson@example.com', '555-3489', '678 Birch Road', 'Boston', 'USA');


INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Cereal', 'Food & Beverages', 4.99, 100),
('Milk', 'Food & Beverages', 2.49, 200),
('Bread', 'Food & Beverages', 1.99, 150),
('Toothpaste', 'Personal Care', 3.49, 120),
('Shampoo', 'Personal Care', 5.99, 80),
('Detergent', 'Household Supplies', 12.99, 60),
('Canned Beans', 'Food & Beverages', 1.49, 180),
('Paper Towels', 'Household Supplies', 8.99, 75),
('Orange Juice', 'Food & Beverages', 3.49, 110),
('Soda', 'Food & Beverages', 1.25, 300),
('Body Lotion', 'Personal Care', 8.49, 90),
('Dish Soap', 'Household Supplies', 3.99, 65),
('Crisps', 'Snacks', 2.99, 180),
('Chocolate Bar', 'Snacks', 1.99, 150),
('Frozen Pizza', 'Frozen Foods', 6.99, 50),
('Ice Cream', 'Frozen Foods', 4.99, 100);



INSERT INTO transactions (customer_id, transaction_date, status, total_amount) VALUES
(1, '2024-10-01', 'Completed', 22.45),
(2, '2024-10-02', 'Completed', 7.98),
(3, '2024-10-03', 'Cancelled', 0.00),
(4, '2024-10-04', 'Pending', 19.96),
(5, '2024-10-05', 'Completed', 8.98),
(6, '2024-10-06', 'Pending', 5.48),
(7, '2024-10-07', 'Completed', 19.96),
(8, '2024-10-08', 'Cancelled', 0.00);



INSERT INTO transaction_items (transaction_id, product_id, quantity, price) VALUES
(1, 1, 2, 4.99),    
(1, 2, 1, 2.49),    
(1, 4, 1, 3.49),    
(2, 3, 2, 1.99),     
(4, 5, 1, 5.99),    
(4, 6, 1, 12.99),
(5, 7, 1, 6.99),     
(5, 8, 1, 1.99),    
(6, 10, 2, 2.99),   
(7, 3, 2, 1.99),   
(7, 4, 1, 3.49),    
(7, 9, 1, 8.49);


