### **My Understanding On Student Performance Classification Tutorial**

My understanding on this tutorial, it provides a hands-on guide to building a predictive model that determines whether a student passes based on their study habits and class attendance.





##### **Overview**

This tutorial is to compare two popular machine learning algorithms - Logistic Regression and Decision Tree. It is to see which best predicts student results based on small sample dataset **(studentsMark.csv)**





##### **Key Features**

* **Data Cleaning :** Handling unique identifiers and encoding categorical variables
* **Data Splitting :** Using **train\_test\_split** to create training and evaluation sets (35% test size)
* **Hyperparameter Tuning :** Implementing **GridSearchCV** to optimize model parameters like regularization strength for Logistic Regression and **max\_depth** for Decision Trees
* **Model Evaluation :** Comparing models using Recall and F1-score to ensure balanced performance.





##### **Concepts Explain**

**Logistic Regression**

A linear model used for binary classification. It estimates the probability that an instance belongs to a particular class. It is robust and less likely to overfit small datasets.



**Decision Tree**

A non-linear model that splits data into branches based on feature importance. It is highly interpretable (like a flowchart) but can easily overfit if the tree becomes too complex.







