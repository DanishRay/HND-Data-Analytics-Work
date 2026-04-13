### **Project Overview**

This is an interactive command-line application that allows users to load, process, and visualize automotive datasets (specifically focusing on features like engine size, fuel types, and mileage). The tool combines statistical summaries with graphical representations to provide immediate insights into vehicle trends and distributions.



### **Key Features**

Interactive File Selection: Uses tkinter to provide a graphical "Open File" dialog, making it easy to load CSV datasets without manual path entry.



**Comprehensive Statistics:**



* General Overview: Instant feedback on dataset shape, column types, and missing values.



* Numerical Analysis: Detailed breakdown of engine sizes (mean, median, standard deviation).



* Categorical Analysis: Frequency counts and percentages for variables like Fuel Type.





**Dynamic Visualizations: Integrated matplotlib and seaborn charts, including:**



* Histograms for Engine Size distribution.



* Boxplots for identifying mileage outliers.



* Bar charts for Fuel Type and Transmission distributions.



* Robust Error Handling: Built-in fallback mechanisms and exception handling to manage incorrect file formats or missing data.



### **Data Focus**

While the tool is flexible, it is optimized for datasets containing:

* Engine\_Size\_L: Numerical analysis of displacement.



* Fuel\_Type: Categorical tracking of Petrol, Diesel, Hybrid, and Electric variants.



* Mileage: Performance and usage metrics.



### **References**

* **Python Language Reference (v3.12)**



* **Pandas Development Team Documentation**



* **Matplotlib 2D Graphics Environment standards**

