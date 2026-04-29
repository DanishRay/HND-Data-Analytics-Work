### **Revision Set 3**

This repository sub-file contains materials for practicing data cleaning, data visualization and machine learning using Python and pandas library





#### **Overview**

This revisions is divided into three sections, each focusing on a different dataset and set of analytical tasks. It includes raw data files, Python scripts (.ipynb) and study notes





#### **Repository Contents**

**Dataset**

* **SupplyChain.csv** : Data containing order IDs, shipping costs, and warehouse locations
* **MembershipData.csv** : Data containing customer spending, tenure, and renewal status
* **TechSales.csv**: Data containing product sales, profit, and regional information



**Scripts**

* **scripts\_question\_1.ipynb:** Focuses on data cleaning, missing value treatment, and basic data analysis
* **scripts\_question\_2.ipynb:** Focuses on machine learning preparation, model training (Random Forest and Logistic Regression), and model evaluation
* **scripts\_question\_3.ipynb:** Focuses on descriptive statistics and data visualization using seaborn and matplotlib





#### **Summaries**

**Question 1 : Data Cleaning and Analysis**

* **Missing Values**: Empty cells in the shipping column are filled using the median value



* **Consistency**: Product categories are converted to uppercase letters to ensure uniform data



* **Binning**: Shipping costs are divided into three groups: Economy, Standard, and Premium



* **Mapping**: Warehouse codes are replaced with Urban or Rural labels for easier reading



**Question 2 : Machine Learning Model**

* **Data Split**: The data is separated into a training set (80%) and a test set (20%) using stratified sampling.



* **Scaling**: The Tenure column is standardized so the average is 0 and the spread is 1.



* **Algorithms**: Two models are trained: a Random Forest Classifier and a Logistic Regression model.



* **Evaluation**: Performance is measured using Precision and F1-Score. The final analysis identifies which model best avoids False Positive errors.



**Question 3 : Visualization \& Insights**

* **Summaries:** A table is generated showing the total and average revenue for each product



* **Distribution:** A Boxplot shows the range of profit across different geographical regions



* **Comparison:** A Horizontal Bar Chart compares the total profit of multiple products across all regions

