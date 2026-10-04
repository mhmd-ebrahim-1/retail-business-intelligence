"""
RFM (Recency, Frequency, Monetary) Customer Segmentation Module.
Computes quintile scores and business segment classifications for customer retention and marketing strategy.
"""

from typing import Optional, Dict, Any
import pandas as pd
import numpy as np


def compute_rfm_table(df: pd.DataFrame, reference_date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    """
    Computes raw Recency, Frequency, and Monetary metrics for each unique customer.
    
    Args:
        df: Transaction dataframe containing Customer_ID, Customer_Name, Segment, Order_Date, Order_ID, Sales.
        reference_date: Snapshot date for recency calculation. Defaults to max(Order_Date) + 1 day.
        
    Returns:
        DataFrame with Customer_ID, Customer_Name, Segment, Recency (days), Frequency (orders), Monetary ($).
    """
    order_date_col = "Order_Date" if "Order_Date" in df.columns else "Order Date"
    cust_id_col = "Customer_ID" if "Customer_ID" in df.columns else "Customer ID"
    cust_name_col = "Customer_Name" if "Customer_Name" in df.columns else "Customer Name"
    order_id_col = "Order_ID" if "Order_ID" in df.columns else "Order ID"
    sales_col = "Sales"
    profit_col = "Profit"
    segment_col = "Segment"
    
    dates = pd.to_datetime(df[order_date_col])
    if reference_date is None:
        reference_date = dates.max() + pd.Timedelta(days=1)
        
    rfm = df.groupby([cust_id_col, cust_name_col, segment_col]).agg(
        Recency=(order_date_col, lambda x: (reference_date - pd.to_datetime(x).max()).days),
        Frequency=(order_id_col, "nunique"),
        Monetary=(sales_col, "sum"),
        Total_Profit=(profit_col, "sum")
    ).reset_index()
    
    return rfm


def score_rfm(rfm_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns quintile scores (1 to 5) to Recency, Frequency, and Monetary values.
    
    Scoring:
    - Recency: Lower days = Higher Score (5 = most recent, 1 = least recent)
    - Frequency: Higher orders = Higher Score (5 = most frequent, 1 = least frequent)
    - Monetary: Higher revenue = Higher Score (5 = highest spend, 1 = lowest spend)
    """
    scored = rfm_df.copy()
    
    # Recency quintiles (inverted: lowest days gets 5)
    scored["R_Score"] = pd.qcut(scored["Recency"], q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    
    # Frequency: Use rank-based qcut to handle non-unique bin edges
    scored["F_Score"] = pd.qcut(scored["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Monetary quintiles
    scored["M_Score"] = pd.qcut(scored["Monetary"], q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Composite RFM Score
    scored["RFM_Score"] = scored["R_Score"].astype(str) + scored["F_Score"].astype(str) + scored["M_Score"].astype(str)
    scored["RFM_Mean_Score"] = (scored["R_Score"] + scored["F_Score"] + scored["M_Score"]) / 3.0
    
    return scored


def assign_rfm_segment(row: pd.Series) -> str:
    """
    Maps R_Score and F_Score (plus M_Score) to strategic customer segments.
    """
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]
    
    if (r >= 4) and (f >= 4) and (m >= 4):
        return "Champions"
    elif (r >= 3) and (f >= 3) and (m >= 3):
        return "Loyal Customers"
    elif (r >= 4) and (f in [2, 3]):
        return "Potential Loyalists"
    elif (r >= 4) and (f == 1):
        return "New Customers"
    elif (r == 3) and (f in [1, 2]):
        return "Promising"
    elif (r in [2, 3]) and (f in [2, 3]):
        return "Need Attention"
    elif (r in [2, 3]) and (f == 1):
        return "About to Sleep"
    elif (r <= 2) and (f >= 4) and (m >= 4):
        return "Cannot Lose Them"
    elif (r <= 2) and (f >= 3):
        return "At Risk"
    elif (r <= 2) and (f in [1, 2]):
        return "Hibernating"
    else:
        return "Lost"


def run_rfm_segmentation(df: pd.DataFrame, reference_date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    """
    Executes end-to-end RFM segmentation pipeline.
    """
    rfm = compute_rfm_table(df, reference_date=reference_date)
    scored = score_rfm(rfm)
    scored["Segment_Label"] = scored.apply(assign_rfm_segment, axis=1)
    return scored


def summarize_rfm_segments(rfm_segmented_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates metrics by RFM segment to inform marketing and retention strategy.
    """
    summary = rfm_segmented_df.groupby("Segment_Label").agg(
        Customer_Count=("Customer_ID", "count"),
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Total_Revenue=("Monetary", "sum"),
        Avg_Revenue=("Monetary", "mean"),
        Total_Profit=("Total_Profit", "sum")
    ).reset_index()
    
    total_revenue = summary["Total_Revenue"].sum()
    total_customers = summary["Customer_Count"].sum()
    
    summary["Customer_Share_Pct"] = (summary["Customer_Count"] / total_customers) * 100
    summary["Revenue_Share_Pct"] = (summary["Total_Revenue"] / total_revenue) * 100
    summary["Profit_Margin"] = summary["Total_Profit"] / summary["Total_Revenue"]
    
    return summary.sort_values(by="Total_Revenue", ascending=False)
