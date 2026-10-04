-- ============================================================================
-- SCRIPT: 05_customer_analysis.sql
-- PURPOSE: Customer Segmentation, RFM Scoring, Pareto Distribution, and Cohorts
-- ============================================================================

-- Q13. Top 10 Customers Ranked by Lifetime Revenue
SELECT 
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    DENSE_RANK() OVER (ORDER BY SUM(sales) DESC) AS revenue_rank
FROM ecommerce_sales
GROUP BY customer_id, customer_name, segment
ORDER BY total_revenue DESC
LIMIT 10;

-- Q14. Customer Pareto Analysis (Cumulative 80/20 Contribution)
WITH customer_revenue AS (
    SELECT 
        customer_id,
        customer_name,
        SUM(sales) AS customer_sales
    FROM ecommerce_sales
    GROUP BY customer_id, customer_name
),
ranked_customers AS (
    SELECT 
        customer_id,
        customer_name,
        customer_sales,
        ROW_NUMBER() OVER (ORDER BY customer_sales DESC) AS cust_rank,
        COUNT(*) OVER () AS total_customers,
        SUM(customer_sales) OVER (ORDER BY customer_sales DESC) AS cumulative_sales,
        SUM(customer_sales) OVER () AS total_sales
    FROM customer_revenue
)
SELECT 
    customer_id,
    customer_name,
    ROUND(customer_sales, 2) AS customer_sales,
    cust_rank,
    ROUND(cust_rank * 100.0 / total_customers, 2) AS cumulative_customer_pct,
    ROUND(cumulative_sales * 100.0 / total_sales, 2) AS cumulative_sales_pct
FROM ranked_customers
ORDER BY cust_rank;

-- Q15. Customer RFM Calculation and Scoring
WITH customer_rfm_base AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        DATEDIFF(day, MAX(order_date), '2017-12-31') AS recency_days,
        COUNT(DISTINCT order_id) AS frequency_orders,
        SUM(sales) AS monetary_spend,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY customer_id, customer_name, segment
),
rfm_scores AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        recency_days,
        frequency_orders,
        monetary_spend,
        total_profit,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score, -- lower days = higher score
        NTILE(5) OVER (ORDER BY frequency_orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_spend ASC) AS m_score
    FROM customer_rfm_base
)
SELECT 
    customer_id,
    customer_name,
    segment,
    recency_days,
    frequency_orders,
    ROUND(monetary_spend, 2) AS monetary_spend,
    r_score,
    f_score,
    m_score,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score IN (2, 3) THEN 'Potential Loyalists'
        WHEN r_score >= 4 AND f_score = 1 THEN 'New Customers'
        WHEN r_score = 3 AND f_score IN (1, 2) THEN 'Promising'
        WHEN r_score IN (2, 3) AND f_score IN (2, 3) THEN 'Need Attention'
        WHEN r_score IN (2, 3) AND f_score = 1 THEN 'About to Sleep'
        WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 4 THEN 'Cannot Lose Them'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score IN (1, 2) THEN 'Hibernating'
        ELSE 'Lost'
    END AS rfm_segment
FROM rfm_scores
ORDER BY monetary_spend DESC;

-- Q16. Repeat Customer Purchase Rate
WITH customer_order_counts AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM ecommerce_sales
    GROUP BY customer_id
)
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END) AS single_order_customers,
    ROUND(SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS repeat_customer_rate_pct
FROM customer_order_counts;

-- Q17. Top Loss-Making Customer Accounts
SELECT 
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_loss,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_received
FROM ecommerce_sales
GROUP BY customer_id, customer_name, segment
HAVING SUM(profit) < 0
ORDER BY total_loss ASC
LIMIT 15;
