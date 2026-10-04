"""
Feature Engineering and Dimensional Modeling Module
Project: Retail Business Intelligence & Customer Analytics Platform

1. Calculates high-value business features and metrics.
2. Generates a Star Schema Dimensional Model (Fact & Dimension tables) in data/processed/.
"""
from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_PATH = BASE_DIR / "data" / "cleaned" / "superstore_cleaned.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create analytical, operational, and financial features.
    """
    df_feat = df.copy()
    
    # 1. Temporal Features
    df_feat["order_year"] = df_feat["order_date"].dt.year
    df_feat["order_month"] = df_feat["order_date"].dt.month
    df_feat["order_month_name"] = df_feat["order_date"].dt.month_name()
    df_feat["order_quarter"] = "Q" + df_feat["order_date"].dt.quarter.astype(str)
    df_feat["year_month"] = df_feat["order_date"].dt.strftime("%Y-%m")
    df_feat["order_day_of_week"] = df_feat["order_date"].dt.day_name()
    df_feat["is_weekend"] = df_feat["order_date"].dt.dayofweek.isin([5, 6]).astype(int)
    
    # 2. Operational Features
    df_feat["ship_days"] = (df_feat["ship_date"] - df_feat["order_date"]).dt.days
    
    def categorize_shipping(days: int) -> str:
        if days == 0:
            return "Same Day"
        elif days <= 2:
            return "Fast (1-2 Days)"
        elif days <= 5:
            return "Standard (3-5 Days)"
        else:
            return "Delayed (6+ Days)"
            
    df_feat["shipping_delay_category"] = df_feat["ship_days"].apply(categorize_shipping)
    
    # 3. Financial & Margin Features
    df_feat["profit_margin"] = np.where(
        df_feat["sales"] > 0,
        (df_feat["profit"] / df_feat["sales"]).round(4),
        0.0
    )
    
    df_feat["profit_status"] = np.where(
        df_feat["profit"] > 0,
        "Profitable",
        np.where(df_feat["profit"] < 0, "Loss-Making", "Breakeven")
    )
    
    # Discount Bands
    def categorize_discount(d: float) -> str:
        if d == 0:
            return "0% (No Discount)"
        elif d <= 0.10:
            return "1% - 10% (Low)"
        elif d <= 0.20:
            return "11% - 20% (Moderate)"
        elif d <= 0.50:
            return "21% - 50% (High)"
        else:
            return "> 50% (Deep)"
            
    df_feat["discount_band"] = df_feat["discount"].apply(categorize_discount)
    
    # Order Value Bands
    def categorize_order_val(s: float) -> str:
        if s < 50:
            return "< $50 (Small)"
        elif s <= 250:
            return "$50 - $250 (Medium)"
        elif s <= 1000:
            return "$250 - $1,000 (Large)"
        else:
            return "> $1,000 (Enterprise)"
            
    df_feat["order_value_band"] = df_feat["sales"].apply(categorize_order_val)
    
    return df_feat


def build_star_schema(df: pd.DataFrame, output_dir: Path = PROCESSED_DIR) -> dict:
    """
    Construct a star schema dimensional model with surrogate keys.
    Outputs:
    - dim_date
    - dim_customer
    - dim_product
    - dim_geography
    - dim_ship_mode
    - fact_sales
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # --- 1. DIM_SHIP_MODE ---
    ship_modes = sorted(df["ship_mode"].unique())
    dim_ship_mode = pd.DataFrame({
        "ship_mode_key": range(1, len(ship_modes) + 1),
        "ship_mode": ship_modes
    })
    
    # --- 2. DIM_GEOGRAPHY ---
    geo_df = df[["country", "region", "state", "city", "postal_code"]].drop_duplicates().reset_index(drop=True)
    geo_df["geography_key"] = range(1, len(geo_df) + 1)
    dim_geography = geo_df[["geography_key", "country", "region", "state", "city", "postal_code"]]
    
    # --- 3. DIM_CUSTOMER ---
    # Customer dimension with aggregated customer lifetime metrics
    cust_agg = df.groupby(["customer_id", "customer_name", "segment"]).agg(
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max"),
        total_orders=("order_id", "nunique"),
        total_spend=("sales", "sum"),
        total_profit=("profit", "sum")
    ).reset_index()
    cust_agg["customer_key"] = range(1, len(cust_agg) + 1)
    dim_customer = cust_agg[[
        "customer_key", "customer_id", "customer_name", "segment",
        "first_order_date", "last_order_date", "total_orders", "total_spend", "total_profit"
    ]]
    
    # --- 4. DIM_PRODUCT ---
    prod_df = df[["product_id", "category", "sub_category", "product_name"]].drop_duplicates(subset=["product_id", "product_name"]).reset_index(drop=True)
    prod_df["product_key"] = range(1, len(prod_df) + 1)
    dim_product = prod_df[["product_key", "product_id", "product_name", "category", "sub_category"]]
    
    # --- 5. DIM_DATE ---
    all_dates = pd.date_range(
        start=min(df["order_date"].min(), df["ship_date"].min()),
        end=max(df["order_date"].max(), df["ship_date"].max()),
        freq="D"
    )
    dim_date = pd.DataFrame({
        "date_key": all_dates.strftime("%Y%m%d").astype(int),
        "full_date": all_dates,
        "year": all_dates.year,
        "quarter": "Q" + all_dates.quarter.astype(str),
        "month": all_dates.month,
        "month_name": all_dates.month_name(),
        "day": all_dates.day,
        "day_name": all_dates.day_name(),
        "day_of_week": all_dates.dayofweek + 1,  # 1 = Monday
        "is_weekend": all_dates.dayofweek.isin([5, 6]).astype(int),
        "year_month": all_dates.strftime("%Y-%m")
    })
    
    # --- 6. FACT_SALES ---
    # Merge keys to create star schema fact table
    fact = df.copy()
    
    # Map foreign keys
    fact = fact.merge(dim_ship_mode, on="ship_mode", how="left")
    fact = fact.merge(dim_geography, on=["country", "region", "state", "city", "postal_code"], how="left")
    fact = fact.merge(dim_customer[["customer_key", "customer_id"]], on="customer_id", how="left")
    fact = fact.merge(dim_product[["product_key", "product_id", "product_name"]], on=["product_id", "product_name"], how="left")
    
    fact["order_date_key"] = fact["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact["ship_date_key"] = fact["ship_date"].dt.strftime("%Y%m%d").astype(int)
    fact["sale_id"] = range(1, len(fact) + 1)
    
    fact_sales = fact[[
        "sale_id", "row_id", "order_id",
        "order_date_key", "ship_date_key",
        "customer_key", "product_key", "geography_key", "ship_mode_key",
        "sales", "quantity", "discount", "profit",
        "ship_days", "profit_margin", "profit_status",
        "discount_band", "order_value_band", "shipping_delay_category"
    ]]
    
    # Save all tables to CSV
    tables = {
        "dim_date": dim_date,
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_geography": dim_geography,
        "dim_ship_mode": dim_ship_mode,
        "fact_sales": fact_sales
    }
    
    for name, table in tables.items():
        save_path = output_dir / f"{name}.csv"
        table.to_csv(save_path, index=False)
        print(f"Saved {name}: {table.shape[0]} rows, {table.shape[1]} columns -> {save_path.name}")
        
    return tables


def run_feature_engineering_pipeline():
    print(f"Loading cleaned data from: {CLEANED_PATH}")
    df_clean = pd.read_csv(CLEANED_PATH)
    df_clean["order_date"] = pd.to_datetime(df_clean["order_date"])
    df_clean["ship_date"] = pd.to_datetime(df_clean["ship_date"])
    
    print("Engineering analytical features...")
    df_feat = engineer_features(df_clean)
    
    # Save enriched master dataset
    enriched_path = PROCESSED_DIR / "superstore_enriched.csv"
    df_feat.to_csv(enriched_path, index=False)
    print(f"Saved enriched master dataset to: {enriched_path}")
    
    print("\nBuilding Star Schema relational model...")
    tables = build_star_schema(df_feat)
    print("Star schema built and exported successfully!")


if __name__ == "__main__":
    run_feature_engineering_pipeline()

