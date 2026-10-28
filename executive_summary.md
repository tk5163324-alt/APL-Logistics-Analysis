# Executive Summary
## Customer, Product, and Profitability Performance Analysis in Supply Chain Operations

**Organization Context:** APL Logistics (KWE Group)  
**Project Program:** Unified Mentor

## 1. Purpose

This project analyzes revenue, recorded profit, customer contributions, product and category profitability, discount patterns, and geographic performance. A Streamlit dashboard allows users to explore the supplied dataset through interactive filters and visualizations.

The objective is to support business understanding of profitability and identify areas that may require further investigation.

## 2. Key Financial Results

The dashboard reports the following results:

| KPI | Reported Value |
|---|---:|
| Total Revenue | $36,784,734.31 |
| Total Recorded Profit | $3,966,902.97 |
| Profit Margin | 10.78% |
| Unique Customers | 20,652 |
| Negative-Profit Records | 33,784 |

The source dataset does not specify its currency, so the dollar symbol is used for presentation only. Total recorded profit is calculated by summing the supplied `Order Profit Per Order` field; its precise accounting definition should be verified before final financial reporting.

## 3. Main Findings

### Product and Category Performance

The dashboard identifies products with substantial revenue but relatively low margins.

For example, the displayed results for Children's heaters are:

- Revenue: $75,348.10
- Recorded profit: $4,612.29
- Profit margin: approximately 6.12%

The As Seen on TV! category is shown as loss-making, with revenue of $6,299.37, recorded profit of -$345.89, and a margin of approximately -5.49%.

These results highlight the need to examine revenue and profitability together.

### Discount Analysis

The dashboard reports a profit margin of approximately 10.65% for discounted records and 13.09% for non-discounted records.

The difference is approximately 2.44 percentage points. This is an observed association, not proof that discounts caused lower profitability.

The dashboard also provides discount-band analysis and a simplified what-if discount scenario.

### Customer and Geographic Performance

The Customer Value dashboard provides customer-level comparisons, while the Market & Data Quality section compares profitability across markets, regions, and countries.

Detailed customer rankings and geographic findings should be confirmed against the corresponding generated analysis outputs before being used for management decisions.

### Data Quality

The dashboard reports:

- 180,519 original rows.
- 180,519 rows used in financial analysis.
- No rows excluded by the reported financial filters.
- No missing Sales values.
- No missing recorded-profit values.
- No duplicate full rows.
- 33,784 negative-profit records.

Negative-profit records require investigation but are not automatically data errors.

## 4. Dashboard Features

The Streamlit dashboard contains five sections:

1. Revenue & Profit Overview
2. Customer Value
3. Product & Category Performance
4. Discount Impact
5. Market & Data Quality

Interactive filters allow users to explore customer segments, product categories, products, markets, regions, and discount thresholds.

## 5. Recommended Actions

1. Investigate products with high revenue but weak margins.
2. Review the costs, pricing, and product mix of loss-making categories.
3. Examine discount levels alongside profitability and customer/product mix.
4. Investigate repeated negative-profit outcomes.
5. Compare market and regional performance using both recorded profit and margin.
6. Confirm the source currency and the meaning of `Order Profit Per Order` before final financial reporting.

## 6. Limitations

The dataset does not contain an order-date field, so daily or monthly trends cannot be calculated. The currency is unspecified, discount comparisons do not establish causation, and the what-if scenario is a simplified sensitivity tool rather than a complete pricing forecast.

Customer names and street addresses should be masked in public reports and screenshots.

## 7. Conclusion

The project provides an interactive view of customer, product, category, discount, market, and regional profitability. Its current findings highlight differences in observed margins, a low-margin product example, and a loss-making category.

Validating the source financial definitions and reviewing detailed analysis outputs will improve the reliability of the final recommendations and support responsible business interpretation.