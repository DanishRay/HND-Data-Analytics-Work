-- 1. List all unique brands
SELECT DISTINCT brand FROM products;

-- 2. Find low stock items
SELECT name, stock_quantity
FROM products
WHERE stock_quantity < 10;

-- 3. Count total customers
SELECT COUNT (*) AS total_users FROM customers;

-- 4. Sort products by price
SELECT name, price
FROM products ORDER BY price DESC;

-- 5. Search for a specific customer
SELECT * FROM customers 
WHERE first_name LIKE '%User%';

-- 6. Showing product with Category name
SELECT p.name, c.category_name 
FROM products p 
JOIN categories c ON p.category_id = c.category_id;

-- 7. List all orders wth customers name
SELECT o.order_id, c.first_name, c.last_name, o.total_amount 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id;

-- 8. Find which products are in which orders
SELECT oi.order_id, p.name, oi.quantity 
FROM order_items oi 
JOIN products p ON oi.product_id = p.product_id
ORDER BY oi.order_id ASC;

-- 9. List suppliers and the countries they operate in
SELECT company_name, country
FROM suppliers;

-- 10. Find customers who joined in the last 30 days
SELECT first_name, created_at
FROM customers WHERE created_at > CURRENT_DATE - INTERVAL '30_days';

-- 11. Total revenue per category
SELECT 
    c.category_name, 
    SUM(oi.quantity * oi.unti_price_at_sale) AS total_revenue
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY c.category_name
ORDER BY total_revenue DESC;

-- 12. Average price of products per brand
SELECT brand, ROUND(AVG(price), 2) AS avg_price 
FROM products GROUP BY brand;

-- 13. Count how many orders each customers placed
SELECT customer_id, COUNT(order_id) AS order_count 
FROM orders GROUP BY customer_id;

-- 14. Find the most expensive item over sold
SELECT MAX(unit_price_at_sale) FROM order_items;

-- 15. Total sales amount per day
SELECT order_date, SUM(total_amount) FROM orders GROUP BY order_date;

-- 16. Find products that have never been sold
SELECT name FROM products 
WHERE product_id NOT IN (SELECT product_id FROM order_items);

-- 17. Top 3 cusomters by spending
SELECT c.first_name, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.first_name
ORDER BY total_spent DESC LIMIT 3;

-- 18. Join of Cusomter + Order + Product
SELECT c.last_name, o.order_date, p.name AS product_purchased, oi.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- 19. Identify brands with more than 5 products in stock
SELECT brand, COUNT(*) FROM products 
GROUP BY brand HAVING COUNT(*) > 5;

-- 20. Calculate the profit gap. Current price vs Sale price
SELECT p.name, p.price AS current_price, oi.unit_price_at_sale AS sold_at,
(p.price - oi.unit_price_at_sale) AS price_difference
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id;
