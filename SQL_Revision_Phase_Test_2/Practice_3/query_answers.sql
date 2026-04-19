-- Question a
-- Write a query to rank products within each category based on their price
SELECT category, product_name, price,
RANK() OVER ( -- RANK() function assigns a '1' to the most expensive item in each category
	PARTITION BY category -- This reset the ranking for each category.
	ORDER BY price DESC -- To make the highest price will be rank 1
) AS price_rank
FROM products;
-- In PRODUCTS table, the household supplies category has 'Detergent'($12.99) and 'Paper Towels'($8.99).
-- This query would automatically label Detergant as 1 and Paper Towels as 2 within that specific group.


-- Question b
-- Write a query to find all customers who have only made transactions where the total_amount was less than $10
SELECT first_name, last_name
FROM customers
WHERE customer_id NOT IN( -- Exclusion filter
	SELECT customer_id
	FROM transactions
	WHERE total_amount >= 10
); -- This inner part runs first | It identifies every customer who has made a more than $10 purchases
-- Using NOT IN is simpler than trying to write a complex positive filter.


-- Question c
-- Write a query to list every transaction, the name of the customer, and the total number of unique items in that transaction
SELECT t.transaction_id, c.first_name, c.last_name,
COUNT(DISTINCT ti.product_id) AS unique_item_count -- This count how many different types of products are in the transaction
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
GROUP BY t.transaction_id, c.first_name, c.last_name; -- Using GROUP BY because of aggregate function (COUNT), SQL need to know how to group the results
-- Using triple join :- Start with customer to get their names -> JOIN TRANSACTIONS to link names to specific order IDS -> JOIN TRANSACTION_ITEM to see the products purchased


-- Question d
-- Categorize transactions based on how recently they were maade compared to a specific date (e.g '2024-10-05')
SELECT transaction_id, transaction_date,
CASE
	WHEN transaction_date >= '2024-10-05' THEN 'Recent' -- Checks if the date is on or after the cutoff
	ELSE 'Old'
END AS recenct_status -- Closes the logic and gives the new readable name column
FROM transactions;


-- Question e
-- For each customer, calculate the difference in total_amount between their current transaction and their previous one
SELECT customer_id, transaction_date, total_amount,
total_amount - LAG(total_amount) -- LAG(TOTAL_AMOUNT) function looks at the previous row TOTAL_AMOUNT and make differences calculation. If there is none - it returns NULL
OVER(PARTITION BY customer_id -- It ensures the reaches back stays within the same customer. | Without this, the query might compare Customer's B first purchase to Customer's A last purchase
	ORDER BY transaction_date -- Defines previous. It tells SQL to look at the transactions in chronological order
	) AS difference_from_previous
FROM transactions;
-- Use the LAG() function to track changes in spending habits. This reaches back to a previous row within a specific group (PARTITION) to pull a value forward
-- Allowing it to perform math between two different transactions


-- Question f
-- Calculate what percentage of the total stock quantity ech product represent within it's own category
SELECT product_name, category, stock_quantity,
(stock_quantity * 100.0 / SUM(stock_quantity) OVER(PARTITION BY category)) AS percentage_category_stock
FROM products;
-- STOCK_QUANTITY * 100.0 ;- Multiply by 100.0 to ensure the result is a precentage and to force the database to use decimals instead of whole numbers
-- SUM(STOCK_QUANTITY) ;- This is the total part of the fraction. The window function (OVER(...)) calculates the sum for the group without collapsing the rows
-- PARTITION BY CATEGORY ;- Ensures the total only includes items in the same category