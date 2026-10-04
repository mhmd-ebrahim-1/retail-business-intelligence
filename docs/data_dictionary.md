# Enterprise Data Dictionary

This document defines all schema attributes, raw transactional columns, and derived analytical features in the **Retail Business Intelligence & Customer Analytics** repository.

---

## 1. Raw Transactional Attributes

| Column Name | Data Type | Nullable | Example Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| `Row_ID` | `INT` | No | `1` | Unique surrogate key identifying the order line record |
| `Order_ID` | `VARCHAR(50)` | No | `CA-2016-152156` | Unique natural business order transaction number |
| `Order_Date` | `DATE` | No | `2016-11-08` | Date when the order was placed |
| `Ship_Date` | `DATE` | No | `2016-11-11` | Date when the order was shipped from the fulfillment center |
| `Ship_Mode` | `VARCHAR(50)` | No | `Second Class` | Delivery service level: Standard Class, Second Class, First Class, Same Day |
| `Customer_ID` | `VARCHAR(50)` | No | `CG-12520` | Unique alphanumeric customer account identifier |
| `Customer_Name` | `VARCHAR(100)`| No | `Claire Gute` | Full legal or commercial name of the customer |
| `Segment` | `VARCHAR(50)` | No | `Consumer` | Customer market segment: Consumer, Corporate, Home Office |
| `Country` | `VARCHAR(50)` | No | `United States` | Sovereign country of destination |
| `City` | `VARCHAR(50)` | No | `Henderson` | Municipality or city of destination |
| `State` | `VARCHAR(50)` | No | `Kentucky` | US State or administrative district of destination |
| `Postal_Code` | `INT` | Yes | `42420` | 5-digit US ZIP postal code |
| `Region` | `VARCHAR(50)` | No | `South` | Commercial sales territory: West, East, Central, South |
| `Product_ID` | `VARCHAR(50)` | No | `FUR-BO-10001798`| Unique product catalog SKU identifier |
| `Category` | `VARCHAR(50)` | No | `Furniture` | Top-level product category: Technology, Furniture, Office Supplies |
| `Sub_Category` | `VARCHAR(50)` | No | `Bookcases` | Granular product sub-classification (17 distinct types) |
| `Product_Name` | `VARCHAR(255)`| No | `Bush Somerset...`| Full descriptive product catalog title |
| `Sales` | `DECIMAL(12,4)`| No | `261.9600` | Net billed revenue for the line item |
| `Quantity` | `INT` | No | `2` | Number of physical units purchased |
| `Discount` | `DECIMAL(6,4)` | No | `0.0000` | Promotional discount rate applied (0.00 to 0.80) |
| `Profit` | `DECIMAL(12,4)`| No | `41.9136` | Net dollar contribution margin (can be negative) |

---

## 2. Derived Feature-Engineered Attributes

| Column Name | Data Type | Formula / Logic | Description |
| :--- | :--- | :--- | :--- |
| `Year` | `INT` | `YEAR(Order_Date)` | Calendar year of purchase (2014–2017) |
| `Quarter` | `INT` | `QUARTER(Order_Date)` | Calendar quarter (1 to 4) |
| `Month` | `INT` | `MONTH(Order_Date)` | Month index (1 to 12) |
| `Month_Name` | `VARCHAR(20)` | `FORMAT(Order_Date, 'MMMM')`| Full month title (e.g., November) |
| `Year_Month` | `VARCHAR(7)` | `YYYY-MM` | Standard monthly time series grain |
| `Week` | `INT` | `WEEK(Order_Date)` | ISO calendar week number (1 to 53) |
| `Day_of_Week` | `VARCHAR(20)` | `FORMAT(Order_Date, 'dddd')`| Day of the week (Monday through Sunday) |
| `Order_to_Ship_Days` | `INT` | `Ship_Date - Order_Date` | Operational fulfillment duration in days |
| `Shipping_Delay_Category`| `VARCHAR(50)` | Lead time tiers | Express (0-2d), Standard (3-4d), Delayed (5-6d), Severely Delayed (7+d) |
| `Is_Delayed` | `BOOLEAN` | `Order_to_Ship_Days > 5` | Flag indicating SLA breach |
| `Profit_Margin` | `DECIMAL(8,4)` | `Profit / Sales` | Financial margin efficiency ratio |
| `Sales_per_Quantity` | `DECIMAL(12,4)`| `Sales / Quantity` | Effective unit selling price |
| `Unit_Cost` | `DECIMAL(12,4)`| `(Sales - Profit) / Quantity`| Estimated unit manufacturing/procurement cost |
| `Discount_Band` | `VARCHAR(50)` | Tiered discount levels | No Discount (0%), Low (1-20%), Medium (21-40%), High (>40%) |
| `Is_Discounted` | `BOOLEAN` | `Discount > 0` | Flag indicating discounted purchase |
| `Is_Loss_Making` | `BOOLEAN` | `Profit < 0` | Flag indicating unprofitable line item |
| `High_Value_Order` | `BOOLEAN` | `Sales >= 1000` | Flag indicating large ticket commercial transaction |

---

## 3. Customer-Level Aggregated Metrics

| Metric Name | Data Type | Aggregation Level | Business Definition |
| :--- | :--- | :--- | :--- |
| `Customer_Order_Count` | `INT` | Customer | Total unique orders placed across lifetime |
| `Customer_Total_Sales` | `DECIMAL(12,4)`| Customer | Lifetime gross spend across all orders |
| `Customer_Total_Profit`| `DECIMAL(12,4)`| Customer | Lifetime cumulative net margin contribution |
| `Customer_AOV` | `DECIMAL(12,4)`| Customer | Average spend per order (`Total Sales / Total Orders`) |
| `Customer_Overall_Margin`|`DECIMAL(8,4)`| Customer | Lifetime margin percentage (`Total Profit / Total Sales`) |
| `R_Score`, `F_Score`, `M_Score` | `INT` (1–5) | Customer | Statistical quintile RFM ranks |
| `RFM_Segment` | `VARCHAR(50)` | Customer | Strategic segment (Champions, Loyalists, At Risk, etc.) |
