---
name: pfa-dataset
description: 'Schema reference for the Privacy Friendly Analytics (PFA) dataset. Use when the user mentions "Privacy Friendly Analytics", "PFA", or references privacy_friendly_analytics tables. Provides full schema, data quirks, and query patterns for the events and sessions tables.'
user-invocable: false
disable-model-invocation: false
---

# Privacy Friendly Analytics (PFA) Dataset

## When to Use

Apply this skill when the data source involves:
- "Privacy Friendly Analytics" or "PFA"
- `{project}.privacy_friendly_analytics` BigQuery dataset
- The `events` or `sessions` tables from PFA

This skill provides pre-built schema knowledge so the data-explorer agent can
skip basic schema discovery and focus on profiling and quality assessment.

## Dataset Overview

- **Project:** `{project}` (resolve from active dataset manifest)
- **Dataset:** `privacy_friendly_analytics`
- **Warehouse:** BigQuery
- **Tables:** `events`, `sessions`
- **Grain:** `events` is one row per event; `sessions` is one row per session
- **Join key:** `session_id` links events to sessions; `user_pseudo_id` links across users

## Schema: `events`

Table: `{project}.privacy_friendly_analytics.events`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| event_date | DATE | YES | Partition key — date of the event |
| platform | STRING | YES | Platform: web, ios, android |
| subsidiary | STRING | YES | Subsidiary code (e.g., "nl", "be") |
| language | STRING | YES | Language code |
| event_name | STRING | YES | Event type identifier (e.g., page_view, add_to_cart) |
| event_id | INT64 | YES | Unique event identifier |
| event_timestamp_bucket_utc | TIMESTAMP | YES | Bucketed event timestamp (UTC) |
| event_datetime | DATETIME | YES | Exact event datetime |
| event_timestamp_micros | INT64 | YES | Event timestamp in microseconds |
| user_pseudo_id | INT64 | YES | Pseudonymized user identifier |
| session_id | INT64 | YES | Session identifier — joins to sessions table |
| session_date | DATE | YES | Date the session started |
| session_start_datetime | DATETIME | YES | Session start datetime |
| session_start_timestamp_micros | INT64 | YES | Session start in microseconds |
| context | STRING | YES | Page/screen context (e.g., "product_page", "checkout") |
| context_item_id | INT64 | YES | Item ID associated with the context |
| urls | STRUCT | YES | URL information (see nested schema below) |
| order_ids | STRUCT | YES | Order correlation and transaction IDs |
| item_ids | STRUCT | YES | Product/item identifiers (see nested schema below) |
| params | STRUCT | YES | Event parameters: context, feature, sub_feature, content, order_type, store info |
| context_params | STRUCT | YES | Contextual parameters: content_type, form_type, shipment, stock, warranty, discount flags |
| split_tests | ARRAY\<STRUCT\> | NO | A/B test assignments: experiment_id, variation_id, parameter |
| split_test_flags | STRUCT | YES | Feature flag assignments: test_name, variation_id |
| marketing_identifiers | STRUCT | YES | Marketing attribution: UTM params, click IDs (gclid, fbclid, etc.) |
| device | STRUCT | YES | Device info: category, brand, model, OS, browser, app version |
| tracking_setup | STRUCT | YES | Tracking metadata: platform, version, is_webview, web_application |
| cookie_preference | STRUCT | YES | Consent state: analytical, marketing, functional consent booleans |
| user_identity | STRUCT | YES | User identity: cookie_id, account_id, auth_state, customer_type, bot/internal flags |
| known_bot_session | BOOL | YES | Whether session is from a known bot |
| internal_user_session | BOOL | YES | Whether session is from an internal user |
| intraday | BOOL | YES | Whether this is intraday (not yet finalized) data |
| web_performance | STRUCT | YES | Core Web Vitals: CLS, FCP, FID, INP, LCP, TTFB |
| is_new_session | BOOL | YES | Whether this event started a new session |
| time_diff_micros | INT64 | YES | Time difference from previous event in microseconds |
| subsidiary_name | STRING | YES | Full subsidiary name |
| subsidiary_id | INT64 | YES | Subsidiary numeric identifier |
| segment | STRING | YES | User segment classification |

