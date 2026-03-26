---
name: transaction-margin-dataset
description: 'Schema reference for the Transaction Margin dataset. Use when the analysis involves transactions, margins, sales, revenue, invoices, order economics, cost breakdown, or product profitability. References {project}.ods.transaction_margin.'
user-invocable: false
disable-model-invocation: false
---

# Transaction Margin Dataset

## When to Use

Apply this skill when the framed question or analysis goals involve:
- Transactions, sales, revenue, or invoices
- Margins (product margin, transaction margin, profitability)
- Cost breakdown (shipping, packaging, payment, warehouse, returns)
- Order economics or unit economics
- Product-level or team-level financial performance
- Attached/cross-sell product analysis
- Marketing campaign ROI at the transaction level

**Trigger keywords:** transaction, margin, sales, revenue, invoice, cost, profitability, cross-sell, attached product, order economics, unit economics, COGS, stock value.

## Dataset Overview

- **Project:** `{project}` (resolve from active dataset manifest)
- **Dataset:** `ods`
- **Table:** `transaction_margin`
- **Warehouse:** BigQuery
- **Grain:** One row per **invoice line item** — each row represents a single product on a single invoice
- **Key identifiers:** `invoice_id` + `invoice_line_id` uniquely identify a row; `order_id` groups lines into orders; `customer_id` identifies the buyer

## Schema

Table: `{project}.ods.transaction_margin`

### Identity & Order Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| invoice_id | INT64 | YES | Invoice identifier |
| credit_invoice_id | INT64 | YES | Credit invoice ID (for returns/credits) |
| invoice_date | TIMESTAMP | YES | Invoice date — use for time-based analysis |
| invoice_line_id | INT64 | YES | Line item within the invoice |
| order_id | INT64 | YES | Order identifier — joins to GA4/PFA sessions via order IDs |
| order_line_id | INT64 | YES | Order line identifier |
| order_line_item_id | INT64 | YES | Order line item identifier |
| order_date | TIMESTAMP | YES | Order placement date |
| order_date_time | TIMESTAMP | YES | Order placement datetime |
| customer_id | INT64 | YES | Customer identifier |
| user_id | INT64 | YES | User identifier |
| b2b_customer | STRING | YES | B2B customer flag/classification |
| export_customer | BOOL | YES | Whether this is an export customer |

### Subsidiary & Geography

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| subsidiary_id | INT64 | YES | Subsidiary numeric identifier |
| subsidiary_name | STRING | YES | Full subsidiary name |
| inter_company_id | INT64 | YES | Inter-company identifier |
| inter_company_name | STRING | YES | Inter-company name |
| language_id | INT64 | YES | Language numeric ID |
| language | STRING | YES | Language code |
| region_hierarchy_id | INT64 | YES | Region hierarchy identifier |
| region_hierarchy_country | STRING | YES | Country |
| region_hierarchy_region | STRING | YES | Region |
| region_hierarchy_subregion | STRING | YES | Subregion |

### Channel & Outlet

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| shop_outlet_id | INT64 | YES | Shop/outlet identifier |
| shop_outlet_name | STRING | YES | Shop/outlet name |
| outlet_type_id | INT64 | YES | Outlet type identifier |
| outlet_type_name | STRING | YES | Outlet type (e.g., online, store) |
| order_source_id | INT64 | YES | Order source identifier |
| order_source_name | STRING | YES | Order source name |
| order_source_group | STRING | YES | Order source group |
| order_reason_id | INT64 | YES | Order reason identifier |
| order_reason | STRING | YES | Order reason description |

### Product Hierarchy

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| product_id | INT64 | YES | Product identifier for this line item |
| product_name | STRING | YES | Product name |
| product_type_id | INT64 | YES | Product type identifier |
| product_type_name | STRING | YES | Product type name |
| brand_id | INT64 | YES | Brand identifier |
| brand_name | STRING | YES | Brand name |
| primary_product_id | INT64 | YES | Primary (main) product in the order |
| primary_product_name | STRING | YES | Primary product name |
| attached_product_id | INT64 | YES | Attached (cross-sell) product |
| attached_product_name | STRING | YES | Attached product name |
| attached_product_cross_sell_type_id | INT64 | YES | Cross-sell type identifier |
| attached_product_cross_sell_type | STRING | YES | Cross-sell type (e.g., accessory, warranty) |

