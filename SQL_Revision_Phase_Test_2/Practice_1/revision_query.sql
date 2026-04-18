-- Question 1
-- Write a query to calculate the total amount (transaction table) spent by each customer across all their transaction
SELECT DISTINCT -- Using DISTINCT to ensures only see customer's name once in the final output
c.customer_id, c.first_name, c.last_name, -- Getting the columns from the table
SUM(t.total_amount) OVER(PARTITION BY c.customer_id) AS total_spent -- A window function and it the PARTITION tells the databse to reset the sum for every new customer 
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id; -- Connect the CUSTOMERS table (c) to the TRANSACTION table (t) using the CUSTOMER_ID column found in both


-- Question 2
-- Write a query to find the names of all products that have a price higher than the average price of all products
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products); -- The subquery(inner logic) | it calculates the mean price of every item in the PRODUCTS table
-- Once the database has that single value, it looks at the PRODUCTS table again, it will check each row of PRICE column and only return PRODUCT_NAME and PRICE
-- If the value is greater than average


-- Question 3
-- Write a query to list all transaction along with the corresponding customer names and total amounts
SELECT t.transaction_id, c.first_name, c.last_name, t.total_amount
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id; -- Using JOIN to find rows where the CUSOMTER_ID in the TRANSACTIONS table matches the CUSTOMER_ID in the CUSTOMERS table


-- Question 4
-- Write a query to categorize each transaction based on it's status
-- 'Completed' for transaction with status 'Completed'
-- 'In Progress' for transactions with status 'Pending'
-- 'Failed' for transactions with status 'Cancelled', else 'Unknown'
SELECT transaction_id, status,
	CASE
		WHEN status = 'Completed' THEN 'Completed'
		WHEN status = 'Pending' THEN 'In Progress'
		WHEN status = 'Cancelled' THEN 'Failed'
		ELSE 'Unknown'
	END AS transaction_category -- This act as like 'if-then-else' logic within SQL query
FROM transactions;


-- Question 5
-- Write a query to calculate the running total of the total_amount for all transactions over time
SELECT transaction_id, transaction_date, total_amount,
SUM(total_amount) OVER(ORDER BY transaction_date) AS running_total -- Using the window function to calculate the running total
FROM transactions
ORDER BY transaction_date; -- Running total order by TRANSACTION_DATE
-- When include an ORDER BY inside the OVER clause without a PARTITION BY - every row, it sums the current
-- TOTAL_AMOUNT plus all TOTAL_AMOUNT values from the rows that came before it chronologically


-- Question 6
-- Write a query to calculate the average total amount spent by all customers, partitioned by status of the transactions.
SELECT transaction_id, status, total_amount,
AVG(total_amount) OVER(PARTITION BY status) AS avg_total_amount
FROM transactions;
-- AVG(TOTAL_AMOUNT) - The aggregate function that calculates the mean value of the sspending
-- OVER - It signals that the query using a window function rather than standard grouping
-- PARTITION BY status - To divide the rows into groups based on their STATUS. The average is then calculated separately for each bucket


-- Question 7
-- Write a query to find the names of all customers (customer table) who have not made any transactions
SELECT first_name, last_name
FROM customers
WHERE customer_id NOT IN(SELECT customer_id FROM transactions); -- The subquery. It runs first to create a list of every CUSTOMER_ID that has actually made purchase


-- Question 8
-- Write a query to list all products that have been sold in any transaction
SELECT p.product_name, ti.quantity
FROM products p 
JOIN transaction_items ti -- Brings in the table that records individual items within each sale, using the 'ti' alias 
ON p.product_id = ti.product_id; -- This is the connect part - it link rows only when the ID in the product catalog matches the ID in the transaction list


-- Question 9
-- Write a query to categorize products based on their stock_quantity
-- 'In Stock' if the stock_quantity is greater than 50
-- 'Low Stock' if the stock_quantity is between 1 and 50
-- 'Out of Stock' if the stock_quantity is 0, else 'Unknown'
SELECT product_name, stock_quantity,
	CASE
		WHEN stock_quantity > 50 THEN 'In Stock'
		WHEN stock_quantity BETWEEN 1 AND 50 THEN 'Low Stock'
		WHEN stock_quantity = 0 THEN 'Out of Stock'
		ELSE 'Unknown'
	END AS stock_status
FROM products;


-- Question 10 
-- Write a query to find the first and last transaction date for each customer
SELECT customer_id,
MIN(transaction_date) AS first_transaction_date, -- Function to looks at all dates for a specific customer and selects the earliest one
MAX(transaction_date) AS last_transaction_date -- This function to looks and selects the most recent one
FROM transactions
GROUP BY customer_id -- this is to calculate the MIN and MAX for each unique customer searately
ORDER BY customer_id; -- For organizes the final list numerically by ID