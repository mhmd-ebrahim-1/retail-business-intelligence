"""
Customer Intelligence Module for Retail Business Intelligence.
Calculates customer concentration (Pareto), repeat purchase rate, customer lifetime metrics,
and customer profitability profiles.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def calculate_repeat_customer_rate(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes single vs repeat customer counts and the repeat customer conversion rate.
    
    Returns:
        Dictionary with total_customers, repeat_customers, single_order_customers, repeat_rate_pct.
    """
    cust_orders = df.groupby("Customer_ID")["Order_ID"].nunique()
    total_customers = len(cust_orders)
    repeat_customers = int((cust_orders > 1).sum())
    single_customers = int((cust_orders == 1).sum())
    repeat_rate = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0.0
    
    return {
        "total_customers": total_customers,
        "repeat_customers": repeat_customers,
        "single_order_customers": single_customers,
        "repeat_customer_rate_pct": round(repeat_rate, 2)
    }


def calculate_pareto_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Pareto cumulative distribution of customer revenue.
    
    Returns:
        DataFrame with Customer_ID, Total_Sales, Cumulative_Sales, Pct_of_Total_Sales,
        Customer_Rank, Cumulative_Customer_Pct.
    """
    cust_sales = df.groupby(["Customer_ID", "Customer_Name"])["Sales"].sum().reset_index()
    cust_sales = cust_sales.sort_values(by="Sales", ascending=False).reset_index(drop=True)
    
    total_sales = cust_sales["Sales"].sum()
    total_customers = len(cust_sales)
    
    cust_sales["Customer_Rank"] = cust_sales.index + 1
    cust_sales["Cumulative_Customer_Pct"] = (cust_sales["Customer_Rank"] / total_customers) * 100
    cust_sales["Cumulative_Sales"] = cust_sales["Sales"].cumsum()
    cust_sales["Cumulative_Sales_Pct"] = (cust_sales["Cumulative_Sales"] / total_sales) * 100
    
    return cust_sales


def get_top_customers(df: pd.DataFrame, n: int = 10, by: str = "Sales") -> pd.DataFrame:
    """
    Returns top N customers ranked by Sales or Profit.
    """
    top = df.groupby(["Customer_ID", "Customer_Name", "Segment"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_ID", "nunique"),
        Total_Quantity=("Quantity", "sum")
    ).reset_index()
    
    top["Profit_Margin"] = top["Total_Profit"] / top["Total_Sales"]
    top["AOV"] = top["Total_Sales"] / top["Total_Orders"]
    
    return top.sort_values(by=f"Total_{by}", ascending=False).head(n)


def get_loss_making_customers(df: pd.DataFrame, threshold: float = 0.0) -> pd.DataFrame:
    """
    Identifies customers generating net negative profit across their order history.
    """
    cust_summary = df.groupby(["Customer_ID", "Customer_Name", "Segment"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_ID", "nunique"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    
    loss_customers = cust_summary[cust_summary["Total_Profit"] < threshold].copy()
    loss_customers["Profit_Margin"] = loss_customers["Total_Profit"] / loss_customers["Total_Sales"]
    return loss_customers.sort_values(by="Total_Profit", ascending=True)


def analyze_customer_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes key commercial performance metrics across customer segments.
    """
    summary = df.groupby("Segment").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_ID", "nunique"),
        Unique_Customers=("Customer_ID", "nunique"),
        Total_Units=("Quantity", "sum"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    
    summary["Profit_Margin"] = summary["Total_Profit"] / summary["Total_Sales"]
    summary["AOV"] = summary["Total_Sales"] / summary["Total_Orders"]
    summary["Sales_per_Customer"] = summary["Total_Sales"] / summary["Unique_Customers"]
    summary["Sales_Share_Pct"] = (summary["Total_Sales"] / summary["Total_Sales"].sum()) * 100
    summary["Profit_Share_Pct"] = (summary["Total_Profit"] / summary["Total_Profit"].sum()) * 100
    
    return summary