### Team Ownership

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| team_id | INT64 | YES | Team owning this product |
| team_name | STRING | YES | Team name |
| attached_team_id | INT64 | YES | Team owning the attached product |
| attached_team_name | STRING | YES | Attached product team name |
| primary_team_id | INT64 | YES | Team owning the primary product |
| primary_team_name | STRING | YES | Primary product team name |

### Quantity Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| quantity | FLOAT64 | YES | Quantity on this line (can be fractional) |
| primary_product_quantity | INT64 | YES | Quantity of primary product |
| attached_product_quantity | INT64 | YES | Quantity of attached product |
| invoice_product_quantity | INT64 | YES | Quantity invoiced for this product |
| invoice_order_line_item_quantity | INT64 | YES | Line item quantity on invoice |
| primary_order_line_item_quantity | INT64 | YES | Primary product line item quantity |
| attached_order_line_item_quantity | INT64 | YES | Attached product line item quantity |

### Revenue & Margin Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| stock_value | FLOAT64 | YES | Cost of goods (stock value) |
| margin_invoice_price | FLOAT64 | YES | Invoice price used for margin calculation |
| primary_product_invoiced | FLOAT64 | YES | Revenue from primary product |
| attached_product_invoiced | FLOAT64 | YES | Revenue from attached product |
| invoice_product_invoiced | FLOAT64 | YES | Total invoiced amount for this product |
| primary_product_margin | FLOAT64 | YES | Margin on primary product |
| attached_product_margin | FLOAT64 | YES | Margin on attached product |
| invoice_product_margin | FLOAT64 | YES | Margin on this invoice line |
| transaction_margin | FLOAT64 | YES | **Final transaction margin** after all costs |

### Margin with Agreements

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| primary_product_margin_including_rebate_purchase_discount_and_listing_fee | FLOAT64 | YES | Primary margin + rebate + purchase discount + listing fee |
| attached_product_margin_including_rebate_purchase_discount_and_listing_fee | FLOAT64 | YES | Attached margin + rebate + purchase discount + listing fee |
| invoice_product_margin_including_rebate_purchase_discount_and_listing_fee | FLOAT64 | YES | Invoice margin + rebate + purchase discount + listing fee |
| primary_product_margin_including_all_agreements | FLOAT64 | YES | Primary margin including all vendor agreements |
| attached_product_margin_including_all_agreements | FLOAT64 | YES | Attached margin including all vendor agreements |
| invoice_product_margin_including_all_agreements | FLOAT64 | YES | Invoice margin including all vendor agreements |
| primary_product_margin_including_media_fee | FLOAT64 | YES | Primary margin including media fee |
| attached_product_margin_including_media_fee | FLOAT64 | YES | Attached margin including media fee |
| invoice_product_margin_including_media_fee | FLOAT64 | YES | Invoice margin including media fee |

### Vendor Agreement Components

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| media_fee | FLOAT64 | YES | Media fee component |
| rebate | FLOAT64 | YES | Rebate component |
| purchase_discount | FLOAT64 | YES | Purchase discount component |
| listing_fee | FLOAT64 | YES | Listing fee component |

### Cost Breakdown

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| packaging_cost | FLOAT64 | YES | Packaging cost |
| payment_cost | FLOAT64 | YES | Payment processing cost |
| shipment_cost | FLOAT64 | YES | Shipment cost |
| customer_service_cost | FLOAT64 | YES | Customer service cost |
| warehouse_handling_cost | FLOAT64 | YES | Warehouse handling cost |
| returns_handling_cost | FLOAT64 | YES | Returns handling cost |
| second_chance_cost | FLOAT64 | YES | Second-chance (refurbished) cost |
| store_handling_cost | FLOAT64 | YES | Store handling cost |
| return_writeoff_cost | FLOAT64 | YES | Write-off cost for returns |
| invoice_variable_cost | FLOAT64 | YES | Total variable cost on this invoice line |

