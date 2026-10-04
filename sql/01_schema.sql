-- ============================================================================
-- SCRIPT: 01_schema.sql
-- PURPOSE: Star Schema DDL, Analytical Table DDL, and View Definitions
-- DIALECT: ANSI SQL / Microsoft SQL Server Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. DENORMALIZED ANALYTICAL BASE TABLE
-- ----------------------------------------------------------------------------
CREATE TABLE ecommerce_sales (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code INT,
    region VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    sales DECIMAL(12, 4) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(6, 4) NOT NULL,
    profit DECIMAL(12, 4) NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    year_month VARCHAR(7),
    week INT,
    day_of_week VARCHAR(20),
    order_to_ship_days INT,
    profit_margin DECIMAL(8, 4),
    sales_per_quantity DECIMAL(12, 4),
    discount_band VARCHAR(50)
);

-- ----------------------------------------------------------------------------
-- 2. STAR SCHEMA DIMENSIONAL MODEL TABLES
-- ----------------------------------------------------------------------------

-- DIMENSION: CUSTOMER
CREATE TABLE dim_customer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL
);

-- DIMENSION: PRODUCT
CREATE TABLE dim_product (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    CONSTRAINT uq_dim_product UNIQUE (product_id, product_name)
);

-- DIMENSION: LOCATION / GEOGRAPHY
CREATE TABLE dim_location (
    location_key INT IDENTITY(1,1) PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    postal_code INT
);

-- DIMENSION: SHIP MODE
CREATE TABLE dim_ship_mode (
    ship_mode_key INT IDENTITY(1,1) PRIMARY KEY,
    ship_mode VARCHAR(50) NOT NULL UNIQUE
);

-- DIMENSION: DATE
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY, -- Format: YYYYMMDD
    full_date DATE NOT NULL UNIQUE,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    year_month VARCHAR(7) NOT NULL,
    week_of_year INT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    day_of_month INT NOT NULL,
    is_weekend BIT NOT NULL
);

-- FACT TABLE: SALES TRANSACTIONS
CREATE TABLE fact_sales (
    sales_fact_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    row_id INT NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    order_date_key INT NOT NULL,
    ship_date_key INT NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    location_key INT NOT NULL,
    ship_mode_key INT NOT NULL,
    sales DECIMAL(12, 4) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(6, 4) NOT NULL,
    profit DECIMAL(12, 4) NOT NULL,
    order_to_ship_days INT NOT NULL,
    profit_margin DECIMAL(8, 4) NOT NULL,
    FOREIGN KEY (order_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (ship_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key),
    FOREIGN KEY (ship_mode_key) REFERENCES dim_ship_mode(ship_mode_key)
);

-- ----------------------------------------------------------------------------
-- 3. ANALYTICAL VIEWS
-- ----------------------------------------------------------------------------

-- View: Executive Order Summary
CREATE OR REPLACE VIEW vw_order_summary AS
SELECT 
    order_id,
    order_date,
    customer_id,
    customer_name,
    segment,
    region,
    state,
    COUNT(row_id) AS total_items,
    SUM(quantity) AS total_units,
    SUM(sales) AS order_revenue,
    SUM(profit) AS order_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS order_profit_margin_pct,
    AVG(discount) AS average_discount
FROM ecommerce_sales
GROUP BY 
    order_id, order_date, customer_id, customer_name, segment, region, state;

-- View: Customer Lifetime Summary
CREATE OR REPLACE VIEW vw_customer_lifetime AS
SELECT 
    customer_id,
    customer_name,
    segment,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS latest_order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(sales) AS lifetime_revenue,
    SUM(profit) AS lifetime_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS lifetime_margin_pct
FROM ecommerce_sales
GROUP BY customer_id, customer_name, segment;
