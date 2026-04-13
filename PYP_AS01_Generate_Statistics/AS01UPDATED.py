# --- References--- 
#
# Python Software Foundation. (2025). *The Python language reference* (Version 3.12). 
#     Retrieved from https://docs.python.org/3/reference/index.html
#
# Python Software Foundation. (2025). *os — Miscellaneous operating system interfaces*. 
#     (Python 3.12.0 documentation). Retrieved from https://docs.python.org/3/library/os.html
#
# Python Software Foundation. (2025). *tkinter — Python interface to Tcl/Tk*. 
#     (Python 3.12.0 documentation). Retrieved from https://docs.python.org/3/library/tkinter.html
#
# The pandas development team. (2025). *pandas* (Version 2.1.2) [Software]. Zenodo. 
#     https://doi.org/10.5281/zenodo.10091871.
#
# Walt, S. van der, Colbert, S. C., & Varoquaux, G. (2011). The NumPy array: 
#     A structure for efficient numerical computation. *Computing in Science & Engineering*, 
#     *13*(2), 22–30. https://doi.org/10.1109/MCSE.2011.37.
#
# Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & 
#     Engineering*, *9*(3), 90–95.
#     Retrieved from https://doi.org/10.1109/MCSE.2007.55
#
# The pandas development team. (2025). *pandas* (Version 2.1.2). Zenodo. 
#     https://doi.org/10.5281/zenodo.10091871.
#
# Walt, S. van der, Colbert, S. C., & Varoquaux, G. (2011). The NumPy array: 
#     A structure for efficient numerical computation. *Computing in Science & Engineering*, 
#     *13*(2), 22–30. https://doi.org/10.1109/MCSE.2011.37.
#
# Python Software Foundation. (2025). *The Python language reference* (Version 3.12). 
#     Retrieved from https://docs.python.org/3/reference/index.html
#
# Python Software Foundation. (2025). *os — Miscellaneous operating system interfaces*. 
#     (Python 3.12.0 documentation). Retrieved from https://docs.python.org/3/library/os.html
#
# Python Software Foundation. (2025). *tkinter — Python interface to Tcl/Tk*. 
#     (Python 3.12.0 documentation). Retrieved from https://docs.python.org/3/library/tkinter.html
# ---

import pandas as pd
import os
from tkinter import Tk, filedialog
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter 

# --- Data Loading Utility Function ---
def load_data():
    """
    Function to open a file dialogue and load data.
    """
    try:
        root = Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Select the CSV file"
        )
        
        if file_path:
            df = pd.read_csv(file_path)
            print(f"File loaded successfully: {os.path.basename(file_path)}")
            return df, file_path
        else:
            print("File selection cancelled or no file selected.")
            return None, None
            
    except FileNotFoundError:
        print("Error: The selected file was not found.")
        return None, None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}. Trying local file read...")
        return None, None


# --- General Analysis Functions (The Previous / Old Statistics) ---

def analyze_dataframe(df):
    """Prints a summary of the DataFrame: shape, columns, and data types."""
    print("\n" + "="*50)
    print("GENERAL STATISTICS: DATAFRAME OVERVIEW")
    print("="*50)
    # Using df.info() with verbose=False for a concise summary
    df.info(verbose=False, buf=None) 
    print("\nFirst 5 rows:")
    print(df.head().to_markdown(index=False))

def analyze_numeric_column(df, col_engine="Engine_Size_L"):
    """Numeric column analysis (Engine_Size_L)."""
    print("\n" + "="*70)
    print("GENERAL STATISTICS: NUMERIC ANALYSIS (Engine Size)")
    print("="*70)
    print(f"\nNumeric Analysis for '{col_engine}':")
    if col_engine in df.columns:
        cleaned_numeric = pd.to_numeric(df[col_engine], errors='coerce').dropna()
        if not cleaned_numeric.empty:
            print(f" - Count: {cleaned_numeric.count()}")
            print(f" - Mean: {cleaned_numeric.mean():.2f}")
            print(f" - Median: {cleaned_numeric.median():.2f}")
            print(f" - Standard Deviation: {cleaned_numeric.std():.2f}")
            print(f" - Min: {cleaned_numeric.min():.2f}")
            print(f" - Max: {cleaned_numeric.max():.2f}")
            print(f"\n*Analysis: The engine size ranges from {cleaned_numeric.min():.2f}L to {cleaned_numeric.max():.2f}L, with an average size of {cleaned_numeric.mean():.2f}L.")
        else:
            print(f" - No valid numeric values found in '{col_engine}'.")
    else:
        print(f" - Error: Column '{col_engine}' not found.")