### Nested STRUCT details — `urls`

```
urls.page_location         STRING   — Full page URL
urls.referrer              STRING   — Referrer URL
urls.deeplink_url          STRING   — App deeplink URL
urls.deeplink_referrer     STRING   — App deeplink referrer
urls.info.url_domain       STRING   — Extracted domain
urls.info.referrer_domain  STRING   — Extracted referrer domain
urls.info.url_path         STRING   — URL path component
urls.info.url_query_string STRING   — Query string
urls.info.url_fragment     STRING   — URL fragment
urls.info.language         STRING   — Language from URL
urls.info.subsidiary       STRING   — Subsidiary from URL
urls.info.context          STRING   — Context from URL
urls.info.context_item_id  INT64    — Item ID from URL
```

### Nested STRUCT details — `item_ids`

```
item_ids.item_id                  INT64          — Primary item ID for this event
item_ids.primary_item_id          INT64          — Primary (parent) product ID
item_ids.attached_item_id         INT64          — Single attached item
item_ids.attached_item_ids        ARRAY<INT64>   — Multiple attached items
item_ids.context_item_id          INT64          — Item from page context
item_ids.context_item_ids         ARRAY<INT64>   — Multiple context items
item_ids.context_related_item_id  INT64          — Related item in context
item_ids.context_product_type_ids ARRAY<INT64>   — Product type IDs in context
item_ids.context_brand_ids        ARRAY<INT64>   — Brand IDs in context
item_ids.cart_item_ids            ARRAY<INT64>   — Items in cart
```

### Nested STRUCT details — `marketing_identifiers`

```
marketing_identifiers.source      STRING — Traffic source
marketing_identifiers.referrer    STRING — Referrer
marketing_identifiers.utm_source  STRING — UTM source
marketing_identifiers.utm_medium  STRING — UTM medium
marketing_identifiers.utm_campaign STRING — UTM campaign
marketing_identifiers.utm_content STRING — UTM content
marketing_identifiers.utm_term   STRING — UTM term
marketing_identifiers.cmt        STRING — Custom marketing tag
marketing_identifiers.gclid      STRING — Google click ID
marketing_identifiers.gbraid     STRING — Google broad match ID
marketing_identifiers.wbraid     STRING — Google web-to-app ID
marketing_identifiers.msclkid    STRING — Microsoft click ID
marketing_identifiers.fbclid     STRING — Facebook click ID
marketing_identifiers.dclid      STRING — DoubleClick ID
marketing_identifiers.message_id STRING — Message ID
marketing_identifiers.clickref   STRING — Click reference
marketing_identifiers.push_id    STRING — Push notification ID
marketing_identifiers.ttclid     STRING — TikTok click ID
marketing_identifiers.soluteclid STRING — Solute click ID
```

## Schema: `sessions`

Table: `{project}.privacy_friendly_analytics.sessions`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| session_date | DATE | YES | Partition key — date the session started |
| platform | STRING | YES | Platform: WEB, IOS, ANDROID |
| subsidiary | STRING | YES | Subsidiary code |
| language | STRING | YES | Language code |
| session_id | INT64 | YES | Unique session identifier — joins to events table |
| session_start_datetime | DATETIME | YES | Session start time |
| session_end_datetime | DATETIME | YES | Session end time |
| user_pseudo_id | INT64 | YES | Pseudonymized user identifier |
| context_set | STRUCT | YES | Distinct contexts visited: unique_items, first, last |
| page_location_set | STRUCT | YES | Distinct pages visited: unique_items, first, last |
| count_distinct | STRUCT | YES | Session-level counts (see nested schema below) |
| user_identity | STRUCT | YES | User identity: cookie_id, account_id, customer_id, auth_state, customer_type, bot/internal flags |
| intraday | BOOL | YES | Whether this is intraday (not yet finalized) data |
| cookie_preference_set | STRUCT | YES | Consent states during session (first/last for each type) |
| device | STRUCT | YES | Device info: category, brand, model, OS, browser, app |
| tracking_setup | STRUCT | YES | Tracking metadata: platform, version, web_application_set |
| subsidiary_name | STRING | YES | Full subsidiary name |
| subsidiary_id | INT64 | YES | Subsidiary numeric identifier |
| subsidiary_set | STRUCT | YES | Subsidiaries visited during session |
| language_set | STRUCT | YES | Languages used during session |
| seen_context | STRUCT | YES | Page types seen during session (see nested schema below) |
| split_tests | ARRAY\<STRUCT\> | NO | A/B test assignments |
| split_test_flags | ARRAY\<STRUCT\> | NO | Feature flag assignments |
| traffic_sources | ARRAY\<STRUCT\> | NO | Traffic source landings with marketing identifiers and ad info |
| order_placed | INT64 | YES | Number of orders placed in session |
| orders | ARRAY\<STRUCT\> | NO | Order details: order_id, order_datetime, primary_product_id |
| add_to_cart | INT64 | YES | Number of add-to-cart actions |
| add_to_cart_set | STRUCT | YES | Product IDs added to cart (first/last) |
| product_page_set | STRUCT | YES | Product IDs viewed (first/last) |
| product_attribution | STRUCT | YES | Product attribution: product_id, attribution_type |
| bounce | INT64 | YES | Whether session was a bounce (1 = bounce) |
| segment_set | STRUCT | YES | User segments during session |
| is_first_app_instance | BOOL | YES | First app launch for this device |
| is_continued_session | BOOL | YES | Session continued from previous day |

