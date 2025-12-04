# Task 0: Load data & basic info

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("default")  # optional

# Load data from file
file_path = "online_retail_II.xlsx"

# Read data from file
df = pd.read_excel(file_path, sheet_name="Year 2010-2011")

# Print rows and columns
print("Rows and Columns:", df.shape)

print(df.head())
print(df.info())
print(df.describe())
