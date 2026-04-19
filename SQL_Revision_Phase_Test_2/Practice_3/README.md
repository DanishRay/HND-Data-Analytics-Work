##### **HIGHLIGHTS**

* **Ranking Data:** Using RANK() with PARTITION BY to order products by price within their specific categories.



* **Time-Series Analysis:** Implementing the LAG() function to compare spending amounts between a customer's current and previous transactions.



* **Inventory Metrics:** Calculating the percentage of stock each product represents within its category using the SUM() window function.



* **Exclusion Logic:** Using subqueries with NOT IN to filter for specific customer behaviors, such as those who only make small purchases.



* **Multi-Table** Aggregation: Combining three tables (Customers, Transactions, and Items) to count unique products per order.



* **Conditional Labels:** Applying CASE statements to categorize transactions based on a specific cutoff date.







##### **Personal References Notes**

* **Logic Explanations:** Why a GROUP BY is needed for certain counts.



* **Function Breakdowns:** How window functions like OVER(PARTITION BY ...) prevent rows from collapsing while still performing calculations.



* **Practical Examples:** Comments explaining how the results (like ranking or percentages) would look in a real-world scenario.

