# Customer, Product, and Profitability Performance Analysis in Supply Chain Operations

**Organization Context:** APL Logistics (KWE Group)  
**Project Program:** Unified Mentor

## Abstract

This project analyzes sales, recorded profit, customer value, product and category profitability, discount-related margin patterns, and market and regional performance. A Python-based Streamlit dashboard provides interactive filters, visualizations, and financial summaries to support business analysis.

The dataset contains 180,519 records and 20,652 unique customers. The dashboard reports total revenue of $36,784,734.31, total recorded profit of $3,966,902.97, and an overall profit margin of 10.78%. These values are calculated from the supplied dataset and should be interpreted with the limitations described in this report.

## 1. Introduction

Revenue alone does not fully explain business performance. Products, customers, and markets that generate substantial revenue may contribute relatively little profit or may even generate losses.

Profitability analysis helps businesses understand financial performance, identify potential risks, evaluate discount practices, and make informed decisions about products, customers, and geographic markets.

This project uses Python, Pandas, Plotly, and Streamlit to develop an interactive dashboard for exploring these areas.

## 2. Problem Statement

The project addresses the following business questions:

- What are the total revenue, recorded profit, and overall profit margin?
- Which customers contribute the most and least recorded profit?
- Which products and categories have strong or weak profitability?
- Which products generate high revenue but relatively low profit margins?
- How do discount rates relate to recorded profit and margin?
- Which markets, regions, and countries contribute the most profit?
- What data-quality limitations should be considered when interpreting the results?

## 3. Project Objectives

1. Examine the financial performance of the supplied dataset.
2. Calculate and present important profitability KPIs.
3. Compare customer contributions and identify potential customer-value differences.
4. Evaluate product and category profitability.
5. Analyze the relationship between discounts and profitability.
6. Compare profitability across markets, regions, and countries.
7. Build an interactive Streamlit dashboard.
8. Provide recommendations based on verified analytical findings.

## 4. Dataset Description

The project uses the supplied APL Logistics CSV dataset.

The dataset contains 180,519 records and includes fields relating to sales, recorded profit, discounts, customers, products, categories, markets, regions, shipping, and delivery information.

Important fields include:

- `Sales`
- `Order Profit Per Order`
- `Order Item Discount`
- `Order Item Discount Rate`
- `Order Item Profit Ratio`
- `Order Customer Id`
- `Customer Segment`
- `Category Name`
- `Product Name`
- `Market`
- `Order Region`
- `Order Country`

The source file does not explicitly specify the currency. Dollar symbols in the dashboard are therefore used for presentation and should not be interpreted as a verified source currency.

The dataset does not contain an order-date field, which prevents reliable daily or monthly trend analysis using this file alone.

## 5. Methodology

### 5.1 Data Loading

The dataset is loaded into Python using Pandas. The application supports alternative text encodings where necessary.

### 5.2 Data Cleaning and Validation

The analysis checks missing values in core financial fields and identifies records with non-positive sales.

The dashboard reports:

- Original dataset rows: 180,519
- Rows used in financial analysis: 180,519
- Rows excluded for missing or non-positive sales or missing profit: 0
- Missing Sales values: 0
- Missing `Order Profit Per Order` values: 0
- Duplicate full rows: 0
- Negative-profit records: 33,784

Negative-profit records are retained because they may represent genuine financial losses rather than data errors.

### 5.3 Financial Analysis

The dashboard uses `Sales` as its revenue measure and `Order Profit Per Order` as its recorded-profit measure.

Profit margin is calculated as:

**Profit Margin (%) = Total Recorded Profit / Total Revenue × 100**

Financial summaries are grouped by customers, products, categories, markets, regions, and countries.

The meaning of `Order Profit Per Order` should be verified against the dataset documentation before its summed value is interpreted as profit across distinct orders.

### 5.4 Customer Analysis

Customer records are grouped using `Order Customer Id` to compare recorded profit and sales contributions.

The dashboard provides customer rankings and customer-level comparisons to help identify high- and low-contribution customers.

### 5.5 Product and Category Analysis

Products and categories are compared using revenue, recorded profit, and profit margin.

The analysis highlights products that generate substantial revenue but have relatively low margins, as well as categories with negative recorded profit.

### 5.6 Discount Analysis

Discounted and non-discounted records are compared using revenue, recorded profit, and profit margin.

Discount rates are also examined alongside profit ratios and margin bands.

These comparisons are descriptive. They identify associations in the observed data but do not prove that discounts caused changes in profitability.

### 5.7 Market and Regional Analysis

Revenue, recorded profit, and margin are compared across markets, order regions, and countries to identify differences in geographic performance.

### 5.8 What-If Discount Scenario

The dashboard includes a simplified scenario calculator that estimates the effect of an additional discount on current revenue and recorded profit.

The scenario assumes that units and underlying costs remain constant. It is intended for sensitivity discussion rather than as a causal forecast or a complete pricing model.

## 6. Key Performance Indicators

The dashboard includes the following KPIs:

**Total Revenue:** Sum of `Sales`.

**Total Recorded Profit:** Sum of `Order Profit Per Order`.

**Profit Margin (%):** Total recorded profit divided by total revenue, multiplied by 100.

**Customer Value Index:** The dashboard defines this as total recorded profit divided by the number of unique customers. It represents average recorded profit per unique customer, not customer lifetime value.

**Category Margin:** The dashboard displays the unweighted average of the selected categories' individual margins.

