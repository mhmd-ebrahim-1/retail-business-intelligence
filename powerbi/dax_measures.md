# Production DAX Measure Catalog

This document provides the complete, production-grade DAX (Data Analysis Expressions) measure repository for the **Retail Business Intelligence & Customer Analytics** solution.

---

## 1. Core Financial & Volume Measures

### `[Total Sales]`
- **Purpose:** Calculates total gross revenue across all filtered transactions.
- **Formula:**
  ```dax
  Total Sales = SUM(fact_sales[sales])
  ```
- **Business Meaning:** Baseline commercial revenue volume in USD ($).

---

### `[Total Profit]`
- **Purpose:** Calculates total net operating margin contribution.
- **Formula:**
  ```dax
  Total Profit = SUM(fact_sales[profit])
  ```
- **Business Meaning:** Net dollar earnings after accounting for standard unit costs and discounts.

---

### `[Profit Margin %]`
- **Purpose:** Computes the blended return on sales (operating margin ratio).
- **Formula:**
  ```dax
  Profit Margin % = 
  DIVIDE(
      [Total Profit],
      [Total Sales],
      0
  )
  ```
- **Business Meaning:** Profitability efficiency percentage (Enterprise baseline = 12.47%).

---

### `[Total Orders]`
- **Purpose:** Counts unique business order transactions.
- **Formula:**
  ```dax
  Total Orders = DISTINCTCOUNT(fact_sales[order_id])
  ```
- **Business Meaning:** Volume of distinct checkout orders placed.

---

### `[Total Unique Customers]`
- **Purpose:** Counts unique active customers within current filter context.
- **Formula:**
  ```dax
  Total Unique Customers = DISTINCTCOUNT(fact_sales[customer_key])
  ```
- **Business Meaning:** Reach and active customer count.

---

### `[Average Order Value (AOV)]`
- **Purpose:** Computes the average monetary value per order.
- **Formula:**
  ```dax
  Average Order Value (AOV) = 
  DIVIDE(
      [Total Sales],
      [Total Orders],
      0
  )
  ```
- **Business Meaning:** Revenue generated per order checkout (Baseline = $458.61).

---

### `[Total Units Sold]`
- **Purpose:** Total physical product units delivered.
- **Formula:**
  ```dax
  Total Units Sold = SUM(fact_sales[quantity])
  ```
- **Business Meaning:** Inventory throughput and shipment volume.

---

### `[Average Discount %]`
- **Purpose:** Average promotional discount applied per transaction.
- **Formula:**
  ```dax
  Average Discount % = AVERAGE(fact_sales[discount])
  ```
- **Business Meaning:** Pricing concession intensity (Baseline = 15.62%).

---

## 2. Time Intelligence & Growth Measures

### `[Sales Prior Year (PY)]`
- **Purpose:** Computes total sales for the equivalent period in the previous calendar year.
- **Formula:**
  ```dax
  Sales Prior Year (PY) = 
  CALCULATE(
      [Total Sales],
      SAMEPERIODLASTYEAR(dim_date[full_date])
  )
  ```
- **Business Meaning:** Benchmark baseline for annual comparative evaluation.

---

### `[YoY Sales Growth $]`
- **Purpose:** Computes absolute dollar difference between current year and prior year sales.
- **Formula:**
  ```dax
  YoY Sales Growth $ = [Total Sales] - [Sales Prior Year (PY)]
  ```
- **Business Meaning:** Net top-line annual expansion or contraction in dollars.

---

### `[YoY Sales Growth %]`
- **Purpose:** Computes percentage expansion rate of sales versus prior year.
- **Formula:**
  ```dax
  YoY Sales Growth % = 
  DIVIDE(
      [YoY Sales Growth $],
      [Sales Prior Year (PY)],
      0
  )
  ```
- **Business Meaning:** Year-over-year revenue growth velocity.

---

### `[Profit Prior Year (PY)]`
- **Purpose:** Computes total profit for the same period in the previous year.
- **Formula:**
  ```dax
  Profit Prior Year (PY) = 
  CALCULATE(
      [Total Profit],
      SAMEPERIODLASTYEAR(dim_date[full_date])
  )
  ```
- **Business Meaning:** Bottom-line baseline for annual comparative evaluation.

---

### `[YoY Profit Growth %]`
- **Purpose:** Percentage expansion or contraction in net margin versus prior year.
- **Formula:**
  ```dax
  YoY Profit Growth % = 
  DIVIDE(
      [Total Profit] - [Profit Prior Year (PY)],
      [Profit Prior Year (PY)],
      0
  )
  ```
