"""
Data Loader Module
Provides standard functions to load raw, cleaned, enriched, and processed datasets.
Project: Retail Business Intelligence & Customer Analytics Platform
"""
from pathlib import Path
from typing import Optional
import pandas as pd


# Project Root Directory & Standard Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "superstore_raw.csv"
CLEANED_DATA_PATH = BASE_DIR / "data" / "cleaned" / "superstore_cleaned.csv"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
ENRICHED_DATA_PATH = PROCESSED_DATA_DIR / "superstore_enriched.csv"


def load_raw_data(file_path: Optional[Path] = None, encoding: str = "utf-8") -> pd.DataFrame:
    """
    Load raw Superstore transaction dataset.
    
    Parameters:
        file_path (Path, optional): Path to raw CSV file.
        encoding (str): Encoding of raw file.
        
    Returns:
        pd.DataFrame: Raw dataset.
    """
    path = file_path or RAW_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {path}")
    return pd.read_csv(path, encoding=encoding)


def load_cleaned_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load cleaned Superstore transaction dataset with parsed dates and string postal codes.
    
    Parameters:
        file_path (Path, optional): Path to cleaned CSV file.
        
    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    path = file_path or CLEANED_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at: {path}. Run data_cleaning.py first.")
    df = pd.read_csv(path, dtype={"postal_code": str})
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])
    return df


def load_enriched_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load enriched master dataset with engineered analytical features.
    
    Parameters:
        file_path (Path, optional): Path to enriched CSV file.
        
    Returns:
        pd.DataFrame: Enriched dataset with datetime features.
    """
    path = file_path or ENRICHED_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Enriched dataset not found at: {path}. Run feature_engineering.py first.")
    df = pd.read_csv(path, dtype={"postal_code": str})
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])
    return df


def load_processed_table(table_name: str) -> pd.DataFrame:
    """
    Load a dimensional or fact table from the processed data directory.
    
    Parameters:
        table_name (str): Name of table (e.g., 'fact_sales', 'dim_customer', 'dim_product', 'dim_geography', 'dim_date', 'dim_ship_mode').
        
    Returns:
        pd.DataFrame: Table dataframe.
    """
    file_path = PROCESSED_DATA_DIR / f"{table_name}.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Processed table '{table_name}' not found at: {file_path}")
    
    dtype_dict = {}
    if table_name in ["dim_geography", "superstore_cleaned", "superstore_enriched"]:
        dtype_dict["postal_code"] = str
        
    return pd.read_csv(file_path, dtype=dtype_dict)


def load_rfm_data() -> pd.DataFrame:
    """
    Load RFM customer segmentation dataset.
    
    Returns:
        pd.DataFrame: Customer-level RFM scores and segment labels.
    """
    return load_processed_table("rfm_customer_segments")


if __name__ == "__main__":
    df_raw = load_raw_data()
    print(f"Loaded raw data: {df_raw.shape[0]:,} rows, {df_raw.shape[1]} columns")
    
    df_clean = load_cleaned_data()
    print(f"Loaded cleaned data: {df_clean.shape[0]:,} rows, {df_clean.shape[1]} columns")
    
    df_rfm = load_rfm_data()
    print(f"Loaded RFM data: {df_rfm.shape[0]:,} customers across {df_rfm['customer_segment'].nunique()} segments")

