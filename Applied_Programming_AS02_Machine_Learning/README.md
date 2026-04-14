# **Student Performance Analytics : Machine Learning Implementation**

This repository contains a comprehensive machine learning pipeline and a Streamlit web application designed to predict student exam outcomes (Pass/Fail). The project focuses on data integrity, automated preprocessing, and a multi-model consensus approach to predictive analytics.



### **Core Features**

Automated Data Pipeline: Implements a ColumnTransformer to handle numerical scaling (StandardScaler) and categorical encoding (One-Hot Encoding) automatically, preventing data leakage during training.



Multi-Model Architecture: Features three distinct classification algorithms:



* **Random Forest:** Captures complex, non-linear student patterns using ensemble bagging.



* **Logistic Regression:** Provides a linear baseline with hyperparameter tuning via GridSearchCV.



* **Naive Bayes:** Offers rapid, probabilistic inference for real-time predictions.



Interactive Streamlit Dashboard: A professional-grade UI featuring:



* **Executive Analytics:** Visual distribution of grades and demographic data.



* **Predictive Lab:** A simulation environment to test "what-if" scenarios by adjusting attendance, GPA, and study habits.



* **Performance Audit:** Detailed model evaluation metrics, including Confusion Matrices and Accuracy scores.



### **Technical Architecture**

**The system is built using a modular approach to ensure scalability and reproducibility.**



##### **Preprocessing Logic**

Numerical features are imputed with the median and standardized to a mean of 0 and variance of 1. Categorical variables are handled with a constant imputer and converted into binary vectors via One-Hot Encoding to ensure the models can process text-based environmental signals.



##### **Model Implementation**

The project utilizes Scikit-Learn Pipeline objects to encapsulate the entire workflow from raw data to prediction. This ensures that any data fed into the models—whether during testing or through the Streamlit UI—undergoes the exact same transformations as the training set

