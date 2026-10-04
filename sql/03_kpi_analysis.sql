-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 03: Executive Business KPIs & YoY Growth Analysis
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. High-Level Executive KPI Scorecard
-- ----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100.0, 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_key) AS total_customers,
    COUNT(DISTINCT product_key) AS total_unique_products,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(CAST(SUM(quantity) AS FLOAT) / COUNT(DISTINCT order_id), 2) AS avg_items_per_order
FROM fact_sales;


-- ----------------------------------------------------------------------------
-- 2. Annual Performance & Year-over-Year (YoY) Growth
-- Uses LAG window function to compare current year vs prior year.
-- ----------------------------------------------------------------------------
WITH annual_sales AS (
    SELECT 
        d.year,
        COUNT(DISTINCT f.order_id) AS total_orders,
        COUNT(DISTINCT f.customer_key) AS active_customers,
        ROUND(SUM(f.sales), 2) AS annual_sales,
        ROUND(SUM(f.profit), 2) AS annual_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct
    FROM fact_sales f
    JOIN dim_date d ON f.order_date_key = d.date_key
    GROUP BY d.year
)
SELECT 
    year,
    total_orders,
    active_customers,
    annual_sales,
    LAG(annual_sales, 1) OVER (ORDER BY year) AS prior_year_sales,
    ROUND(((annual_sales - LAG(annual_sales, 1) OVER (ORDER BY year)) / 
           LAG(annual_sales, 1) OVER (ORDER BY year)) * 100.0, 2) AS yoy_sales_growth_pct,
    annual_profit,
    LAG(annual_profit, 1) OVER (ORDER BY year) AS prior_year_profit,
    ROUND(((annual_profit - LAG(annual_profit, 1) OVER (ORDER BY year)) / 
           LAG(annual_profit, 1) OVER (ORDER BY year)) * 100.0, 2) AS yoy_profit_growth_pct,
    profit_margin_pct
FROM annual_sales
ORDER BY year;


-- ----------------------------------------------------------------------------
-- 3. Quarterly Performance Trend with QoQ & YoY Metrics
-- ----------------------------------------------------------------------------
WITH quarterly_metrics AS (
    SELECT 
        d.year,
        d.quarter,
        d.year || '-' || d.quarter AS year_quarter,
        ROUND(SUM(f.sales), 2) AS quarterly_sales,
        ROUND(SUM(f.profit), 2) AS quarterly_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS quarterly_margin_pct,
        COUNT(DISTINCT f.order_id) AS order_volume
    FROM fact_sales f
    JOIN dim_date d ON f.order_date_key = d.date_key
    GROUP BY d.year, d.quarter, d.year || '-' || d.quarter
)
SELECT 
    year_quarter,
    order_volume,
    quarterly_sales,
    LAG(quarterly_sales, 1) OVER (ORDER BY year, quarter) AS prior_quarter_sales,
    ROUND(((quarterly_sales - LAG(quarterly_sales, 1) OVER (ORDER BY year, quarter)) / 
           LAG(quarterly_sales, 1) OVER (ORDER BY year, quarter)) * 100.0, 2) AS qoq_sales_growth_pct,
    LAG(quarterly_sales, 4) OVER (ORDER BY year, quarter) AS prior_year_same_quarter_sales,
    ROUND(((quarterly_sales - LAG(quarterly_sales, 4) OVER (ORDER BY year, quarter)) / 
           LAG(quarterly_sales, 4) OVER (ORDER BY year, quarter)) * 100.0, 2) AS yoy_quarterly_growth_pct,
    quarterly_profit,
    quarterly_margin_pct
FROM quarterly_metrics
ORDER BY year_quarter;


-- ----------------------------------------------------------------------------
-- 4. Monthly Trend & 3-Month Moving Average
-- ----------------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        d.year_month,
        ROUND(SUM(f.sales), 2) AS monthly_sales,
        ROUND(SUM(f.profit), 2) AS monthly_profit,
        COUNT(DISTINCT f.order_id) AS order_count
    FROM fact_sales f
    JOIN dim_date d ON f.order_date_key = d.date_key
    GROUP BY d.year_month
)
SELECT 
    year_month,
    order_count,
    monthly_sales,
    ROUND(AVG(monthly_sales) OVER (
        ORDER BY year_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS sales_3m_moving_avg,
    monthly_profit,
    ROUND(SUM(monthly_sales) OVER (
        PARTITION BY SUBSTR(year_month, 1, 4) 
        ORDER BY year_month
    ), 2) AS ytd_cumulative_sales
FROM monthly_sales
ORDER BY year_month;

