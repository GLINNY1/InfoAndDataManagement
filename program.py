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

#Column names and data types
print(df.info())

#Basic statistics for numeric columns
print(df.describe())

#Task 2: Data Cleaning
#Check for missing values
print("\nMissing values per column:")
print(df.isna().sum())

#Drop rows with missing values in Description column
df = df.dropna(subset=["Description"])

#Remove rows with invalid transaction values
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

#Remove rows with cancelled transactions
df = df[~df["Invoice"].astype(str).str.startswith("C")]

#Create total price column
df["TotalPrice"] = df["Quantity"] * df["Price"]

#Remove outliers from TotalPrice column
q_low = np.percentile(df["TotalPrice"], 1)
q_high = np.percentile(df["TotalPrice"], 99)
df = df[(df["TotalPrice"] >= q_low) & (df["TotalPrice"] <= q_high)]