### Nested STRUCT details — `count_distinct`

```
count_distinct.page_views                              INT64 — Distinct page views
count_distinct.view_contexts                           INT64 — Distinct view contexts
count_distinct.add_to_carts                            INT64 — Total add-to-cart events
count_distinct.add_to_carts_by_type.add_to_cart        INT64 — Standard add-to-cart
count_distinct.add_to_carts_by_type.add_bundle_to_cart INT64 — Bundle add-to-cart
count_distinct.add_to_carts_by_type.add_accessory_to_cart INT64 — Accessory add-to-cart
count_distinct.add_to_carts_by_type.reserve_item       INT64 — Reserve item
count_distinct.show_errors                             INT64 — Error events
count_distinct.add_to_wishlists                        INT64 — Wishlist additions
count_distinct.events                                  INT64 — Total events
count_distinct.contexts                                INT64 — Distinct contexts
count_distinct.page_locations                          INT64 — Distinct page locations
```

### Nested STRUCT details — `seen_context`

```
seen_context.home_page                                      INT64
seen_context.visual_page                                    INT64
seen_context.search_page                                    INT64
seen_context.filter_page                                    INT64
seen_context.product_page                                   INT64
seen_context.product_page_by_type.product_page              INT64
seen_context.product_page_by_type.second_chance_page        INT64
seen_context.product_page_by_type.subscription_page         INT64
seen_context.shopping_cart                                   INT64
seen_context.checkout_page                                   INT64
seen_context.checkout_by_type.checkout_overview_page        INT64
seen_context.checkout_by_type.checkout_details_page         INT64
seen_context.checkout_by_type.checkout_delivery_method_page INT64
seen_context.checkout_by_type.checkout_delivery_partner_pickup_page INT64
seen_context.checkout_by_type.checkout_timeslot_page        INT64
seen_context.checkout_by_type.checkout_payment_page         INT64
seen_context.checkout_by_type.checkout_thankyou_page        INT64
seen_context.checkout_by_type.checkout_login_page           INT64
seen_context.checkout_by_type.checkout                      INT64
seen_context.wishlist_page                                   INT64
seen_context.advice_page                                     INT64
seen_context.product_support_hub                             INT64
seen_context.energy                                          INT64
```

### Nested STRUCT details — `traffic_sources` (array element)

```
traffic_sources[].landing_number                    INT64
traffic_sources[].landing_id                        INT64
traffic_sources[].marketing_channel                 STRING
traffic_sources[].landing_timestamp_micros          INT64
traffic_sources[].marketing_identifiers.source      STRING
traffic_sources[].marketing_identifiers.utm_source  STRING
traffic_sources[].marketing_identifiers.utm_medium  STRING
traffic_sources[].marketing_identifiers.utm_campaign STRING
traffic_sources[].marketing_identifiers.utm_content STRING
traffic_sources[].marketing_identifiers.utm_term   STRING
traffic_sources[].marketing_identifiers.gclid      STRING
traffic_sources[].marketing_identifiers.fbclid     STRING
traffic_sources[].marketing_identifiers.msclkid    STRING
traffic_sources[].ad_info.google_ad_group_id       STRING
traffic_sources[].ad_info.bing_ad_group_id         STRING
```

