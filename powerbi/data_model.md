# 🏛️ Power BI Dimensional Data Model Specification
**Project:** Retail Business Intelligence & Customer Analytics Platform

---

## 1. Dimensional Model Overview
The Power BI semantic model is architected as a pure **Star Schema** with 1 Fact Table and 5 Conformed Dimension Tables, ensuring optimal VertiPaq engine compression, rapid query performance, and unambiguous filter propagation.

---

## 2. Table Definitions & Schemas

### A. Fact Table: `fact_sales`
- **Source File:** `data/processed/fact_sales.csv`
- **Granularity:** 1 row per individual order line item (9,994 rows)

| Column Name | Data Type | Role | Description |
| :--- | :--- | :--- | :--- |
| `sale_id` | Integer | Primary Key | Unique surrogate transaction identifier |
| `row_id` | Integer | Attribute | Original row identifier |
| `order_id` | Text | Degenerate Dim | Order tracking code |
| `order_date_key` | Integer | Foreign Key | Maps to `dim_date[date_key]` |
| `ship_date_key` | Integer | Foreign Key | Maps to `dim_date[date_key]` (inactive relationship for lead time) |
| `customer_key` | Integer | Foreign Key | Maps to `dim_customer[customer_key]` |
| `product_key` | Integer | Foreign Key | Maps to `dim_product[product_key]` |
| `geography_key` | Integer | Foreign Key | Maps to `dim_geography[geography_key]` |
| `ship_mode_key` | Integer | Foreign Key | Maps to `dim_ship_mode[ship_mode_key]` |
| `sales` | Decimal Number (Currency) | Measure | Revenue generated after line-item discount |
| `quantity` | Whole Number | Measure | Units purchased |
| `discount` | Decimal Number (Percentage) | Measure | Discount rate applied (0.00 to 0.80) |
| `profit` | Decimal Number (Currency) | Measure | Net profit or loss for transaction |
| `ship_days` | Whole Number | Measure | Elapsed days between order date and ship date |
| `profit_margin` | Decimal Number (Percentage) | Measure | Calculated margin (`profit / sales`) |
| `profit_status` | Text | Attribute | "Profitable", "Loss-Making", "Breakeven" |
| `discount_band` | Text | Attribute | Discount classification bucket |
| `order_value_band` | Text | Attribute | Transaction size bucket |
| `shipping_delay_category` | Text | Attribute | Shipping speed classification |

---

### B. Dimension Table: `dim_date`
- **Source File:** `data/processed/dim_date.csv`
- **Role:** Master calendar table (1,464 daily records from 2014-01-01 to 2018-01-05)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `date_key` | Whole Number | Surrogate key (YYYYMMDD) - Primary Key |
| `full_date` | Date | Standard calendar date |
| `year` | Whole Number | Calendar Year (2014, 2015, 2016, 2017) |
| `quarter` | Text | Quarter label ('Q1', 'Q2', 'Q3', 'Q4') |
| `month` | Whole Number | Month number (1 to 12) |
| `month_name` | Text | Full month name ('January', etc.) - Sorted by `month` |
| `day` | Whole Number | Day of month |
| `day_name` | Text | Day name ('Monday', etc.) |
| `day_of_week` | Whole Number | 1 (Monday) to 7 (Sunday) |
| `is_weekend` | Whole Number | 1 if Saturday/Sunday, else 0 |
| `year_month` | Text | Sortable year-month string ('2016-11') |

---

### C. Dimension Table: `dim_customer`
- **Source File:** `data/processed/dim_customer.csv` (793 distinct customers)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `customer_key` | Whole Number | Surrogate Primary Key |
| `customer_id` | Text | Business Key (e.g., 'CG-12520') |
| `customer_name` | Text | Full Customer Name |
| `segment` | Text | Market segment ('Consumer', 'Corporate', 'Home Office') |
| `first_order_date` | Date | Customer acquisition date |
| `last_order_date` | Date | Most recent order date |
| `total_orders` | Whole Number | Lifetime order count |
| `total_spend` | Decimal Number | Lifetime cumulative revenue |
| `total_profit` | Decimal Number | Lifetime cumulative profit |

---

### D. Dimension Table: `dim_product`
- **Source File:** `data/processed/dim_product.csv` (1,894 product entities)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `product_key` | Whole Number | Surrogate Primary Key |
| `product_id` | Text | Catalog SKU identifier |
| `product_name` | Text | Full descriptive product name |
| `category` | Text | High-level category ('Furniture', 'Office Supplies', 'Technology') |
| `sub_category` | Text | Sub-category ('Chairs', 'Phones', 'Binders', etc.) |

---

### E. Dimension Table: `dim_geography`
- **Source File:** `data/processed/dim_geography.csv` (632 unique geographic locations)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `geography_key` | Whole Number | Surrogate Primary Key |
| `country` | Text | Country ('United States') |
| `region` | Text | Sales Region ('Central', 'East', 'South', 'West') |
| `state` | Text | US State name |
| `city` | Text | City name |
| `postal_code` | Text | 5-digit US ZIP Code |

---

### F. Dimension Table: `dim_ship_mode`
- **Source File:** `data/processed/dim_ship_mode.csv` (4 fulfillment tiers)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `ship_mode_key` | Whole Number | Surrogate Primary Key |
| `ship_mode` | Text | 'Standard Class', 'Second Class', 'First Class', 'Same Day' |

---

## 3. Relationships & Cardinality Configuration

| From Table (Many Side: *) | Foreign Key | To Table (One Side: 1) | Primary Key | Cardinality | Cross Filter | State |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `fact_sales` | `order_date_key` | `dim_date` | `date_key` | Many to One (*:1) | Single (`dim_date` filters `fact_sales`) | Active |
| `fact_sales` | `ship_date_key` | `dim_date` | `date_key` | Many to One (*:1) | Single | Inactive |
| `fact_sales` | `customer_key` | `dim_customer` | `customer_key` | Many to One (*:1) | Single (`dim_customer` filters `fact_sales`) | Active |
| `fact_sales` | `product_key` | `dim_product` | `product_key` | Many to One (*:1) | Single (`dim_product` filters `fact_sales`) | Active |
| `fact_sales` | `geography_key` | `dim_geography` | `geography_key` | Many to One (*:1) | Single (`dim_geography` filters `fact_sales`) | Active |
| `fact_sales` | `ship_mode_key` | `dim_ship_mode` | `ship_mode_key` | Many to One (*:1) | Single (`dim_ship_mode` filters `fact_sales`) | Active |

---

## 4. Best Practices Applied
1. **Star Schema Purity**: No snowflake normalized hierarchies, eliminating expensive multi-hop joins.
2. **Surrogate Keys**: Fast integer join paths instead of wide composite string comparisons.
3. **No Bi-Directional Cross-Filtering**: Prevents ambiguous filter paths and keeps DAX context transitions deterministic.
4. **Dates Table Marked as Official Date Table**: Enables built-in Time Intelligence functions (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`).

