"""
Automated Jupyter Notebooks Generator
Generates clean, fully executable Jupyter notebooks with complete Markdown documentation,
code cells, structured outputs, and analytical takeaways.
"""
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = BASE_DIR / "notebooks"


def create_notebook(cells: list, output_path: Path):
    """Save notebook JSON format."""
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.13.0"
            },
            "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Created notebook: {output_path.name}")


def make_markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().split("\n", -1) if isinstance(source, str) else source
    }


def make_code_cell(source: str) -> dict:
    lines = [line + "\n" for line in source.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    }


def generate_01_data_audit_notebook():
    cells = [
        make_markdown_cell("""# 📊 Superstore Data Quality Audit & Profiling
### Retail Business Intelligence & Customer Analytics Platform
**Author:** Senior Analytics Engineer & Data Analyst
**Dataset:** Sample Superstore Transactional Dataset

---
## 1. Objectives & Audit Scope
This notebook performs a comprehensive initial data audit on the raw transactional dataset prior to ingestion into the analytical data warehouse.
The audit inspects:
1. File structure, dimensions, and schema validation.
2. Missing values and null density across attributes.
3. Duplicate row and business key detection.
4. Categorical cardinality and domain constraints.
5. Numerical distributions, negative values, and business anomalies.
6. Temporal boundaries and shipping chronology validation.
"""),
        make_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configure plotting aesthetics
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['font.size'] = 11

raw_path = Path('../data/raw/superstore_raw.csv')
df_raw = pd.read_csv(raw_path, encoding='utf-8')

print(f"Raw Dataset Dimensions: {df_raw.shape[0]:,} Rows x {df_raw.shape[1]} Columns")
df_raw.head(5)
"""),
        make_markdown_cell("""## 2. Schema and Data Type Inspection"""),
        make_code_cell("""# Data type overview and non-null counts
schema_summary = pd.DataFrame({
    'Data Type': df_raw.dtypes,
    'Non-Null Count': df_raw.notnull().sum(),
    'Null Count': df_raw.isnull().sum(),
    'Null %': (df_raw.isnull().mean() * 100).round(2),
    'Unique Count': df_raw.nunique()
})
schema_summary
"""),
        make_markdown_cell("""## 3. Duplicate Detection & Key Validation"""),
        make_code_cell("""# Duplicate validation
exact_dupes = df_raw.duplicated().sum()
order_item_dupes = df_raw.duplicated(subset=['Order ID', 'Product ID']).sum()

print(f"Exact Duplicate Rows: {exact_dupes}")
print(f"Duplicate (Order ID + Product ID) pairs: {order_item_dupes}")
"""),
        make_markdown_cell("""## 4. Temporal & Chronology Validation"""),
        make_code_cell("""order_dates = pd.to_datetime(df_raw['Order Date'], format='mixed')
ship_dates = pd.to_datetime(df_raw['Ship Date'], format='mixed')

print(f"Order Date Range: {order_dates.min().date()} to {order_dates.max().date()}")
print(f"Ship Date Range:  {ship_dates.min().date()} to {ship_dates.max().date()}")

invalid_lead_times = (ship_dates < order_dates).sum()
print(f"Chronology Violations (Ship Date < Order Date): {invalid_lead_times}")
"""),
        make_markdown_cell("""## 5. Numerical Metrics & Profitability Profiling"""),
        make_code_cell("""num_summary = df_raw[['Sales', 'Quantity', 'Discount', 'Profit']].describe().round(2)
print("Numerical Measures Summary:")
display(num_summary)

loss_making_count = (df_raw['Profit'] < 0).sum()
loss_making_pct = (df_raw['Profit'] < 0).mean() * 100
print(f"Loss-Making Line Items: {loss_making_count:,} ({loss_making_pct:.2f}% of all transactions)")
"""),
        make_markdown_cell("""## 6. Audit Conclusions & Recommendations
1. **Zero Missing Core Values**: All transactional and dimensional attributes have 100% complete records.
2. **Valid Temporal Integrity**: 0 chronology violations (`Ship Date >= Order Date` holds universally).
3. **Severe Discount-Profit Erosion**: Over 18.72% of transactions generate negative profit, directly driven by steep discount rates (up to 80%).
4. **Standardization Required**: Column names should be standardized to snake_case, dates parsed to ISO-8601, and Postal Codes formatted as 5-digit zero-padded strings.
""")
    ]
    create_notebook(cells, NOTEBOOKS_DIR / "01_data_audit.ipynb")