### Direct Fixed Costs

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| direct_fixed_customer_service_cost | FLOAT64 | YES | Fixed customer service cost allocation |
| direct_fixed_warehouse_handling_cost | FLOAT64 | YES | Fixed warehouse handling cost allocation |
| direct_fixed_returns_handling_cost | FLOAT64 | YES | Fixed returns handling cost allocation |
| direct_fixed_store_handling_cost | FLOAT64 | YES | Fixed store handling cost allocation |
| direct_fixed_shipment_cost | FLOAT64 | YES | Fixed shipment cost allocation |

### Shipment & Fulfillment

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| shipment_method_id | INT64 | YES | Shipment method identifier |
| shipment_method_name | STRING | YES | Shipment method name |
| stock_location_id | INT64 | YES | Stock location identifier |
| stock_location_name | STRING | YES | Stock location name |
| store_location_name | STRING | YES | Store location name |
| multi_warehouse_type_id | INT64 | YES | Multi-warehouse type identifier |
| multi_warehouse_type_name | STRING | YES | Multi-warehouse type name |

### Marketing

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| marketing_campaign_reference_id | INT64 | YES | Marketing campaign reference ID |
| reference | STRING | YES | Marketing reference code |
| marketing_campaign_id | INT64 | YES | Campaign identifier |
| marketing_campaign_name | STRING | YES | Campaign name |
| marketing_partner_id | INT64 | YES | Marketing partner identifier |
| marketing_partner_name | STRING | YES | Marketing partner name |
| parent_marketing_partner_id | INT64 | YES | Parent marketing partner ID |
| parent_marketing_partner_name | STRING | YES | Parent marketing partner name |
| marketing_tracking_variable | STRING | YES | Marketing tracking variable |

### Sales Actions

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| sales_action_id | INT64 | YES | Sales action/promotion identifier |
| sales_action_name | STRING | YES | Sales action/promotion name |

### Metadata

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ingest_timestamp | TIMESTAMP | YES | Data ingestion timestamp |

## Data Quirks

- **Grain is invoice line item, not order.** Each row is one product on one invoice. An order with 3 products produces 3 rows. Always aggregate to the desired level (order, customer, product type) before analysis.
- **Returns appear as credit invoices.** When `credit_invoice_id` is populated, this line represents a return/credit. The `quantity` may be negative. Filter or handle returns explicitly depending on the analysis.
- **`quantity` is FLOAT64.** Can be fractional (e.g., partial returns). Use `invoice_product_quantity` (INT64) for whole-unit counts.
- **Multiple margin definitions.** Choose the right margin level:
  - `invoice_product_margin` — base product margin
  - `*_including_rebate_purchase_discount_and_listing_fee` — margin with vendor discounts
  - `*_including_all_agreements` — margin with all vendor agreements
  - `*_including_media_fee` — margin with media fees
  - `transaction_margin` — final margin after all costs (most complete)
- **Primary vs. attached products.** Each row has both primary and attached product dimensions. The `product_id` is the actual line item; `primary_product_id` and `attached_product_id` indicate the relationship. For cross-sell analysis, filter on `attached_product_id IS NOT NULL`.
- **Cost columns are per-line.** All cost columns (`packaging_cost`, `shipment_cost`, etc.) are allocated to the invoice line level. Sum them for order-level or customer-level costs.
- **`invoice_date` vs `order_date`.** `invoice_date` is when the invoice was created (often = shipment date). `order_date` is when the customer placed the order. Use `order_date` for conversion analysis, `invoice_date` for revenue recognition.
- **`transaction_margin` formula.** Roughly: `margin_invoice_price - stock_value - variable_costs - fixed_costs + agreement_components`. Use this column directly rather than recomputing.
- **B2B customers.** `b2b_customer` identifies business customers. Filter on this for B2C-only analysis.
- **`ingest_timestamp` for freshness.** Check `MAX(ingest_timestamp)` to verify data recency.

