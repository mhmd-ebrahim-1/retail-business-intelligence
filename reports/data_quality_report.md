# Enterprise Data Quality & Pipeline Audit Report

**System:** Retail Business Intelligence Data Pipeline  
**Dataset:** US Superstore Transaction Ledger (2014 – 2017)  
**Execution Status:** PASS (All Data Quality Gates Cleared)  

---

## 1. Data Quality Scorecard Summary

| Audit Dimension | Test Rule | Expected Value | Actual Value | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Completeness** | Null check on primary keys | 0 Nulls | 0 Nulls | **PASSED** |
| **Completeness** | Null check on financial metrics | 0 Nulls | 0 Nulls | **PASSED** |
| **Uniqueness** | Full row duplicate check | 0 Duplicates | 0 Duplicates | **PASSED** |
| **Uniqueness** | Row ID surrogate key uniqueness | 9,994 Distinct | 9,994 Distinct | **PASSED** |
| **Validity** | Positive Sales values | Sales > $0 | 9,994 valid (Min: $0.44) | **PASSED** |
| **Validity** | Positive Quantity values | Quantity >= 1 | 9,994 valid (1 to 14) | **PASSED** |
| **Validity** | Discount domain boundary | 0.00 <= Disc <= 1.00 | 9,994 valid (0.00 to 0.80) | **PASSED** |
| **Consistency** | Date chronological sequence | Order Date <= Ship Date | 9,994 valid (0 violations) | **PASSED** |
| **Consistency** | Max fulfillment duration | Ship Days <= 14 | Max: 7 days, Avg: 3.96 days | **PASSED** |
| **Integrity** | Foreign Key referential checks | 0 Orphan records | 0 Orphans | **PASSED** |

---

## 2. Detailed Dimension Assessment

### A. Completeness & Schema Conformity
- **Total Records Evaluated:** 9,994 rows across 21 raw columns.
- **Null / Missing Values:** 0 null values detected across all categorical, financial, and date attributes.
- **Data Type Casting:** All numeric columns successfully cast to standard 64-bit float and integer types; date columns parsed to ISO `datetime64`.

### B. Business Constraint Validation
- **Negative Sales Check:** 0 records with Sales <= 0.
- **Quantity Check:** 0 records with Quantity <= 0.
- **Discount Outliers:** All discount values reside within the valid operational range of `[0.00, 0.80]`.
- **Loss-Making Transactions:** 1,871 records (18.72%) contain negative profit values, reflecting genuine commercial discounting practices rather than data collection errors.

---

## 3. Automated Testing Verification
The test suite in `tests/test_data_quality.py` programmatically asserts all constraints on every data ingestion run.
