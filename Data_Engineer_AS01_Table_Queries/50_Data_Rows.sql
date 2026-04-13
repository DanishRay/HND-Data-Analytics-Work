-- NOTES**
-- [generate_series] :- An engine. to generate (e.g 1 - 50) instead of typing manually
-- [random()] :- To make the data look real by varying the data values instead of everything being the same
-- [ARRAY[...]] :- The scripts will reaches in and pull out random([floor(random() * 5) + 1]) of values for every rows

-- Categories
INSERT INTO categories (category_name)
SELECT 'Category ' || i FROM generate_series(1, 50) AS i;

-- Suppliers
INSERT INTO suppliers (company_name, contact_name, phone, country)
SELECT 
    'Supplier Group ' || i, 
    'Manager ' || i, 
    '555-' || LPAD(i::text, 4, '0'), 
    (ARRAY['USA', 'China', 'Germany', 'Japan', 'South Korea'])[floor(random() * 5) + 1]
FROM generate_series(1, 50) AS i;

-- Locations
INSERT INTO locations (location_name, city)
SELECT 
    'Branch ' || i, 
    (ARRAY['New York', 'London', 'Tokyo', 'Berlin', 'Singapore'])[floor(random() * 5) + 1]
FROM generate_series(1, 50) AS i;

-- Products
INSERT INTO products (name, brand, price, stock_quantity, category_id)
SELECT 
    'Product Model ' || i,
    (ARRAY['TechCorp', 'GigaByte', 'Apex', 'Nexus', 'Volt'])[floor(random() * 5) + 1],
    (random() * (2000 - 10) + 10)::numeric(10,2), -- Price between 10 and 2000
    floor(random() * 100) + 1,
    (i % 50) + 1 -- Distributes across the 50 categories
FROM generate_series(1, 50) AS i;

-- Customers
INSERT INTO customers (first_name, last_name, email)
SELECT 
    'User' || i, 
    'LastName' || i, 
    'user' || i || '@email.com'
FROM generate_series(1, 50) AS i;

-- Orders
INSERT INTO orders (customer_id, product_id, total_amount)
SELECT 
    (i % 50) + 1, 
    floor(random() * 49) + 1, 
    (random() * 500 + 50)::numeric(10,2)
FROM generate_series(1, 50) AS i;

-- Order Items 
INSERT INTO order_items (order_id, product_id, quantity, unit_price_at_sale)
SELECT 
    (i % 50) + 1, 
    floor(random() * 49) + 1, 
    floor(random() * 5) + 1,
    (random() * 1500 + 20)::numeric(10,2)
FROM generate_series(1, 50) AS i;