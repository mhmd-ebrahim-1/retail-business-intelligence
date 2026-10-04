-- ============================================================================
-- RETAIL BUSINESS INTELLIGENCE & CUSTOMER ANALYTICS PLATFORM
-- SCRIPT 01: Relational Schema & Dimensional Star Schema Definition
-- Compatible with: PostgreSQL & SQLite
-- ============================================================================

-- Drop tables if they already exist to enable clean recreation
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_geography;
DROP TABLE IF EXISTS dim_ship_mode;

-- ----------------------------------------------------------------------------
-- 1. DIM_SHIP_MODE (Shipping Mode Dimension)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_ship_mode (
    ship_mode_key INTEGER PRIMARY KEY,
    ship_mode VARCHAR(50) NOT NULL UNIQUE
);

-- ----------------------------------------------------------------------------
-- 2. DIM_GEOGRAPHY (Geographical Dimension)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_geography (
    geography_key INTEGER PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL
);

CREATE INDEX idx_geo_region ON dim_geography(region);
CREATE INDEX idx_geo_state ON dim_geography(state);

-- ----------------------------------------------------------------------------
-- 3. DIM_CUSTOMER (Customer Dimension with Lifetime Aggregates)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    first_order_date DATE,
    last_order_date DATE,
    total_orders INTEGER,
    total_spend NUMERIC(12, 2),
    total_profit NUMERIC(12, 2)
);

CREATE INDEX idx_customer_id ON dim_customer(customer_id);
CREATE INDEX idx_customer_segment ON dim_customer(segment);

-- ----------------------------------------------------------------------------
-- 4. DIM_PRODUCT (Product Dimension)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL
);

CREATE INDEX idx_product_id ON dim_product(product_id);
CREATE INDEX idx_product_category ON dim_product(category);
CREATE INDEX idx_product_subcategory ON dim_product(sub_category);

-- ----------------------------------------------------------------------------
-- 5. DIM_DATE (Calendar Date Dimension)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY, -- YYYYMMDD
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    day_of_week INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL,
    year_month VARCHAR(10) NOT NULL
);

CREATE INDEX idx_date_year ON dim_date(year);
CREATE INDEX idx_date_year_month ON dim_date(year_month);

-- ----------------------------------------------------------------------------
-- 6. FACT_SALES (Core Transaction Fact Table)
-- ----------------------------------------------------------------------------
CREATE TABLE fact_sales (
    sale_id INTEGER PRIMARY KEY,
    row_id INTEGER NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    order_date_key INTEGER NOT NULL,
    ship_date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    geography_key INTEGER NOT NULL,
    ship_mode_key INTEGER NOT NULL,
    sales NUMERIC(12, 4) NOT NULL,
    quantity INTEGER NOT NULL,
    discount NUMERIC(6, 4) NOT NULL,
    profit NUMERIC(12, 4) NOT NULL,
    ship_days INTEGER NOT NULL,
    profit_margin NUMERIC(8, 4) NOT NULL,
    profit_status VARCHAR(20) NOT NULL,
    discount_band VARCHAR(50) NOT NULL,
    order_value_band VARCHAR(50) NOT NULL,
    shipping_delay_category VARCHAR(50) NOT NULL,
    FOREIGN KEY (order_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (ship_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (geography_key) REFERENCES dim_geography(geography_key),
    FOREIGN KEY (ship_mode_key) REFERENCES dim_ship_mode(ship_mode_key)
);

CREATE INDEX idx_fact_order_date ON fact_sales(order_date_key);
CREATE INDEX idx_fact_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_product ON fact_sales(product_key);
CREATE INDEX idx_fact_geography ON fact_sales(geography_key);
CREATE INDEX idx_fact_order_id ON fact_sales(order_id);

