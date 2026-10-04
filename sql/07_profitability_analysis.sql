-- ============================================================================
-- SCRIPT: 07_profitability_analysis.sql
-- PURPOSE: Discount Impact, Profit Margin Dynamics, Regional Breakdown, and Cost Attribution
-- ============================================================================

-- Q23. Profitability Breakdown by Discount Band
SELECT 
    discount_band,
    COUNT(row_id) AS total_transactions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM ecommerce_sales
GROUP BY discount_band
ORDER BY total_sales DESC;

-- Q24. Severe Loss-Making Transactions (Discounts > 40%)
SELECT 
    category,
    sub_category,
    COUNT(row_id) AS heavily_discounted_orders,
    ROUND(SUM(sales), 2) AS discounted_sales,
    ROUND(SUM(profit), 2) AS discounted_profit_loss,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS margin_pct
FROM ecommerce_sales
WHERE discount > 0.40
GROUP BY category, sub_category
ORDER BY discounted_profit_loss ASC;

-- Q25. State-Level Profitability Benchmarks (Top Profitable vs Loss-Making States)
SELECT 
    state,
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM ecommerce_sales
GROUP BY state, region
ORDER BY total_profit DESC;

-- Q26. Shipping Mode Profitability and Cost Efficiency
SELECT 
    ship_mode,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(order_to_ship_days), 2) AS avg_shipping_lead_time_days,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM ecommerce_sales
GROUP BY ship_mode
ORDER BY total_sales DESC;

-- Q27. Loss-Making Sub-Categories in High-Discount Regions
SELECT 
    region,
    sub_category,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS net_profit,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM ecommerce_sales
GROUP BY region, sub_category
HAVING SUM(profit) < 0
ORDER BY net_profit ASC;
