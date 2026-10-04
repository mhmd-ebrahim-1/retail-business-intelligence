-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 05: Customer Intelligence & Retention Analytics
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Top 15 Most Valuable Customers by Total Lifetime Sales & Profit
-- ----------------------------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_units_bought,
    ROUND(SUM(f.sales), 2) AS lifetime_sales,
    ROUND(SUM(f.profit), 2) AS lifetime_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100.0, 2) AS lifetime_margin_pct,
    ROUND(SUM(f.sales) / COUNT(DISTINCT f.order_id), 2) AS avg_order_value,
    DENSE_RANK() OVER (ORDER BY SUM(f.sales) DESC) AS sales_rank
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY lifetime_sales DESC
LIMIT 15;


-- ----------------------------------------------------------------------------
-- 2. Repeat Customer Rate Analysis
-- Calculates the proportion of customers making repeated purchases.
-- ----------------------------------------------------------------------------
WITH customer_orders AS (
    SELECT 
        customer_key,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_sales
    GROUP BY customer_key
)
SELECT 
    COUNT(*) AS total_unique_customers,
    COUNT(CASE WHEN order_count > 1 THEN 1 END) AS repeat_customers,
    COUNT(CASE WHEN order_count = 1 THEN 1 END) AS single_order_customers,
    ROUND((COUNT(CASE WHEN order_count > 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS repeat_customer_rate_pct
FROM customer_orders;


-- ----------------------------------------------------------------------------
-- 3. New vs. Returning Customers by Year (Cohort Acquisition)
-- ----------------------------------------------------------------------------
WITH customer_first_order AS (
    SELECT 
        customer_key,
        MIN(d.year) AS acquisition_year
    FROM fact_sales f
    JOIN dim_date d ON f.order_date_key = d.date_key
    GROUP BY customer_key
),
yearly_customer_activity AS (
    SELECT 
        d.year,
        f.customer_key,
        cfo.acquisition_year,
        CASE WHEN d.year = cfo.acquisition_year THEN 'New Customer' ELSE 'Returning Customer' END AS customer_type,
        f.sales,
        f.profit
    FROM fact_sales f
    JOIN dim_date d ON f.order_date_key = d.date_key
    JOIN customer_first_order cfo ON f.customer_key = cfo.customer_key
)
SELECT 
    year,
    customer_type,
    COUNT(DISTINCT customer_key) AS active_customer_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100.0, 2) AS profit_margin_pct
FROM yearly_customer_activity
GROUP BY year, customer_type
ORDER BY year, customer_type;


-- ----------------------------------------------------------------------------
-- 4. Customer Order Frequency Distribution Tiering
-- ----------------------------------------------------------------------------
WITH cust_order_tiers AS (
    SELECT 
        c.customer_id,
        COUNT(DISTINCT f.order_id) AS order_count,
        SUM(f.sales) AS total_spend,
        SUM(f.profit) AS total_profit,
        CASE 
            WHEN COUNT(DISTINCT f.order_id) = 1 THEN '1 Order (One-Time)'
            WHEN COUNT(DISTINCT f.order_id) BETWEEN 2 AND 5 THEN '2 - 5 Orders (Occasional)'
            WHEN COUNT(DISTINCT f.order_id) BETWEEN 6 AND 10 THEN '6 - 10 Orders (Regular)'
            ELSE '10+ Orders (Power Buyer)'
        END AS frequency_tier
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_id
)
SELECT 
    frequency_tier,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dim_customer), 2) AS pct_of_customers,
    ROUND(SUM(total_spend), 2) AS total_revenue,
    ROUND(SUM(total_spend) * 100.0 / (SELECT SUM(sales) FROM fact_sales), 2) AS pct_of_revenue,
    ROUND(SUM(total_profit), 2) AS total_profit,
    ROUND(AVG(total_spend / order_count), 2) AS avg_aov_per_tier
FROM cust_order_tiers
GROUP BY frequency_tier
ORDER BY total_revenue DESC;


-- ----------------------------------------------------------------------------
-- 5. High-Value Customers At Risk of Churn
-- Criteria: Lifetime Spend > $3,000 AND No order placed in the last 180 days of dataset.
-- ----------------------------------------------------------------------------
WITH latest_dataset_date AS (
    SELECT MAX(full_date) AS max_date FROM dim_date WHERE date_key IN (SELECT order_date_key FROM fact_sales)
),
customer_recency AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        MAX(d.full_date) AS last_order_date,
        (SELECT max_date FROM latest_dataset_date) AS reference_date,
        ROUND(SUM(f.sales), 2) AS lifetime_spend,
        ROUND(SUM(f.profit), 2) AS lifetime_profit,
        COUNT(DISTINCT f.order_id) AS total_orders
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    JOIN dim_date d ON f.order_date_key = d.date_key
    GROUP BY c.customer_id, c.customer_name, c.segment
)
SELECT 
    customer_id,
    customer_name,
    segment,
    last_order_date,
    total_orders,
    lifetime_spend,
    lifetime_profit
FROM customer_recency
WHERE lifetime_spend > 3000.0
ORDER BY lifetime_spend DESC
LIMIT 15;