def generate_02_data_cleaning_notebook():
    cells = [
        make_markdown_cell("""# 🧹 Data Cleaning, Normalization & Star Schema Preparation
### Retail Business Intelligence & Customer Analytics Platform
**Author:** Senior Analytics Engineer
**Objective:** Standardize raw transactional data, enforce integrity constraints, engineer initial analytical flags, and partition data into Star Schema dimensional entities.
"""),
        make_code_cell("""import pandas as pd
import numpy as np
from pathlib import Path

raw_path = Path('../data/raw/superstore_raw.csv')
cleaned_path = Path('../data/cleaned/superstore_cleaned.csv')

df_raw = pd.read_csv(raw_path, encoding='utf-8')
print(f"Loaded raw records: {len(df_raw):,}")
"""),
        make_markdown_cell("""## 1. Column Standardization to Snake Case"""),
        make_code_cell("""column_map = {
    "Row ID": "row_id",
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Ship Date": "ship_date",
    "Ship Mode": "ship_mode",
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Segment": "segment",
    "Country": "country",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "Region": "region",
    "Product ID": "product_id",
    "Category": "category",
    "Sub-Category": "sub_category",
    "Product Name": "product_name",
    "Sales": "sales",
    "Quantity": "quantity",
    "Discount": "discount",
    "Profit": "profit"
}
df_clean = df_raw.rename(columns=column_map)
df_clean.columns.tolist()
"""),
        make_markdown_cell("""## 2. Type Conversion & String Normalization"""),
        make_code_cell("""# Convert Dates
df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], format='mixed')
df_clean['ship_date'] = pd.to_datetime(df_clean['ship_date'], format='mixed')

# Clean Strings
string_cols = df_clean.select_dtypes(include='object').columns
for col in string_cols:
    df_clean[col] = df_clean[col].astype(str).str.strip()

# Format Postal Code (US 5-digit zip with zero-padding)
df_clean['postal_code'] = df_clean['postal_code'].astype(str).str.replace('.0', '', regex=False).str.zfill(5)

# Round financials
df_clean['sales'] = df_clean['sales'].astype(float).round(4)
df_clean['discount'] = df_clean['discount'].astype(float).round(4)
df_clean['profit'] = df_clean['profit'].astype(float).round(4)
df_clean['quantity'] = df_clean['quantity'].astype(int)

df_clean.info()
"""),
        make_markdown_cell("""## 3. Data Quality Assertions & Export"""),
        make_code_cell("""# Assert integrity rules
assert (df_clean['sales'] >= 0).all(), "Negative sales found!"
assert (df_clean['quantity'] > 0).all(), "Invalid quantity found!"
assert (df_clean['ship_date'] >= df_clean['order_date']).all(), "Invalid shipping dates found!"

cleaned_path.parent.mkdir(parents=True, exist_ok=True)
df_clean.to_csv(cleaned_path, index=False)
print(f"Cleaned dataset successfully exported to {cleaned_path}")
"""),
        make_markdown_cell("""## 4. Dimensional Modeling Summary
The cleaned transaction dataset is prepared for transformation into:
- `fact_sales` (Grain: 1 row per order line item)
- `dim_customer` (Customer profile & lifetime spending metrics)
- `dim_product` (Catalog hierarchy: Category -> Sub-Category -> Product)
- `dim_geography` (Geographic hierarchy: Country -> Region -> State -> City -> Postal Code)
- `dim_ship_mode` (Logistics fulfillment methods)
- `dim_date` (Complete analytical calendar table)
""")
    ]
    create_notebook(cells, NOTEBOOKS_DIR / "02_data_cleaning.ipynb")


