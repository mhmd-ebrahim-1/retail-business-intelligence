# 🚀 End-to-End Project Walkthrough & Execution Guide
**Project:** Retail Business Intelligence & Customer Analytics Platform

---

## 1. Prerequisites & Environment Setup
Ensure you have Python 3.9+ and Git installed on your machine.

Clone the repository and install all dependencies:
```bash
git clone https://github.com/mhmd-ebrahim-1/retail-business-intelligence.git
cd retail-business-intelligence
pip install -r requirements.txt
```

---

## 2. Executing the Data Pipeline

### Step 1: Raw Data Audit
To profile the raw dataset and verify baseline statistics:
```bash
python python/data_quality.py
```

### Step 2: Data Cleaning & Normalization
To execute standardizations, date parsing, and validation rules:
```bash
python python/data_cleaning.py
```
*Output: `data/cleaned/superstore_cleaned.csv`*

### Step 3: Feature Engineering & Star Schema Dimensional Modeling
To compute business features and export the 6 dimensional tables:
```bash
python python/feature_engineering.py
```
*Outputs: `data/processed/fact_sales.csv`, `dim_date.csv`, `dim_customer.csv`, `dim_product.csv`, `dim_geography.csv`, `dim_ship_mode.csv`*

### Step 4: RFM Customer Segmentation
To run quantile-based RFM scoring and assign customer segments:
```bash
python python/rfm_analysis.py
```
*Outputs: `data/processed/rfm_customer_segments.csv`, `rfm_segment_summary.csv`*

### Step 5: SQL Warehouse Build & Analytics Verification
To create the SQLite database and execute all 8 SQL analytics scripts:
```bash
python python/build_database.py
```
*Output: `sql/retail_bi.db`*

### Step 6: Generate Excel Analytics Model
To build the multi-sheet formatted Excel workbook:
```bash
python python/create_excel_model.py
```
*Output: `reports/retail_analytics.xlsx`*

### Step 7: Run Automated Unit Tests
To validate data quality and integrity via pytest:
```bash
pytest tests/
```

---

## 3. Power BI Dashboard Reproduction
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Folder** or **Text/CSV**, pointing to `data/processed/`.
3. Load `fact_sales.csv`, `dim_date.csv`, `dim_customer.csv`, `dim_product.csv`, `dim_geography.csv`, and `dim_ship_mode.csv`.
4. In the **Model View**, establish the 1-to-many relationships documented in [`powerbi/data_model.md`](../powerbi/data_model.md).
5. Create a new measure table `_Measures` and paste the DAX formulas from [`powerbi/dax_measures.md`](../powerbi/dax_measures.md).
6. Build the 4 pages following the visual layouts in `powerbi/screenshots/`.