## Common Query Patterns

### Revenue and margin by subsidiary
```sql
SELECT
  subsidiary_name,
  SUM(invoice_product_invoiced) AS revenue,
  SUM(transaction_margin) AS total_margin,
  SAFE_DIVIDE(SUM(transaction_margin), SUM(invoice_product_invoiced)) AS margin_pct
FROM `{project}.ods.transaction_margin`
WHERE invoice_date BETWEEN {{start_date}} and {{end_date}}
  AND credit_invoice_id IS NULL  -- exclude returns
GROUP BY subsidiary_name
ORDER BY revenue DESC
```

### Cost waterfall per order
```sql
SELECT
  order_id,
  SUM(invoice_product_invoiced) AS revenue,
  SUM(stock_value) AS cogs,
  SUM(invoice_product_margin) AS product_margin,
  SUM(packaging_cost) AS packaging,
  SUM(payment_cost) AS payment,
  SUM(shipment_cost) AS shipment,
  SUM(customer_service_cost) AS cs_cost,
  SUM(warehouse_handling_cost) AS warehouse,
  SUM(returns_handling_cost) AS returns,
  SUM(transaction_margin) AS net_margin
FROM `{project}.ods.transaction_margin`
WHERE invoice_date BETWEEN {{start_date}} and {{end_date}}
GROUP BY order_id
```

### Cross-sell / attached product analysis
```sql
SELECT
  attached_product_cross_sell_type,
  COUNT(DISTINCT order_id) AS orders,
  SUM(attached_product_quantity) AS units,
  SUM(attached_product_invoiced) AS revenue,
  SUM(attached_product_margin) AS margin
FROM `{project}.ods.transaction_margin`
WHERE invoice_date BETWEEN {{start_date}} and {{end_date}}
  AND attached_product_id IS NOT NULL
  AND credit_invoice_id IS NULL
GROUP BY attached_product_cross_sell_type
ORDER BY margin DESC
```

### Margin by product type and brand
```sql
SELECT
  product_type_name,
  brand_name,
  SUM(invoice_product_invoiced) AS revenue,
  SUM(transaction_margin) AS margin,
  SAFE_DIVIDE(SUM(transaction_margin), SUM(invoice_product_invoiced)) AS margin_pct,
  COUNT(DISTINCT order_id) AS orders
FROM `{project}.ods.transaction_margin`
WHERE invoice_date BETWEEN {{start_date}} and {{end_date}}
  AND credit_invoice_id IS NULL
GROUP BY product_type_name, brand_name
HAVING revenue > 1000
ORDER BY margin DESC
```

## Entity Relationships

```
transaction_margin.order_id       → GA4 sessions.order_ids[].orderid  (join transactions to web sessions)
transaction_margin.order_id       → PFA sessions.orders[].order_id    (join transactions to PFA sessions)
transaction_margin.customer_id    → sessions.customer_id              (join via customer)
transaction_margin.product_id     → product catalog tables            (product attributes)
transaction_margin.subsidiary_id  → shared subsidiary dimension
```

## Supported Analyses

- **Revenue & margin trends:** By subsidiary, product type, brand, team — over time using `invoice_date` or `order_date`
- **Cost structure analysis:** Break down `transaction_margin` into cost components (shipping, packaging, payment, warehouse, returns)
- **Cross-sell effectiveness:** Attached product revenue, margin, and attachment rate by cross-sell type
- **Return impact:** Compare credit invoice lines to original invoices for return rate and margin erosion
- **Marketing ROI:** Link marketing campaigns to transaction margin via `marketing_campaign_id`
- **Channel comparison:** Order source, outlet type, and shipment method margin differences
- **Product profitability:** Product-level or product-type-level margin analysis including vendor agreements
- **Geographic performance:** Revenue and margin by region hierarchy
- **B2B vs B2C:** Split analysis on `b2b_customer` and `export_customer`
