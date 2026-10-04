-- ============================================================================
-- SCRIPT: 04_sales_analysis.sql
-- PURPOSE: Detailed Revenue Analysis, Growth Trends, Seasonality, and Moving Averages
-- ============================================================================

-- Q7. Monthly Revenue Trends and Month-over-Month (MoM) Growth
WITH monthly_metrics AS (
    SELECT 
        year_month,
        year,
        month,
        ROUND(SUM(sales), 2) AS monthly_sales,
        ROUND(SUM(profit), 2) AS monthly_profit
    FROM ecommerce_sales
    GROUP BY year_month, year, month
)
SELECT 
    year_month,
    monthly_sales,
    monthly_profit,
    LAG(monthly_sales, 1) OVER (ORDER BY year_month) AS prev_month_sales,
    ROUND((monthly_sales - LAG(monthly_sales, 1) OVER (ORDER BY year_month)) / 
          NULLIF(LAG(monthly_sales, 1) OVER (ORDER BY year_month), 0) * 100, 2) AS mom_sales_growth_pct
FROM monthly_metrics
ORDER BY year_month;

-- Q8. Year-over-Year (YoY) Sales Growth by Month
WITH monthly_data AS (
    SELECT 
        year,
        month,
        month_name,
        SUM(sales) AS current_year_sales
    FROM ecommerce_sales
    GROUP BY year, month, month_name
)
SELECT 
    m1.year,
    m1.month,
    m1.month_name,
    ROUND(m1.current_year_sales, 2) AS sales,
    ROUND(m2.current_year_sales, 2) AS prior_year_sales,
    ROUND((m1.current_year_sales - m2.current_year_sales) / NULLIF(m2.current_year_sales, 0) * 100, 2) AS yoy_sales_growth_pct
FROM monthly_data m1
LEFT JOIN monthly_data m2 
    ON m1.month = m2.month AND m1.year = m2.year + 1
ORDER BY m1.year, m1.month;

-- Q9. Cumulative Running Total Sales by Year
SELECT 
    year_month,
    year,
    month,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(SUM(sales)) OVER (PARTITION BY year ORDER BY month), 2) AS ytd_running_sales
FROM ecommerce_sales
GROUP BY year_month, year, month
ORDER BY year_month;

-- Q10. 3-Month Moving Average of Sales
WITH monthly_sales AS (
    SELECT 
        year_month,
        SUM(sales) AS total_sales
    FROM ecommerce_sales
    GROUP BY year_month
)
SELECT 
    year_month,
    ROUND(total_sales, 2) AS monthly_sales,
    ROUND(AVG(total_sales) OVER (
        ORDER BY year_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS sales_3m_moving_avg
FROM monthly_sales
ORDER BY year_month;

-- Q11. Day of Week Sales Pattern
SELECT 
    day_of_week,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS avg_sales_per_item
FROM ecommerce_sales
GROUP BY day_of_week
ORDER BY total_sales DESC;

-- Q12. Sub-Category Contribution to Parent Category Revenue
SELECT 
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS subcategory_sales,
    ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER (PARTITION BY category), 2) AS category_share_pct,
    ROUND(SUM(profit), 2) AS subcategory_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM ecommerce_sales
GROUP BY category, sub_category
ORDER BY category, subcategory_sales DESC;
