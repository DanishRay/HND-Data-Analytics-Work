### **Overview**

This file contains notes and revisions of set 2, using Python scripts and Jupyter Notebooks on data manipulation, predictive modeling and data visualization. The revision is divided into three main section based on different datasets



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_



#### **Question Structure**



1. **Environmental Analysis (script\_question\_1.ipynb)**
* **Data Cleaning :** Filled missing pollutant using the median
* **Feature Engineering :** Created a **TotalImpact** column by applying a mathematical multiplier (1.25) to raw levels
* **Data Binning :** Classified data into three categories; **Safe, Moderate** and **Hazardous**
* **Statistics :** Identified the specific Reading ID with the highest pollution level



**2. Medical Diagnostic Modelling (script\_question\_2.ipynb)**

* **Preparation :** Scaled numerical features (Glucose Level) to a range between 0 and 1
* **Logistic Regression Model :** Trained and tuned to provide interpretable results for medical staff
* **Random Forest :** Trained for higher accuracy and complex pattern recognition
* **Evaluation :** Models were compared based on Accuracy and Precision to determine the safest tool for clinical use



**3. Olympic Games Visualization (script\_question\_3.ipynb)**

* Removing duplicate records by checking the athlete and the event
* **Stacked Bar Chart :** Displays the Top 10 countries by medal count using specific colors for Gold, Silver, Bronze
* Includes a calculated ratio of Gold medals to the total number of medals won per country





#### **Program / Library Used**

* **Python**
* **Pandas**
* **Scikit-Learn**
* **Matplotlib**

