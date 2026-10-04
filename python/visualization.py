"""
Visualization Module for Retail Business Intelligence.
Provides standardized, publication-quality Matplotlib and Seaborn plotting routines.
"""

from typing import Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# Set global professional aesthetic
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8


def plot_monthly_trends(df: pd.DataFrame, figsize: Tuple[int, int] = (14, 6), save_path: Optional[str] = None) -> plt.Figure:
    """Plots dual-axis or subplots of monthly sales and profit trends over time."""
    monthly = df.groupby("Year_Month").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    
    fig, ax1 = plt.subplots(figsize=figsize)
    
    color_sales = "#1f77b4"
    color_profit = "#2ca02c"
    
    ax1.set_xlabel("Year-Month", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Sales ($)", color=color_sales, fontsize=11, fontweight="bold")
    line1 = ax1.plot(monthly["Year_Month"], monthly["Sales"], color=color_sales, marker="o", linewidth=2, label="Monthly Sales")
    ax1.tick_params(axis="y", labelcolor=color_sales)
    ax1.set_xticks(range(0, len(monthly), 3))
    ax1.set_xticklabels(monthly["Year_Month"].iloc[::3], rotation=45)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel("Profit ($)", color=color_profit, fontsize=11, fontweight="bold")
    line2 = ax2.plot(monthly["Year_Month"], monthly["Profit"], color=color_profit, marker="s", linestyle="--", linewidth=2, label="Monthly Profit")
    ax2.tick_params(axis="y", labelcolor=color_profit)
    ax2.grid(False)
    
    plt.title("Monthly Sales & Profit Performance (2014 - 2017)", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_category_performance(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 5), save_path: Optional[str] = None) -> plt.Figure:
    """Plots side-by-side bar chart of Sales and Profit by Category."""
    cat_df = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    
    x = np.arange(len(cat_df))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=figsize)
    rects1 = ax.bar(x - width/2, cat_df["Sales"], width, label="Sales ($)", color="#2b5c8f")
    rects2 = ax.bar(x + width/2, cat_df["Profit"], width, label="Profit ($)", color="#38a169")
    
    ax.set_ylabel("USD ($)", fontsize=11, fontweight="bold")
    ax.set_title("Revenue & Profit Contribution by Category", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_df["Category"], fontsize=11)
    ax.legend(frameon=True)
    
    # Value labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"${h:,.0f}", (rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"${h:,.0f}", (rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)
        
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_discount_vs_profit(df: pd.DataFrame, figsize: Tuple[int, int] = (10, 6), save_path: Optional[str] = None) -> plt.Figure:
    """Plots scatter plot and regression line showing profit erosion caused by discounts."""
    fig, ax = plt.subplots(figsize=figsize)
    
    sns.scatterplot(
        data=df,
        x="Discount",
        y="Profit",
        hue="Category",
        alpha=0.6,
        palette="tab10",
        ax=ax
    )
    
    ax.axhline(0, color="red", linestyle="--", alpha=0.7, label="Break-Even ($0 Profit)")
    ax.set_title("Impact of Discount Level on Transaction Profitability", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Discount Level (Ratio)", fontsize=11)
    ax.set_ylabel("Profit ($)", fontsize=11)
    ax.legend(title="Category", frameon=True)
    
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_pareto_curve(pareto_df: pd.DataFrame, figsize: Tuple[int, int] = (10, 6), save_path: Optional[str] = None) -> plt.Figure:
    """Plots Pareto cumulative customer distribution curve."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(pareto_df["Cumulative_Customer_Pct"], pareto_df["Cumulative_Sales_Pct"], color="#805ad5", linewidth=2.5, label="Cumulative Sales %")
    ax.plot([0, 100], [0, 100], color="#a0aec0", linestyle="--", label="Equal Distribution Reference")
    
    # 80/20 crosshair
    ax.axvline(20, color="#e53e3e", linestyle=":", alpha=0.8)
    top20_sales = pareto_df[pareto_df["Cumulative_Customer_Pct"] <= 20]["Cumulative_Sales_Pct"].max()
    ax.axhline(top20_sales, color="#e53e3e", linestyle=":", alpha=0.8)
    ax.annotate(f"Top 20% Customers = {top20_sales:.1f}% Sales", 
                xy=(20, top20_sales), xytext=(30, top20_sales - 10),
                arrowprops=dict(arrowstyle="->", color="#e53e3e", lw=1.5),
                fontweight="bold", color="#e53e3e")
    
    ax.set_xlabel("Cumulative Percentage of Customers (%)", fontsize=11)
    ax.set_ylabel("Cumulative Percentage of Revenue (%)", fontsize=11)
    ax.set_title("Customer Revenue Concentration (Pareto Analysis)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(loc="lower right", frameon=True)
    
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig
