-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 04: Sales Performance & Regional Breakdown
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Sales Performance by Category & Sub-Category with Contribution %
-- ----------------------------------------------------------------------------
WITH cat_sales AS (
    SELECT 
        p.category,
        p.sub_category,
        ROUND(SUM(f.sales), 2) AS subcategory_sales,
        ROUND(SUM(f.profit), 2) AS subcategory_profit,
        SUM(f.quantity) AS total_quantity,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct
    FROM fact_sales f
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY p.category, p.sub_category
),
total_calc AS (
    SELECT SUM(sales) AS grand_total_sales FROM fact_sales
)
SELECT 
    c.category,
    c.sub_category,
    c.subcategory_sales,
    ROUND((c.subcategory_sales / t.grand_total_sales) * 100.0, 2) AS pct_of_total_sales,
    c.subcategory_profit,
    c.profit_margin_pct,
    c.total_quantity,
    RANK() OVER (PARTITION BY c.category ORDER BY c.subcategory_sales DESC) AS rank_within_category
FROM cat_sales c
CROSS JOIN total_calc t
ORDER BY c.category, c.subcategory_sales DESC;


-- ----------------------------------------------------------------------------
-- 2. Regional Sales & Profit Performance
-- ----------------------------------------------------------------------------
SELECT 
    g.region,
    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(DISTINCT f.customer_key) AS customer_reach,
    ROUND(SUM(f.sales), 2) AS regional_sales,
    ROUND((SUM(f.sales) / (SELECT SUM(sales) FROM fact_sales)) * 100.0, 2) AS sales_share_pct,
    ROUND(SUM(f.profit), 2) AS regional_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS regional_margin_pct,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_pct
FROM fact_sales f
JOIN dim_geography g ON f.geography_key = g.geography_key
GROUP BY g.region
ORDER BY regional_sales DESC;


-- ----------------------------------------------------------------------------
-- 3. Top 10 States by Sales Revenue and Profitability
-- ----------------------------------------------------------------------------
WITH state_performance AS (
    SELECT 
        g.state,
        g.region,
        ROUND(SUM(f.sales), 2) AS state_sales,
        ROUND(SUM(f.profit), 2) AS state_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS state_margin_pct,
        COUNT(DISTINCT f.order_id) AS order_count
    FROM fact_sales f
    JOIN dim_geography g ON f.geography_key = g.geography_key
    GROUP BY g.state, g.region
)
SELECT 
    state,
    region,
    state_sales,
    state_profit,
    state_margin_pct,
    order_count,
    DENSE_RANK() OVER (ORDER BY state_sales DESC) AS sales_rank
FROM state_performance
ORDER BY state_sales DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- 4. Top 10 Best-Selling Products
-- ----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    SUM(f.quantity) AS total_units_sold,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS margin_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
ORDER BY total_sales DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- 5. Customer Segment Performance by Year
-- ----------------------------------------------------------------------------
SELECT 
    d.year,
    c.segment,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.sales), 2) AS segment_sales,
    ROUND(SUM(f.profit), 2) AS segment_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS segment_margin_pct
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY d.year, c.segment
ORDER BY d.year, segment_sales DESC;

