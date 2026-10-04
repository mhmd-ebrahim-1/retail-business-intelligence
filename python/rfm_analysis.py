"""
Customer RFM Analysis and Segmentation Module
Project: Retail Business Intelligence & Customer Analytics Platform

Calculates Recency, Frequency, and Monetary (RFM) metrics,
applies quantile-based scoring, assigns actionable customer segments,
and generates summary reporting tables.
"""
from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_PATH = BASE_DIR / "data" / "cleaned" / "superstore_cleaned.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "rfm_customer_segments.csv"
SUMMARY_PATH = BASE_DIR / "data" / "processed" / "rfm_segment_summary.csv"


def calculate_rfm(df: pd.DataFrame, reference_date: pd.Timestamp = None) -> pd.DataFrame:
    """
    Calculate customer-level RFM metrics and scores.
    """
    if reference_date is None:
        reference_date = df["order_date"].max() + pd.Timedelta(days=1)
        
    print(f"RFM Reference Analysis Date: {reference_date.strftime('%Y-%m-%d')}")
    
    # 1. Aggregate customer transaction metrics
    rfm = df.groupby(["customer_id", "customer_name", "segment"]).agg(
        recency_days=("order_date", lambda d: (reference_date - d.max()).days),
        frequency=("order_id", "nunique"),
        monetary_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_items=("quantity", "sum"),
        first_order=("order_date", "min"),
        last_order=("order_date", "max")
    ).reset_index()
    
    rfm["average_order_value"] = (rfm["monetary_sales"] / rfm["frequency"]).round(2)
    rfm["profit_margin_pct"] = ((rfm["total_profit"] / rfm["monetary_sales"]) * 100).round(2)
    
    # 2. Quantile Scoring (1 to 5)
    # Recency: Lower days is better -> 5 = most recent
    rfm["r_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    
    # Frequency: Higher frequency is better -> 5 = highest frequency
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Monetary: Higher spend is better -> 5 = highest spend
    rfm["m_score"] = pd.qcut(rfm["monetary_sales"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Combined scores
    rfm["rfm_cell"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)
    rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]
    
    # 3. Actionable Segment Definition
    def assign_segment(row) -> str:
        r, f, m = row["r_score"], row["f_score"], row["m_score"]
        
        # Champions: Top tier across all dimensions
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        
        # Cannot Lose Them: High historic spend/orders, but dropping off
        if r <= 2 and (f >= 4 or m >= 4):
            return "Cannot Lose Them"
            
        # Loyal Customers: High frequency and consistent activity
        if r >= 3 and f >= 3:
            return "Loyal Customers"
            
        # At Risk: Moderately high value, long recency
        if r <= 2 and f >= 2:
            return "At Risk"
            
        # Potential Loyalists: Recent buyers with decent spend
        if r >= 4 and f >= 2:
            return "Potential Loyalists"
            
        # New Customers: Very recent buyers with low frequency
        if r >= 4 and f == 1:
            return "New Customers"
            
        # Promising: Recent/moderate activity, low/mid spend
        if r >= 3 and f <= 2:
            return "Promising"
            
        # Hibernating: Low recency, low-to-mid engagement
        if r <= 2 and f <= 2 and (r > 1 or f > 1 or m > 1):
            return "Hibernating"
            
        # Lost: Lowest scores across all dimensions
        return "Lost"

    rfm["customer_segment"] = rfm.apply(assign_segment, axis=1)
    
    return rfm


def generate_rfm_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    """Generate segment level summary for executive reporting."""
    summary = rfm.groupby("customer_segment").agg(
        customer_count=("customer_id", "count"),
        total_revenue=("monetary_sales", "sum"),
        total_profit=("total_profit", "sum"),
        avg_recency=("recency_days", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_aov=("average_order_value", "mean"),
        avg_profit_margin=("profit_margin_pct", "mean")
    ).reset_index()
    
    total_cust = len(rfm)
    total_rev = rfm["monetary_sales"].sum()
    total_prof = rfm["total_profit"].sum()
    
    summary["pct_of_customers"] = ((summary["customer_count"] / total_cust) * 100).round(2)
    summary["pct_of_revenue"] = ((summary["total_revenue"] / total_rev) * 100).round(2)
    summary["pct_of_profit"] = ((summary["total_profit"] / total_prof) * 100).round(2)
    
    summary["avg_recency"] = summary["avg_recency"].round(1)
    summary["avg_frequency"] = summary["avg_frequency"].round(1)
    summary["avg_aov"] = summary["avg_aov"].round(2)
    summary["avg_profit_margin"] = summary["avg_profit_margin"].round(2)
    summary["total_revenue"] = summary["total_revenue"].round(2)
    summary["total_profit"] = summary["total_profit"].round(2)
    
    # Sort by total revenue descending
    summary = summary.sort_values(by="total_revenue", ascending=False).reset_index(drop=True)
    return summary


def run_rfm_pipeline():
    print(f"Loading cleaned data from: {CLEANED_PATH}")
    df = pd.read_csv(CLEANED_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    print("Computing RFM Segmentation...")
    rfm_df = calculate_rfm(df)
    
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rfm_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Customer RFM table saved to: {OUTPUT_PATH}")
    
    summary_df = generate_rfm_summary(rfm_df)
    summary_df.to_csv(SUMMARY_PATH, index=False)
    print(f"RFM Summary saved to: {SUMMARY_PATH}")
    
    print("\n--- RFM SEGMENT PERFORMANCE SUMMARY ---")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    run_rfm_pipeline()

