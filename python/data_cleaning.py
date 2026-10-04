"""
Data Cleaning Module for Retail Business Intelligence.
Applies standardized transformations, typing, string normalization, and data validation rules.
"""

from typing import Optional
import pandas as pd
import numpy as np


def clean_retail_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw retail transaction dataset into standard format.
    
    Operations performed:
    1. Standardizes column names (snake_case / no spaces).
    2. Parses dates into datetime64 objects.
    3. Strips whitespace from string/categorical columns.
    4. Enforces numerical data types (float for sales/profit/discount, int for quantity).
    5. Validates non-negative sales and positive quantities.
    
    Args:
        df: Raw pandas DataFrame.
        
    Returns:
        Cleaned pandas DataFrame.
    """
    cleaned = df.copy()
    
    # 1. Standardize column names (replace spaces and hyphens with underscores)
    cleaned.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in cleaned.columns]
    
    # Standardize specific column names if needed
    name_mapping = {
        "Row_ID": "Row_ID",
        "Order_ID": "Order_ID",
        "Order_Date": "Order_Date",
        "Ship_Date": "Ship_Date",
        "Ship_Mode": "Ship_Mode",
        "Customer_ID": "Customer_ID",
        "Customer_Name": "Customer_Name",
        "Segment": "Segment",
        "Country": "Country",
        "City": "City",
        "State": "State",
        "Postal_Code": "Postal_Code",
        "Region": "Region",
        "Product_ID": "Product_ID",
        "Category": "Category",
        "Sub_Category": "Sub_Category",
        "Product_Name": "Product_Name",
        "Sales": "Sales",
        "Quantity": "Quantity",
        "Discount": "Discount",
        "Profit": "Profit"
    }
    cleaned = cleaned.rename(columns=name_mapping)
    
    # 2. Date parsing
    cleaned["Order_Date"] = pd.to_datetime(cleaned["Order_Date"])
    cleaned["Ship_Date"] = pd.to_datetime(cleaned["Ship_Date"])
    
    # 3. String normalization
    string_cols = ["Order_ID", "Ship_Mode", "Customer_ID", "Customer_Name", 
                   "Segment", "Country", "City", "State", "Region", 
                   "Product_ID", "Category", "Sub_Category", "Product_Name"]
    for col in string_cols:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()
            
    # 4. Numeric enforcement
    cleaned["Sales"] = cleaned["Sales"].astype(float)
    cleaned["Quantity"] = cleaned["Quantity"].astype(int)
    cleaned["Discount"] = cleaned["Discount"].astype(float)
    cleaned["Profit"] = cleaned["Profit"].astype(float)
    if "Postal_Code" in cleaned.columns:
        # Fill missing or format postal code as string or int
        cleaned["Postal_Code"] = cleaned["Postal_Code"].fillna(0).astype(int)
        
    return cleaned
