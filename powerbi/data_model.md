# Enterprise Star Schema Data Model Specification

This document details the dimensional modeling architecture designed for Power BI, SQL Server, and analytical data pipelines.

---

## 1. Dimensional Model Overview

```
                                  +-------------------+
                                  |     DIM_DATE      |
                                  +-------------------+
                                  | PK: DateKey       |
                                  | Date              |
                                  | Year, Quarter     |
                                  | Month, MonthName  |
                                  | DayOfWeek, Week   |
                                  +---------+---------+
                                            | 1
                                            |
                                            | * (OrderDateKey, ShipDateKey)
+--------------------+            +---------v---------+            +--------------------+
|    DIM_CUSTOMER    | 1        * |    FACT_SALES     | *        1 |    DIM_PRODUCT     |
+--------------------+------------>-------------------<------------+--------------------+
| PK: CustomerKey    |            | PK: SalesFactID   |            | PK: ProductKey     |
| CustomerID (Nat)   |            | FK: OrderDateKey  |            | ProductID (Nat)    |
| CustomerName       |            | FK: ShipDateKey   |            | ProductName        |
| Segment            |            | FK: CustomerKey   |            | Category           |
+--------------------+            | FK: ProductKey    |            | SubCategory        |
                                  | FK: LocationKey   |            +--------------------+
                                  | FK: ShipModeKey   |
+--------------------+            | Measures:         |            +--------------------+
|   DIM_GEOGRAPHY    | 1        * |   Sales           | *        1 |   DIM_SHIP_MODE    |
+--------------------+------------>   Quantity        <------------+--------------------+
| PK: LocationKey    |            |   Discount        |            | PK: ShipModeKey    |
| Country, Region    |            |   Profit          |            | ShipModeName       |
| State, City, ZIP   |            |   ShippingDays    |            +--------------------+
+--------------------+            +-------------------+
```

---

## 2. Table Specifications & Granularity

### A. Fact Table: `FACT_SALES`
- **Granularity (Grain):** Individual product item line within an order (1 record per order line).
- **Primary Key:** `SalesFactID` (Surrogate Key) / Natural key `(Order ID, Product ID)`.

| Column | Type | Constraint | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `SalesFactID` | `BIGINT` | PK, Identity | Surrogate Key | Unique fact transaction identifier |
| `OrderDateKey` | `INT` | FK -> `DIM_DATE` | Foreign Key | Integer date key (YYYYMMDD) for order date |
| `ShipDateKey` | `INT` | FK -> `DIM_DATE` | Foreign Key | Integer date key (YYYYMMDD) for shipment date |
| `CustomerKey` | `INT` | FK -> `DIM_CUSTOMER` | Foreign Key | Reference to purchasing customer |
| `ProductKey` | `INT` | FK -> `DIM_PRODUCT` | Foreign Key | Reference to purchased SKU |
| `LocationKey` | `INT` | FK -> `DIM_GEOGRAPHY` | Foreign Key | Reference to destination geography |
| `ShipModeKey` | `INT` | FK -> `DIM_SHIP_MODE` | Foreign Key | Reference to shipping method |
| `Sales` | `DECIMAL(12,4)` | NOT NULL | Additive Measure | Net dollar revenue for line item |
| `Quantity` | `INT` | NOT NULL | Additive Measure | Units sold |
| `Discount` | `DECIMAL(6,4)` | NOT NULL | Non-Additive Measure | Promotional discount percentage |
| `Profit` | `DECIMAL(12,4)` | NOT NULL | Additive Measure | Net dollar contribution margin |
| `OrderToShipDays` | `INT` | NOT NULL | Additive Measure | Fulfillment lead time (Ship Date - Order Date) |
| `ProfitMargin` | `DECIMAL(8,4)` | NOT NULL | Semi-Additive Measure | Line-level profit margin ratio |

---

### B. Dimension Tables

#### 1. `DIM_CUSTOMER`
- **Grain:** 1 record per unique customer (793 records).
- **Primary Key:** `CustomerKey` (Surrogate Key).

| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `CustomerKey` | `INT` | PK | Surrogate primary key |
| `CustomerID` | `VARCHAR(50)` | Unique, Business Key | Natural customer identifier (e.g. CG-12520) |
| `CustomerName` | `VARCHAR(100)` | NOT NULL | Full name of customer |
| `Segment` | `VARCHAR(50)` | NOT NULL | Customer segment (Consumer, Corporate, Home Office) |

