"""
Data Quality Validation Module for Retail Business Intelligence.
Performs comprehensive schema, constraint, consistency, and integrity checks.
"""

from typing import Dict, List, Any
import pandas as pd
import numpy as np


class DataQualityAuditor:
    """Performs multi-dimensional data quality auditing on retail transaction datasets."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.results: Dict[str, Any] = {}
        
    def check_missing_values(self) -> pd.DataFrame:
        """Audits null, NaN, and blank values across all columns."""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        audit_df = pd.DataFrame({
            "Column": self.df.columns,
            "Missing_Count": missing.values,
            "Missing_Percentage": missing_pct.values
        }).sort_values(by="Missing_Count", ascending=False)
        self.results["missing_values"] = audit_df
        return audit_df
        
    def check_duplicates(self) -> Dict[str, int]:
        """Audits full row duplicates and identifier duplicates."""
        row_id_col = "Row ID" if "Row ID" in self.df.columns else "Row_ID"
        order_id_col = "Order ID" if "Order ID" in self.df.columns else "Order_ID"
        
        full_dups = int(self.df.duplicated().sum())
        row_id_dups = int(self.df[row_id_col].duplicated().sum()) if row_id_col in self.df.columns else 0
        total_unique_orders = int(self.df[order_id_col].nunique()) if order_id_col in self.df.columns else 0
        
        dup_metrics = {
            "total_rows": len(self.df),
            "full_row_duplicates": full_dups,
            "row_id_duplicates": row_id_dups,
            "unique_orders": total_unique_orders,
            "total_line_items": len(self.df)
        }
        self.results["duplicates"] = dup_metrics
        return dup_metrics
        
    def check_date_validity(self) -> Dict[str, Any]:
        """Validates date consistency (Order Date <= Ship Date)."""
        order_date_col = "Order Date" if "Order Date" in self.df.columns else "Order_Date"
        ship_date_col = "Ship Date" if "Ship Date" in self.df.columns else "Ship_Date"
        
        o_date = pd.to_datetime(self.df[order_date_col])
        s_date = pd.to_datetime(self.df[ship_date_col])
        
        invalid_sequence = (s_date < o_date).sum()
        date_metrics = {
            "min_order_date": str(o_date.min().date()),
            "max_order_date": str(o_date.max().date()),
            "min_ship_date": str(s_date.min().date()),
            "max_ship_date": str(s_date.max().date()),
            "invalid_date_sequences": int(invalid_sequence),
            "max_shipping_days": int((s_date - o_date).dt.days.max()),
            "min_shipping_days": int((s_date - o_date).dt.days.min()),
            "avg_shipping_days": round(float((s_date - o_date).dt.days.mean()), 2)
        }
        self.results["date_validity"] = date_metrics
        return date_metrics

    def check_numeric_constraints(self) -> Dict[str, Any]:
        """Validates numerical ranges and constraints (Sales > 0, Quantity > 0, 0 <= Discount <= 1)."""
        sales_col = "Sales"
        qty_col = "Quantity"
        disc_col = "Discount"
        prof_col = "Profit"
        
        sales_negative = int((self.df[sales_col] <= 0).sum())
        qty_negative = int((self.df[qty_col] <= 0).sum())
        disc_invalid = int(((self.df[disc_col] < 0) | (self.df[disc_col] > 1)).sum())
        loss_making_count = int((self.df[prof_col] < 0).sum())
        
        numeric_metrics = {
            "negative_or_zero_sales_count": sales_negative,
            "negative_or_zero_quantity_count": qty_negative,
            "invalid_discount_range_count": disc_invalid,
            "loss_making_transactions_count": loss_making_count,
            "loss_making_transactions_pct": round(float(loss_making_count / len(self.df) * 100), 2),
            "total_sales": round(float(self.df[sales_col].sum()), 2),
            "total_profit": round(float(self.df[prof_col].sum()), 2),
            "profit_margin_pct": round(float(self.df[prof_col].sum() / self.df[sales_col].sum() * 100), 2)
        }
        self.results["numeric_constraints"] = numeric_metrics
        return numeric_metrics

    def check_categorical_consistency(self) -> Dict[str, List[str]]:
        """Audits categorical values and cardinality across segments, regions, categories."""
        cat_cols = ["Segment", "Region", "Category", "Ship Mode" if "Ship Mode" in self.df.columns else "Ship_Mode"]
        cat_metrics = {}
        for col in cat_cols:
            if col in self.df.columns:
                cat_metrics[col] = self.df[col].dropna().unique().tolist()
        self.results["categorical_consistency"] = cat_metrics
        return cat_metrics

    def run_full_audit(self) -> Dict[str, Any]:
        """Executes all data quality verification routines."""
        self.check_missing_values()
        self.check_duplicates()
        self.check_date_validity()
        self.check_numeric_constraints()
        self.check_categorical_consistency()
        return self.results
