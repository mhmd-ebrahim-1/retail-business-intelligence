"""
Automated Data Quality & Integrity Test Suite
Project: Retail Business Intelligence & Customer Analytics Platform
Framework: PyTest
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "superstore_raw.csv"
CLEANED_PATH = BASE_DIR / "data" / "cleaned" / "superstore_cleaned.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


@pytest.fixture(scope="module")
def raw_data():
    assert RAW_PATH.exists(), f"Raw file missing: {RAW_PATH}"
    return pd.read_csv(RAW_PATH, encoding="utf-8")


@pytest.fixture(scope="module")
def cleaned_data():
    assert CLEANED_PATH.exists(), f"Cleaned file missing: {CLEANED_PATH}"
    df = pd.read_csv(CLEANED_PATH, dtype={"postal_code": str})
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])
    return df


@pytest.fixture(scope="module")
def processed_tables():
    tables = {}
    names = ["fact_sales", "dim_date", "dim_customer", "dim_product", "dim_geography", "dim_ship_mode", "rfm_customer_segments"]
    for name in names:
        path = PROCESSED_DIR / f"{name}.csv"
        assert path.exists(), f"Processed table missing: {path}"
        tables[name] = pd.read_csv(path)
    return tables


# --- TEST SUITE ---

def test_raw_data_shape(raw_data):
    """Verify raw dataset has standard 9,994 rows and 21 columns."""
    assert len(raw_data) == 9994, f"Expected 9,994 rows, found {len(raw_data)}"
    assert len(raw_data.columns) == 21, f"Expected 21 columns, found {len(raw_data.columns)}"


def test_cleaned_data_columns(cleaned_data):
    """Verify cleaned dataset contains all standardized snake_case columns."""
    expected_cols = [
        "row_id", "order_id", "order_date", "ship_date", "ship_mode",
        "customer_id", "customer_name", "segment", "country", "city",
        "state", "postal_code", "region", "product_id", "category",
        "sub_category", "product_name", "sales", "quantity", "discount", "profit"
    ]
    for col in expected_cols:
        assert col in cleaned_data.columns, f"Missing required column: {col}"


def test_date_chronology(cleaned_data):
    """Assert that ship date is never prior to order date."""
    violations = cleaned_data[cleaned_data["ship_date"] < cleaned_data["order_date"]]
    assert len(violations) == 0, f"Found {len(violations)} records where ship_date < order_date"


def test_financial_constraints(cleaned_data):
    """Assert sales >= 0, quantity >= 1, and discount is bounded in [0.0, 1.0]."""
    assert (cleaned_data["sales"] >= 0).all(), "Negative sales values found!"
    assert (cleaned_data["quantity"] > 0).all(), "Invalid quantity found (<= 0)!"
    assert ((cleaned_data["discount"] >= 0.0) & (cleaned_data["discount"] <= 1.0)).all(), "Discounts out of bounds!"


def test_star_schema_referential_integrity(processed_tables):
    """Assert fact table foreign keys cleanly join to dimension tables without orphans."""
    fact = processed_tables["fact_sales"]
    cust = processed_tables["dim_customer"]
    prod = processed_tables["dim_product"]
    geo = processed_tables["dim_geography"]
    ship = processed_tables["dim_ship_mode"]
    date_dim = processed_tables["dim_date"]

    assert fact["customer_key"].isin(cust["customer_key"]).all(), "Orphan customer_key detected!"
    assert fact["product_key"].isin(prod["product_key"]).all(), "Orphan product_key detected!"
    assert fact["geography_key"].isin(geo["geography_key"]).all(), "Orphan geography_key detected!"
    assert fact["ship_mode_key"].isin(ship["ship_mode_key"]).all(), "Orphan ship_mode_key detected!"
    assert fact["order_date_key"].isin(date_dim["date_key"]).all(), "Orphan order_date_key detected!"


def test_fact_sales_primary_key(processed_tables):
    """Assert sale_id in fact_sales is strictly unique."""
    fact = processed_tables["fact_sales"]
    assert fact["sale_id"].nunique() == len(fact), "Duplicate primary key sale_id in fact_sales!"


def test_rfm_segmentation_integrity(processed_tables):
    """Assert that RFM segments cover all 793 customers without nulls."""
    rfm = processed_tables["rfm_customer_segments"]
    assert len(rfm) == 793, f"Expected 793 segmented customers, found {len(rfm)}"
    assert rfm["customer_segment"].isnull().sum() == 0, "Null customer segments found!"
    assert rfm["monetary_sales"].sum() > 2200000, "RFM total monetary sales deviates from actual sales!"


def test_postal_code_formatting(cleaned_data):
    """Assert postal codes are clean 5-digit strings or 'Unknown'."""
    assert cleaned_data["postal_code"].isnull().sum() == 0, "Null postal codes found!"
    non_standard = cleaned_data[~cleaned_data["postal_code"].astype(str).str.match(r"^(\d{5}|Unknown)$")]
    assert len(non_standard) == 0, f"Found {len(non_standard)} invalid postal codes"