#### 2. `DIM_PRODUCT`
- **Grain:** 1 record per unique product item (1,862 records).
- **Primary Key:** `ProductKey` (Surrogate Key).

| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `ProductKey` | `INT` | PK | Surrogate primary key |
| `ProductID` | `VARCHAR(50)` | NOT NULL, Business Key | Catalog SKU code |
| `ProductName` | `VARCHAR(255)` | NOT NULL | Full product descriptive title |
| `Category` | `VARCHAR(50)` | NOT NULL | Top-level category (Technology, Furniture, Office Supplies) |
| `SubCategory` | `VARCHAR(50)` | NOT NULL | Granular sub-category (17 items) |

#### 3. `DIM_GEOGRAPHY`
- **Grain:** 1 record per unique geographic market/location (631 records).
- **Primary Key:** `LocationKey` (Surrogate Key).

| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `LocationKey` | `INT` | PK | Surrogate primary key |
| `Country` | `VARCHAR(50)` | NOT NULL | Country name (United States) |
| `Region` | `VARCHAR(50)` | NOT NULL | US Geographic region (West, East, Central, South) |
| `State` | `VARCHAR(50)` | NOT NULL | US State (49 distinct states) |
| `City` | `VARCHAR(50)` | NOT NULL | Municipal city (531 cities) |
| `PostalCode` | `INT` | NULL | 5-digit US ZIP postal code |

#### 4. `DIM_SHIP_MODE`
- **Grain:** 1 record per fulfillment delivery method (4 records).
- **Primary Key:** `ShipModeKey` (Surrogate Key).

| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `ShipModeKey` | `INT` | PK | Surrogate primary key |
| `ShipModeName` | `VARCHAR(50)` | NOT NULL, Unique | Standard Class, Second Class, First Class, Same Day |

#### 5. `DIM_DATE`
- **Grain:** 1 record per calendar day across operating window (1,461 days: 2014-01-01 to 2017-12-31).
- **Primary Key:** `DateKey` (Integer: YYYYMMDD).

| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `DateKey` | `INT` | PK | Integer key (e.g. 20161108) |
| `FullDate` | `DATE` | NOT NULL, Unique | Standard date representation |
| `Year` | `INT` | NOT NULL | Calendar year (2014 - 2017) |
| `Quarter` | `INT` | NOT NULL | Calendar quarter (1 - 4) |
| `Month` | `INT` | NOT NULL | Month number (1 - 12) |
| `MonthName` | `VARCHAR(20)` | NOT NULL | Full month name (January - December) |
| `YearMonth` | `VARCHAR(7)` | NOT NULL | YYYY-MM format |
| `WeekOfYear` | `INT` | NOT NULL | ISO week number (1 - 53) |
| `DayOfWeek` | `VARCHAR(20)` | NOT NULL | Monday - Sunday |
| `IsWeekend` | `BIT` | NOT NULL | 1 if Saturday/Sunday, 0 otherwise |

---

## 3. Relationship Matrix & Cardinality

| From Table | From Column | To Table | To Column | Cardinality | Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `FACT_SALES` | `OrderDateKey` | `DIM_DATE` | `DateKey` | Many-to-One (*:1) | Single (DIM -> FACT) |
| `FACT_SALES` | `ShipDateKey` | `DIM_DATE` | `DateKey` | Many-to-One (*:1) | Inactive (Role-Playing) |
| `FACT_SALES` | `CustomerKey` | `DIM_CUSTOMER` | `CustomerKey` | Many-to-One (*:1) | Single (DIM -> FACT) |
| `FACT_SALES` | `ProductKey` | `DIM_PRODUCT` | `ProductKey` | Many-to-One (*:1) | Single (DIM -> FACT) |
| `FACT_SALES` | `LocationKey` | `DIM_GEOGRAPHY` | `LocationKey` | Many-to-One (*:1) | Single (DIM -> FACT) |
| `FACT_SALES` | `ShipModeKey` | `DIM_SHIP_MODE` | `ShipModeKey` | Many-to-One (*:1) | Single (DIM -> FACT) |

---

## 4. Modeling Best Practices Implemented
1. **Pure Star Schema:** Avoids slow snowflake joins by denormalizing category into product and state/region into geography.
2. **Surrogate Keys:** High-performance integer join keys rather than wide composite string natural keys.
3. **Role-Playing Date Handling:** Active relationship on `OrderDateKey`, inactive relationship on `ShipDateKey` leveraged via DAX `USERELATIONSHIP()`.
4. **Single-Direction Filtering:** Prevents ambiguous filter paths and bidirectional cross-filtering performance degradation.
