# 📖 Data Dictionary & Entity Reference
**Project:** Retail Business Intelligence & Customer Analytics Platform
**Dataset Origin:** Sample Superstore Transactional Dataset (2014 - 2017)
**Grain:** 1 record per order line-item

---

## 1. Raw Dataset Field Specifications

| Column Name | Data Type | Null Count | Unique Count | Business Meaning & Description | Example Value | Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Row ID` | Integer | 0 | 9,994 | Sequential index of transactional rows | `1`, `2` | Strictly Unique & Positive |
| `Order ID` | String | 0 | 5,009 | Unique alpha-numeric order identifier | `CA-2016-152156` | Format: `[Country]-[Year]-[ID]` |
| `Order Date` | Date (String) | 0 | 1,237 | Calendar date when the customer placed the order | `11/8/2016` | Must be $\le$ `Ship Date` |
| `Ship Date` | Date (String) | 0 | 1,334 | Calendar date when goods were dispatched | `11/11/2016` | Must be $\ge$ `Order Date` |
| `Ship Mode` | String | 0 | 4 | Fulfillment shipping tier selected by customer | `Standard Class` | One of 4 predefined modes |
| `Customer ID` | String | 0 | 793 | Unique customer account identifier | `CG-12520` | Format: `[Initials]-[ID]` |
| `Customer Name` | String | 0 | 793 | Full name of individual or enterprise customer | `Claire Gute` | Trimmed string |
| `Segment` | String | 0 | 3 | Strategic market customer tier | `Consumer` | `Consumer`, `Corporate`, `Home Office` |
| `Country` | String | 0 | 1 | Country of sale | `United States` | Fixed domain |
| `City` | String | 0 | 531 | Municipal city of customer location | `Henderson` | String |
| `State` | String | 0 | 49 | US State of shipping destination | `Kentucky` | Valid US state name |
| `Postal Code` | Integer / String | 0 | 631 | 5-digit US ZIP postal code | `42420` | Formatted as 5-digit zero-padded string |
| `Region` | String | 0 | 4 | Macro geographic territory | `South` | `Central`, `East`, `South`, `West` |
| `Product ID` | String | 0 | 1,862 | Unique catalog SKU identifier | `FUR-BO-10001798` | Format: `[Cat]-[SubCat]-[ID]` |
| `Category` | String | 0 | 3 | Broad commercial product division | `Furniture` | `Furniture`, `Office Supplies`, `Technology` |
| `Sub-Category` | String | 0 | 17 | Detailed product classification | `Bookcases` | 17 standard industry subcategories |
| `Product Name` | String | 0 | 1,850 | Full commercial title of the item sold | `Bush Somerset Bookcase` | String |
| `Sales` | Float | 0 | 6,144 | Gross revenue generated after discount | `$261.96` | Float $\ge 0.00$ |
| `Quantity` | Integer | 0 | 14 | Number of individual units purchased | `2` | Integer $\ge 1$ |
| `Discount` | Float | 0 | 12 | Promotional discount rate applied (0.00 to 0.80) | `0.00`, `0.20` | Float within $[0.0, 1.0]$ |
| `Profit` | Float | 0 | 7,545 | Net operating income/loss from line item | `$41.9136` | Can be positive or negative |

---

## 2. Engineered Feature Specifications

| Feature Name | Derived From | Data Type | Business Purpose | Logical Calculation |
| :--- | :--- | :--- | :--- | :--- |
| `order_year` | `order_date` | Integer | Annual YoY aggregation | `YEAR(order_date)` |
| `order_month` | `order_date` | Integer | Monthly seasonality tracking | `MONTH(order_date)` |
| `order_quarter` | `order_date` | String | Quarterly financial reporting | `'Q' + QUARTER(order_date)` |
| `year_month` | `order_date` | String | Time-series trend index | `YYYY-MM` |
| `ship_days` | `ship_date`, `order_date` | Integer | Fulfillment operational lead time | `ship_date - order_date` (days) |
| `shipping_delay_category` | `ship_days` | String | Logistics SLA performance tier | `<1d: Same Day, 1-2d: Fast, 3-5d: Standard, >5d: Delayed` |
| `profit_margin` | `profit`, `sales` | Float | Percentage profitability of line item | `profit / sales` |
| `profit_status` | `profit` | String | Quick loss-leader flagging | `Profit > 0: Profitable, Profit < 0: Loss-Making, =0: Breakeven` |
| `discount_band` | `discount` | String | Discount sensitivity cohorting | `0%: No Discount, 1-10%: Low, 11-20%: Moderate, 21-50%: High, >50%: Deep` |
| `order_value_band` | `sales` | String | Basket size stratification | `<$50: Small, $50-$250: Medium, $250-$1k: Large, >$1k: Enterprise` |