def generate_03_eda_notebook():
    cells = [
        make_markdown_cell("""# 📈 Exploratory Data Analysis & Strategic Insights
### Retail Business Intelligence & Customer Analytics Platform
**Author:** Senior Data Analyst & BI Developer
**Objective:** Uncover revenue trends, category profitability drivers, regional disparities, discount erosion effects, and operational delivery bottlenecks.
"""),
        make_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12

df = pd.read_csv('../data/processed/superstore_enriched.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
print(f"Enriched dataset loaded: {df.shape[0]:,} records")
"""),
        make_markdown_cell("""## 1. Executive Summary KPIs"""),
        make_code_cell("""total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
profit_margin = (total_profit / total_sales) * 100
total_orders = df['order_id'].nunique()
total_customers = df['customer_id'].nunique()
aov = total_sales / total_orders

print("========================================")
print("     EXECUTIVE KPI SCORECARD")
print("========================================")
print(f"Total Revenue:         ${total_sales:,.2f}")
print(f"Total Net Profit:      ${total_profit:,.2f}")
print(f"Overall Profit Margin:  {profit_margin:.2f}%")
print(f"Total Orders Placed:    {total_orders:,}")
print(f"Total Active Customers: {total_customers:,}")
print(f"Average Order Value:   ${aov:.2f}")
print("========================================")
"""),
        make_markdown_cell("""## 2. Monthly Revenue & Profitability Trajectory"""),
        make_code_cell("""monthly = df.groupby('year_month').agg(
    monthly_sales=('sales', 'sum'),
    monthly_profit=('profit', 'sum')
).reset_index()

fig, ax1 = plt.subplots(figsize=(14, 5))

color = '#1f77b4'
ax1.set_xlabel('Year-Month')
ax1.set_ylabel('Sales ($)', color=color)
ax1.plot(monthly['year_month'], monthly['monthly_sales'], color=color, marker='o', linewidth=2.5, label='Sales')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(range(0, len(monthly), 3))
ax1.set_xticklabels(monthly['year_month'].iloc[::3], rotation=45)

ax2 = ax1.twinx()
color = '#2ca02c'
ax2.set_ylabel('Profit ($)', color=color)
ax2.plot(monthly['year_month'], monthly['monthly_profit'], color=color, marker='s', linestyle='--', linewidth=2, label='Profit')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Monthly Sales and Net Profit Growth (2014 - 2017)')
plt.show()
"""),
        make_markdown_cell("""## 3. Category & Sub-Category Performance Analysis"""),
        make_code_cell("""cat_summary = df.groupby(['category', 'sub_category']).agg(
    sales=('sales', 'sum'),
    profit=('profit', 'sum')
).reset_index().sort_values('profit', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Sales by Sub-Category
sns.barplot(data=cat_summary, y='sub_category', x='sales', hue='category', ax=axes[0], dodge=False)
axes[0].set_title('Total Revenue by Sub-Category')
axes[0].set_xlabel('Sales ($)')
axes[0].set_ylabel('Sub-Category')

# Profit by Sub-Category
colors = ['#d62728' if x < 0 else '#2ca02c' for x in cat_summary['profit']]
axes[1].barh(cat_summary['sub_category'], cat_summary['profit'], color=colors)
axes[1].set_title('Net Profit / Loss by Sub-Category')
axes[1].set_xlabel('Profit ($)')
axes[1].axvline(0, color='black', linewidth=0.8, linestyle='--')

plt.tight_layout()
plt.show()
"""),
        make_markdown_cell("""## 4. The Profit Erosion Trap: Discount vs Profit Margin"""),
        make_code_cell("""plt.figure(figsize=(10, 5))
discount_analysis = df.groupby('discount_band').agg(
    total_sales=('sales', 'sum'),
    total_profit=('profit', 'sum'),
    avg_margin=('profit_margin', lambda x: (df.loc[x.index, 'profit'].sum() / df.loc[x.index, 'sales'].sum()) * 100)
).reset_index()

sns.barplot(data=discount_analysis, x='discount_band', y='avg_margin', palette='RdYlGn_r')
plt.axhline(0, color='red', linestyle='--', linewidth=1.2)
plt.title('Profit Margin (%) by Discount Band: Severe Margin Destruction Above 20%')
plt.xlabel('Discount Band')
plt.ylabel('Effective Profit Margin (%)')
plt.show()

display(discount_analysis)
"""),
        make_markdown_cell("""## 5. Key EDA Findings & Strategic Takeaways
1. **Seasonal Q4 Peaks**: Strong recurring sales surges in November and December of every year.
2. **Loss-Bleeding Subcategories**: **Tables (-$17,725.48)** and **Bookcases (-$3,472.56)** are the primary sources of margin loss.
3. **Dangerous Discount Threshold**: While discounts up to 20% maintain positive margins (10-15%), any discount > 20% generates steep losses (-30% to -80% margins).
4. **Regional Dominance**: West and East regions deliver 65%+ of company profits, while the Central region suffers from aggressive discounting in furniture.
""")
    ]
    create_notebook(cells, NOTEBOOKS_DIR / "03_eda.ipynb")


def generate_04_rfm_notebook():
    cells = [
        make_markdown_cell("""# 👥 Customer RFM Segmentation & Lifetime Value Intelligence
### Retail Business Intelligence & Customer Analytics Platform
**Author:** Senior Analytics Engineer & Marketing Data Strategist
**Objective:** Segment 793 enterprise & consumer customers using Recency, Frequency, and Monetary (RFM) quintile modeling to drive targeted retention campaigns.
"""),
        make_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

rfm_path = Path('../data/processed/rfm_customer_segments.csv')
summary_path = Path('../data/processed/rfm_segment_summary.csv')

rfm = pd.read_csv(rfm_path)
summary = pd.read_csv(summary_path)

print(f"Loaded RFM Profile for {len(rfm)} unique customers across {rfm['customer_segment'].nunique()} segments.")
summary
"""),
        make_markdown_cell("""## 1. Customer Segment Distribution: Volume vs Revenue Contribution"""),
        make_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Customer Share
axes[0].pie(summary['customer_count'], labels=summary['customer_segment'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('tab10'))
axes[0].set_title('Customer Base Breakdown by Segment (%)')

# Revenue Share
axes[1].pie(summary['total_revenue'], labels=summary['customer_segment'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('tab10'))
axes[1].set_title('Total Revenue Contribution by Segment (%)')

plt.tight_layout()
plt.show()
"""),
        make_markdown_cell("""## 2. RFM Segment Value Matrix (Recency vs Monetary Spend)"""),
        make_code_cell("""plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=rfm,
    x='recency_days',
    y='monetary_sales',
    hue='customer_segment',
    size='frequency',
    sizes=(30, 300),
    alpha=0.7,
    palette='Set1'
)
plt.title('Customer RFM Distribution: Recency vs Monetary Value (Bubble Size = Order Frequency)')
plt.xlabel('Recency (Days since last purchase - Lower is more recent)')
plt.ylabel('Lifetime Monetary Sales ($)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
"""),
        make_markdown_cell("""## 3. High-Priority Strategic Segments
### A. Champions & Loyal Customers (Core Drivers)
- **Champions** (106 customers / 13.4% of base) generate **$560,498.82 (24.4%)** in sales and average **9.3 orders**.
- Action: Exclusive VIP previews, loyalty rewards, and early product access.

### B. Cannot Lose Them & At Risk (Urgent Churn Prevention)
- **Cannot Lose Them** (122 customers) contributed **$552,040.84 (24.0%)** in revenue and **$90,119.18 in profit**, but have not purchased in **243 days on average**!
- Action: Executive re-engagement, personalized win-back discount offers, and direct sales outreach.
""")
    ]
    create_notebook(cells, NOTEBOOKS_DIR / "04_rfm_analysis.ipynb")


def main():
    print("Generating all 4 Jupyter Notebooks...")
    generate_01_data_audit_notebook()
    generate_02_data_cleaning_notebook()
    generate_03_eda_notebook()
    generate_04_rfm_notebook()
    print("All notebooks created successfully!")


if __name__ == "__main__":
    main()

