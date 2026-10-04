# Analytical Methodology & Statistical Modeling

This document outlines the analytical frameworks, statistical scoring algorithms, and financial calculation methodologies utilized in the **Retail Business Intelligence & Customer Analytics** project.

---

## 1. End-to-End Analytics Lifecycle

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Raw Ingest  │ ──> │ Quality Gate │ ──> │ Feature Eng. │ ──> │ Star Schema  │
│  Multi-codec │     │  Zero-defect │     │ Time, Lead,  │     │ Fact & Dims  │
│  CSV reader  │     │  Validation  │     │ Profit bands │     │ SQL modeling │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
┌──────────────┐     ┌──────────────┐     ┌──────────────┐             │
│ Exec Reports │ <── │  Power BI BI │ <── │ Customer RFM │ <───────────┘
│  Actionable  │     │  Interactive │     │  Quintile    │
│  Scorecards  │     │  DAX model   │     │  Behavioral  │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## 2. Customer RFM Segmentation Methodology

### A. Core Dimension Calculations
1. **Recency ($R$):** Elapsed days from the customer's most recent order to the benchmark snapshot date ($T_{snapshot} = 2017\text{-}12\text{-}31$):
   $$R_i = T_{snapshot} - \max(OrderDate_i)$$
2. **Frequency ($F$):** Total count of unique checkout orders placed across the customer's multi-year history:
   $$F_i = |\{OrderID_i\}|$$
3. **Monetary Value ($M$):** Cumulative net revenue spend:
   $$M_i = \sum Sales_i$$

### B. Statistical Quintile Scoring
To prevent artificial bias, customers are assigned scores from 1 (lowest) to 5 (highest) using rank-based quintile binning (`pd.qcut` / SQL `NTILE(5)`):
- **Recency:** Inverted ranking (lowest elapsed days = Score 5; highest days = Score 1).
- **Frequency:** Standard ranking with tie-breaking (highest order count = Score 5; lowest = Score 1).
- **Monetary:** Standard ranking (highest cumulative spend = Score 5; lowest = Score 1).

### C. Strategic Segmentation Matrix
| Segment Name | Score Criteria | Strategic Interpretation |
| :--- | :--- | :--- |
| **Champions** | $R \ge 4, F \ge 4, M \ge 4$ | Highest value, highly active, brand advocates. |
| **Loyal Customers** | $R \ge 3, F \ge 3, M \ge 3$ | Consistent repeat spenders; responsive to upsells. |
| **Potential Loyalists** | $R \ge 4, F \in [2,3]$ | High potential buyers; cultivate with loyalty rewards. |
| **New Customers** | $R \ge 4, F = 1$ | Recent first-time purchasers; require onboarding flows. |
| **Promising** | $R = 3, F \in [1,2]$ | Moderate activity; nurture with targeted promotions. |
| **Need Attention** | $R \in [2,3], F \in [2,3]$ | Above average value slipping in engagement. |
| **About to Sleep** | $R \in [2,3], F = 1$ | Below average recency with only 1 order; churn risk. |
| **Cannot Lose Them** | $R \le 2, F \ge 4, M \ge 4$ | Historically top-tier customers entering dormancy. |
| **At Risk** | $R \le 2, F \ge 3$ | Frequent buyers who have not purchased recently. |
| **Hibernating** | $R \le 2, F \in [1,2]$ | Low spenders with high days since last purchase. |
| **Lost** | $R = 1, F = 1, M = 1$ | Lowest recency, single low-value purchase. |

---

## 3. Financial & Margin Computation Standards

1. **Line-Level Profit Margin:**
   $$\text{Profit Margin} = \frac{\text{Profit}}{\text{Sales}}$$
2. **Blended Portfolio Margin:**
   $$\text{Blended Margin \%} = \frac{\sum \text{Profit}}{\sum \text{Sales}} \times 100$$
3. **Average Order Value (AOV):**
   $$\text{AOV} = \frac{\sum \text{Sales}}{|\{OrderID\}|}$$
4. **Estimated Unit Cost:**
   $$\text{Unit Cost} = \frac{\text{Sales} - \text{Profit}}{\text{Quantity}}$$
5. **Discount Price Impact:**
   $$\text{Gross Undiscounted Price} = \frac{\text{Sales}}{1 - \text{Discount}}$$

---

## 4. Pareto 80/20 Cumulative Distribution Analysis
The Pareto distribution algorithm ranks all 793 customers by descending total spend, computes running cumulative spend, and divides by total enterprise revenue:
$$\text{Cumulative Sales \%}_k = \frac{\sum_{i=1}^k Sales_{(i)}}{\sum_{i=1}^N Sales_{(i)}} \times 100$$
The resulting inflection points provide empirical evidence of revenue concentration.
