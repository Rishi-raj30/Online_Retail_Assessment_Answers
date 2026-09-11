# Online Retail Data Analyst Assessment

## Dataset
UCI Online Retail dataset.
Official source: https://archive.ics.uci.edu/dataset/352/online-retail
The UCI record describes 541,909 transaction rows for a UK-based non-store online retailer covering 01-Dec-2010 to 09-Dec-2011.

## Business Objective
Understand the drivers of revenue and customer value, identify high-value customers/products/markets, and find opportunities to improve sales performance and retention.

## Main Processing Rules
1. Load the raw Excel dataset.
2. Remove exact duplicate rows.
3. Convert date/numeric fields to appropriate types.
4. Identify cancellation invoices (InvoiceNo beginning with C).
5. Exclude cancellations, non-positive quantities and non-positive unit prices from positive-sales KPIs.
6. Exclude missing CustomerID from customer-level KPIs.
7. Exclude missing Description from product-level analysis.
8. Create Revenue = Quantity × UnitPrice.
9. Create YearMonth, Year, Month and MonthName.
10. Create OrderValue at invoice level.

## Actual Results
- Raw rows: 541,909
- Raw columns: 8
- Exact duplicates: 5,268
- Missing CustomerID: 135,080
- Negative-quantity rows: 10,624
- Cancellation invoices: 9,288
- Valid positive-sales rows used for the main analysis: 392,692
- Valid sales revenue: £8,887,208.89
- Identified customers: 4,338
- Orders: 18,532
- Average order value: £479.56
- Products: 3,665
- Countries in valid sales: 37

## Key Findings
1. Repeat customers are the core revenue engine. 2,845 repeat customers (65.6% of identified customers) generated 93.1% of valid revenue. Average revenue per repeat customer was about £2,908 versus £411 for one-time customers.
2. The UK generated £7.29M, approximately 82.0% of valid revenue.
3. November 2011 was the strongest full month at £1.16M. September revenue increased 47.6% versus August. December 2011 is a partial month and should not be compared directly with complete months.
4. The top 10 identifiable products generated about 9.8% of valid revenue.
5. The top 10 customers generated 17.3% of revenue and the top 100 generated 40.6%, indicating meaningful but not extreme customer concentration.

## Surprising Finding
Customer 12346 was a one-time customer but generated £77,183.60 from one order, approximately 0.87% of valid revenue, involving 74,215 units. This may represent a wholesale/bulk transaction or another unusual order. The dataset alone cannot establish the exact reason, so this should be validated before taking customer-level action.

## Limitations
- Historical data from 2010–2011.
- Missing CustomerID limits customer-level analysis.
- No marketing spend, profit/margin, inventory or acquisition-cost data.
- The analysis shows patterns and associations; it does not prove causation.

## Files
- `Processed_Data.csv` — analysis-ready dataset.
- `Online_Retail_Assessment_Answers.xlsx` — Q1–Q7, Q10, KPI and analysis tables.
- `analysis.py` — reproducible Python workflow.
- `Management_Presentation_Online_Retail.pptx` — 7-slide management presentation.
- PNG files — recommended dashboard visualizations.

## Looker Studio
Upload `Processed_Data.csv` to Google Sheets, then connect that Google Sheet as a Looker Studio data source. Recommended dashboard:
- KPI cards: Revenue, Customers, Orders, Average Order Value, Repeat Revenue %
- Monthly Revenue Trend
- Revenue by Country
- Top 10 Products by Revenue
- Repeat vs One-time Revenue
- Filters: Year, Month, Country, Customer Segment

## AI Disclosure
ChatGPT was used for dataset understanding, analytical brainstorming, Python support, debugging, documentation and visualization planning. All important calculations were independently checked against the uploaded raw data before being used.
