# Project Walkthrough & Developer Execution Guide

This guide walks you through executing the entire **Retail Business Intelligence & Customer Analytics** repository from scratch.

---

## 1. Environment Setup

### A. Clone and Navigate to Repository
```bash
git clone https://github.com/mhmd-ebrahim-1/retail-business-intelligence.git
cd retail-business-intelligence
```

### B. Create and Activate Virtual Environment
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### C. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 2. Running Automated Tests

Validate data quality rules, schema integrity, and statistical calculations:
```bash
pytest tests/ -v
```

All tests should report `PASSED`.

---

## 3. Running the Python Pipeline

Execute the data pipeline to ingest, clean, feature-engineer, and generate processed data artifacts:
```bash
python -c "
from python.data_loader import load_raw_data, save_processed_data
from python.data_cleaning import clean_retail_data
from python.feature_engineering import engineer_features, add_customer_metrics

raw = load_raw_data()
clean = clean_retail_data(raw)
enriched = engineer_features(clean)
final = add_customer_metrics(enriched)

save_processed_data(clean, 'data/cleaned/ecommerce_cleaned.csv')
save_processed_data(final, 'data/processed/ecommerce_processed.csv')
print('Data pipeline completed successfully.')
"
```

---

## 4. Running Jupyter Notebooks

Launch Jupyter Notebook or JupyterLab:
```bash
jupyter lab
```

Execute the notebooks in order:
1. `notebooks/01_data_audit.ipynb`: Schema validation and null checks.
2. `notebooks/02_data_cleaning.ipynb`: Pipeline transformation and feature engineering.
3. `notebooks/03_eda.ipynb`: Exploratory data analysis and financial visualizations.
4. `notebooks/04_customer_rfm.ipynb`: RFM customer segmentation and Pareto curve.
5. `notebooks/05_advanced_analytics.ipynb`: Product profitability matrix and logistics SLA analysis.

---

## 5. Executing SQL Analytics

The `sql/` directory contains 8 organized SQL scripts with 40+ business questions:
- `sql/01_schema.sql`: DDL for Star Schema and analytical views.
- `sql/02_data_quality.sql`: Automated data quality checks.
- `sql/03_kpi_analysis.sql`: Executive KPI summaries.
- `sql/04_sales_analysis.sql`: MoM, YoY, and moving average revenue queries.
- `sql/05_customer_analysis.sql`: RFM segmentation and top customer rankings.
- `sql/06_product_analysis.sql`: Product profitability matrix and loss leaders.
- `sql/07_profitability_analysis.sql`: Discount margin erosion and regional breakdowns.
- `sql/08_advanced_analytics.sql`: Cohort retention, CLV, and simulation models.

Run the scripts in SQL Server Management Studio (SSMS), Azure Data Studio, DBeaver, or via Python SQLite/DuckDB.

---

## 6. Power BI Dashboard Exploration

1. Open Power BI Desktop.
2. Navigate to `powerbi/retail_analytics.pbix`.
3. Explore the 5 interactive report pages:
   - **Page 1:** Executive Overview
   - **Page 2:** Sales & Profitability Analysis
   - **Page 3:** Customer Intelligence & RFM
   - **Page 4:** Product & Regional Performance
   - **Page 5:** Operations & Shipping Logistics
4. Refer to `powerbi/dax_measures.md` for complete DAX formulas.
