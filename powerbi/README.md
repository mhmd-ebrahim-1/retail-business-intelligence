# 📊 Power BI Business Intelligence Architecture & Dashboard Guide
**Project:** Retail Business Intelligence & Customer Analytics Platform

---

## 🌟 Executive Overview
This directory contains the production data model architecture, DAX measure library, visual specifications, and layout guidelines for the **Retail BI & Customer Analytics Platform**.

The dashboard is structured into **4 executive-ready pages**:
1. **Executive Overview**: High-level KPI scorecard, 4-year revenue trajectory, regional contribution, and core business health metrics.
2. **Sales & Profitability Analytics**: Deep-dive into category/sub-category margins, loss-making products, discount erosion analysis, and regional profitability matrices.
3. **Customer Intelligence & RFM Segmentation**: Customer lifetime value, repeat purchase rates, 9-tier RFM segmentation, and high-value churn risk monitoring.
4. **Operations & Logistics Performance**: Delivery lead-time distribution, on-time fulfillment rates by region, and shipping mode cost/margin analysis.

---

## 🏗️ Relational Star Schema Architecture
```
                     +-------------------+
                     |     DIM_DATE      |
                     |-------------------|
                     | date_key (PK)     |
                     | full_date         |
                     | year, quarter     |
                     | month, day        |
                     +---------+---------+
                               | 1
                               |
                               | *
+-------------------+ 1       +-------------------+       1 +-------------------+
|   DIM_CUSTOMER    |<--------|    FACT_SALES     |-------->|    DIM_PRODUCT    |
|-------------------| *       |-------------------|       * |-------------------|
| customer_key (PK) |         | sale_id (PK)      |         | product_key (PK)  |
| customer_id       |         | order_id          |         | product_id        |
| customer_name     |         | order_date_key    |         | product_name      |
| segment           |         | ship_date_key     |         | category          |
| total_orders      |         | customer_key      |         | sub_category      |
| total_spend       |         | product_key       |         +-------------------+
+-------------------+         | geography_key     |
                              | ship_mode_key     |
+-------------------+ 1       | sales, quantity   |       1 +-------------------+
|   DIM_GEOGRAPHY   |<--------| discount, profit  |-------->|   DIM_SHIP_MODE   |
|-------------------| *       | ship_days         |       * |-------------------|
| geography_key(PK) |         | profit_margin     |         | ship_mode_key(PK) |
| region, state     |         +-------------------+         | ship_mode         |
| city, postal_code |                                       +-------------------+
+-------------------+
```

---

## 📐 Key Design System & Color Palette
- **Primary Navy:** `#1F4E78` (KPI headers, primary bars, brand anchors)
- **Accent Blue:** `#2F5597` (Secondary series, active slicers)
- **Positive Green:** `#2CA02C` / `#28A745` (Profitable margins, YoY gains)
- **Alert Red:** `#D62728` / `#DC3545` (Negative profit, loss-making subcategories, churn risk)
- **Neutral Background:** `#F8F9FA` (Clean container cards with subtle borders)
- **Typography:** Segoe UI / Calibri (Consistent font hierarchy across all cards and visuals)

---

## 📂 Implementation Files
- [`data_model.md`](data_model.md) - Exact star schema relationships, cardinality, cross-filtering, and column data types.
- [`dax_measures.md`](dax_measures.md) - Complete production DAX formulas for 30+ business measures.

