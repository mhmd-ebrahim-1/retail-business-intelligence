"""
Comprehensive Data Quality and Audit Module
Project: Retail Business Intelligence & Customer Analytics Platform
"""
import pandas as pd
import numpy as np
from pathlib import Path


def run_data_audit(raw_file_path: str) -> dict:
    df = pd.read_csv(raw_file_path, encoding='utf-8')
    
    order_dates = pd.to_datetime(df['Order Date'], format='mixed')
    ship_dates = pd.to_datetime(df['Ship Date'], format='mixed')
    
    audit_results = {
        "file_name": Path(raw_file_path).name,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "data_types": {col: str(df[col].dtype) for col in df.columns},
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_order_product_pairs": int(df.duplicated(subset=['Order ID', 'Product ID']).sum()),
        "order_date_min": order_dates.min().strftime('%Y-%m-%d'),
        "order_date_max": order_dates.max().strftime('%Y-%m-%d'),
        "ship_date_min": ship_dates.min().strftime('%Y-%m-%d'),
        "ship_date_max": ship_dates.max().strftime('%Y-%m-%d'),
        "invalid_ship_dates": int((ship_dates < order_dates).sum()),
        "postal_code_nulls": int(df['Postal Code'].isnull().sum()),
        "unique_orders": int(df['Order ID'].nunique()),
        "unique_customers": int(df['Customer ID'].nunique()),
        "unique_products": int(df['Product ID'].nunique()),
        "unique_categories": int(df['Category'].nunique()),
        "categories": df['Category'].unique().tolist(),
        "unique_subcategories": int(df['Sub-Category'].nunique()),
        "subcategories": df['Sub-Category'].unique().tolist(),
        "unique_regions": int(df['Region'].nunique()),
        "regions": df['Region'].unique().tolist(),
        "unique_states": int(df['State'].nunique()),
        "unique_cities": int(df['City'].nunique()),
        "unique_segments": int(df['Segment'].nunique()),
        "segments": df['Segment'].unique().tolist(),
        "unique_ship_modes": int(df['Ship Mode'].nunique()),
        "ship_modes": df['Ship Mode'].unique().tolist(),
        "negative_sales": int((df['Sales'] < 0).sum()),
        "zero_or_negative_quantity": int((df['Quantity'] <= 0).sum()),
        "negative_profit_count": int((df['Profit'] < 0).sum()),
        "negative_profit_pct": float((df['Profit'] < 0).mean() * 100),
        "discount_min": float(df['Discount'].min()),
        "discount_max": float(df['Discount'].max()),
        "total_sales": float(df['Sales'].sum()),
        "total_profit": float(df['Profit'].sum()),
        "overall_profit_margin": float((df['Profit'].sum() / df['Sales'].sum()) * 100),
        "total_quantity": int(df['Quantity'].sum())
    }
    return audit_results


if __name__ == "__main__":
    raw_path = r"D:\Downloads\retail-business-intelligence\data\raw\superstore_raw.csv"
    res = run_data_audit(raw_path)
    print("=" * 60)
    print("DATA AUDIT REPORT SUMMARY")
    print("=" * 60)
    for k, v in res.items():
        print(f"{k}: {v}")

