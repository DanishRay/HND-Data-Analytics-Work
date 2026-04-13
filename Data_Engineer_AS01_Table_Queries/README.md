### **Project Overview**

This repository contains a full SQL-based implementation of an inventory and order management system. It features a relational database designed to track products, categories, suppliers, and customer orders. The project includes automated data generation scripts and a suite of analytical queries to extract business insights.



### **File Structure**

* Table\_SQL.sql: The core schema definition. It establishes the relational structure including Primary Keys, Foreign Keys, and constraints for tables like Products, Categories, Customers, and Orders.



* 50\_Data\_Rows.sql: A PostgreSQL-optimized script that uses generate\_series and random() functions to automatically populate the database with 50 rows of diverse, realistic test data.



* Query\_SQL.sql: A collection of 20+ business intelligence queries ranging from simple stock checks to complex multi-table joins and spending analysis.



* ERD\_DIAGRAM.png: A visual representation of the database architecture, illustrating the relationships between entities.



### **Database Schema**

The system is built on a highly relational architecture:



* Inventory: Managed through categories, products, and suppliers.



* Sales: Tracked via customers, orders, and order\_items.



* Logistics: Organized by locations.





### **Key Insights \& Features**

* Automation: Uses generate\_series for rapid prototyping.



* Referential Integrity: Strict use of Foreign Keys ensures data consistency across orders and inventory.



* Business Intelligence: Pre-written queries provide instant visibility into sales performance and stock levels.