def analyze_categorical_column(df, col_fuel="Fuel_Type"):
    """Categorical column analysis (Fuel_Type)."""
    print("\n" + "="*70)
    print("GENERAL STATISTICS: CATEGORICAL ANALYSIS (Fuel Type)")
    print("="*70)
    print(f"\nCategorical Analysis for '{col_fuel}':")
    if col_fuel in df.columns:
        missing_count = df[col_fuel].isnull().sum()
        mode_series = df[col_fuel].mode()
        value_counts = df[col_fuel].value_counts()

        print(f" - Missing values: {missing_count}")
        
        if not mode_series.empty:
            mode = mode_series.iloc[0]
            print(f" - Most common value (Mode): {mode}")
            print(" - Value Counts:")
            print(value_counts.to_string())
            print(f"\n*Analysis: The most common fuel type is **{mode}**, accounting for {value_counts.iloc[0]:,} records.")
        else:
            print(f" - No values or mode found in '{col_fuel}'.")
    else:
        print(f" - Error: Column '{col_fuel}' not found.")


# --- MENU STATISTICS ---

def stats_price_vs_mileage(df):
    """A. Prints the statistics for Price vs. Mileage (Binned Average)"""
    print("\n" + "="*70)
    print("\nMENU STATS: A. Price vs. Mileage (Binned Average)")
    
    # Data prep
    correlation = df['Mileage_KM'].corr(df['Price_USD'])
    bins = pd.cut(df['Mileage_KM'], bins=5, labels=['Low', 'Low-Mid', 'Mid', 'Mid-High', 'High'], include_lowest=True)
    binned_price = df.groupby(bins, observed=False)['Price_USD'].mean()
    
    # Text output 
    print(f"Overall Pearson Correlation (Mileage_KM vs. Price_USD): {correlation:.4f}")
    print("\nAverage Price (USD) by Mileage Bin:")
    print(binned_price.to_string(float_format="${:,.0f}".format))
    print(f"\n*Observation: The overall correlation is weak ({correlation:.4f}). Prices tend to drop as mileage increases across bins.")
    print("="*70)

    # This code first finds out how strongly the total mileage and price are linked using a number called Pearson Correlation. 
    # Then, it sorts the cars into five groups based on their mileage (like "low miles" or "high miles") and calculates the 
    # average price for each of those groups. Finally, it prints all these numbers to show exactly how the typical price 
    # changes as the car is driven more miles.



def stats_sales_classification(df):
    """B. Prints the statistics for Sales Classification Distribution"""
    print("\n" + "-"*70)
    print("\nMENU STATS: B. Sales Volume Distribution by Classification")
    
    # Data prep
    sales_stats = df.groupby('Sales_Classification')['Sales_Volume'].agg(['count', 'mean', 'median', 'std'])
    sales_counts = df['Sales_Classification'].value_counts()

    print("Sales Volume Statistics by Sales Classification:")
    print(sales_stats.to_markdown(numalign="left", stralign="left"))
    
    # Text output 
    print("\nDistribution of Sales Classification:")
    print(sales_counts.to_string())
    print(f"\n*Observation: There is a critical class imbalance, with Low sales accounting for {sales_counts.iloc[0]:,} records.")
    print("="*70)

    # It figures out the count (how many records are there), the average sales, the middle sales value, 
    # and how much the sales vary within each category. It also prints the total number of records in 
    # each category, checking if one type of sale is too rare.



def stats_top_models(df):
    """C. Prints the statistics for Top 5 Car Models by Count"""
    print("\n" + "-"*70)
    print("\nMENU STATS: C. Top 5 Car Models by Frequency")
    
    # Data prep
    top_models = df['Model'].value_counts().head(5)
    
    # Text output
    print("Top 5 Model Counts:")
    print(top_models.to_string())
    most_frequent_model = top_models.index[0]
    print(f"\n*Observation: The {most_frequent_model} is the most frequently recorded model in the dataset.")
    print("="*70)

    # This section simply counts up how many times each car model appears, 
    # finds the top 5 most frequent ones, and then shows you which model is 
    # the most common overall.




# --- CHART GENERATION FUNCTIONS ---

