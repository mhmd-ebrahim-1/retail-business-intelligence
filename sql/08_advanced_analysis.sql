-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 08: Advanced SQL Analytics (Pareto 80/20, Cohorts, Running Totals)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Customer Pareto Analysis (80/20 Rule on Revenue)
-- Identifies the exact cumulative distribution of revenue across customers.
-- ----------------------------------------------------------------------------
WITH customer_revenue AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        ROUND(SUM(f.sales), 2) AS customer_sales
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_id, c.customer_name
),
cumulative_rev AS (
    SELECT 
        customer_id,
        customer_name,
        customer_sales,
        ROW_NUMBER() OVER (ORDER BY customer_sales DESC) AS customer_rank,
        COUNT(*) OVER () AS total_customers_count,
        SUM(customer_sales) OVER (ORDER BY customer_sales DESC) AS running_sales,
        SUM(customer_sales) OVER () AS grand_total_sales
    FROM customer_revenue
)
SELECT 
    customer_id,
    customer_name,
    customer_sales,
    customer_rank,
    ROUND((customer_rank * 100.0 / total_customers_count), 2) AS cumulative_customer_pct,
    running_sales,
    ROUND((running_sales * 100.0 / grand_total_sales), 2) AS cumulative_revenue_pct,
    CASE 
        WHEN (running_sales * 100.0 / grand_total_sales) <= 80.0 THEN 'Top 80% Revenue Driver'
        ELSE 'Long Tail (Remaining 20%)'
    END AS pareto_segment
FROM cumulative_rev
ORDER BY customer_sales DESC
LIMIT 25;


-- ----------------------------------------------------------------------------
-- 2. Product Profit Pareto Analysis (80/20 Rule on Profit)
-- Identifies the top products responsible for driving 80% of total profit.
-- ----------------------------------------------------------------------------
WITH product_profit AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        ROUND(SUM(f.profit), 2) AS product_profit
    FROM fact_sales f
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY p.product_id, p.product_name, p.category
    HAVING SUM(f.profit) > 0
),
cumulative_profit AS (
    SELECT 
        product_id,
        product_name,
        category,
        product_profit,
        ROW_NUMBER() OVER (ORDER BY product_profit DESC) AS profit_rank,
        COUNT(*) OVER () AS total_profitable_products,
        SUM(product_profit) OVER (ORDER BY product_profit DESC) AS running_profit,
        SUM(product_profit) OVER () AS total_positive_profit
    FROM product_profit
)
SELECT 
    product_id,
    product_name,
    category,
    product_profit,
    profit_rank,
    ROUND((profit_rank * 100.0 / total_profitable_products), 2) AS cumulative_product_pct,
    running_profit,
    ROUND((running_profit * 100.0 / total_positive_profit), 2) AS cumulative_profit_pct
FROM cumulative_profit
WHERE (running_profit * 100.0 / total_positive_profit) <= 80.0
ORDER BY product_profit DESC
LIMIT 20;


-- ----------------------------------------------------------------------------
-- 3. Operational Shipping Delay Analysis by Region
-- Analyzes average lead times and identifies excessive delays (> 5 days).
-- ----------------------------------------------------------------------------
SELECT 
    g.region,
    s.ship_mode,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(AVG(f.ship_days), 2) AS avg_ship_days,
    MIN(f.ship_days) AS min_ship_days,
    MAX(f.ship_days) AS max_ship_days,
    COUNT(CASE WHEN f.ship_days > 5 THEN 1 END) AS delayed_orders_count,
    ROUND(COUNT(CASE WHEN f.ship_days > 5 THEN 1 END) * 100.0 / COUNT(DISTINCT f.order_id), 2) AS delay_rate_pct
FROM fact_sales f
JOIN dim_geography g ON f.geography_key = g.geography_key
JOIN dim_ship_mode s ON f.ship_mode_key = s.ship_mode_key
GROUP BY g.region, s.ship_mode
ORDER BY g.region, avg_ship_days DESC;


-- ----------------------------------------------------------------------------
-- 4. Cumulative Year-over-Year Running Sales & Profit Tracking
-- ----------------------------------------------------------------------------
WITH monthly_perf AS (
    SELECT 
        d.year,
        d.month,
        d.year_month,
        ROUND(SUM(f.sales), 2) AS monthly_sales,
        ROUND(SUM(f.profit), 2) AS monthly_profit
    FROM fact_sales f
    JOIN dim_date d ON f.order_date_key = d.date_key
    GROUP BY d.year, d.month, d.year_month
)
SELECT 
    year,
    month,
    year_month,
    monthly_sales,
    SUM(monthly_sales) OVER (PARTITION BY year ORDER BY month) AS ytd_running_sales,
    monthly_profit,
    SUM(monthly_profit) OVER (PARTITION BY year ORDER BY month) AS ytd_running_profit,
    ROUND((SUM(monthly_profit) OVER (PARTITION BY year ORDER BY month) / 
           SUM(monthly_sales) OVER (PARTITION BY year ORDER BY month)) * 100.0, 2) AS ytd_running_margin_pct
FROM monthly_perf
ORDER BY year, month;

