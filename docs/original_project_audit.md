# Original Project Baseline Audit Report

**Project Audited:** E-Commerce Sales & Profit Analyst (`E-Commerce-Sales-Profit-Analyst-main`)  
**Reference Repository:** [Dheeraj-Official/E-Commerce-Sales-Profit-Analyst](https://github.com/Dheeraj-Official/E-Commerce-Sales-Profit-Analyst)  
**Audit Date:** October 2026  
**Auditor / Analytics Engineer:** Senior Data Analyst & BI Developer  

---

## 1. Executive Summary

This audit evaluates the baseline open-source project `E-Commerce Sales & Profit Analyst` prior to executing a non-destructive refactoring and elevation into the production-grade portfolio project **Retail Business Intelligence & Customer Analytics** (`retail-business-intelligence`).

The reference project provides an analytical baseline over the classic United States Superstore retail dataset (2014–2017). It includes raw and processed CSV datasets, an exploratory Jupyter Notebook, a SQL Server data loading script, an extensive collection of T-SQL queries (104+ files), a Power BI desktop model (`.pbix`), and dashboard screenshots.

---

## 2. Complete File Inventory

```
E-Commerce-Sales-Profit-Analyst-main/
│
├── .gitignore
├── README.md                                  (6,846 bytes)
├── requirements.txt                           (60 bytes)
│
├── data/
│   ├── dictionary/
│   │   └── data_dictionary.csv                (3,289 bytes)
│   ├── raw/
│   │   └── ecommerce_raw.csv                  (2,277,811 bytes, 9,994 rows)
│   └── processed/
│       └── ecommerce_clean.csv                (2,909,128 bytes, 9,994 rows, 32 cols)
│
├── notebooks/
│   ├── ecommerce_analysis.ipynb              (1,173,560 bytes, 82 cells)
│   └── import_data_mssql.ipynb                (103,042 bytes, SQL Server loader)
│
├── power BI/
│   ├── PowerBI.pbix                           (1,862,313 bytes)
│   └── Icon Images/                           (13 SVG/PNG visual assets)
│
├── screenshots/
│   ├── PowerBI_Screenshots/                   (5 dashboard page captures)
│   └── Notebook_Screenshots/                  (13 notebook chart captures)
│
└── sql/
    ├── 01_Database_and_Table_setup/           (3 SQL scripts: DB, Tables, Views)
    ├── 02_Data_cleaning_sql/                  (8 SQL scripts: Quality checks, Outliers)
    ├── 03_KPI_Analysis/                       (9 SQL scripts: Core KPIs & breakdowns)
    ├── 04_Customer_Analysis/                  (15 SQL scripts: Top customers, RFM, cohorts)
    ├── 05_Product_Analysis/                   (17 SQL scripts: Category, sub-category, matrix)
    ├── 06_Time_Series_Analysis/               (15 SQL scripts: Trends, MoM, YoY, rolling)
    ├── 07_Advanced_Business_Question/         (30 individual SQL questions + SUMMARY script)
    ├── 08_ETL_Star_Schema/                    (6 SQL ETL dimension/fact population scripts)
    └── ER_Diagram.png                         (Dimensional Model Diagram)
```

---

## 3. Dataset Profile & Dimensions

### A. Core Dataset Identifiers
- **Dataset Name:** Sample Superstore Transactional Dataset
- **Domain:** Retail & E-Commerce Omnichannel (Office Supplies, Furniture, Technology)
- **Granularity (Grain):** 1 row per product item per order line

### B. Dataset Dimensions & Schema
| Metric | Raw Dataset (`ecommerce_raw.csv`) | Processed Dataset (`ecommerce_clean.csv`) |
| :--- | :--- | :--- |
| **Row Count** | 9,994 rows | 9,994 rows |
| **Column Count** | 21 columns | 32 columns |
| **Encoding** | Windows-1252 / ISO-8859-1 (0xa0 non-breaking spaces present) | UTF-8 |
| **Unique Orders** | 5,009 | 5,009 |
| **Unique Customers** | 793 | 793 |
| **Unique Products** | 1,862 | 1,862 |
| **Unique Postal Codes** | 631 (in 531 Cities, 49 States, 4 Regions) | 631 |

### C. Column Definitions & Raw Data Types
| Column Name | Raw Data Type | Target Logical Type | Description |
| :--- | :--- | :--- | :--- |
| `Row ID` | `int64` | Integer | Primary key surrogate identifier for the record |
| `Order ID` | `object` (string) | String | Business order identifier (e.g., CA-2016-152156) |
| `Order Date` | `object` (string) | Date | Date order placed (`YYYY-MM-DD` or `MM/DD/YYYY`) |
| `Ship Date` | `object` (string) | Date | Date order shipped |
| `Ship Mode` | `object` (string) | Categorical | Standard Class, Second Class, First Class, Same Day |
| `Customer ID` | `object` (string) | String | Unique customer identifier (e.g., CG-12520) |
| `Customer Name` | `object` (string) | String | Full name of purchasing customer |
| `Segment` | `object` (string) | Categorical | Consumer (5,191), Corporate (3,020), Home Office (1,783) |
| `Country` | `object` (string) | Categorical | United States (100%) |
| `City` | `object` (string) | Categorical | 531 distinct US cities |
| `State` | `object` (string) | Categorical | 49 distinct US states |
| `Postal Code` | `int64` | String / Postal | US 5-digit ZIP code (Burlington VT lacks ZIP in raw Superstore variants) |
| `Region` | `object` (string) | Categorical | West (3,203), East (2,848), Central (2,323), South (1,620) |
| `Product ID` | `object` (string) | String | Unique product catalog ID |
| `Category` | `object` (string) | Categorical | Technology, Furniture, Office Supplies |
| `Sub-Category` | `object` (string) | Categorical | 17 Sub-categories (e.g. Binders, Paper, Phones, Chairs) |
| `Product Name` | `object` (string) | String | Full descriptive product title |
| `Sales` | `float64` | Decimal (Currency) | Gross revenue after line item discount |
| `Quantity` | `int64` | Integer | Units ordered (range 1 to 14) |
| `Discount` | `float64` | Decimal (Ratio) | Promotional discount percentage applied (0.00 to 0.80) |
| `Profit` | `float64` | Decimal (Currency) | Net financial margin on line item (can be negative) |

---

## 4. Data Quality & Distribution Findings

### A. Quality Assessment Results
1. **Missing Values:** `0` missing values across all 21 raw columns.
2. **Duplicate Rows:** `0` exact row duplicates.
3. **Date Range:** `2014-01-03` to `2017-12-30` (4 complete calendar years).
4. **Encoding Constraint:** The raw CSV contains byte `0xa0` (non-breaking space) which throws standard `utf-8` decoding errors in Python unless specified with `encoding='windows-1252'` or `encoding_errors='replace'`.

### B. Statistical Summary of Core Financials
| Metric | Sales ($) | Quantity | Discount (%) | Profit ($) |
| :--- | :--- | :--- | :--- | :--- |
| **Mean** | $229.86 | 3.79 | 15.62% | $28.66 |
| **Std Dev** | $623.25 | 2.23 | 20.65% | $234.26 |
| **Min** | $0.44 | 1.00 | 0.00% | -$6,599.98 |
| **25th Percentile** | $17.28 | 2.00 | 0.00% | $1.73 |
| **Median (50%)** | $54.49 | 3.00 | 20.00% | $8.67 |
| **75th Percentile** | $209.94 | 5.00 | 20.00% | $29.36 |
| **Max** | $22,638.48 | 14.00 | 80.00% | $8,399.98 |
| **Total Sum** | **$2,297,200.86** | **37,873 units** | **15.62% avg** | **$286,397.02** |

### C. Core Baseline KPIs
- **Total Revenue:** $2,297,200.86
- **Total Profit:** $286,397.02
- **Net Profit Margin:** 12.47%
- **Total Orders:** 5,009
- **Average Order Value (AOV):** $458.61 ($2,297,200.86 / 5,009 orders)
- **Total Line Items:** 9,994
- **Profitable Transactions:** 8,123 (81.28% of rows, contributing +$442,528.31)
- **Loss-Making Transactions:** 1,871 (18.72% of rows, eroding -$156,131.29)

---

## 5. Architectural & Technical Audit

### A. SQL Layer
- **Dialect:** Microsoft SQL Server (T-SQL).
- **Structure:** 8 numbered directories containing over 104 separate `.sql` files.
- **Star Schema Implementation:** Defines `dim_customer`, `dim_product`, `dim_date`, `dim_location`, and `fact_sales`.
- **Query Patterns:** Extensive use of `SUM`, `AVG`, `COUNT`, `GROUP BY`, `HAVING`, CTEs (`WITH ...`), and Window Functions (`RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`, `LAG()`, `SUM() OVER(ORDER BY ...)`).

### B. Python Analytics Layer
- **Architecture:** Monolithic Jupyter notebook `ecommerce_analysis.ipynb` (82 cells) combining data loading, cleaning, basic statistics, and Plotly charts.
- **ETL Notebook:** `import_data_mssql.ipynb` connecting to local MSSQL via `pyodbc` / `sqlalchemy`.
- **Modularity:** None. No reusable `.py` scripts, modules, or package definitions.

### C. Power BI Layer
- **File:** `power BI/PowerBI.pbix` (1.86 MB).
- **Visuals:** 5 main views (Dashboard Overview, Sales, Profit, Customer, Region).
- **Assets:** Custom SVG icon assets for KPI cards.

---

## 6. Identified Strengths & Weaknesses

### Strengths of Reference Project
1. **Rich Query Surface:** A broad spectrum of business questions is addressed in SQL.
2. **Solid Dimensional Foundation:** Star Schema tables are well conceived.
3. **Discount Sensitivity:** Strong focus on identifying how deep discounts (>20%) destroy profitability.

### Key Weaknesses & Technical Gaps
1. **Extreme SQL Fragmentation:** 104+ tiny files (often 4–10 lines each) create high cognitive friction and maintenance overhead.
2. **Lack of Python Modularity:** No standalone Python library or reusable scripts; all logic is locked inside an untestable `.ipynb`.
3. **Absence of Testing:** Zero automated data quality unit tests (no `pytest` suite).
4. **Encoding Fragility:** CSV loader crashes under UTF-8 due to Windows-1252 characters.
5. **Basic RFM Logic:** RFM segmentation used arbitrary manual thresholds rather than quintile-based statistical scoring.
6. **No DAX Measure Catalog:** DAX formulas in Power BI are not documented.
7. **Directory Layout:** Directory names contained spaces (`power BI`), non-standard folder hierarchy.

---

## 7. Safe Transformation Plan (Roadmap)

1. **Modular Python Engine:** Build a clean Python package (`python/`):
   - `data_loader.py` (robust encoding fallback)
   - `data_quality.py` (rule-based validation engine)
   - `data_cleaning.py` (standardized cleaning pipeline)
   - `feature_engineering.py` (derived attributes, discount bands, shipping metrics)
   - `customer_analysis.py` & `rfm_analysis.py` (quintile scoring, churn risk, LTV)
   - `visualization.py` (publication-ready charting functions)
2. **Organized SQL Architecture:** Consolidate SQL into 8 structured scripts covering over 40+ business questions with CTEs, window functions, and analytics.
3. **Multi-Notebook Workflow:** Split analysis into 5 focused notebooks (`01_data_audit`, `02_data_cleaning`, `03_eda`, `04_customer_rfm`, `05_advanced_analytics`).
4. **Data Modeling & DAX Catalog:** Provide formal Star Schema documentation (`docs/architecture.md`, `powerbi/data_model.md`) and a complete DAX measure reference (`powerbi/dax_measures.md`).
5. **Automated Testing Suite:** Build `tests/test_data_quality.py` executable via `pytest`.
6. **Executive Reporting:** Generate comprehensive markdown reports in `reports/` for executive leadership, actionable insights, and recommendations.
7. **Fresh Git Repository:** Initialize a clean, professional Git repository for `mhmd-ebrahim-1/retail-business-intelligence` with meaningful atomic commits.
