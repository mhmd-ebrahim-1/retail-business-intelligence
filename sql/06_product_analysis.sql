-- ============================================================================
-- SCRIPT: 06_product_analysis.sql
-- PURPOSE: Product Performance, Profitability Matrix, and Loss-Making SKUs
-- ============================================================================

-- Q18. Top 10 Most Profitable Products
SELECT 
    product_id,
    product_name,
    category,
    sub_category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM ecommerce_sales
GROUP BY product_id, product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 10;

-- Q19. Top 10 Heaviest Loss-Making Products
SELECT 
    product_id,
    product_name,
    category,
    sub_category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS net_loss,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM ecommerce_sales
GROUP BY product_id, product_name, category, sub_category
ORDER BY net_loss ASC
LIMIT 10;

-- Q20. High Sales but Low / Negative Profit Products (Margin Traps)
SELECT 
    product_id,
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM ecommerce_sales
GROUP BY product_id, product_name, category, sub_category
HAVING SUM(sales) > 3000 AND (SUM(profit) / SUM(sales)) < 0.05
ORDER BY total_sales DESC;

-- Q21. Product Profitability Portfolio Matrix (Volume vs Margin Quadrants)
WITH product_stats AS (
    SELECT 
        product_id,
        product_name,
        category,
        sub_category,
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit,
        SUM(profit) / NULLIF(SUM(sales), 0) AS profit_margin
    FROM ecommerce_sales
    GROUP BY product_id, product_name, category, sub_category
),
medians AS (
    SELECT 
        AVG(total_sales) AS threshold_sales,
        AVG(profit_margin) AS threshold_margin
    FROM product_stats
)
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(p.total_sales, 2) AS sales,
    ROUND(p.total_profit, 2) AS profit,
    ROUND(p.profit_margin * 100, 2) AS margin_pct,
    CASE 
        WHEN p.total_sales >= m.threshold_sales AND p.profit_margin >= m.threshold_margin THEN 'Star Product'
        WHEN p.total_sales >= m.threshold_sales AND p.profit_margin < m.threshold_margin THEN 'Volume Driver (Low Margin)'
        WHEN p.total_sales < m.threshold_sales AND p.profit_margin >= m.threshold_margin THEN 'Niche High Margin'
        ELSE 'Underperformer / Problem SKU'
    END AS product_quadrant
FROM product_stats p
CROSS JOIN medians m
ORDER BY p.total_sales DESC;

-- Q22. Most Frequently Ordered Products
SELECT 
    product_id,
    product_name,
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_sales
GROUP BY product_id, product_name, category
ORDER BY total_orders DESC
LIMIT 10;
