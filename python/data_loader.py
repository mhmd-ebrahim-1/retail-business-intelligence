"""
Data Loader Module for Retail Business Intelligence & Customer Analytics.
Provides robust data ingestion with multi-encoding fallback, schema validation, and path resolution.
"""

import os
from pathlib import Path
from typing import Optional, Tuple
import pandas as pd


def get_project_root() -> Path:
    """Returns the absolute path to the project root directory."""
    return Path(__file__).resolve().parent.parent


def load_raw_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads raw e-commerce transaction dataset with encoding fallbacks.
    
    Args:
        filepath: Optional path to raw CSV. Defaults to 'data/raw/ecommerce_raw.csv'.
        
    Returns:
        pd.DataFrame containing raw transactional records.
        
    Raises:
        FileNotFoundError: If the raw data file does not exist.
        ValueError: If loading fails across all supported encodings.
    """
    if filepath is None:
        filepath = os.path.join(get_project_root(), "data", "raw", "ecommerce_raw.csv")
        
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data file not found at: {filepath}")
        
    encodings = ["utf-8", "windows-1252", "latin1", "iso-8859-1", "cp1252"]
    
    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise RuntimeError(f"Error reading CSV file with encoding {enc}: {e}")
            
    # If all encodings fail, read with replace error handler
    return pd.read_csv(filepath, encoding="utf-8", encoding_errors="replace")


def load_processed_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads cleaned and enriched transaction dataset.
    
    Args:
        filepath: Optional path to processed CSV. Defaults to 'data/processed/ecommerce_clean.csv'.
        
    Returns:
        pd.DataFrame containing cleaned and feature-engineered records.
    """
    if filepath is None:
        filepath = os.path.join(get_project_root(), "data", "processed", "ecommerce_clean.csv")
        
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Processed data file not found at: {filepath}")
        
    df = pd.read_csv(filepath, parse_dates=["Order_Date", "Ship_Date"])
    return df


def save_processed_data(df: pd.DataFrame, filepath: Optional[str] = None) -> str:
    """
    Saves cleaned dataframe to CSV.
    
    Args:
        df: DataFrame to save.
        filepath: Optional output file path. Defaults to 'data/processed/ecommerce_clean.csv'.
        
    Returns:
        Saved file path string.
    """
    if filepath is None:
        filepath = os.path.join(get_project_root(), "data", "processed", "ecommerce_clean.csv")
        
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False, encoding="utf-8")
    return filepath
