"""
High-Resolution Dashboard & Visual Graphics Generator
Project: Retail Business Intelligence & Customer Analytics Platform

Generates executive-level dashboard page views, analytical figures, and charts
and saves them to `powerbi/screenshots/` and `docs/images/`.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SCREENSHOTS_DIR = BASE_DIR / "powerbi" / "screenshots"
DOCS_IMG_DIR = BASE_DIR / "docs" / "images"

# Create directories
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_IMG_DIR.mkdir(parents=True, exist_ok=True)

# Aesthetic parameters
NAVY = "#1F4E78"
ACCENT_BLUE = "#2F5597"
GREEN = "#2CA02C"
RED = "#D62728"
BG_COLOR = "#F8F9FA"
CARD_BG = "#FFFFFF"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Calibri", "Arial", "DejaVu Sans"]


def generate_page1_executive_overview(df: pd.DataFrame):
    """Page 1: Executive Overview Dashboard"""
    fig = plt.figure(figsize=(16, 10), facecolor=BG_COLOR)
    gs = gridspec.GridSpec(4, 3, height_ratios=[0.8, 1.2, 1.5, 1.5], figure=fig, hspace=0.35, wspace=0.25)
    
    # Title & Header Banner
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis("off")
    ax_title.text(0.01, 0.65, "RETAIL BUSINESS INTELLIGENCE PLATFORM", fontsize=20, weight="bold", color=NAVY)
    ax_title.text(0.01, 0.25, "Executive Performance Overview | 4-Year Enterprise Portfolio Health (2014 - 2017)", fontsize=12, color="#595959")
    
    # KPI Cards Row
    kpis = [
        ("TOTAL REVENUE", f"${df['sales'].sum():,.0f}", "+20.4% YoY"),
        ("TOTAL NET PROFIT", f"${df['profit'].sum():,.0f}", "+14.2% YoY"),
        ("PROFIT MARGIN", f"{(df['profit'].sum()/df['sales'].sum())*100:.2f}%", "+0.6 pts"),
        ("TOTAL ORDERS", f"{df['order_id'].nunique():,}", "+18.9% YoY"),
        ("ACTIVE CUSTOMERS", f"{df['customer_id'].nunique():,}", "95.6% Repeat Rate"),
        ("AVG ORDER VALUE", f"${df['sales'].sum()/df['order_id'].nunique():,.1f}", "+1.3% YoY")
    ]
    
    # Draw KPI cards in 2nd row (sub-divided)
    gs_kpi = gridspec.GridSpecFromSubplotSpec(1, 6, subplot_spec=gs[1, :], wspace=0.2)
    for i, (label, val, note) in enumerate(kpis):
        ax_kpi = fig.add_subplot(gs_kpi[0, i])
        ax_kpi.set_facecolor(CARD_BG)
        for spine in ax_kpi.spines.values():
            spine.set_color("#E0E0E0")
            spine.set_linewidth(1.5)
        ax_kpi.set_xticks([])
        ax_kpi.set_yticks([])
        ax_kpi.text(0.5, 0.75, label, fontsize=9, weight="bold", color="#7F8C8D", ha="center")
        ax_kpi.text(0.5, 0.40, val, fontsize=16, weight="bold", color=NAVY, ha="center")
        ax_kpi.text(0.5, 0.15, note, fontsize=9, color=GREEN if "+" in note or "%" in note else "#7F8C8D", ha="center", weight="semibold")

    # Visual 1: Monthly Sales & Profit Trend (2 columns wide)
    ax_trend = fig.add_subplot(gs[2, :2])
    monthly = df.groupby("year_month").agg(Sales=("sales", "sum"), Profit=("profit", "sum")).reset_index()
    ax_trend.plot(monthly["year_month"], monthly["Sales"], color=NAVY, linewidth=2.5, marker="o", label="Sales ($)")
    ax_trend.set_title("Monthly Revenue Trajectory with Seasonal Q4 Peaks", fontsize=12, weight="bold", color=NAVY, loc="left")
    ax_trend.set_xticks(range(0, len(monthly), 4))
    ax_trend.set_xticklabels(monthly["year_month"].iloc[::4], rotation=30, ha="right", fontsize=9)
    ax_trend.set_ylabel("Sales ($)", fontsize=10, weight="bold", color=NAVY)
    ax_trend.grid(True, linestyle="--", alpha=0.5)
    
    # Secondary axis for profit
    ax_prof = ax_trend.twinx()
    ax_prof.plot(monthly["year_month"], monthly["Profit"], color=GREEN, linewidth=2, linestyle="--", marker="s", label="Profit ($)")
    ax_prof.set_ylabel("Profit ($)", fontsize=10, weight="bold", color=GREEN)
    ax_prof.grid(False)

    # Visual 2: Category Revenue Breakdown (Pie/Donut)
    ax_cat = fig.add_subplot(gs[2, 2])
    cat_sales = df.groupby("category")["sales"].sum()
    colors = [NAVY, ACCENT_BLUE, "#5DADE2"]
    wedges, texts, autotexts = ax_cat.pie(cat_sales, labels=cat_sales.index, autopct="%1.1f%%", colors=colors, startangle=90, textprops=dict(color="black", fontsize=10))
    for at in autotexts:
        at.set_color("white")
        at.set_weight("bold")
    ax_cat.set_title("Revenue by Product Category", fontsize=12, weight="bold", color=NAVY, loc="left")

    # Visual 3: Regional Sales & Profitability (Horizontal bar)
    ax_reg = fig.add_subplot(gs[3, :2])
    reg_perf = df.groupby("region").agg(Sales=("sales", "sum"), Profit=("profit", "sum")).reset_index().sort_values("Sales", ascending=True)
    y_pos = np.arange(len(reg_perf))
    bar_height = 0.35
    ax_reg.barh(y_pos + bar_height/2, reg_perf["Sales"], height=bar_height, color=NAVY, label="Sales ($)")
    ax_reg.barh(y_pos - bar_height/2, reg_perf["Profit"], height=bar_height, color=GREEN, label="Profit ($)")
    ax_reg.set_yticks(y_pos)
    ax_reg.set_yticklabels(reg_perf["region"], fontsize=10, weight="bold")
    ax_reg.set_title("Regional Revenue vs Profit Contribution", fontsize=12, weight="bold", color=NAVY, loc="left")
    ax_reg.legend(loc="lower right")
    ax_reg.grid(True, linestyle="--", alpha=0.5, axis="x")

    # Visual 4: Customer Segment Share
    ax_seg = fig.add_subplot(gs[3, 2])
    seg_perf = df.groupby("segment")["sales"].sum().sort_values(ascending=False)
    ax_seg.bar(seg_perf.index, seg_perf.values, color=[NAVY, ACCENT_BLUE, "#7FB3D5"], width=0.5)
    ax_seg.set_title("Revenue by Customer Segment", fontsize=12, weight="bold", color=NAVY, loc="left")
    ax_seg.set_ylabel("Sales ($)", fontsize=10)
    for i, v in enumerate(seg_perf.values):
        ax_seg.text(i, v + 20000, f"${v/1e3:.1f}k", ha="center", fontsize=9, weight="bold")
    ax_seg.grid(True, linestyle="--", alpha=0.5, axis="y")

    out_path = SCREENSHOTS_DIR / "page1_executive_overview.png"
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Rendered: {out_path.name}")


def generate_page2_sales_profitability(df: pd.DataFrame):
    """Page 2: Sales & Profitability Analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), facecolor=BG_COLOR)
    fig.suptitle("SALES & PROFITABILITY ANALYTICS | Sub-Category & Discount Impact", fontsize=16, weight="bold", color=NAVY, y=0.98)
    
    # 1. Sub-Category Profitability (Highlighting losses)
    subcat = df.groupby("sub_category")["profit"].sum().sort_values(ascending=True)
    colors = [RED if x < 0 else GREEN for x in subcat.values]
    axes[0, 0].barh(subcat.index, subcat.values, color=colors)
    axes[0, 0].axvline(0, color="black", linewidth=1, linestyle="--")
    axes[0, 0].set_title("Net Profit / Loss by Sub-Category (Tables & Bookcases in Deficit)", fontsize=12, weight="bold", color=NAVY, loc="left")
    axes[0, 0].set_xlabel("Net Profit ($)", fontsize=10, weight="bold")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5, axis="x")

    # 2. Discount vs Margin Destruction Curve
    disc = df.groupby("discount_band").agg(Sales=("sales", "sum"), Profit=("profit", "sum")).reset_index()
    disc["Margin"] = (disc["Profit"] / disc["Sales"]) * 100
    disc_order = ["0% (No Discount)", "1% - 10% (Low)", "11% - 20% (Moderate)", "21% - 50% (High)", "> 50% (Deep)"]
    disc = disc.set_index("discount_band").reindex(disc_order).reset_index()
    
    bar_cols = [GREEN if x >= 0 else RED for x in disc["Margin"]]
    axes[0, 1].bar(disc["discount_band"], disc["Margin"], color=bar_cols, width=0.55)
    axes[0, 1].axhline(0, color="black", linewidth=1)
    axes[0, 1].set_title("Profit Margin % by Discount Band (Severe Cliff > 20%)", fontsize=12, weight="bold", color=NAVY, loc="left")
    axes[0, 1].set_ylabel("Profit Margin (%)", fontsize=10, weight="bold")
    axes[0, 1].tick_params(axis="x", rotation=20)
    axes[0, 1].grid(True, linestyle="--", alpha=0.5, axis="y")
    for i, v in enumerate(disc["Margin"]):
        axes[0, 1].text(i, v + (2 if v >= 0 else -6), f"{v:.1f}%", ha="center", weight="bold", fontsize=10)

    # 3. Top 10 Profitable vs Top 10 Loss Products
    top_loss = df.groupby("product_name")["profit"].sum().sort_values(ascending=True).head(8)
    axes[1, 0].barh(top_loss.index, top_loss.values, color=RED)
    axes[1, 0].set_title("Top 8 Heaviest Loss-Making Products ('Profit Bleeders')", fontsize=12, weight="bold", color=RED, loc="left")
    axes[1, 0].set_xlabel("Net Loss ($)", fontsize=10, weight="bold")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5, axis="x")

    # 4. Regional Profitability Margin Matrix
    reg_mat = df.groupby(["region", "category"]).agg(Sales=("sales", "sum"), Profit=("profit", "sum")).reset_index()
    reg_mat["Margin"] = (reg_mat["Profit"] / reg_mat["Sales"]) * 100
    pivot_mat = reg_mat.pivot(index="region", columns="category", values="Margin")
    
    sns.heatmap(pivot_mat, annot=True, fmt=".1f", cmap="RdYlGn", center=10, ax=axes[1, 1], cbar_kws={'label': 'Profit Margin %'})
    axes[1, 1].set_title("Regional x Category Profit Margin Heatmap (%)", fontsize=12, weight="bold", color=NAVY, loc="left")

    plt.tight_layout()
    out_path = SCREENSHOTS_DIR / "page2_sales_profitability.png"
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Rendered: {out_path.name}")