**Discount Burden Ratio:** Total recorded discount divided by revenue, expressed as a percentage. This is a discount-burden measure, not a causal estimate of profit loss.

## 7. Dashboard Design

The Streamlit dashboard contains five main sections:

1. **Revenue & Profit Overview:** Presents overall financial KPIs and available financial summaries.
2. **Customer Value:** Compares customer contributions and customer profitability.
3. **Product & Category Performance:** Examines product margins, category profitability, and loss-making categories.
4. **Discount Impact:** Compares discounted and non-discounted records and includes a simplified what-if scenario.
5. **Market & Data Quality:** Compares market, regional, and country performance and reports data-quality checks.

The sidebar provides filters for customer segment, product category, product, market, order region, and maximum discount rate.

## 8. Results and Findings

### 8.1 Overall Financial Performance

The dashboard reports the following financial results:

| KPI | Reported Value |
|---|---:|
| Total Revenue | $36,784,734.31 |
| Total Recorded Profit | $3,966,902.97 |
| Overall Profit Margin | 10.78% |
| Unique Customers | 20,652 |
| Negative-Profit Records | 33,784 |

These are the values displayed by the dashboard. The source currency and the precise accounting meaning of the recorded-profit field have not been independently verified.

### 8.2 Customer Profitability

The Customer Value dashboard provides customer rankings and comparisons.

The top five and bottom five customers by recorded profit should be reported from the generated customer-profitability analysis outputs after validating the aggregation method. Specific customer-level numerical findings are not included here because they have not yet been verified for this report.

### 8.3 Product and Category Profitability

The dashboard identifies products with high revenue and relatively low margins.

One displayed example is **Children's heaters**, with:

- Revenue: $75,348.10
- Recorded profit: $4,612.29
- Profit margin: approximately 6.12%

This illustrates why revenue should be evaluated alongside profitability.

The dashboard also identifies **As Seen on TV!** as a loss-making category in the displayed results:

- Revenue: $6,299.37
- Recorded profit: -$345.89
- Profit margin: approximately -5.49%

These findings suggest that low-margin products and loss-making categories deserve further investigation.

### 8.4 Discount Analysis

The dashboard reports the following comparison:

| Metric | Discounted Records | Non-Discounted Records |
|---|---:|---:|
| Number of Records | 170,491 | 10,028 |
| Revenue | $34,742,365.17 | $2,042,369.14 |
| Recorded Profit | $3,699,490.57 | $267,412.40 |
| Profit Margin | 10.65% | 13.09% |

The observed profit margin is approximately 2.44 percentage points lower for discounted records.

This difference indicates an association between discount status and recorded profitability. It does not establish that discounts caused the difference because product mix, customer characteristics, and other factors may also influence profitability.

### 8.5 Market and Regional Performance

The market-profit chart shows Europe with the highest profit bar among the displayed markets and Africa with the lowest.

The dashboard also provides regional-profit comparisons and a country-profitability table.

Detailed market and regional numerical rankings should be taken from the corresponding analysis outputs before publication.

### 8.6 Data Quality

The dashboard reports 180,519 original rows and 180,519 rows used in financial analysis. It reports no excluded rows, no missing Sales values, no missing recorded-profit values, and no duplicate full rows.

There are 33,784 negative-profit records. These require business interpretation and should not automatically be treated as data-quality errors.

## 9. Recommendations

Based on the findings available in the dashboard, the following actions are recommended:

1. **Review low-margin products:** Investigate high-revenue products with weak profit margins, including the displayed Children's heaters example.
2. **Investigate loss-making categories:** Examine the costs, pricing, and product mix associated with the As Seen on TV! category.
3. **Review discount practices:** Compare margins across discount levels while considering differences in products and customers.
4. **Investigate negative-profit records:** Determine whether negative profitability reflects legitimate commercial outcomes or data-definition issues.
5. **Compare geographic performance:** Evaluate markets and regions using both recorded profit and profit margin.
6. **Validate financial definitions:** Confirm the meaning of `Order Profit Per Order` and the source currency with the data owner.
7. **Improve reporting reliability:** Use the generated analysis outputs to validate all detailed customer, product, and geographic findings before making decisions.

These recommendations should be refined as additional verified findings become available.

## 10. Limitations

The analysis has several limitations:

- The dataset does not contain an order-date field, so genuine daily or monthly trends cannot be calculated.
- The source currency is not explicitly stated.
- The definition of `Order Profit Per Order` requires verification before its sum can be interpreted as distinct-order profit.
- Discount comparisons are observational and do not prove causation.
- The what-if discount calculator uses simplified assumptions and is not a demand-sensitive pricing forecast.
- Customer names and street addresses in the source data should not be exposed in public reports or screenshots.
- Detailed customer and regional findings must be validated against the generated analysis outputs before publication.

## 11. Conclusion

This project provides an interactive dashboard for examining revenue, recorded profit, customer contributions, product and category margins, discount patterns, and geographic performance.

The displayed results highlight differences between discounted and non-discounted records, identify a low-margin product example, and reveal a loss-making category. These findings demonstrate the value of examining profitability alongside revenue.

Before final business decisions are made, the recorded-profit definition, currency, and detailed aggregation results should be verified. The dashboard can then support more reliable commercial analysis and management discussions.

## References

1. Unified Mentor project brief supplied for this assignment.
2. Supplied APL Logistics CSV dataset.
3. Pandas documentation: https://pandas.pydata.org/docs/
4. Plotly documentation: https://plotly.com/python/
5. Streamlit documentation: https://docs.streamlit.io/