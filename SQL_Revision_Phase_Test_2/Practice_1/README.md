##### **These queries are written for a PostgreSQL environment. Each query is documented with comments as a notes** 





###### **OVERVIEW**

This file contains a SQL queries for a revision questions provided by the lecturer. The queries demonstrate intermediate database management skills using a retail database schema including customers, products and transactions





###### **QUERIES DEMONSTRANTED**

**Window Functions:** Used SUM() with PARTITION BY to calculate total spending per customer and AVG() to find mean transaction values by status.



**Running Totals:** Implemented a chronological running total of revenue using the OVER(ORDER BY ...) clause.



**Subqueries:** Created nested queries to filter products priced above the average and to identify customers who have not made any purchases.



**Conditional Logic:** Applied CASE statements to create custom categories for transaction statuses and inventory stock levels.



**Table Joins:** Linked multiple tables (Customers, Transactions, and Products) to retrieve related data across the database.



**Aggregations:** Used MIN(), MAX(), and GROUP BY to identify the first and last activity dates for individual users.

