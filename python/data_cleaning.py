"""
Data Cleaning and Preprocessing Module
Project: Retail Business Intelligence & Customer Analytics Platform

Standardizes schemas, normalizes data types, fixes formatting issues,
and outputs clean, validated data.
"""
from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "superstore_raw.csv"
CLEANED_PATH = BASE_DIR / "data" / "cleaned" / "superstore_cleaned.csv"


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to standard snake_case."""
    mapping = {
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
    return df.rename(columns=mapping)


def clean_superstore_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform full data cleaning and validation pipeline.
    
    Steps:
    1. Standardize column names.
    2. Convert Order Date and Ship Date to datetime.
    3. Strip whitespace from all string fields.
    4. Format Postal Code as 5-digit zero-padded string.
    5. Enforce numeric types and precision on financial metrics.
    6. Validate business rules (e.g. ship_date >= order_date, quantity >= 1).
    """
    df_clean = df.copy()
    
    # 1. Standardize columns
    df_clean = standardize_column_names(df_clean)
    
    # 2. Date parsing
    df_clean["order_date"] = pd.to_datetime(df_clean["order_date"], format="mixed")
    df_clean["ship_date"] = pd.to_datetime(df_clean["ship_date"], format="mixed")
    
    # Validate date integrity
    invalid_dates = df_clean["ship_date"] < df_clean["order_date"]
    if invalid_dates.any():
        raise ValueError(f"Found {invalid_dates.sum()} rows where Ship Date is earlier than Order Date!")
    
    # 3. String cleanup
    string_cols = [
        "order_id", "ship_mode", "customer_id", "customer_name",
        "segment", "country", "city", "state", "region",
        "product_id", "category", "sub_category", "product_name"
    ]
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
    
    # 4. Postal Code normalization (handles leading zeros in US zip codes)
    df_clean["postal_code"] = df_clean["postal_code"].fillna(0).astype(int).astype(str).str.zfill(5)
    # If postal code was 00000 (missing), fill with 'Unknown'
    df_clean["postal_code"] = df_clean["postal_code"].replace("00000", "Unknown")
    
    # 5. Numerical columns validation & rounding
    df_clean["sales"] = df_clean["sales"].astype(float).round(4)
    df_clean["quantity"] = df_clean["quantity"].astype(int)
    df_clean["discount"] = df_clean["discount"].astype(float).round(4)
    df_clean["profit"] = df_clean["profit"].astype(float).round(4)
    
    # Validation checks
    assert (df_clean["sales"] >= 0).all(), "Negative sales values detected!"
    assert (df_clean["quantity"] > 0).all(), "Zero or negative quantities detected!"
    assert ((df_clean["discount"] >= 0.0) & (df_clean["discount"] <= 1.0)).all(), "Invalid discount range detected!"
    
    # Sort for deterministic output
    df_clean = df_clean.sort_values(by=["order_date", "order_id", "row_id"]).reset_index(drop=True)
    
    return df_clean


def run_cleaning_pipeline(raw_path: Path = RAW_PATH, cleaned_path: Path = CLEANED_PATH) -> pd.DataFrame:
    """Execute cleaning and save output."""
    print(f"Loading raw data from: {raw_path}")
    df_raw = pd.read_csv(raw_path, encoding="utf-8")
    
    print("Executing cleaning pipeline...")
    df_clean = clean_superstore_data(df_raw)
    
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(cleaned_path, index=False)
    print(f"Cleaned dataset saved successfully to: {cleaned_path}")
    print(f"Final shape: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")
    return df_clean


if __name__ == "__main__":
    run_cleaning_pipeline()