def currency_formatter(x, pos):
    """Formats y-axis ticks as currency."""
    return '${:,.0f}'.format(x)

def generate_chart_price_vs_mileage(df):
    """A. Generates the Bar Chart for Price vs. Mileage (Binned Average) with mouse hover tooltips."""
    plt.style.use('seaborn-v0_8-whitegrid')
    formatter = FuncFormatter(currency_formatter)

    print("\nGenerating Chart A: Price vs. Mileage (Binned Average)...")
    
    # Data prep
    bins = pd.cut(df['Mileage_KM'], bins=5, labels=['Low', 'Low-Mid', 'Mid', 'Mid-High', 'High'], include_lowest=True)
    binned_price = df.groupby(bins, observed=False)['Price_USD'].mean()
    
    # Matplotlib Plot 1: Bar Chart 
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    bars = ax1.bar(binned_price.index.astype(str), binned_price.values, color='#3498db') 
    ax1.set_title('A. Average Price (USD) by Mileage Bin (Hover for Value)', fontsize=16, fontweight='bold', pad=15)
    ax1.set_xlabel('Mileage Bin (KM)', fontsize=12)
    ax1.set_ylabel('Average Price (USD)', fontsize=12)
    
    # Apply currency formatter
    ax1.yaxis.set_major_formatter(formatter)
    
    # Initialize annotation (tooltip)
    annot = ax1.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="yellow", alpha=0.7),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    # Function to update the annotation position and text
    def update_annot(bar, index):
        x = bar.get_x() + bar.get_width() / 2.
        y = bar.get_y() + bar.get_height()
        annot.xy = (x, y)
        
        # Get the value for the specific bar (rounded for display)
        price_value = binned_price.values[index]
        text = f"${price_value:,.0f}"
        
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.7)
        annot.get_bbox_patch().set_facecolor('#d35400') # Orange background
        annot.set_color('white') # White text
        annot.set_ha('center') # Center the text
        
    # Information pop-up where mouse hover 
    def hover(event):
        if event.inaxes == ax1:
            # Check if mouse is over any bar
            contains = False
            bar_index = -1
            for i, bar in enumerate(bars):
                if bar.contains(event)[0]:
                    contains = True
                    bar_index = i
                    break
            
            if contains:
                update_annot(bars[bar_index], bar_index)
                annot.set_visible(True)
                fig1.canvas.draw_idle()
            else:
                if annot.get_visible():
                    annot.set_visible(False)
                    fig1.canvas.draw_idle()

    # Connect the hover function to the mouse
    fig1.canvas.mpl_connect("motion_notify_event", hover)

    fig1.tight_layout()
    plt.show()
    print("Chart A displayed (Interactive: Hover over bars for values).")

    # This code generates an bar chart that visualizes the average price of vehicles binned by their mileage, 
    # featuring a dynamic tooltip that displays the exact average price when the mouse hovers over a bar.




def generate_chart_sales_classification(df):
    """B. Generates the Pie Chart for Sales Classification Distribution"""
    plt.style.use('seaborn-v0_8-whitegrid')

    print("\nGenerating Chart B: Sales Classification Distribution (Pie Chart)...")
    
    # Data prep
    sales_counts = df['Sales_Classification'].value_counts()
    
    # Matplotlib Plot 2: Pie Chart 
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    ax2.pie(
        sales_counts, 
        labels=[f"{idx} ({count:,})" for idx, count in sales_counts.items()], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#e74c3c', '#2ecc71'], 
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'fontsize': 12, 'color': 'black'},
        explode=(0.0, 0.05) 
    )
    ax2.set_title('B. Distribution of Sales Classification', fontsize=16, fontweight='bold', pad=15)
    ax2.set_ylabel('')
    ax2.set_aspect('equal') 
    
    fig2.tight_layout()
    plt.show()
    print("Chart B displayed.")

    # This code generates a pie chart to visually display 
    # the distribution and percentage breakdown of records 
    # across different Sales Classifications.



