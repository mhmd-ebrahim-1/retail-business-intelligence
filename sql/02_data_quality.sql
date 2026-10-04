-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 02: SQL Data Quality & Integrity Validation
-- ============================================================================

-- ----------------------------------------------------------------------------
-- CHECK 1: Fact Table Primary Key Uniqueness
-- What it checks: Ensures no duplicate sale_id primary keys in fact_sales.
-- Why it matters: Duplicate PKs corrupt transaction grain and inflate financial metrics.
-- Expected Result: 0 rows.
-- ----------------------------------------------------------------------------
SELECT 
    sale_id, 
    COUNT(*) AS occurrence_count
FROM fact_sales
GROUP BY sale_id
HAVING COUNT(*) > 1;


-- ----------------------------------------------------------------------------
-- CHECK 2: Foreign Key Referential Integrity (Orphan Detection)
-- What it checks: Ensures all foreign keys in fact_sales point to valid dimension rows.
-- Why it matters: Orphan fact rows lead to lost revenue/sales in joined BI reporting.
-- Expected Result: 0 rows for all missing key checks.
-- ----------------------------------------------------------------------------
SELECT 
    'Missing Customer Key' AS issue_type, COUNT(*) AS orphan_count
FROM fact_sales f
LEFT JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE c.customer_key IS NULL
UNION ALL
SELECT 
    'Missing Product Key', COUNT(*)
FROM fact_sales f
LEFT JOIN dim_product p ON f.product_key = p.product_key
WHERE p.product_key IS NULL
UNION ALL
SELECT 
    'Missing Geography Key', COUNT(*)
FROM fact_sales f
LEFT JOIN dim_geography g ON f.geography_key = g.geography_key
WHERE g.geography_key IS NULL
UNION ALL
SELECT 
    'Missing Ship Mode Key', COUNT(*)
FROM fact_sales f
LEFT JOIN dim_ship_mode s ON f.ship_mode_key = s.ship_mode_key
WHERE s.ship_mode_key IS NULL
UNION ALL
SELECT 
    'Missing Order Date Key', COUNT(*)
FROM fact_sales f
LEFT JOIN dim_date d ON f.order_date_key = d.date_key
WHERE d.date_key IS NULL;


-- ----------------------------------------------------------------------------
-- CHECK 3: NULL Value Validation on Critical Business Metrics
-- What it checks: Verifies that core measures and keys are never NULL.
-- Why it matters: NULLs in financial fields lead to erroneous aggregations in BI tools.
-- Expected Result: 0 rows.
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(CASE WHEN sale_id IS NULL THEN 1 END) AS null_sale_id,
    COUNT(CASE WHEN order_id IS NULL THEN 1 END) AS null_order_id,
    COUNT(CASE WHEN sales IS NULL THEN 1 END) AS null_sales,
    COUNT(CASE WHEN quantity IS NULL THEN 1 END) AS null_quantity,
    COUNT(CASE WHEN discount IS NULL THEN 1 END) AS null_discount,
    COUNT(CASE WHEN profit IS NULL THEN 1 END) AS null_profit
FROM fact_sales;


-- ----------------------------------------------------------------------------
-- CHECK 4: Numerical Range & Business Logic Constraints
-- What it checks: Validates that sales is non-negative, quantity is strictly positive,
--                 and discount is bounded within [0.0, 1.0].
-- Why it matters: Invalid numeric ranges distort profitability and operational models.
-- Expected Result: 0 rows.
-- ----------------------------------------------------------------------------
SELECT 
    sale_id,
    order_id,
    sales,
    quantity,
    discount,
    profit
FROM fact_sales
WHERE sales < 0 
   OR quantity <= 0 
   OR discount < 0 
   OR discount > 1.0;


-- ----------------------------------------------------------------------------
-- CHECK 5: Shipping Logic & Temporal Chronology
-- What it checks: Ensures ship_date_key is never chronologically before order_date_key.
-- Why it matters: An order cannot be shipped before it is placed.
-- Expected Result: 0 rows.
-- ----------------------------------------------------------------------------
SELECT 
    sale_id,
    order_id,
    order_date_key,
    ship_date_key,
    ship_days
FROM fact_sales
WHERE ship_date_key < order_date_key
   OR ship_days < 0;


-- ----------------------------------------------------------------------------
-- CHECK 6: Customer Multi-Segment Mapping Consistency
-- What it checks: Verifies that each unique Customer ID maps to a single customer name & segment.
-- Why it matters: Changing customer segments creates inconsistency in cohort analytics.
-- Expected Result: 0 rows.
-- ----------------------------------------------------------------------------
SELECT 
    customer_id, 
    COUNT(DISTINCT segment) AS distinct_segments,
    COUNT(DISTINCT customer_name) AS distinct_names
FROM dim_customer
GROUP BY customer_id
HAVING COUNT(DISTINCT segment) > 1 OR COUNT(DISTINCT customer_name) > 1;

