-- ============================================================================
-- SCRIPT: 03_kpi_analysis.sql
-- PURPOSE: Executive KPIs, Macro Performance Summaries, and Multi-Level Breakdowns
-- ============================================================================

-- Q1. Core Enterprise KPIs
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_unique_customers,
    COUNT(row_id) AS total_order_items,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS overall_profit_margin_pct,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(AVG(discount) * 100, 2) AS average_discount_pct
FROM ecommerce_sales;

-- Q2. Annual Enterprise KPI Trends (YoY Comparison)
SELECT 
    year,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS aov
FROM ecommerce_sales
GROUP BY year
ORDER BY year;

-- Q3. Executive KPI Breakdown by Category
SELECT 
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER(), 2) AS revenue_share_pct
FROM ecommerce_sales
GROUP BY category
ORDER BY total_sales DESC;

-- Q4. Executive KPI Breakdown by Region
SELECT 
    region,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM ecommerce_sales
GROUP BY region
ORDER BY total_sales DESC;

-- Q5. Executive KPI Breakdown by Customer Segment
SELECT 
    segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS aov
FROM ecommerce_sales
GROUP BY segment
ORDER BY total_sales DESC;

-- Q6. Comprehensive Quarterly KPI Dashboard
SELECT 
    year,
    quarter,
    COUNT(DISTINCT order_id) AS quarterly_orders,
    ROUND(SUM(sales), 2) AS quarterly_sales,
    ROUND(SUM(profit), 2) AS quarterly_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS quarterly_margin_pct
FROM ecommerce_sales
GROUP BY year, quarter
ORDER BY year, quarter;