- **Business Meaning:** Net margin improvement velocity.

---

### `[Sales YTD]`
- **Purpose:** Calculates cumulative year-to-date sales from January 1st to current date.
- **Formula:**
  ```dax
  Sales YTD = 
  TOTALYTD(
      [Total Sales],
      dim_date[full_date]
  )
  ```
- **Business Meaning:** Cumulative fiscal progress throughout the annual cycle.

---

### `[Sales 3M Moving Average]`
- **Purpose:** Smooths short-term monthly volatility with a rolling 3-month trailing average.
- **Formula:**
  ```dax
  Sales 3M Moving Average = 
  AVERAGEX(
      DATESINPERIOD(
          dim_date[full_date],
          LASTDATE(dim_date[full_date]),
          -3,
          MONTH
      ),
      [Total Sales]
  )
  ```
- **Business Meaning:** Trend indicator removing cyclical noise.

---

## 3. Customer Intelligence & RFM Measures

### `[Repeat Customer Rate %]`
- **Purpose:** Percentage of customers who have placed more than 1 distinct order.
- **Formula:**
  ```dax
  Repeat Customer Rate % = 
  VAR CustomerOrderTable = 
      ADDCOLUMNS(
          VALUES(dim_customer[customer_key]),
          "@OrderCount", CALCULATE(DISTINCTCOUNT(fact_sales[order_id]))
      )
  VAR TotalCust = COUNTROWS(CustomerOrderTable)
  VAR RepeatCust = COUNTROWS(FILTER(CustomerOrderTable, [@OrderCount] > 1))
  RETURN
      DIVIDE(RepeatCust, TotalCust, 0)
  ```
- **Business Meaning:** Measure of customer stickiness and repeat purchase loyalty (98.49%).

---

### `[Revenue at Risk]`
- **Purpose:** Total historical revenue generated by customers currently dormant (>180 days since last purchase).
- **Formula:**
  ```dax
  Revenue at Risk = 
  VAR MaxDate = MAX(dim_date[full_date])
  VAR DormantCustomers = 
      FILTER(
          VALUES(dim_customer[customer_key]),
          VAR LastOrder = CALCULATE(MAX(fact_sales[order_date_key]))
          VAR DaysSince = DATEDIFF(CONVERT(FORMAT(LastOrder, "0000-00-00"), DATETIME), MaxDate, DAY)
          RETURN DaysSince > 180
      )
  RETURN
      CALCULATE([Total Sales], DormantCustomers)
  ```
- **Business Meaning:** Top-line revenue vulnerable to permanent churn without re-engagement.

---

### `[Champions Revenue Share %]`
- **Purpose:** Share of enterprise revenue generated by top-tier "Champion" customers.
- **Formula:**
  ```dax
  Champions Revenue Share % = 
  DIVIDE(
      CALCULATE([Total Sales], dim_customer[Segment] = "Champions"),
      CALCULATE([Total Sales], ALL(dim_customer)),
      0
  )
  ```
- **Business Meaning:** Revenue concentration within highest value customer tier.

---

## 4. Profitability & Operational Risk Measures

### `[Loss-Making Sales Volume]`
- **Purpose:** Revenue generated by transactions sold at a negative profit margin.
- **Formula:**
  ```dax
  Loss-Making Sales Volume = 
  CALCULATE(
      [Total Sales],
      fact_sales[profit] < 0
  )
  ```
- **Business Meaning:** Unproductive revenue that drains bottom-line cash.

---

### `[Total Profit Loss Amount]`
- **Purpose:** Sum of all negative profit amounts across unprofitable orders.
- **Formula:**
  ```dax
  Total Profit Loss Amount = 
  CALCULATE(
      SUM(fact_sales[profit]),
      fact_sales[profit] < 0
  )
  ```
- **Business Meaning:** Total capital eroded by unprofitable transactions (-$156,131.29 baseline).

---

### `[Average Shipping Days]`
- **Purpose:** Average turnaround time from order placement to shipment dispatch.
- **Formula:**
  ```dax
  Average Shipping Days = AVERAGE(fact_sales[order_to_ship_days])
  ```
- **Business Meaning:** Operational fulfillment velocity (Enterprise baseline = 3.96 days).

---

### `[Delayed Order Count]`
- **Purpose:** Count of orders taking longer than 5 days to fulfill.
- **Formula:**
  ```dax
  Delayed Order Count = 
  CALCULATE(
      DISTINCTCOUNT(fact_sales[order_id]),
      fact_sales[order_to_ship_days] > 5
  )
  ```
- **Business Meaning:** Orders failing standard 5-day fulfillment SLA.