## Data Quirks

- **Partition columns:** `events` partitions on `event_date`; `sessions` partitions on `session_date`. Always filter on the partition column to avoid full table scans.
- **Intraday rows:** When `intraday = TRUE`, the data is not yet finalized and may change. Exclude intraday rows for reliable analysis: `WHERE intraday = FALSE` or `WHERE intraday IS FALSE`.
- **Bot & internal traffic:** Filter out bots and internal users for user-facing analysis: `WHERE known_bot_session = FALSE AND internal_user_session = FALSE` (events) or `WHERE user_identity.is_bot = FALSE AND user_identity.is_internal_user = FALSE` (sessions).
- **Nested STRUCTs:** Many columns are deeply nested. Use BigQuery dot notation (e.g., `urls.info.url_path`) or `UNNEST()` for arrays (e.g., `split_tests`, `orders`, `traffic_sources`).
- **`_set` columns in sessions:** Columns ending in `_set` (e.g., `context_set`, `subsidiary_set`) contain `STRUCT<unique_items ARRAY, first, last>` — use `.unique_items` for all distinct values, `.first`/`.last` for session entry/exit.
- **`seen_context` for funnel analysis:** The `seen_context` struct on sessions is pre-aggregated — use it for funnel analysis instead of re-aggregating from events.
- **`count_distinct` for session metrics:** Pre-aggregated counts per session — use these instead of counting events.
- **`split_tests` is NOT NULL:** The `split_tests` column is `NOT NULL` (returns empty array, not null). Use `ARRAY_LENGTH(split_tests) > 0` to check for experiment participation.
- **Timestamp granularity:** `event_timestamp_micros` and `session_start_timestamp_micros` are in microseconds. Divide by 1000000 to get seconds for Unix timestamp operations.
- **`bounce`:** Stored as INT64 (0 or 1), not BOOL. Use `bounce = 1` for bounce sessions.
- **`order_placed`:** Stored as INT64 count, not BOOL. `order_placed > 0` means the session had a conversion.

## Common Query Patterns

### Filter template (always start with this)
```sql
WHERE event_date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
  AND known_bot_session = FALSE
  AND internal_user_session = FALSE
```

### Funnel from sessions table
```sql
SELECT
  subsidiary,
  COUNT(*) AS sessions,
  COUNTIF(seen_context.product_page > 0) AS saw_product,
  COUNTIF(add_to_cart > 0) AS added_to_cart,
  COUNTIF(seen_context.checkout_page > 0) AS reached_checkout,
  COUNTIF(order_placed > 0) AS converted
FROM `{project}.privacy_friendly_analytics.sessions`
WHERE session_date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
  AND user_identity.is_bot = FALSE
  AND user_identity.is_internal_user = FALSE
GROUP BY subsidiary
```

### Unnest experiment assignments
```sql
SELECT
  st.experiment_id,
  st.variation_id,
  COUNT(DISTINCT session_id) AS sessions
FROM `{project}.privacy_friendly_analytics.sessions`,
  UNNEST(split_tests) AS st
WHERE session_date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
GROUP BY 1, 2
```

## Entity Relationships

```
events.session_id      → sessions.session_id      (many-to-one)
events.user_pseudo_id  → sessions.user_pseudo_id  (many-to-many via sessions)
events.subsidiary_id   → sessions.subsidiary_id   (shared dimension)
```

## Supported Analyses

Given this schema, the following analyses are well-supported:
- **Funnel analysis:** `seen_context` + `order_placed` on sessions, or event-level sequence from events
- **Segmentation:** By platform, subsidiary, device.category, segment, customer_type
- **Traffic attribution:** `traffic_sources` array with marketing channel and UTM params
- **A/B test analysis:** `split_tests` array on both tables
- **Web performance:** `web_performance` struct on events (Core Web Vitals)
- **Conversion drivers:** Combine session-level counts with conversion outcome
- **User journey:** Event sequences within sessions using event_datetime ordering
