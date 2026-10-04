"""
Feature Engineering Module for Retail Business Intelligence.
Generates analytical time attributes, operational shipping metrics, profitability ratios,
discount bands, and customer-level aggregation attributes.
"""

import pandas as pd
import numpy as np


def assign_discount_band(discount: float) -> str:
    """Categorizes discount percentage into business strategy tiers."""
    if discount == 0.0:
        return "No Discount (0%)"
    elif discount <= 0.20:
        return "Low Discount (1-20%)"
    elif discount <= 0.40:
        return "Medium Discount (21-40%)"
    else:
        return "High Discount (>40%)"


def assign_shipping_delay_category(days: int) -> str:
    """Classifies shipping fulfillment lead time."""
    if days <= 2:
        return "Express (0-2 Days)"
    elif days <= 4:
        return "Standard (3-4 Days)"
    elif days <= 6:
        return "Delayed (5-6 Days)"
    else:
        return "Severely Delayed (7+ Days)"


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies comprehensive feature engineering to cleaned transaction dataframe.
    
    Derived Features Added:
    - Time Features: Year, Quarter, Month, Month_Name, Year_Month, Week, Day_of_Week
    - Operational Features: Order_to_Ship_Days, Shipping_Delay_Category, Is_Delayed
    - Financial Ratios: Profit_Margin, Sales_per_Quantity, Unit_Cost
    - Discount Strategies: Discount_Band, Is_Discounted
    - Performance Flags: Is_Loss_Making, High_Value_Order
    
    Args:
        df: Cleaned pandas DataFrame with Order_Date, Ship_Date, Sales, Profit, Quantity, Discount.
        
    Returns:
        Enriched DataFrame with all analytical features.
    """
    enriched = df.copy()
    
    # 1. Date and Time Features
    enriched["Year"] = enriched["Order_Date"].dt.year
    enriched["Quarter"] = enriched["Order_Date"].dt.quarter
    enriched["Month"] = enriched["Order_Date"].dt.month
    enriched["Month_Name"] = enriched["Order_Date"].dt.strftime("%B")
    enriched["Year_Month"] = enriched["Order_Date"].dt.strftime("%Y-%m")
    enriched["Week"] = enriched["Order_Date"].dt.isocalendar().week.astype(int)
    enriched["Day_of_Week"] = enriched["Order_Date"].dt.strftime("%A")
    
    # 2. Shipping & Operational Features
    enriched["Order_to_Ship_Days"] = (enriched["Ship_Date"] - enriched["Order_Date"]).dt.days
    enriched["Shipping_Delay_Category"] = enriched["Order_to_Ship_Days"].apply(assign_shipping_delay_category)
    enriched["Is_Delayed"] = enriched["Order_to_Ship_Days"] > 5
    
    # 3. Financial Ratios
    # Safe profit margin computation (handle zero sales edge case)
    enriched["Profit_Margin"] = np.where(
        enriched["Sales"] > 0,
        (enriched["Profit"] / enriched["Sales"]),
        0.0
    )
    enriched["Sales_per_Quantity"] = enriched["Sales"] / enriched["Quantity"]
    # Estimated unit cost = (Sales - Profit) / Quantity
    enriched["Unit_Cost"] = (enriched["Sales"] - enriched["Profit"]) / enriched["Quantity"]
    
    # 4. Discount Categorization
    enriched["Discount_Band"] = enriched["Discount"].apply(assign_discount_band)
    enriched["Is_Discounted"] = enriched["Discount"] > 0
    
    # 5. Business Segmentation & Risk Flags
    enriched["Is_Loss_Making"] = enriched["Profit"] < 0
    enriched["High_Value_Order"] = enriched["Sales"] >= 1000.0
    
    return enriched


def add_customer_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates customer-level summary metrics and merges them back into transaction dataframe.
    """
    cust_summary = df.groupby("Customer_ID").agg(
        Customer_Order_Count=("Order_ID", "nunique"),
        Customer_Total_Sales=("Sales", "sum"),
        Customer_Total_Profit=("Profit", "sum"),
        Customer_Total_Quantity=("Quantity", "sum")
    ).reset_index()
    
    cust_summary["Customer_AOV"] = cust_summary["Customer_Total_Sales"] / cust_summary["Customer_Order_Count"]
    cust_summary["Customer_Overall_Margin"] = cust_summary["Customer_Total_Profit"] / cust_summary["Customer_Total_Sales"]
    
    return df.merge(cust_summary, on="Customer_ID", how="left")
