# Technical System Architecture

This document provides a comprehensive architectural overview of the **Retail Business Intelligence & Customer Analytics** enterprise analytics platform.

---

## 1. High-Level System Architecture

```
+-----------------------------------------------------------------------------+
|                              DATA STORAGE LAYER                             |
|  +---------------------------+       +-----------------------------------+  |
|  | data/raw/                 | ----> | data/cleaned/ & data/processed/   |  |
|  | Multi-codec Raw CSV (9.9K)|       | Standardized UTF-8 Datasets       |  |
|  +---------------------------+       +-----------------------------------+  |
+-----------------------------------------------------------------------------+
                                       │
                                       ▼
+-----------------------------------------------------------------------------+
|                          PYTHON ANALYTICS ENGINE                            |
|  +------------------+  +-------------------+  +--------------------------+  |
|  | data_loader.py   |  | data_quality.py   |  | data_cleaning.py         |  |
|  +------------------+  +-------------------+  +--------------------------+  |
|  +------------------+  +-------------------+  +--------------------------+  |
|  | feature_eng.py   |  | rfm_analysis.py   |  | visualization.py         |  |
|  +------------------+  +-------------------+  +--------------------------+  |
+-----------------------------------------------------------------------------+
                                       │
                                       ▼
+-----------------------------------------------------------------------------+
|                        SQL & DIMENSIONAL MODEL LAYER                        |
|  +-----------------------------------------------------------------------+  |
|  | Star Schema: FACT_SALES, DIM_CUSTOMER, DIM_PRODUCT, DIM_DATE,         |  |
|  |             DIM_GEOGRAPHY, DIM_SHIP_MODE                              |  |
|  | 40+ Analytical Queries across 8 Structured Scripts                    |  |
|  +-----------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------+
                                       │
                                       ▼
+-----------------------------------------------------------------------------+
|                         POWER BI PRESENTATION LAYER                         |
|  +-------------------+  +---------------------+  +-----------------------+  |
|  | Executive Cockpit |  | Margin Diagnostics  |  | Customer RFM Matrix   |  |
|  +-------------------+  +---------------------+  +-----------------------+  |
|  | Product Matrix    |  | Fulfillment SLA     |  | 20+ Production DAX    |  |
|  +-------------------+  +---------------------+  +-----------------------+  |
+-----------------------------------------------------------------------------+
```

---

## 2. Technology Stack

| Layer | Technologies / Libraries | Version / Standard | Purpose |
| :--- | :--- | :--- | :--- |
| **Ingestion & Data Processing** | Python, Pandas, NumPy | Python 3.10+ | Robust data parsing, cleaning, and transformation |
| **Statistical Analysis** | SciPy, Pandas Quantiles | Standard | RFM quintiles, Pareto distribution, Z-Score outlier detection |
| **Data Visualization** | Matplotlib, Seaborn | Matplotlib 3.8+ | Publication-quality static visual charts and distributions |
| **Interactive Analytics** | Jupyter Notebooks (nbformat) | Notebook v4 | Step-by-step reproducible analysis workflows |
| **Relational Database** | ANSI SQL / T-SQL / SQLite | SQL-92+ | Star Schema modeling, CTEs, Window Functions |
| **Business Intelligence** | Microsoft Power BI Desktop | Latest | Interactive executive dashboards, DAX modeling |
| **Testing & Quality Control** | Pytest, Unittest | Pytest 8.0+ | Automated unit tests and data quality assertions |
| **Version Control** | Git, GitHub | Git 2.40+ | Version control and collaborative documentation |

---

## 3. Modular Python Architecture

The `python/` package contains 7 specialized, decoupled modules:
1. `data_loader.py`: Handles file resolution, multi-codec fallback (`windows-1252`, `utf-8`), and clean persistence.
2. `data_quality.py`: Evaluates null counts, uniqueness, date sequences, negative values, and range violations.
3. `data_cleaning.py`: Normalizes column names, trims strings, and casts standardized data types.
4. `feature_engineering.py`: Computes calendar attributes, shipping lead times, margin ratios, and discount tiers.
5. `customer_analysis.py`: Computes repeat customer rates, Pareto curve distributions, and top/bottom accounts.
6. `rfm_analysis.py`: Calculates Recency, Frequency, and Monetary scores and maps customers to 11 strategic segments.
7. `visualization.py`: Standardizes chart aesthetics, palettes, and formats for trend charts, categories, and Pareto curves.

---

## 4. Star Schema Architecture

The analytical data warehouse follows Kimball dimensional modeling principles:
- **Central Fact:** `FACT_SALES` at the transaction order line grain.
- **Surrogate Keys:** High-speed integer keys linking 5 clean dimensions.
- **Dimensional Conformance:** All metrics are filterable across customer segments, geographic regions, product categories, and temporal hierarchies.
