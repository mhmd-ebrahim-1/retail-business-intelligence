# Power BI Business Intelligence Architecture

This directory houses the Power BI analytical assets, star schema data model specifications, and comprehensive DAX measure catalog for the **Retail Business Intelligence & Customer Analytics** enterprise solution.

---

## 1. Dashboard Structure & Pages

The dashboard report is structured into 5 dedicated executive and operational reporting views:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    RETAIL BUSINESS INTELLIGENCE SUITE                      │
├─────────────────┬─────────────────┬─────────────────┬──────────────────────┤
│ Page 1:         │ Page 2:         │ Page 3:         │ Page 4 & 5:          │
│ Executive       │ Sales & Margin  │ Customer        │ Regional, Product,   │
│ Overview        │ Dynamics        │ Intelligence    │ & Fulfillment Ops    │
└─────────────────┴─────────────────┴─────────────────┴──────────────────────┘
```

### Page 1: Executive Overview
- **Strategic Purpose:** High-level KPI cockpit for C-suite and department heads to monitor financial pulse.
- **Key Metrics:** Total Revenue, Gross Profit, Blended Margin %, Total Orders, Active Customers, AOV, YoY Growth %.
- **Visuals:** Top KPI Summary Cards, Multi-Year Revenue & Profit Area Chart, Regional Breakdown Donut, Category Contribution Stacked Bar.

### Page 2: Sales & Profitability Analysis
- **Strategic Purpose:** Drill-down analysis into category/sub-category margins, loss-making transactions, and promotional discounting impact.
- **Key Metrics:** Loss-Making Sales Volume, Net Margin Erosion, Discount Band Contribution, High-Margin vs Loss-Making Sub-categories.
- **Visuals:** Discount vs Profit Margin Scatter Plot with trend line, Category Matrix, Loss Waterfall.

### Page 3: Customer Intelligence & RFM Segmentation
- **Strategic Purpose:** Actionable customer lifecycle segmentation, retention benchmarking, and high-value customer tiering.
- **Key Metrics:** Repeat Customer Rate (98.5%), Champions Revenue Share, Revenue-at-Risk %, CLV by Segment.
- **Visuals:** Pareto Customer Revenue Concentration Curve, RFM Segment Distribution Treemap, Top 15 Customer Lifetime Value Leaderboard.

### Page 4: Product & Regional Performance
- **Strategic Purpose:** SKU rationalization matrix and geographic performance diagnostics.
- **Key Metrics:** Star Products vs Problem SKUs, State-Level Profitability, Regional Margin Variance.
- **Visuals:** Product Profitability 4-Quadrant Matrix (Sales vs Margin), State Choropleth Map, Sub-Category Profit Matrix.

### Page 5: Operations & Shipping Logistics
- **Strategic Purpose:** Fulfillment SLA tracking, carrier lead time efficiency, and delivery delay impact on margin.
- **Key Metrics:** Average Shipping Days (3.96 days), On-Time Fulfillment Rate %, Delayed Order Margin Impact.
- **Visuals:** Lead Time by Ship Mode Bar Chart, Delivery Delay Category Distribution, Shipping Cost & Margin Correlation.

---

## 2. Directory Contents

- `retail_analytics.pbix`: Power BI Desktop model file containing configured relationships, measures, and visual canvases.
- `data_model.md`: Detailed technical specification of the Star Schema dimensional model, grain, keys, and cardinalities.
- `dax_measures.md`: Comprehensive catalog of all production DAX measures categorized by business domain.
- `screenshots/`: High-resolution captures of all report pages and visual layouts.