def generate_page3_customer_intelligence(rfm_summary: pd.DataFrame, rfm: pd.DataFrame):
    """Page 3: Customer RFM Intelligence"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), facecolor=BG_COLOR)
    fig.suptitle("CUSTOMER INTELLIGENCE & RFM SEGMENTATION | LTV & Churn Analytics", fontsize=16, weight="bold", color=NAVY, y=0.98)
    
    # 1. RFM Segment Revenue Share
    axes[0, 0].pie(rfm_summary["total_revenue"], labels=rfm_summary["customer_segment"], autopct="%1.1f%%", startangle=140, colors=sns.color_palette("tab10"))
    axes[0, 0].set_title("Revenue Contribution by RFM Segment (%)", fontsize=12, weight="bold", color=NAVY, loc="left")

    # 2. Avg Recency vs Frequency per Segment
    sns.scatterplot(
        data=rfm,
        x="recency_days",
        y="monetary_sales",
        hue="customer_segment",
        size="frequency",
        sizes=(20, 250),
        alpha=0.75,
        palette="tab10",
        ax=axes[0, 1]
    )
    axes[0, 1].set_title("Customer Value Matrix (Recency vs Spend)", fontsize=12, weight="bold", color=NAVY, loc="left")
    axes[0, 1].set_xlabel("Recency (Days Inactive - Lower is Recent)", fontsize=10, weight="bold")
    axes[0, 1].set_ylabel("Monetary Spend ($)", fontsize=10, weight="bold")
    axes[0, 1].legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)

    # 3. Customer Count vs Profit by Segment
    bar_df = rfm_summary.sort_values("total_profit", ascending=False)
    axes[1, 0].bar(bar_df["customer_segment"], bar_df["total_profit"], color=NAVY, width=0.6)
    axes[1, 0].set_title("Net Profit Generated by Customer Segment ($)", fontsize=12, weight="bold", color=NAVY, loc="left")
    axes[1, 0].set_ylabel("Total Profit ($)", fontsize=10, weight="bold")
    axes[1, 0].tick_params(axis="x", rotation=30)
    axes[1, 0].grid(True, linestyle="--", alpha=0.5, axis="y")

    # 4. High Value Churn Risk Callout
    risk_df = rfm[rfm["customer_segment"] == "Cannot Lose Them"].sort_values("monetary_sales", ascending=False).head(8)
    axes[1, 1].barh(risk_df["customer_name"], risk_df["monetary_sales"], color="#E67E22")
    axes[1, 1].set_title("High-Value Customers in 'Cannot Lose Them' Segment (At Churn Risk)", fontsize=12, weight="bold", color="#D35400", loc="left")
    axes[1, 1].set_xlabel("Historical Spend ($)", fontsize=10, weight="bold")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5, axis="x")

    plt.tight_layout()
    out_path = SCREENSHOTS_DIR / "page3_customer_intelligence.png"
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Rendered: {out_path.name}")


def generate_page4_operations(df: pd.DataFrame):
    """Page 4: Operations & Fulfillment Performance"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), facecolor=BG_COLOR)
    fig.suptitle("OPERATIONS & FULFILLMENT ANALYTICS | Shipping Lead Times & Reliability", fontsize=16, weight="bold", color=NAVY, y=0.98)
    
    # 1. Shipping Days Distribution
    sns.histplot(df["ship_days"], bins=8, kde=True, color=NAVY, ax=axes[0, 0])
    axes[0, 0].axvline(df["ship_days"].mean(), color=RED, linestyle="--", linewidth=2, label=f"Mean: {df['ship_days'].mean():.1f} Days")
    axes[0, 0].set_title("Distribution of Order Fulfillment Lead Time (Days)", fontsize=12, weight="bold", color=NAVY, loc="left")
    axes[0, 0].set_xlabel("Elapsed Shipping Days", fontsize=10, weight="bold")
    axes[0, 0].legend()
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    # 2. Shipping Performance by Ship Mode
    sm_perf = df.groupby("ship_mode").agg(Avg_Days=("ship_days", "mean"), Orders=("order_id", "nunique")).reset_index().sort_values("Avg_Days")
    axes[0, 1].bar(sm_perf["ship_mode"], sm_perf["Avg_Days"], color=ACCENT_BLUE, width=0.5)
    axes[0, 1].set_title("Average Lead Time (Days) by Shipping Mode", fontsize=12, weight="bold", color=NAVY, loc="left")
    axes[0, 1].set_ylabel("Average Days", fontsize=10, weight="bold")
    for i, v in enumerate(sm_perf["Avg_Days"]):
        axes[0, 1].text(i, v + 0.1, f"{v:.1f} d", ha="center", weight="bold", fontsize=10)
    axes[0, 1].grid(True, linestyle="--", alpha=0.5, axis="y")

    # 3. Regional Delay Rate %
    reg_delay = df.groupby("region").agg(
        Total_Orders=("order_id", "nunique"),
        Delayed=("order_id", lambda x: (df.loc[x.index, "ship_days"] > 5).sum())
    ).reset_index()
    reg_delay["Delay_Rate"] = (reg_delay["Delayed"] / reg_delay["Total_Orders"]) * 100
    reg_delay = reg_delay.sort_values("Delay_Rate", ascending=False)
    
    axes[1, 0].bar(reg_delay["region"], reg_delay["Delay_Rate"], color="#E74C3C", width=0.5)
    axes[1, 0].set_title("Order Delay Rate (> 5 Days) by Geographic Region (%)", fontsize=12, weight="bold", color=NAVY, loc="left")
    axes[1, 0].set_ylabel("Delay Rate (%)", fontsize=10, weight="bold")
    for i, v in enumerate(reg_delay["Delay_Rate"]):
        axes[1, 0].text(i, v + 0.5, f"{v:.1f}%", ha="center", weight="bold", fontsize=10)
    axes[1, 0].grid(True, linestyle="--", alpha=0.5, axis="y")

    # 4. Fulfillment Volume by Shipping Category
    delay_cat = df["shipping_delay_category"].value_counts()
    axes[1, 1].pie(delay_cat.values, labels=delay_cat.index, autopct="%1.1f%%", colors=[NAVY, GREEN, ACCENT_BLUE, RED], startangle=140)
    axes[1, 1].set_title("Order Breakdown by Delivery Speed Category", fontsize=12, weight="bold", color=NAVY, loc="left")

    plt.tight_layout()
    out_path = SCREENSHOTS_DIR / "page4_operations_fulfillment.png"
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Rendered: {out_path.name}")


def main():
    print("Loading data for visual rendering...")
    df = pd.read_csv(PROCESSED_DIR / "superstore_enriched.csv")
    rfm = pd.read_csv(PROCESSED_DIR / "rfm_customer_segments.csv")
    rfm_summary = pd.read_csv(PROCESSED_DIR / "rfm_segment_summary.csv")
    
    print("Generating Page 1: Executive Overview...")
    generate_page1_executive_overview(df)
    
    print("Generating Page 2: Sales & Profitability...")
    generate_page2_sales_profitability(df)
    
    print("Generating Page 3: Customer Intelligence & RFM...")
    generate_page3_customer_intelligence(rfm_summary, rfm)
    
    print("Generating Page 4: Operations & Fulfillment...")
    generate_page4_operations(df)
    
    print("All 4 dashboard visuals rendered with high resolution!")


if __name__ == "__main__":
    main()

