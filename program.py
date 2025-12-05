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

#Print first 5 rows of data
print(df.head())

#Column names and data types
print(df.info())

#Basic statistics for numeric columns
print(df.describe())

#Task 1: Data Cleaning
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

#Print after cleaning
print("\nAfter cleaning, shape:", df.shape)

#Task 2: Time-based Sales Analysis
# Make sure InvoiceDate is datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# InvoiceMonth
df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

# InvoiceDay
df["InvoiceDay"] = df["InvoiceDate"].dt.date

#InvoiceHour
df["InvoiceHour"] = df["InvoiceDate"].dt.hour

#InvoiceWeekday
df["Weekday"] = df["InvoiceDate"].dt.day_name()

# Revenue by month
rev_by_month = df.groupby("InvoiceMonth")["TotalPrice"].sum().sort_index()

# Total revenue per day of week
rev_by_weekday = df.groupby("Weekday")["TotalPrice"].sum()

# Revenue by hour
rev_by_hour = df.groupby("InvoiceHour")["TotalPrice"].sum()

# Reorder weekdays to match standard order
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
rev_by_weekday = rev_by_weekday.reindex(weekday_order)


# Plot revenue by month
plt.figure()
rev_by_month.plot(kind="line")
plt.title("Total Revenue by Month")
plt.xlabel("Month")
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45) # readability purposes
plt.tight_layout()
plt.show()

# Plot revenue by day
plt.figure()
rev_by_weekday.plot(kind="bar")
plt.title("Total Revenue by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45) #readability purposes
plt.tight_layout()
plt.show()

# Plot revenue by hour
plt.figure()
rev_by_hour.plot(kind="bar")
plt.title("Total Revenue by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Revenue (GBP)") 
plt.tight_layout()
plt.show()

#Task 3: Product-based Sales Analysis
#Total revenue by product category
product_rev = df.groupby("Description")["TotalPrice"].sum()

#Total quantity sold by product category
product_qty = df.groupby("Description")["Quantity"].sum()

#Total number of invoices by product category
product_invoices = df.groupby("Description")["Invoice"].nunique()

# Top 10 products by revenue
# breakdown of code: df.groupby("Description")["TotalPrice"].sum() groups the data by the Description column 
# and then sums the TotalPrice column
# sort_values(ascending=False) sorts the data in descending order by the TotalPrice column. 
# head(10) returns the top 10 rows.
top10_rev = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)

# same breakdown as above for quantity
top10_qty = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10)


print("\nTop 10 products by revenue:")
print(top10_rev)

print("\nTop 10 products by quantity:")
print(top10_qty)

# Top 10 by revenue (horizontal bar)
plt.figure(figsize=(10,6))
top10_rev.plot(kind="barh")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (GBP)")
plt.ylabel("Product Description")
plt.gca().invert_yaxis()   # so highest appears at top
plt.tight_layout()
plt.show()

# Top 10 by quantity
plt.figure(figsize=(10,6))
top10_qty.plot(kind="barh")
plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold")
plt.ylabel("Product Description")
plt.gca().invert_yaxis()   # so highest appears at top
plt.tight_layout()
plt.show()

#Invoices distribution by product category
product_invoices = df.groupby("Description")["Invoice"].nunique()

# Top 10 products by revenue (with invoice counts)
top10_rev_invoices = product_invoices[top10_rev.index]
top10_qty_invoices = product_invoices[top10_qty.index]

#print top 10 products by revenue (with invoice counts)
print("\nTop 10 Products by Revenue (with invoice counts):")
print(pd.DataFrame({
    "Revenue": top10_rev,
    "NumInvoices": top10_rev_invoices
}))

#print top 10 products by quantity (with invoice counts)
print("\nTop 10 Products by Quantity (with invoice counts):")
print(pd.DataFrame({
    "Quantity": top10_qty,
    "NumInvoices": top10_qty_invoices
}))
