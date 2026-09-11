"""
Online Retail Assessment - Reproducible Analysis
Dataset: UCI Online Retail
Source: https://archive.ics.uci.edu/dataset/352/online-retail
"""

import pandas as pd
import numpy as np

INPUT_FILE = "Online Retail.xlsx"
OUTPUT_FILE = "Processed_Data.csv"

# 1. Load
df = pd.read_excel(INPUT_FILE)

# 2. Profile
print("Raw shape:", df.shape)
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicates:", df.duplicated().sum())

# 3. Remove exact duplicates
df = df.drop_duplicates().copy()

# 4. Standardize types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# 5. Identify cancellations
df["IsCancellation"] = df["InvoiceNo"].astype(str).str.upper().str.startswith("C")

# 6. Revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# 7. Keep valid positive sales for the main sales analysis
processed = df[
    (~df["IsCancellation"]) &
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0) &
    (df["CustomerID"].notna()) &
    (df["Description"].notna())
].copy()

# 8. Time features
processed["YearMonth"] = processed["InvoiceDate"].dt.to_period("M").astype(str)
processed["Year"] = processed["InvoiceDate"].dt.year
processed["Month"] = processed["InvoiceDate"].dt.month
processed["MonthName"] = processed["InvoiceDate"].dt.strftime("%b")

# 9. Order value
processed["OrderValue"] = processed.groupby("InvoiceNo")["Revenue"].transform("sum")

# 10. Save analysis-ready data
processed.to_csv(OUTPUT_FILE, index=False)

# 11. KPI analysis
total_revenue = processed["Revenue"].sum()
customers = processed["CustomerID"].nunique()
orders = processed["InvoiceNo"].nunique()
aov = processed.groupby("InvoiceNo")["Revenue"].sum().mean()

print("\n--- KPIs ---")
print("Valid sales rows:", len(processed))
print("Revenue:", round(total_revenue, 2))
print("Customers:", customers)
print("Orders:", orders)
print("Average Order Value:", round(aov, 2))

# 12. Country analysis
country = (
    processed.groupby("Country")
    .agg(
        Revenue=("Revenue", "sum"),
        Customers=("CustomerID", "nunique"),
        Orders=("InvoiceNo", "nunique"),
        Units=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)
country["RevenueShare"] = country["Revenue"] / total_revenue

# 13. Product analysis
product = (
    processed.groupby(["StockCode", "Description"])
    .agg(
        Revenue=("Revenue", "sum"),
        Units=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique")
    )
    .sort_values("Revenue", ascending=False)
)

# 14. Customer analysis
customer = (
    processed.groupby("CustomerID")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Units=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

customer["RepeatCustomer"] = customer["Orders"] > 1

repeat_revenue = customer.loc[customer["RepeatCustomer"], "Revenue"].sum()
one_time_revenue = customer.loc[~customer["RepeatCustomer"], "Revenue"].sum()

print("\nRepeat customer revenue share:",
      round(repeat_revenue / total_revenue * 100, 2), "%")

# 15. Monthly trend
monthly = (
    processed.groupby("YearMonth")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Customers=("CustomerID", "nunique")
    )
    .reset_index()
)

monthly["MoM_Growth"] = monthly["Revenue"].pct_change()

print("\nMonthly trend:")
print(monthly)


# Review cancellations/returns separately rather than mixing them into
# positive-sales KPIs.
returns = df[df["Quantity"] < 0].copy()
return_value = -(returns["Quantity"] * returns["UnitPrice"]).sum()
print("\nReturn/cancellation value:", round(return_value, 2))
