# Retail Business Intelligence & Customer Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-ANSI%20%2F%20T--SQL-orange.svg)](https://en.wikipedia.org/wiki/SQL)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: Passed](https://img.shields.io/badge/Tests-8%20Passed-brightgreen.svg)](tests/)

An end-to-end commercial business intelligence, customer lifetime value, and profitability optimization platform built using **Python, SQL, and Microsoft Power BI**.

**Author & Maintainer:** Mohamed Ebrahim ([@mhmd-ebrahim-1](https://github.com/mhmd-ebrahim-1))  
**Repository:** [retail-business-intelligence](https://github.com/mhmd-ebrahim-1/retail-business-intelligence)

---

## 1. Business Problem

Modern multi-channel retailers often experience healthy top-line revenue growth while suffering from hidden margin erosion. In this enterprise dataset:
- Gross sales grew **+51.4%** ($484K to $733K), yet **18.72% of transactions (1,871 orders)** generated net financial losses totaling **-$156,131.29**.
- Deep promotional discounting (>20%) destroyed **$149,075** in operating margin.
- 55 high-value historical accounts holding **$309,642** in past revenue entered dormant churn-risk status.
- Specific product categories (e.g., Furniture Tables and Bookcases) generated structural losses of **-$21,198**.

The objective of this project is to build an institutional-grade analytics suite to diagnose margin leakage, segment customer behavior via statistical RFM modeling, and provide actionable merchandising and pricing strategies.

---

## 2. Project Objectives

1. **Automate Data Quality & Ingestion:** Develop a modular Python ETL pipeline with multi-codec encoding fallback, schema validation, and automated testing.
2. **Kimball Dimensional Modeling:** Architect an analytical Star Schema (`FACT_SALES`, `DIM_CUSTOMER`, `DIM_PRODUCT`, `DIM_GEOGRAPHY`, `DIM_SHIP_MODE`, `DIM_DATE`).
3. **Advanced SQL Analytics:** Design 40+ strategic queries leveraging Common Table Expressions (CTEs), window functions (`RANK`, `LAG`, `NTILE`, rolling sums), and financial simulations.
4. **Behavioral RFM Segmentation:** Segment the customer base into 11 actionable cohorts using statistical quintiles and Pareto 80/20 distribution modeling.
5. **Interactive Power BI Dashboards:** Deliver 5 executive dashboards powered by a catalog of 20+ documented DAX business measures.

---

## 3. Dataset Profile

- **Source:** US Superstore Omnichannel Transaction Ledger (Public Domain).
- **Time Horizon:** 2014-01-03 to 2017-12-30 (4 Full Calendar Years).
- **Scale:** 9,994 transaction line items, 5,009 distinct orders, 793 unique customers, 1,862 catalog SKUs.
- **Geography:** 531 US Cities across 49 States and 4 Operating Regions.

### Core Verified Enterprise Financials
| Metric | Value |
| :--- | :--- |
| **Total Net Revenue** | **$2,297,200.86** |
| **Total Net Profit** | **$286,397.02** |
| **Blended Operating Margin** | **12.47%** |
| **Total Orders** | **5,009** |
| **Average Order Value (AOV)** | **$458.61** |
| **Repeat Customer Rate** | **98.49%** (781 / 793 accounts) |
| **Average Fulfillment Lead Time** | **3.96 Days** |

---

## 4. Technology Stack

- **Data Engineering & Scripting:** Python 3.10+ (`pandas`, `numpy`, `pathlib`, `scipy`)
- **Data Quality & Testing:** `pytest`, `unittest`
- **Visualization:** `matplotlib`, `seaborn`
- **Interactive Workflows:** Jupyter Notebooks (`nbformat`)
- **Database & Data Warehouse:** ANSI SQL, Microsoft SQL Server (T-SQL), SQLite
- **Business Intelligence & Modeling:** Microsoft Power BI Desktop, DAX
- **Version Control:** Git, GitHub

---

## 5. System Architecture & Data Pipeline

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Raw CSV Ledger  │ ───>  │ Data Quality    │ ───>  │ Feature Engine  │
│ (9,994 rows)    │       │ Gate (Pytest)   │       │ Lead Time, RFM  │
└─────────────────┘       └─────────────────┘       └─────────────────┘
                                                             │
┌─────────────────┐       ┌─────────────────┐                ▼
│ Power BI BI     │ <───  │ 40+ SQL Queries │ <───  ┌─────────────────┐
│ 5 Exec Pages    │       │ Star Schema DDL │       │ Star Schema DWH │
│ 20+ Prod DAX    │       │ Views & CTEs    │       │ Fact & 5 Dims   │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

---

## 6. Star Schema Dimensional Model

```
                                  +-------------------+
                                  |     DIM_DATE      |
                                  +-------------------+
                                  | PK: DateKey       |
                                  +---------+---------+
                                            | 1
                                            | * (OrderDateKey, ShipDateKey)
+--------------------+            +---------v---------+            +--------------------+
|    DIM_CUSTOMER    | 1        * |    FACT_SALES     | *        1 |    DIM_PRODUCT     |
+--------------------+------------>-------------------<------------+--------------------+
| PK: CustomerKey    |            | PK: SalesFactID   |            | PK: ProductKey     |
| CustomerID, Segment|            | FK: CustomerKey   |            | ProductID, Category|
+--------------------+            | FK: ProductKey    |            +--------------------+
                                  | FK: LocationKey   |
+--------------------+            | FK: ShipModeKey   |            +--------------------+
|   DIM_GEOGRAPHY    | 1        * | Measures: Sales,  | *        1 |   DIM_SHIP_MODE    |
+--------------------+------------> Profit, Quantity, <------------+--------------------+
| PK: LocationKey    |            | Discount, Days    |            | PK: ShipModeKey    |
+--------------------+            +-------------------+            +--------------------+
```

Detailed technical specifications: [`powerbi/data_model.md`](powerbi/data_model.md) and [`docs/architecture.md`](docs/architecture.md).

---

## 7. Python Modular Package

The repository includes a reusable Python analytics engine in `python/`:
- [`data_loader.py`](python/data_loader.py): Encoding-safe file ingestion with path resolution.
- [`data_quality.py`](python/data_quality.py): Rule-based automated audit suite (`DataQualityAuditor`).
- [`data_cleaning.py`](python/data_cleaning.py): Column standardization and type casting.
- [`feature_engineering.py`](python/feature_engineering.py): Time decomposition, discount tiers, and SLA metrics.
- [`customer_analysis.py`](python/customer_analysis.py): Pareto concentration curves and customer lifetime aggregations.
- [`rfm_analysis.py`](python/rfm_analysis.py): Statistical quintile RFM segmentation engine.
- [`visualization.py`](python/visualization.py): Standardized visualization routines.

---

## 8. Customer RFM Segmentation Matrix

Customers are scored along **Recency ($R$)**, **Frequency ($F$)**, and **Monetary ($M$)** quintiles (1–5):

| Segment | Customers | Share % | Total Revenue | Revenue % | Blended Margin |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Champions** | 106 | 13.4% | $560,500 | 24.4% | 12.10% |
| **Loyal Customers** | 159 | 20.1% | $572,342 | 24.9% | 10.94% |
| **Cannot Lose Them** | 55 | 6.9% | $309,642 | 13.5% | 18.00% |
| **Hibernating** | 113 | 14.2% | $191,556 | 8.3% | 11.52% |
| **Need Attention** | 86 | 10.8% | $168,206 | 7.3% | 8.53% |
| **Promising** | 57 | 7.2% | $141,751 | 6.2% | 6.95% |
| **Potential Loyalists**| 65 | 8.2% | $121,163 | 5.3% | 11.32% |
| **At Risk** | 51 | 6.4% | $98,376 | 4.3% | 16.68% |
| **New Customers** | 39 | 4.9% | $55,408 | 2.4% | 22.00% |
| **Lost** | 38 | 4.8% | $49,101 | 2.1% | 15.45% |
| **About to Sleep** | 24 | 3.0% | $29,158 | 1.3% | 14.14% |

---

## 9. Power BI Dashboard Layer

The Power BI solution (`powerbi/retail_analytics.pbix`) provides 5 interactive pages:
1. **Executive Overview:** High-level KPI cockpit, YoY revenue trends, and category distribution.
2. **Sales & Profitability Analysis:** Margin erosion dynamics, discount band distribution, and loss waterfall.
3. **Customer Intelligence:** Pareto revenue curve, RFM segment treemap, and CLV leaderboard.
4. **Product & Regional Performance:** 4-quadrant product profitability matrix and state margin map.
5. **Operations & Shipping:** SLA turnaround times, delayed orders, and fulfillment economics.

Complete DAX catalog: [`powerbi/dax_measures.md`](powerbi/dax_measures.md).

---

## 10. Top Business Insights

1. **Discount Destruction:** Discounts >20% triggered **-$149,075 in net operating losses** across $484K in sales volume.
2. **Furniture Drag:** Furniture delivered only **2.49% margin**, dragged down by chronic losses in **Tables (-$17.7K)** and **Bookcases (-$3.5K)**.
3. **Customer Concentration:** The top 20% of customer accounts drive **49.8% ($1.14M)** of enterprise revenue.
4. **Dormant Enterprise Accounts:** 55 high-value accounts representing **$309K in past revenue** are inactive and at risk of churn.
5. **Technology Supremacy:** Technology generates **50.8% ($145.5K)** of all company profits at a 17.40% margin.

Full report: [`reports/business_insights.md`](reports/business_insights.md).

---

## 11. Top Strategic Recommendations

1. **Enforce Discount Guardrails:** Implement a 15% representative limit and hard cap at 20%, recapturing **+$70,000/yr** in profit.
2. **Rationalize Furniture Catalog:** Decommission chronic loss-making table SKUs and introduce bulky freight surcharges.
3. **Targeted Win-Back Campaign:** Deploy Key Account Managers to re-engage the 55 dormant "Cannot Lose Them" accounts.
4. **Central Region Pricing Realignment:** Audit Texas (-$25.7K) and Illinois (-$12.6K) branch discount structures.
5. **Advance Q4 Inventory Staging:** Pre-stage high-velocity Technology inventory prior to peak holiday demand.

Full roadmap: [`reports/recommendations.md`](reports/recommendations.md).

---

## 12. Repository Structure

```
retail-business-intelligence/
├── data/
│   ├── raw/ecommerce_raw.csv                  # Raw dataset (9,994 rows)
│   ├── cleaned/ecommerce_cleaned.csv          # Standardized dataset
│   └── processed/ecommerce_processed.csv      # Feature-engineered dataset
├── notebooks/
│   ├── 01_data_audit.ipynb                    # Schema integrity & null checks
│   ├── 02_data_cleaning.ipynb                 # Pipeline transformations
│   ├── 03_eda.ipynb                           # Financial & category EDA
│   ├── 04_customer_rfm.ipynb                  # RFM segmentation & Pareto curve
│   └── 05_advanced_analytics.ipynb            # Product matrix & operations SLA
├── python/
│   ├── __init__.py                            # Package exposure
│   ├── data_loader.py                         # Ingestion & codec handlers
│   ├── data_quality.py                        # Quality auditor engine
│   ├── data_cleaning.py                       # Normalization rules
│   ├── feature_engineering.py                 # Time, lead, and ratio features
│   ├── customer_analysis.py                   # Customer metrics & Pareto
│   ├── rfm_analysis.py                        # RFM scoring & segmentation
│   └── visualization.py                       # Standard plotting routines
├── sql/
│   ├── 01_schema.sql                          # Star schema & view DDL
│   ├── 02_data_quality.sql                    # Data quality audit queries
│   ├── 03_kpi_analysis.sql                    # Core enterprise KPIs
│   ├── 04_sales_analysis.sql                  # MoM, YoY, moving averages
│   ├── 05_customer_analysis.sql               # Top customers & RFM SQL
│   ├── 06_product_analysis.sql                # Product profitability matrix
│   ├── 07_profitability_analysis.sql          # Discount margin erosion
│   └── 08_advanced_analytics.sql              # Cohort retention & CLV models
├── powerbi/
│   ├── README.md                              # BI report overview
│   ├── data_model.md                          # Star schema specification
│   ├── dax_measures.md                        # DAX formula catalog
│   ├── retail_analytics.pbix                  # Power BI report file
│   └── screenshots/                           # Dashboard visual captures
├── reports/
│   ├── executive_summary.md                   # Leadership briefing
│   ├── business_insights.md                   # Top 10 data-driven insights
│   ├── recommendations.md                     # Prioritized action roadmap
│   └── data_quality_report.md                 # QA scorecard
├── docs/
│   ├── original_project_audit.md              # Baseline inspection report
│   ├── change_log.md                          # Elevation changelog
│   ├── data_dictionary.md                     # Column & feature definitions
│   ├── methodology.md                         # Mathematical & RFM algorithms
│   ├── architecture.md                        # System architecture
│   └── project_walkthrough.md                 # Developer execution guide
├── tests/
│   └── test_data_quality.py                   # Pytest automated test suite
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

---

## 13. Installation & Quickstart

```bash
# 1. Clone repository
git clone https://github.com/mhmd-ebrahim-1/retail-business-intelligence.git
cd retail-business-intelligence

# 2. Set up environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run automated test suite
pytest tests/ -v

# 5. Launch Jupyter Notebooks
jupyter lab
```

---

## 14. Data Source & Attribution

- **Dataset:** US Sample Superstore Dataset (Public Domain).
- **Reference Project:** [Dheeraj-Official/E-Commerce-Sales-Profit-Analyst](https://github.com/Dheeraj-Official/E-Commerce-Sales-Profit-Analyst).
- **Independent Implementation:** Developed a modular Python library, automated Pytest suite, 5 sequential notebooks, organized Star Schema SQL scripts (40+ business questions), RFM quintile statistical engine, and comprehensive documentation suite.

---

## 15. Known Limitations & Future Improvements

- **Cost Granularity:** Cost of goods sold (COGS) is estimated from net profit rather than line item unit manufacturing cost records.
- **Future Enhancements:**
  1. Implement automated machine learning customer churn prediction (e.g., XGBoost / Logistic Regression).
  2. Build real-time dbt (data build tool) transformation models for Snowflake / BigQuery.
  3. Integrate CI/CD GitHub Actions workflow to run data quality tests on commit.
