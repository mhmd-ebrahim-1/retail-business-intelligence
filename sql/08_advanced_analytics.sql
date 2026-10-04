-- ============================================================================
-- SCRIPT: 08_advanced_analytics.sql
-- PURPOSE: Advanced Business Intelligence, Cohort Analysis, Window Functions,
--          and Predictive Risk Identification (Queries 28 - 40)
-- ============================================================================

-- Q28. Customer Acquisition Cohort Analysis (First Purchase Year)
WITH customer_cohort AS (
    SELECT 
        customer_id,
        MIN(year) AS acquisition_year
    FROM ecommerce_sales
    GROUP BY customer_id
)
SELECT 
    c.acquisition_year,
    s.year AS transaction_year,
    COUNT(DISTINCT s.customer_id) AS active_cohort_customers,
    ROUND(SUM(s.sales), 2) AS cohort_revenue,
    ROUND(SUM(s.profit), 2) AS cohort_profit
FROM ecommerce_sales s
JOIN customer_cohort c ON s.customer_id = c.customer_id
GROUP BY c.acquisition_year, s.year
ORDER BY c.acquisition_year, s.year;

-- Q29. Customer Lifetime Value (CLV) Estimation by Segment
WITH customer_stats AS (
    SELECT 
        customer_id,
        segment,
        MIN(order_date) AS first_order,
        MAX(order_date) AS last_order,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(sales) AS total_revenue,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY customer_id, segment
)
SELECT 
    segment,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(total_orders), 1) AS avg_orders_per_customer,
    ROUND(AVG(total_revenue), 2) AS avg_clv_revenue,
    ROUND(AVG(total_profit), 2) AS avg_clv_profit,
    ROUND(AVG(total_profit) / AVG(total_revenue) * 100, 2) AS clv_margin_pct
FROM customer_stats
GROUP BY segment;

-- Q30. Revenue Growth Acceleration / Deceleration (2nd Derivative)
WITH monthly_sales AS (
    SELECT 
        year_month,
        SUM(sales) AS sales
    FROM ecommerce_sales
    GROUP BY year_month
),
monthly_growth AS (
    SELECT 
        year_month,
        sales,
        sales - LAG(sales, 1) OVER (ORDER BY year_month) AS mom_diff
    FROM monthly_sales
)
SELECT 
    year_month,
    ROUND(sales, 2) AS sales,
    ROUND(mom_diff, 2) AS monthly_sales_change,
    ROUND(mom_diff - LAG(mom_diff, 1) OVER (ORDER BY year_month), 2) AS growth_acceleration
FROM monthly_growth
ORDER BY year_month;

-- Q31. Category Cross-Sell / Co-Occurrence in Multi-Item Orders
WITH order_categories AS (
    SELECT DISTINCT 
        order_id,
        category
    FROM ecommerce_sales
)
SELECT 
    c1.category AS category_a,
    c2.category AS category_b,
    COUNT(DISTINCT c1.order_id) AS co_occurrence_orders
FROM order_categories c1
JOIN order_categories c2 
    ON c1.order_id = c2.order_id AND c1.category < c2.category
GROUP BY c1.category, c2.category
ORDER BY co_occurrence_orders DESC;

-- Q32. Rolling 12-Month Trailing Revenue & Profit
WITH monthly_totals AS (
    SELECT 
        year_month,
        SUM(sales) AS sales,
        SUM(profit) AS profit
    FROM ecommerce_sales
    GROUP BY year_month
)
SELECT 
    year_month,
    ROUND(sales, 2) AS month_sales,
    ROUND(SUM(sales) OVER (
        ORDER BY year_month 
        ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
    ), 2) AS trailing_12m_revenue,
    ROUND(SUM(profit) OVER (
        ORDER BY year_month 
        ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
    ), 2) AS trailing_12m_profit
FROM monthly_totals
ORDER BY year_month;

-- Q33. Shipping Fulfillment Lead Time Impact on Margin & Discount
SELECT 
    shipping_delay_category,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM ecommerce_sales
GROUP BY shipping_delay_category
ORDER BY total_sales DESC;

-- Q34. Customer Churn Risk Flagging (Inactive > 180 Days with High Prior Spend)
WITH customer_recency AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        MAX(order_date) AS last_order_date,
        DATEDIFF(day, MAX(order_date), '2017-12-31') AS days_since_last_order,
        SUM(sales) AS total_spend,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY customer_id, customer_name, segment
)
SELECT 
    customer_id,
    customer_name,
    segment,
    last_order_date,
    days_since_last_order,
    ROUND(total_spend, 2) AS historical_spend,
    ROUND(total_profit, 2) AS historical_profit,
    CASE 
        WHEN days_since_last_order > 365 THEN 'High Churn Risk (Dormant > 1 Yr)'
        WHEN days_since_last_order > 180 THEN 'Medium Churn Risk (Inactive > 6 Mos)'
        ELSE 'Active'
    END AS churn_status
