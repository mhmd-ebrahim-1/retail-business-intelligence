-- ============================================================================
-- SCRIPT: 02_data_quality.sql
-- PURPOSE: Automated Data Quality Auditing, Integrity Rules, and Outlier Checks
-- ============================================================================

-- Q1. Comprehensive NULL and Empty Value Scan
SELECT 
    COUNT(*) AS total_records,
    SUM(CASE WHEN row_id IS NULL THEN 1 ELSE 0 END) AS null_row_ids,
    SUM(CASE WHEN order_id IS NULL OR order_id = '' THEN 1 ELSE 0 END) AS null_order_ids,
    SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) AS null_order_dates,
    SUM(CASE WHEN ship_date IS NULL THEN 1 ELSE 0 END) AS null_ship_dates,
    SUM(CASE WHEN customer_id IS NULL OR customer_id = '' THEN 1 ELSE 0 END) AS null_customer_ids,
    SUM(CASE WHEN product_id IS NULL OR product_id = '' THEN 1 ELSE 0 END) AS null_product_ids,
    SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END) AS null_quantity,
    SUM(CASE WHEN discount IS NULL THEN 1 ELSE 0 END) AS null_discounts,
    SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS null_profits
FROM ecommerce_sales;

-- Q2. Duplicate Row and Duplicate Natural Key Verification
SELECT 
    row_id,
    COUNT(*) AS duplicate_count
FROM ecommerce_sales
GROUP BY row_id
HAVING COUNT(*) > 1;

-- Q3. Date Sequence Integrity (Orders where Ship Date is earlier than Order Date)
SELECT 
    order_id,
    order_date,
    ship_date,
    order_to_ship_days
FROM ecommerce_sales
WHERE ship_date < order_date OR order_to_ship_days < 0;

-- Q4. Numerical Domain Constraint Checks (Negative Sales, Zero Quantity, Invalid Discount)
SELECT 
    row_id,
    order_id,
    sales,
    quantity,
    discount,
    profit
FROM ecommerce_sales
WHERE sales <= 0 
   OR quantity <= 0 
   OR discount < 0 
   OR discount > 1.0;

-- Q5. Outlier Detection on Sales using IQR / Z-Score Principles
WITH stats AS (
    SELECT 
        AVG(sales) AS avg_sales,
        STDEV(sales) AS std_sales
    FROM ecommerce_sales
)
SELECT 
    e.row_id,
    e.order_id,
    e.product_name,
    e.sales,
    e.profit,
    ROUND((e.sales - s.avg_sales) / NULLIF(s.std_sales, 0), 2) AS z_score
FROM ecommerce_sales e
CROSS JOIN stats s
WHERE (e.sales - s.avg_sales) / NULLIF(s.std_sales, 0) > 3.0
ORDER BY e.sales DESC;

-- Q6. Data Quality Scorecard Summary
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS total_unique_orders,
    COUNT(DISTINCT customer_id) AS total_unique_customers,
    COUNT(DISTINCT product_id) AS total_unique_products,
    MIN(order_date) AS min_order_date,
    MAX(order_date) AS max_order_date,
    SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS loss_making_row_count,
    ROUND(SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS loss_making_row_pct
FROM ecommerce_sales;