def generate_chart_top_models(df):
    """C. Generates the Horizontal Bar Chart for Top 5 Car Models by Count"""
    plt.style.use('seaborn-v0_8-whitegrid')

    print("\nGenerating Chart C: Top 5 Car Models by Frequency (Horizontal Bar Chart)...")
    
    # Data prep
    top_models = df['Model'].value_counts().head(5)
    
    # Matplotlib Plot 3: Horizontal Bar Chart 
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    bars = ax3.barh(top_models.index, top_models.values, color='#f39c12') 
    ax3.set_title('C. Top 5 Car Models by Frequency', fontsize=16, fontweight='bold', pad=15)
    ax3.set_xlabel('Count', fontsize=12)
    ax3.set_ylabel('Model', fontsize=12)
    ax3.invert_yaxis() 
    
    # Add labels to the right of the horizontal bars
    for bar in bars:
        ax3.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, 
                 f'{int(bar.get_width()):,}', va='center', ha='left', 
                 fontsize=10, fontweight='bold')

    fig3.tight_layout()
    plt.show()
    print("Chart C displayed.")

    # This code creates a horizontal bar chart that visually 
    # shows the counts for the top 5 most common car models 
    # in the data, with the exact number printed next to each bar.



# --- Menu Functions ---

def display_main_menu():
    """Displays the main application menu."""
    print("\n" + "="*50)
    print("Welcome to Data Analyzer")
    print("="*50)
    print("1. Generate Statistics")
    print("2. Generate Charts")
    print("3. Exit")
    print("-" * 50)
    return input("Enter your choice (1, 2, or 3): ").strip()

def display_stats_menu(df):
    """Handles the statistics sub-menu for the three key analyses."""
    stats_functions = {
        'A': stats_price_vs_mileage,
        'B': stats_sales_classification,
        'C': stats_top_models
    }
    
    while True:
        print("\n" + "-"*50)
        print("Choose Statistics to View:")
        print("A. Price vs. Mileage (Binned Average)")
        print("B. Sales Classification Distribution")
        print("C. Top 5 Car Models by Count")
        print("D. Back to Main Menu")
        print("-" * 50)
        
        choice = input("Enter your choice (A, B, C, D): ").strip().upper()
        
        if choice == 'D':
            return
        elif choice in stats_functions:
            stats_functions[choice](df)
        else:
            print("Invalid choice. Please enter A, B, C, or D.")
            
def display_charts_menu(df):
    """Handles the charts sub-menu."""
    chart_functions = {
        'A': generate_chart_price_vs_mileage,
        'B': generate_chart_sales_classification,
        'C': generate_chart_top_models
    }

    while True:
        print("\n" + "-"*50)
        print("Choose Chart to Generate:")
        print("A. Price vs. Mileage (Binned Average)")
        print("B. Sales Classification Distribution (Pie Chart)")
        print("C. Top 5 Car Models by Count (Horizontal Bar Chart)")
        print("D. Back to Main Menu")
        print("-" * 50)
        
        choice = input("Enter your choice (A, B, C, D): ").strip().upper()
        
        if choice == 'D':
            return
        elif choice in chart_functions:
            chart_functions[choice](df)
        else:
            print("Invalid choice. Please enter A, B, C, or D.")


def main():
    """
    Main function to run the data loader, automatic statistics, and menu-driven analysis.
    """
    
    # Open a file dialog to select the CSV file.
    df, file_path = load_data()
    
    # If the file dialog failed (df is None), fallback to the known uploaded file name
    if df is None:
        try:
            # FALLBACK to the expected uploaded file name for reliable execution here
            fallback_file_path = "BMW_Car_Sales_Classification.csv"
            df = pd.read_csv(fallback_file_path)
            file_path = fallback_file_path
            print(f"\nSuccessfully loaded data using fallback path: {file_path}")
        except FileNotFoundError:
            print("\nError: Could not load data using file dialog or fallback path. Exiting analysis.")
            return
        except Exception as e:
            print(f"\nAn error occurred during fallback file loading: {e}. Exiting analysis.")
            return

    # Proceed with analysis if df is loaded successfully
    if df is not None:
        print(f"\nAnalysis started for file: {os.path.basename(file_path)}")
        
        # --- GENERAL STATISTICS (Not in a Menu) ---
        analyze_dataframe(df)
        analyze_numeric_column(df, "Engine_Size_L")
        analyze_categorical_column(df, "Fuel_Type")
        
        # --- MENU ANALYSIS ---
        while True:
            main_choice = display_main_menu()
            
            if main_choice == '1':
                display_stats_menu(df)
            elif main_choice == '2':
                display_charts_menu(df)
            elif main_choice == '3':
                print("Exiting Data Analyzer. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    else:
        # if failed or the user cancelled the dialog
        print("Analysis terminated as no data was loaded.")

# Execute the analysis
if __name__ == "__main__":
    main()