FROM customer_recency
WHERE total_spend > 2500 AND days_since_last_order > 180
ORDER BY total_spend DESC;

-- Q35. Discount Price Elasticity Proxy (Volume vs Discount Elasticity)
SELECT 
    sub_category,
    ROUND(AVG(CASE WHEN discount = 0 THEN sales_per_quantity END), 2) AS avg_full_price_unit,
    ROUND(AVG(CASE WHEN discount > 0 THEN sales_per_quantity END), 2) AS avg_discounted_unit,
    SUM(CASE WHEN discount = 0 THEN quantity ELSE 0 END) AS full_price_units_sold,
    SUM(CASE WHEN discount > 0 THEN quantity ELSE 0 END) AS discounted_units_sold,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS overall_margin_pct
FROM ecommerce_sales
GROUP BY sub_category
ORDER BY discounted_units_sold DESC;

-- Q36. Multi-Year Customer Retention Matrix
WITH yearly_customers AS (
    SELECT DISTINCT 
        customer_id,
        year
    FROM ecommerce_sales
)
SELECT 
    y1.year AS base_year,
    COUNT(DISTINCT y1.customer_id) AS base_customers,
    COUNT(DISTINCT y2.customer_id) AS retained_next_year,
    ROUND(COUNT(DISTINCT y2.customer_id) * 100.0 / COUNT(DISTINCT y1.customer_id), 2) AS next_year_retention_rate_pct
FROM yearly_customers y1
LEFT JOIN yearly_customers y2 
    ON y1.customer_id = y2.customer_id AND y1.year + 1 = y2.year
GROUP BY y1.year
ORDER BY y1.year;

-- Q37. Customer Profit Contribution Quintiles
WITH customer_profits AS (
    SELECT 
        customer_id,
        customer_name,
        SUM(profit) AS total_profit,
        NTILE(5) OVER (ORDER BY SUM(profit) DESC) AS profit_quintile
    FROM ecommerce_sales
    GROUP BY customer_id, customer_name
)
SELECT 
    profit_quintile,
    COUNT(*) AS customers_in_tier,
    ROUND(SUM(total_profit), 2) AS tier_profit,
    ROUND(SUM(total_profit) * 100.0 / SUM(SUM(total_profit)) OVER (), 2) AS pct_of_enterprise_profit
FROM customer_profits
GROUP BY profit_quintile
ORDER BY profit_quintile;

-- Q38. Geographic Density & Regional Profit Efficiency
SELECT 
    region,
    COUNT(DISTINCT state) AS states_covered,
    COUNT(DISTINCT city) AS cities_covered,
    COUNT(DISTINCT customer_id) AS customer_base,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / COUNT(DISTINCT customer_id), 2) AS profit_per_customer
FROM ecommerce_sales
GROUP BY region
ORDER BY total_profit DESC;

-- Q39. Order Item Density & Cart Size Analysis
WITH order_cart AS (
    SELECT 
        order_id,
        COUNT(row_id) AS items_in_cart,
        SUM(sales) AS order_value,
        SUM(profit) AS order_profit
    FROM ecommerce_sales
    GROUP BY order_id
)
SELECT 
    items_in_cart,
    COUNT(order_id) AS order_frequency,
    ROUND(AVG(order_value), 2) AS avg_cart_value,
    ROUND(AVG(order_profit), 2) AS avg_cart_profit,
    ROUND(AVG(order_profit) / AVG(order_value) * 100, 2) AS cart_profit_margin_pct
FROM order_cart
GROUP BY items_in_cart
ORDER BY items_in_cart;

-- Q40. Enterprise Loss-Eradication Opportunity Simulation
SELECT 
    COUNT(row_id) AS current_total_transactions,
    ROUND(SUM(sales), 2) AS current_total_revenue,
    ROUND(SUM(profit), 2) AS current_total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS current_margin_pct,
    -- Scenario: Eliminate transactions with discount > 30%
    COUNT(CASE WHEN discount <= 0.30 THEN row_id END) AS optimized_transactions,
    ROUND(SUM(CASE WHEN discount <= 0.30 THEN sales ELSE 0 END), 2) AS simulated_revenue,
    ROUND(SUM(CASE WHEN discount <= 0.30 THEN profit ELSE 0 END), 2) AS simulated_profit,
    ROUND(SUM(CASE WHEN discount <= 0.30 THEN profit ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN discount <= 0.30 THEN sales ELSE 0 END), 0) * 100, 2) AS simulated_margin_pct,
    ROUND(SUM(CASE WHEN discount <= 0.30 THEN profit ELSE 0 END) - SUM(profit), 2) AS potential_profit_gain
FROM ecommerce_sales;
