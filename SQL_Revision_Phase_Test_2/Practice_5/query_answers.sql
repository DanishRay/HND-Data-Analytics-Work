-- Question 1

-- Question a
-- Write a query to show the total number of transactions made by each customer
SELECT c.customer_id, c.first_name, c.last_name, 
COUNT(t.transaction_id) OVER(PARTITION BY c.customer_id) AS total_transaction_count
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id;
-- Counting the total transactions for each specific customer without collapsing the rows into a single summary line
-- It keeps all the transaction details visible while showing the customer's total count side-by-side


-- Question b
-- Write a query to find all products that have a stock_quantity greater than the average stock quantity of all products
SELECT product_id, product_name, stock_quantity
FROM products
WHERE stock_quantity > (SELECT AVG(stock_quantity) FROM products);
-- Subquery inside the parentheses runs first to find the average stock of all products.
-- The outer query then compares every individual product's stock against that single calculated number


-- Question c
-- Write a query to list all transaction items and the category of the product they belong to
SELECT ti.transaction_id, p.product_id, p.category
FROM transaction_items ti
JOIN products p ON ti.product_id = p.product_id;
-- This operation links the transaction items to the product names and categories
-- It only returns rows where a match exist between the two lable based on the PRODUCT_ID


-- Question d
-- Write a query to categorize transactions based on their total_amount
SELECT transaction_id, total_amount,
	CASE
		WHEN total_amount > 20.00 THEN 'High Priority'
		WHEN total_amount BETWEEN 10.00 AND 20.00 THEN 'Standard'
		WHEN total_amount < 10.00 THEN 'Low Priority'
		ELSE 'Zero Value'
	END AS priority_level
FROM transactions;
-- Creates a virtual column.
-- SQL checks each condition in order;- once a match is found
-- It assigns the label and moves to the next row


-- Question e
-- Write a query to calcultte the running total of revenue (using total_amount) across all transactions
SELECT transaction_id, total_amount,
SUM(total_amount) OVER(ORDER BY transaction_id) AS cumulative_revenue
FROM transactions;
-- Using ORDER BY inside the window function without a PARTITION
-- will tell SQL to add the current row's amount to the sum of all previous rows, creating cumulative growth count



-- Question 2

-- Question a
-- Write a query to calculate the average price of products within each category
SELECT product_id, product_name, category,
AVG(price) OVER(PARTITION BY category) AS avg_category_price
FROM products
ORDER BY product_id;
-- This calculates the average price for a specific category
-- And displays that average on every product row belonging to that category


-- Question b
-- Write a query to find the names of all products that have never been part of a 'Completed' transaction
SELECT product_id, product_name
FROM products
WHERE product_id NOT IN(
	SELECT ti.product_id
	FROM transaction_items ti
	JOIN transactions t ON ti.transaction_id = t.transaction_id
	WHERE t.status = 'Completed'
);
-- The WHERE operation identifies all products that have been sold successfully.
-- The NOT IN then will filters the main product list to show only those that are missing



-- Question c
-- Write a query to list all transactions along with the city and country of the customer
SELECT t.transaction_id, c.city, c.country
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id;
-- A standard way to pull personal customer details into a transaction report
-- By matching their unique IDs


-- Question d
-- Write a query to categorize inventory urgency
SELECT product_name, stock_quantity,
	CASE
		WHEN stock_quantity < 70 THEN 'Critical'
		WHEN stock_quantity >= 70 THEN 'Stable'
	END AS urgency_status
FROM products
ORDER BY stock_quantity;
-- WHEN is used for inventory management.
-- It transformts raw numbers into actionable status labels based on the specific business rules provided in the questions



-- Question e
-- Write a query to find the smallest and largest total_amount recorded for each transaction status
SELECT status,
MIN(total_amount) AS min_amount,
MAX(total_amount) AS max_amount
FROM transactions
GROUP BY status;
-- Unlike window functions. GROUP BY collapses the reuslts
-- It will only get one row for 'Completed', 'Pending', etc
-- Showing the lowest and highest values for those groups

