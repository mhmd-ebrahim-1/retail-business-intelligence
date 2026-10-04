"""
Retail Business Intelligence & Customer Analytics Python Package.
Provides data loading, quality auditing, cleaning, feature engineering, RFM segmentation,
customer intelligence, and standardized visualization.
"""

from .data_loader import load_raw_data, load_processed_data, save_processed_data
from .data_quality import DataQualityAuditor
from .data_cleaning import clean_retail_data
from .feature_engineering import engineer_features, add_customer_metrics
from .customer_analysis import (
    calculate_repeat_customer_rate,
    calculate_pareto_distribution,
    get_top_customers,
    get_loss_making_customers,
    analyze_customer_segments
)
from .rfm_analysis import (
    compute_rfm_table,
    score_rfm,
    run_rfm_segmentation,
    summarize_rfm_segments
)
from .visualization import (
    plot_monthly_trends,
    plot_category_performance,
    plot_discount_vs_profit,
    plot_pareto_curve
)

__all__ = [
    "load_raw_data",
    "load_processed_data",
    "save_processed_data",
    "DataQualityAuditor",
    "clean_retail_data",
    "engineer_features",
    "add_customer_metrics",
    "calculate_repeat_customer_rate",
    "calculate_pareto_distribution",
    "get_top_customers",
    "get_loss_making_customers",
    "analyze_customer_segments",
    "compute_rfm_table",
    "score_rfm",
    "run_rfm_segmentation",
    "summarize_rfm_segments",
    "plot_monthly_trends",
    "plot_category_performance",
    "plot_discount_vs_profit",
    "plot_pareto_curve",
]
