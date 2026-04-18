##### **This file contains a practice of SQL code focused on querying techniques from the revision question. It involves solving complex problems using window functions, Common Table Expression(CTEs) and multi-table joins**





#### **Highlights**

* **Revenue Analysis:** Calculates total revenue per product by multiplying quantity and price within a SUM() window function partitioned by product ID.



* **Performance Benchmarking:** Uses scalar subqueries to identify transactions that fall below the overall average spending threshold.



* **Customer Loyalty Tiering:** Implements a LEFT JOIN combined with CASE logic and COUNT() to categorize users as 'Frequent', 'Regular', or 'New' based on their purchase history.



* **Categorical Stock Tracking:** Features a running total of stock quantities that resets with each product category.



* **Advanced Filtering (CTEs):** Employs a Common Table Expression (CTE) to calculate category-specific price averages, enabling a filter for premium-priced items.

