# 🏗️ Solution Architecture & Data Pipeline
**Project:** Retail Business Intelligence & Customer Analytics Platform

---

## 1. System Architecture Overview

```
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│   RAW DATA LAYER       │      │   PROCESSING LAYER     │      │   SERVING / BI LAYER   │
│                        │      │                        │      │                        │
│ • superstore_raw.csv   │ ───► │ • Data Cleaning        │ ───► │ • SQLite DB Engine     │
│   (9,994 records)      │      │ • Feature Engineering  │      │ • Star Schema DW       │
│ • Ingestion Validation │      │ • RFM Segmentation     │      │ • Power BI Dashboards  │
│                        │      │ • Star Schema Split    │      │ • Excel Analytics      │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘
```

---

## 2. Dimensional Data Warehouse Architecture (Star Schema)

### Entity-Relationship Diagram (ERD)

```
                            +---------------------------------+
                            |            DIM_DATE             |
                            +---------------------------------+
                            | PK  date_key (INT, YYYYMMDD)    |
                            |     full_date (DATE)            |
                            |     year (INT)                  |
                            |     quarter (VARCHAR)           |
                            |     month (INT)                 |
                            |     month_name (VARCHAR)        |
                            |     day (INT)                   |
                            |     day_name (VARCHAR)          |
                            |     day_of_week (INT)           |
                            |     is_weekend (INT)            |
                            |     year_month (VARCHAR)        |
                            +----------------+----------------+
                                             |
                                             | 1
                                             |
                                             | *
+------------------------------+ 1          +---------------------------------+          1 +-------------------------------+
|         DIM_CUSTOMER         |<-----------|           FACT_SALES            |----------->|          DIM_PRODUCT          |
+------------------------------+ *          +---------------------------------+          * +-------------------------------+
| PK  customer_key (INT)       |            | PK  sale_id (INT)               |            | PK  product_key (INT)         |
|     customer_id (VARCHAR)    |            |     row_id (INT)                |            |     product_id (VARCHAR)      |
|     customer_name (VARCHAR)  |            |     order_id (VARCHAR)          |            |     product_name (VARCHAR)    |
|     segment (VARCHAR)        |            | FK  order_date_key (INT)        |            |     category (VARCHAR)        |
|     first_order_date (DATE)  |            | FK  ship_date_key (INT)         |            |     sub_category (VARCHAR)    |
|     last_order_date (DATE)   |            | FK  customer_key (INT)          |            +-------------------------------+
|     total_orders (INT)       |            | FK  product_key (INT)           |
|     total_spend (NUMERIC)    |            | FK  geography_key (INT)         |
|     total_profit (NUMERIC)   |            | FK  ship_mode_key (INT)         |
+------------------------------+            |     sales (NUMERIC)             |
                                            |     quantity (INT)              |
+------------------------------+ 1          |     discount (NUMERIC)          |          1 +-------------------------------+
|        DIM_GEOGRAPHY         |<-----------|     profit (NUMERIC)            |----------->|         DIM_SHIP_MODE         |
+------------------------------+ *          |     ship_days (INT)             |          * +-------------------------------+
| PK  geography_key (INT)      |            |     profit_margin (NUMERIC)     |            | PK  ship_mode_key (INT)       |
|     country (VARCHAR)        |            |     profit_status (VARCHAR)     |            |     ship_mode (VARCHAR)       |
|     region (VARCHAR)         |            |     discount_band (VARCHAR)     |            +-------------------------------+
|     state (VARCHAR)          |            |     order_value_band (VARCHAR)  |
|     city (VARCHAR)           |            |     shipping_delay_cat (VARCHAR)|
|     postal_code (VARCHAR)    |            +---------------------------------+
+------------------------------+
```

---

## 3. Storage & Technology Stack
- **Languages:** Python 3.13, SQL (ANSI / SQLite / PostgreSQL compatible), DAX (Power BI), M (Power Query)
- **Database Engine:** SQLite 3 (production-grade local embedded analytics warehouse) / PostgreSQL compatible
- **Python Libraries:** Pandas, NumPy, Matplotlib, Seaborn, OpenPyXL, Scipy, Scikit-Learn
- **Reporting & Visualization:** Power BI Desktop, Microsoft Excel, Markdown Executive Summaries
- **Version Control & CI/CD:** Git, GitHub

