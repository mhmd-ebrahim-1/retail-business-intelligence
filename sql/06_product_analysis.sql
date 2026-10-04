-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 06: Product Portfolio Performance & Profitability Matrix
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Product Sub-Category Profitability & Volume Performance
-- ----------------------------------------------------------------------------
SELECT 
    p.category,
    p.sub_category,
    COUNT(DISTINCT f.product_key) AS unique_products_sold,
    COUNT(DISTINCT f.order_id) AS order_occurrences,
    SUM(f.quantity) AS total_units_sold,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_pct,
    CASE 
        WHEN SUM(f.profit) < 0 THEN 'Loss-Making Subcategory'
        WHEN (SUM(f.profit) / SUM(f.sales)) < 0.10 THEN 'Low Margin (< 10%)'
        WHEN (SUM(f.profit) / SUM(f.sales)) < 0.25 THEN 'Healthy Margin (10-25%)'
        ELSE 'High Margin (> 25%)'
    END AS profitability_tier
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category, p.sub_category
ORDER BY total_profit DESC;


-- ----------------------------------------------------------------------------
-- 2. Top 10 Most Profitable Products
-- ----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct,
    SUM(f.quantity) AS total_units_sold,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
ORDER BY total_profit DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- 3. Top 10 Heaviest Loss-Making Products ("Profit Bleeders")
-- Products generating massive negative profit.
-- ----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_loss,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct,
    SUM(f.quantity) AS units_sold,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
HAVING SUM(f.profit) < 0
ORDER BY total_loss ASC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- 4. High-Revenue Products with Negative Profit ("False Champions")
-- Products with Sales > $5,000 but negative net profit.
-- ----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_loss,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_applied,
    COUNT(DISTINCT f.order_id) AS order_count
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
HAVING SUM(f.sales) > 3000.0 AND SUM(f.profit) < 0
ORDER BY total_sales DESC;


-- ----------------------------------------------------------------------------
-- 5. Product Profitability Quadrant Matrix
-- Classifies products into 4 strategic quadrants based on Median Sales & Profit.
-- ----------------------------------------------------------------------------
WITH product_summary AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        ROUND(SUM(f.sales), 2) AS product_sales,
        ROUND(SUM(f.profit), 2) AS product_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS margin_pct
    FROM fact_sales f
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    product_id,
    product_name,
    category,
    product_sales,
    product_profit,
    margin_pct,
    CASE 
        WHEN product_sales >= 1000 AND product_profit >= 200 THEN 'Star (High Sales, High Profit)'
        WHEN product_sales >= 1000 AND product_profit < 200 THEN 'Volume Driver / Drain (High Sales, Low/Neg Profit)'
        WHEN product_sales < 1000 AND product_profit >= 200 THEN 'Niche Gem (Low Sales, High Profit)'
        ELSE 'Underperformer (Low Sales, Low Profit)'
    END AS strategic_quadrant
FROM product_summary
ORDER BY product_sales DESC;

