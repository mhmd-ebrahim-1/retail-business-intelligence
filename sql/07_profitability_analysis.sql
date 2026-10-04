-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 07: Profitability & Discount Sensitivity Analysis
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Discount Band Profitability Curve
-- Demonstrates the exact inflection point where discounts destroy profitability.
-- ----------------------------------------------------------------------------
SELECT 
    f.discount_band,
    COUNT(*) AS total_transactions,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.sales) * 100.0 / (SELECT SUM(sales) FROM fact_sales), 2) AS sales_share_pct,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_effective_discount_pct,
    COUNT(CASE WHEN f.profit < 0 THEN 1 END) AS loss_making_transactions,
    ROUND(COUNT(CASE WHEN f.profit < 0 THEN 1 END) * 100.0 / COUNT(*), 2) AS loss_transaction_rate_pct
FROM fact_sales f
GROUP BY f.discount_band
ORDER BY avg_effective_discount_pct ASC;


-- ----------------------------------------------------------------------------
-- 2. Discount Sensitivity by Product Category
-- ----------------------------------------------------------------------------
SELECT 
    p.category,
    f.discount_band,
    COUNT(*) AS transaction_count,
    ROUND(SUM(f.sales), 2) AS category_sales,
    ROUND(SUM(f.profit), 2) AS category_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category, f.discount_band
ORDER BY p.category, category_sales DESC;


-- ----------------------------------------------------------------------------
-- 3. Regional Profit Margin & Discount Comparison
-- ----------------------------------------------------------------------------
SELECT 
    g.region,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS net_profit_margin_pct,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_pct,
    COUNT(CASE WHEN f.profit < 0 THEN 1 END) AS unprofitable_orders,
    ROUND(COUNT(CASE WHEN f.profit < 0 THEN 1 END) * 100.0 / COUNT(*), 2) AS unprofitable_order_rate_pct
FROM fact_sales f
JOIN dim_geography g ON f.geography_key = g.geography_key
GROUP BY g.region
ORDER BY net_profit_margin_pct DESC;


-- ----------------------------------------------------------------------------
-- 4. Heaviest Loss-Making Sub-Categories Breakdown
-- ----------------------------------------------------------------------------
SELECT 
    p.sub_category,
    p.category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_rate_pct,
    COUNT(CASE WHEN f.profit < 0 THEN 1 END) AS losing_transactions,
    ROUND(COUNT(CASE WHEN f.profit < 0 THEN 1 END) * 100.0 / COUNT(*), 2) AS pct_transactions_losing_money
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.sub_category, p.category
HAVING SUM(f.profit) < 0 OR (SUM(f.profit) / SUM(f.sales)) < 0.05
ORDER BY total_profit ASC;


-- ----------------------------------------------------------------------------
-- 5. Shipping Mode Profitability & Cost Impact
-- ----------------------------------------------------------------------------
SELECT 
    s.ship_mode,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS profit_margin_pct,
    ROUND(AVG(f.ship_days), 2) AS avg_delivery_days,
    ROUND(AVG(f.discount) * 100.0, 2) AS avg_discount_pct
FROM fact_sales f
JOIN dim_ship_mode s ON f.ship_mode_key = s.ship_mode_key
GROUP BY s.ship_mode
ORDER BY total_sales DESC;

