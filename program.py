# Task 0: Load data & basic info

#In this step, I load the *Online Retail II* dataset from the `Year 2010–2011` sheet.
#I print the shape, first few rows, column types, and summary statistics to understand
#how many rows/columns there are, what each field looks like, and which columns are numeric.
#This helps me see potential issues like missing values, strange data types, or outliers.

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

#  I check for missing values in each column to see where the data is incomplete.
#  I drop rows with missing `Description` because products without names cannot be grouped
#  or analyzed meaningfully.
#  I remove rows where `Quantity` or `Price` are less than or equal to zero, since negative
#  or zero values usually represent returns, errors, or invalid transactions, not real sales.
#  I drop invoices whose ID starts with `"C"`, which indicate cancelled orders, so only
#  completed sales remain.
#  I create a `TotalPrice` column (`Quantity * Price`) to capture the revenue per line item.
#  I remove extreme outliers by keeping only the 1st to 99th percentile of `TotalPrice`.
#  This reduces the impact of unusually large transactions that could distort the analysis.

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

# I convert `InvoiceDate` to a proper datetime type so I can extract months, weekdays, and hours.
# I create `InvoiceMonth` to analyze how revenue changes over time by month.
# I create `InvoiceHour` to see which times of day generate the most revenue.
# I use `day_name()` to create a `Weekday` column so I can compute total revenue per day of week.
# I group by month, weekday, and hour to calculate total revenue for each period.
# I plot three charts (by month, by weekday, and by hour) to visually identify
# the most important time periods for sales and any clear patterns or peaks.

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

#  I group by `Description` to calculate total `TotalPrice` (revenue) and total `Quantity`
#  sold for each product.
#  I also count the number of unique `Invoice` IDs per product to see how many separate
#  orders each product appears in.
#  I identify the **top 10 products by revenue** to see which items generate the most money.
#  I identify the **top 10 products by quantity sold** to see which items are most popular
#  in terms of units.
#  I create horizontal bar charts for both top-10 lists to easily compare products.
#  I combine the top-10 lists with invoice counts to see whether high revenue comes from
#  high prices, high volume, or frequent purchases across many orders.

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

#Task 4: Customer & Country Analysis

# I keep only rows with a valid `Customer ID` so customer-level metrics are accurate.
# I compute total revenue, total quantity, and number of invoices for each customer to
# understand which customers are most valuable and how often they buy.
# I sort customers by revenue and inspect the top 10 to see how concentrated sales are.
# I plot a histogram of customer revenue to see whether a few customers contribute
# most of the revenue (an 80/20 pattern).
# I group by `Country` to compute total revenue per country and then view the top 10 countries.
# I create a bar chart of the top 10 countries by revenue and a separate comparison of
# **United Kingdom vs Rest of World** to see how dominant the UK market is and which
# other regions look promising.

df_customers = df.dropna(subset=["Customer ID"])

# Total revenue by customer
cust_rev = df_customers.groupby("Customer ID")["TotalPrice"].sum()

# Total quantity sold by customer
cust_qty = df_customers.groupby("Customer ID")["Quantity"].sum()

# Total number of invoices by customer
cust_invoices = df_customers.groupby("Customer ID")["Invoice"].nunique()

# Create dataframe with customer-level metrics
cust_stats = pd.DataFrame({
    "Revenue": cust_rev,
    "Quantity": cust_qty,
    "NumInvoices": cust_invoices
}).sort_values("Revenue", ascending=False)

print("\nTop 10 customers by revenue:")
print(cust_stats.head(10))

# Plot distribution of customer revenue
plt.figure()
cust_stats["Revenue"].plot(kind="hist", bins=50)
plt.title("Distribution of Customer Revenue")
plt.xlabel("Revenue (GBP)")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()

#Total revenue by country
country_rev = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False)
print("\nTop 10 countries by revenue:")
print(country_rev.head(10))

# Bar chart top 10 countries
top10_countries = country_rev.head(10)
plt.figure()
top10_countries.plot(kind="bar")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Country")
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Optional UK vs Rest of World
if "United Kingdom" in country_rev.index:
    uk_rev = country_rev["United Kingdom"]
    row_rev = country_rev.drop("United Kingdom").sum()

    plt.figure()
    plt.bar(["UK", "Rest of World"], [uk_rev, row_rev])
    plt.title("Revenue Share: UK vs Rest of World")
    plt.ylabel("Revenue (GBP)")
    plt.tight_layout()
    plt.show()

