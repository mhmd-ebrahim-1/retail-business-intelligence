"""
Automated Data Quality & Pipeline Unit Tests.
Tests dataset schema, constraints, domain validity, and financial calculations.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pandas as pd
import numpy as np
from python.data_loader import load_raw_data, load_processed_data
from python.data_cleaning import clean_retail_data
from python.feature_engineering import engineer_features, add_customer_metrics
from python.data_quality import DataQualityAuditor
from python.rfm_analysis import run_rfm_segmentation


@pytest.fixture(scope="module")
def raw_df():
    return load_raw_data()


@pytest.fixture(scope="module")
def clean_df(raw_df):
    return clean_retail_data(raw_df)


@pytest.fixture(scope="module")
def enriched_df(clean_df):
    return add_customer_metrics(engineer_features(clean_df))


def test_raw_shape_and_columns(raw_df):
    """Asserts raw dataset contains exactly 9,994 rows and required core columns."""
    assert len(raw_df) == 9994
    expected_cols = [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Customer Name", "Segment", "Country", "City",
        "State", "Postal Code", "Region", "Product ID", "Category",
        "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit"
    ]
    for col in expected_cols:
        assert col in raw_df.columns, f"Missing required raw column: {col}"


def test_missing_values(raw_df):
    """Asserts zero null or missing values across raw transactions."""
    null_counts = raw_df.isnull().sum()
    assert null_counts.sum() == 0, f"Detected missing values:\n{null_counts[null_counts > 0]}"


def test_duplicate_rows(raw_df):
    """Asserts zero duplicate rows in the raw dataset."""
    assert raw_df.duplicated().sum() == 0
    row_id_col = "Row ID" if "Row ID" in raw_df.columns else "Row_ID"
    assert raw_df[row_id_col].nunique() == 9994


def test_date_validity(clean_df):
    """Asserts all dates are valid and Order Date <= Ship Date."""
    assert (clean_df["Ship_Date"] < clean_df["Order_Date"]).sum() == 0
    assert clean_df["Order_Date"].min() == pd.Timestamp("2014-01-03")
    assert clean_df["Order_Date"].max() == pd.Timestamp("2017-12-30")


def test_numerical_ranges(clean_df):
    """Asserts Sales > 0, Quantity >= 1, and 0 <= Discount <= 1.0."""
    assert (clean_df["Sales"] <= 0).sum() == 0
    assert (clean_df["Quantity"] <= 0).sum() == 0
    assert ((clean_df["Discount"] < 0) | (clean_df["Discount"] > 1.0)).sum() == 0


def test_baseline_kpi_consistency(clean_df):
    """Asserts financial totals match baseline verified metrics."""
    total_sales = clean_df["Sales"].sum()
    total_profit = clean_df["Profit"].sum()
    margin_pct = (total_profit / total_sales) * 100
    total_orders = clean_df["Order_ID"].nunique()
    total_customers = clean_df["Customer_ID"].nunique()
    
    assert np.isclose(total_sales, 2297200.86, atol=0.01)
    assert np.isclose(total_profit, 286397.02, atol=0.01)
    assert np.isclose(margin_pct, 12.47, atol=0.01)
    assert total_orders == 5009
    assert total_customers == 793


def test_feature_engineering_integrity(enriched_df):
    """Asserts derived temporal, operational, and customer attributes."""
    assert "Order_to_Ship_Days" in enriched_df.columns
    assert "Discount_Band" in enriched_df.columns
    assert "Shipping_Delay_Category" in enriched_df.columns
    assert "Customer_AOV" in enriched_df.columns
    assert (enriched_df["Order_to_Ship_Days"] < 0).sum() == 0
    assert enriched_df["Order_to_Ship_Days"].max() <= 7


def test_rfm_segmentation_logic(clean_df):
    """Asserts RFM customer segmentation assigns valid scores and labels to all 793 customers."""
    rfm = run_rfm_segmentation(clean_df)
    assert len(rfm) == 793
    assert rfm["R_Score"].between(1, 5).all()
    assert rfm["F_Score"].between(1, 5).all()
    assert rfm["M_Score"].between(1, 5).all()
    assert rfm["Segment_Label"].notnull().all()
    valid_segments = {
        "Champions", "Loyal Customers", "Potential Loyalists", "New Customers",
        "Promising", "Need Attention", "About to Sleep", "Cannot Lose Them",
        "At Risk", "Hibernating", "Lost"
    }
    assert set(rfm["Segment_Label"].unique()).issubset(valid_segments)
