---
name: ga4-dataset
description: 'Schema reference for the Google Analytics 4 (GA4) dataset. Use when the user mentions "Google Analytics 4", "GA4", or references cb-data-hub-prod.google_analytics_4 tables. Provides full schema, data quirks, and query patterns for the events and sessions tables.'
user-invocable: false
disable-model-invocation: false
---

# Google Analytics 4 (GA4) Dataset

## When to Use

Apply this skill when the data source involves:
- "Google Analytics 4", "GA4", or "google_analytics_4"
- `cb-data-hub-prod.google_analytics_4` BigQuery project
- The `events` or `sessions` tables from GA4

This skill provides pre-built schema knowledge so the data-explorer agent can
skip basic schema discovery and focus on profiling and quality assessment.

## Dataset Overview

- **Project:** `cb-data-hub-prod`
- **Dataset:** `google_analytics_4`
- **Warehouse:** BigQuery
- **Tables:** `events`, `sessions`
- **Grain:** `events` is one row per event; `sessions` is one row per session
- **Join key:** `total_session_id` links events to sessions; `user_pseudo_id` links across users

## Schema: `sessions`

Table: `cb-data-hub-prod.google_analytics_4.sessions`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| date | DATE | YES | Partition key — session date |
| total_session_id | STRING | YES | Unique session identifier — joins to events table |
| session_start_datetime | DATETIME | YES | Session start time |
| platform | STRING | YES | Platform: web, ios, android |
| subsidiary_id | INT64 | YES | Subsidiary numeric identifier |
| subsidiary_name | STRING | YES | Full subsidiary name |
| account_id | INT64 | YES | User account ID |
| customer_id | INT64 | YES | Customer ID |
| customer_type | STRING | YES | Customer type classification |
| coolblue_cookie_id | STRING | YES | Coolblue cookie identifier |
| user_first_touch_timestamp | INT64 | YES | First touch timestamp (micros) |
| user_pseudo_id | STRING | YES | GA4 pseudonymized user identifier |
| new_user | INT64 | YES | Whether this is a new user (0/1) |
| app_remove | INT64 | YES | App removal event in session (0/1) |
| language | STRING | YES | Language code |
| landing_context | STRING | YES | First page context in session |
| landing_page | STRING | YES | Landing page URL |
| exit_context | STRING | YES | Last page context in session |
| exit_page | STRING | YES | Exit page URL |
| split_test_parameters | STRING | YES | Serialized A/B test assignments |
| traffic_sources | ARRAY\<STRUCT\> | NO | Traffic source landings (see nested schema below) |
| device_category | STRING | YES | Device type: desktop, mobile, tablet |
| device_mobile_brand_name | STRING | YES | Device brand (e.g., Apple, Samsung) |
| device_mobile_model_name | STRING | YES | Device model name |
| device_mobile_marketing_name | STRING | YES | Device marketing name |
| device_operating_system | STRING | YES | OS name |
| device_operating_system_version | STRING | YES | OS version |
| device_browser | STRING | YES | Browser name |
| device_browser_version | STRING | YES | Browser version |
| app_info_version | STRING | YES | App version |
| app_info_latest_version | STRING | YES | Latest available app version |
| location_permission | STRING | YES | Location permission status |
| user_notification_pref | STRING | YES | Notification preference |
| user_interface_style | STRING | YES | UI style (light/dark) |
| app_notification | STRUCT | YES | App notification opt-in states |
| channel_id | STRING | YES | Channel identifier |
| geo_country | STRING | YES | Country |
| geo_region | STRING | YES | Region |
| geo_city | STRING | YES | City |
| engagement | INT64 | YES | Whether session was engaged (0/1) |
| bounce | INT64 | YES | Whether session bounced (0/1) |
| page_views | INT64 | YES | Page view count in session |
| view_contexts | INT64 | YES | Distinct contexts viewed |
| corrected_transactions | FLOAT64 | YES | Corrected transaction count |
| corrected_transactions_excl | FLOAT64 | YES | Corrected transactions excluding certain types |
| order_ids | ARRAY\<STRUCT\> | NO | Orders placed: orderid, transaction_id |
| add_to_wishlist | INT64 | YES | Wishlist additions in session |
| add_to_cart | INT64 | YES | Add-to-cart actions in session |
| last_payment_method_group | STRING | YES | Last payment method group used |
| last_payment_method | STRING | YES | Last payment method used |
| last_bank | STRING | YES | Last bank used for payment |
| login | INT64 | YES | Login events in session |
| logout | INT64 | YES | Logout events in session |
| sim_customer_id | STRING | YES | Simulated customer ID |
| landing_customer_recognition | STRING | YES | Customer recognition state at landing |
| cookie_preference | STRING | YES | Cookie consent preference |
| account_created_precheckout | INT64 | YES | Account created before checkout (0/1) |
| type_problem_solving_step_seen | STRING | YES | Problem-solving step type viewed |
| article_clicked_on_problem_solving_step | INT64 | YES | Article click on support step (0/1) |
| return_requested_through_form | INT64 | YES | Return requested via form (0/1) |
| filter_page_seen | INT64 | YES | Filter page viewed (0/1) |
| product_page_seen | INT64 | YES | Product page viewed (0/1) |
| search_page_seen | INT64 | YES | Search page viewed (0/1) |
| wishlist_page_seen | INT64 | YES | Wishlist page viewed (0/1) |
| cart_page_seen | INT64 | YES | Shopping cart viewed (0/1) |
| checkout_page_seen | INT64 | YES | Checkout page viewed (0/1) |
| checkout_details_page_seen | INT64 | YES | Checkout details page viewed (0/1) |
| checkout_login_page_seen | INT64 | YES | Checkout login page viewed (0/1) |
| checkout_delivery_method_page_seen | INT64 | YES | Delivery method page viewed (0/1) |
| checkout_delivery_partner_pickup_page_seen | INT64 | YES | Partner pickup page viewed (0/1) |
| checkout_timeslot_page_seen | INT64 | YES | Timeslot page viewed (0/1) |
| checkout_payment_page_seen | INT64 | YES | Payment page viewed (0/1) |
| checkout_overview_page_seen | INT64 | YES | Checkout overview page viewed (0/1) |
| checkout_thankyou_page_seen | INT64 | YES | Thank-you page viewed (0/1) |
| fast_checkout_seen | INT64 | YES | Fast checkout used (0/1) |
| advice_page_seen | INT64 | YES | Advice page viewed (0/1) |
| support_page_seen | INT64 | YES | Support page viewed (0/1) |
| home_page_seen | INT64 | YES | Home page viewed (0/1) |
| energy_page_seen | INT64 | YES | Energy page viewed (0/1) |
| login_portal_seen | INT64 | YES | Login portal viewed (0/1) |
| shopping_cart_continuation_session | INT64 | YES | Continuation session from cart (0/1) |
| checkout_login_page_continuation_session | INT64 | YES | Continuation from checkout login (0/1) |
| checkout_details_page_continuation_session | INT64 | YES | Continuation from checkout details (0/1) |
| checkout_delivery_method_page_continuation_session | INT64 | YES | Continuation from delivery method (0/1) |
| checkout_delivery_partner_pickup_page_continuation_session | INT64 | YES | Continuation from partner pickup (0/1) |
| checkout_timeslot_page_continuation_session | INT64 | YES | Continuation from timeslot (0/1) |
| checkout_overview_page_continuation_session | INT64 | YES | Continuation from overview (0/1) |
| checkout_payment_page_continuation_session | INT64 | YES | Continuation from payment (0/1) |
| last_delivery_method | STRING | YES | Last delivery method selected |
| germany_delivery_possible | STRING | YES | Whether Germany delivery was available |
| product_id_excl_historical_allocation | INT64 | YES | Product ID excluding historical allocation |
| product_id | INT64 | YES | Attributed product ID |
| page_category | STRING | YES | Page category classification |
| page_sub_category | STRING | YES | Page sub-category |
| order_placed | INT64 | YES | Number of orders placed (0/1+) |
| intraday | BOOL | YES | Whether this is intraday (not finalized) data |
| is_webshop | BOOL | YES | Whether session is on webshop |
| is_energy | BOOL | YES | Whether session is on energy site |
| product_id_attribution_type | STRING | YES | Product attribution type |
| is_jobs | BOOL | YES | Whether session is on jobs site |
| is_continued_session | BOOL | YES | Session continued from previous day |

### Nested STRUCT details — `traffic_sources` (array element)

```
traffic_sources[].landing_number                              INT64
traffic_sources[].landing_id                                  INT64
traffic_sources[].marketing_channel                           STRING
traffic_sources[].landing_timestamp                           INT64
traffic_sources[].marketing_identifiers_flat.source           STRING
traffic_sources[].marketing_identifiers_flat.referrer         STRING
traffic_sources[].marketing_identifiers_flat.utm_source       STRING
traffic_sources[].marketing_identifiers_flat.utm_medium       STRING
traffic_sources[].marketing_identifiers_flat.utm_campaign     STRING
traffic_sources[].marketing_identifiers_flat.utm_content      STRING
traffic_sources[].marketing_identifiers_flat.cmt              STRING
traffic_sources[].marketing_identifiers_flat.gclid            STRING
traffic_sources[].marketing_identifiers_flat.gbraid           STRING
traffic_sources[].marketing_identifiers_flat.wbraid           STRING
traffic_sources[].marketing_identifiers_flat.msclkid          STRING
traffic_sources[].marketing_identifiers_flat.fbclid           STRING
traffic_sources[].marketing_identifiers_flat.dclid            STRING
traffic_sources[].marketing_identifiers_flat.message_id       STRING
traffic_sources[].marketing_identifiers_flat.clickref         STRING
traffic_sources[].marketing_identifiers_flat.push_id          STRING
traffic_sources[].marketing_identifiers_flat.utm_term         STRING
traffic_sources[].marketing_identifiers_flat.ttclid           STRING
traffic_sources[].marketing_identifiers_flat.soluteclid       STRING
traffic_sources[].marketing_identifiers_flat.fbp              STRING
traffic_sources[].ad_info.google_ad_group_id                  STRING
traffic_sources[].ad_info.bing_ad_group_id                    STRING
traffic_sources[].marketing_identifiers[]                     ARRAY<STRUCT<key, value>>
```

### Nested STRUCT details — `app_notification`

```
app_notification.promotional_optin  INT64 — Promotional notification opt-in (0/1)
app_notification.order_optin        INT64 — Order notification opt-in (0/1)
app_notification.product_optin      INT64 — Product notification opt-in (0/1)
app_notification.stores_optin       INT64 — Stores notification opt-in (0/1)
```

### Nested STRUCT details — `order_ids` (array element)

```
order_ids[].orderid         INT64 — Order ID
order_ids[].transaction_id  INT64 — Transaction ID
```

## Schema: `events`

Table: `cb-data-hub-prod.google_analytics_4.events`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| event_date | STRING | YES | Event date as string (legacy format) |
| date | DATE | YES | Event date as DATE type — prefer this over event_date |
| event_timestamp | INT64 | YES | Event timestamp in microseconds |
| event_datetime | DATETIME | YES | Event datetime |
| event_hour | INT64 | YES | Hour of event (0-23) |
| event_minute | INT64 | YES | Minute of event (0-59) |
| event_name | STRING | YES | Event type identifier |
| event_params | ARRAY\<STRUCT\> | NO | Key-value event parameters |
| context | STRING | YES | Page/screen context |
| context_item_id | INT64 | YES | Item ID associated with the context |
| feature | STRING | YES | Feature name |
| sub_feature | STRING | YES | Sub-feature name |
| page_location | STRING | YES | Full page URL |
| page_category | STRING | YES | Page category classification |
| page_sub_category | STRING | YES | Page sub-category |
| is_non_interactive | BOOL | YES | Whether event is non-interactive |
| index | INT64 | YES | Event index within session |
| content | STRING | YES | Content identifier |
| input_field | STRING | YES | Input field name |
| item_id | INT64 | YES | Item/product ID |
| primary_item_id | INT64 | YES | Primary (parent) product ID |
| typeahead | STRING | YES | Typeahead/autocomplete value |
| session_first_event_datetime | DATETIME | YES | First event datetime in session |
| session_first_event_timestamp | INT64 | YES | First event timestamp in session |
| account_id | INT64 | YES | User account ID |
| user_pseudo_id | STRING | YES | GA4 pseudonymized user identifier |
| total_session_id | STRING | YES | Session identifier — joins to sessions table |
| coolblue_cookie_id | STRING | YES | Coolblue cookie identifier |
| cookie_preference | STRING | YES | Cookie consent preference |
| application | STRING | YES | Application identifier |
| user_properties | ARRAY\<STRUCT\> | NO | User properties key-value pairs |
| user_first_touch_timestamp | INT64 | YES | First touch timestamp (micros) |
| split_test_parameters | STRING | YES | Serialized A/B test assignments |
| language | STRING | YES | Language code |
| transaction_id | INT64 | YES | Transaction ID (for purchase events) |
| correlation_id | STRING | YES | Order correlation ID |
| platform | STRING | YES | Platform: web, ios, android |
| stream_id | STRING | YES | GA4 data stream ID |
| device | STRUCT | YES | Device information (see nested schema below) |
| app_info | STRUCT | YES | App information (see nested schema below) |
| push_id | STRING | YES | Push notification ID |
| channel_id | STRING | YES | Channel identifier |
| traffic_source | STRUCT | YES | Session-level traffic source (name, medium, source) |
| geo | STRUCT | YES | Geography: country, region, city |
| subsidiary_id | INT64 | YES | Subsidiary numeric identifier |
| subsidiary_name | STRING | YES | Full subsidiary name |
| sim_customer_id | STRING | YES | Simulated customer ID |
| intraday | BOOL | YES | Whether this is intraday (not finalized) data |
| event_id | INT64 | YES | Unique event identifier |
| status | STRING | YES | Event status |
| redirect | STRING | YES | Redirect information |
| attached_item_ids | STRING | YES | Attached item IDs (serialized) |
| attached_item_id | STRING | YES | Single attached item ID |
| feedback | STRING | YES | User feedback value |
| context_stock_status | STRING | YES | Stock status in context |
| option_names | STRING | YES | Option names selected |
| item_ids | STRING | YES | Multiple item IDs (serialized) |
| unique_id | STRING | YES | Unique identifier |
| method | STRING | YES | Method used (e.g., login method) |
| direction | STRING | YES | Direction (e.g., scroll direction) |
| search_term | STRING | YES | Search query |
| context_item_ids | STRING | YES | Item IDs in page context (serialized) |
| call_to_action_type | STRING | YES | CTA type clicked |
| segment | STRING | YES | User segment classification |
| authentication_state | STRING | YES | Authentication state |
| context_brand_ids | STRING | YES | Brand IDs in context (serialized) |
| context_product_type_ids | STRING | YES | Product type IDs in context (serialized) |

### Nested STRUCT details — `device`

```
device.category                        STRING — Device type: desktop, mobile, tablet
device.mobile_brand_name               STRING — Device brand
device.mobile_model_name               STRING — Device model
device.mobile_marketing_name           STRING — Marketing name
device.mobile_os_hardware_model        STRING — OS hardware model
device.operating_system                STRING — OS name
device.operating_system_version        STRING — OS version
device.language                        STRING — Device language
device.web_info.browser                STRING — Browser name
device.web_info.browser_version        STRING — Browser version
device.web_info.hostname               STRING — Website hostname
```

### Nested STRUCT details — `app_info`

```
app_info.id               STRING — App bundle ID
app_info.version          STRING — App version
app_info.install_source   STRING — Install source (e.g., Play Store)
app_info.latest_version   STRING — Latest available version
```

### Nested STRUCT details — `traffic_source`

```
traffic_source.name    STRING — Campaign name
traffic_source.medium  STRING — Traffic medium
traffic_source.source  STRING — Traffic source
```

### Nested STRUCT details — `geo`

```
geo.country  STRING — Country
geo.region   STRING — Region
geo.city     STRING — City
```

## Data Quirks

- **Partition columns:** `sessions` partitions on `date`; `events` partitions on `date`. Always filter on the partition column to avoid full table scans.
- **Dual date columns in events:** `event_date` is STRING (legacy), `date` is DATE. Always use `date` for filtering and grouping.
- **Intraday rows:** When `intraday = TRUE`, data is not finalized. Exclude for reliable analysis: `WHERE intraday = FALSE` or `WHERE intraday IS FALSE`.
- **Session join key is STRING:** `total_session_id` is a STRING in both tables (unlike PFA which uses INT64 `session_id`). Join on this column.
- **User identifier is STRING:** `user_pseudo_id` is STRING (unlike PFA where it is INT64).
- **`_seen` columns for funnel analysis:** Sessions has pre-computed `*_page_seen` columns (INT64, 0/1) for each checkout step — use these for funnel analysis instead of aggregating from events.
- **`_continuation_session` columns:** Indicate sessions that started from a specific checkout step (user returned to complete checkout). Important for understanding abandoned checkout recovery.
- **`bounce` and `engagement`:** Stored as INT64 (0/1). `bounce = 1` for bounce; `engagement = 1` for engaged session. These are mutually exclusive.
- **`corrected_transactions` is FLOAT64:** Not INT64. This allows fractional attribution. Use `corrected_transactions > 0` for conversion, not `order_placed > 0` if you need corrected numbers.
- **`order_placed` vs `corrected_transactions`:** `order_placed` is the raw count; `corrected_transactions` is the adjusted count. Clarify which the stakeholder wants.
- **`split_test_parameters` is STRING:** Unlike PFA's array of structs, GA4 stores experiment assignments as a serialized string. Parse it if you need to filter by experiment.
- **`event_params` is key-value array:** Use `UNNEST(event_params)` to extract specific parameters. Common pattern: `(SELECT value FROM UNNEST(event_params) WHERE key = 'param_name')`.
- **`user_properties` is key-value array:** Same pattern as `event_params` — unnest to extract values.
- **Serialized ID columns in events:** `attached_item_ids`, `item_ids`, `context_item_ids`, `context_brand_ids`, `context_product_type_ids` are STRING columns containing serialized lists, not arrays. Parse with `SPLIT()` or `JSON_EXTRACT_ARRAY()` depending on format.
- **`traffic_source` (events) vs `traffic_sources` (sessions):** Events has a single STRUCT for the session-level source. Sessions has the full ARRAY of landing-level sources. Use sessions for multi-touch attribution.
- **No bot/internal user filter columns:** Unlike PFA, GA4 does not have `known_bot_session` or `internal_user_session`. Bot filtering must be done upstream or via user_properties if available.
- **Timestamp granularity:** `event_timestamp`, `user_first_touch_timestamp`, and `session_first_event_timestamp` are in microseconds.
- **Site flags:** `is_webshop`, `is_energy`, `is_jobs` on sessions distinguish between site types. Filter accordingly for webshop-only analysis.

## Common Query Patterns

### Filter template (always start with this)
```sql
WHERE date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
```

### Funnel from sessions table
```sql
SELECT
  subsidiary_name,
  COUNT(*) AS sessions,
  COUNTIF(product_page_seen > 0) AS saw_product,
  COUNTIF(add_to_cart > 0) AS added_to_cart,
  COUNTIF(checkout_page_seen > 0) AS reached_checkout,
  COUNTIF(order_placed > 0) AS converted
FROM `cb-data-hub-prod.google_analytics_4.sessions`
WHERE date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
GROUP BY subsidiary_name
```

### Checkout step funnel (detailed)
```sql
SELECT
  subsidiary_name,
  COUNTIF(cart_page_seen > 0) AS cart,
  COUNTIF(checkout_details_page_seen > 0) AS details,
  COUNTIF(checkout_delivery_method_page_seen > 0) AS delivery,
  COUNTIF(checkout_payment_page_seen > 0) AS payment,
  COUNTIF(checkout_overview_page_seen > 0) AS overview,
  COUNTIF(checkout_thankyou_page_seen > 0) AS thankyou
FROM `cb-data-hub-prod.google_analytics_4.sessions`
WHERE date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
  AND checkout_page_seen > 0
GROUP BY subsidiary_name
```

### Extract event parameter
```sql
SELECT
  event_name,
  (SELECT value FROM UNNEST(event_params) WHERE key = 'param_name') AS param_value,
  COUNT(*) AS event_count
FROM `cb-data-hub-prod.google_analytics_4.events`
WHERE date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
GROUP BY 1, 2
```

### Unnest traffic sources
```sql
SELECT
  ts.marketing_channel,
  ts.marketing_identifiers_flat.utm_source,
  ts.marketing_identifiers_flat.utm_medium,
  COUNT(DISTINCT total_session_id) AS sessions,
  COUNTIF(order_placed > 0) AS conversions
FROM `cb-data-hub-prod.google_analytics_4.sessions`,
  UNNEST(traffic_sources) AS ts
WHERE date BETWEEN {{start_date}} and {{end_date}}
  AND intraday = FALSE
GROUP BY 1, 2, 3
```

## Entity Relationships

```
events.total_session_id   → sessions.total_session_id   (many-to-one)
events.user_pseudo_id     → sessions.user_pseudo_id     (many-to-many via sessions)
events.subsidiary_id      → sessions.subsidiary_id      (shared dimension)
```

## Supported Analyses

Given this schema, the following analyses are well-supported:
- **Funnel analysis:** `*_page_seen` columns on sessions for checkout funnel, or event-level sequences from events
- **Checkout drop-off:** Detailed step-by-step with `*_continuation_session` for recovery analysis
- **Segmentation:** By platform, subsidiary, device_category, customer_type, geo, segment
- **Traffic attribution:** `traffic_sources` array with marketing channels and UTM params
- **Conversion analysis:** `order_placed`, `corrected_transactions`, `add_to_cart` on sessions
- **Search analysis:** `search_term` and `search_page_seen` for search behavior
- **Payment analysis:** `last_payment_method`, `last_bank` for payment funnel
- **App analytics:** `app_info_version`, `app_remove`, notification opt-ins
- **User journey:** Event sequences within sessions using `event_datetime` ordering and `index`
- **Support/returns:** `type_problem_solving_step_seen`, `return_requested_through_form`

## Differences from PFA Dataset

| Aspect | GA4 | PFA |
|--------|-----|-----|
| Session ID type | STRING (`total_session_id`) | INT64 (`session_id`) |
| User ID type | STRING (`user_pseudo_id`) | INT64 (`user_pseudo_id`) |
| Bot filtering | No built-in columns | `known_bot_session`, `internal_user_session` |
| Funnel columns | Flat `*_page_seen` INT64 | Nested `seen_context` STRUCT |
| Split tests | Serialized STRING | ARRAY\<STRUCT\> |
| Event params | Key-value ARRAY | Named STRUCT fields |
| Device info | Flat columns on sessions | Nested STRUCT on both |
| Transactions | `corrected_transactions` FLOAT64 | `order_placed` INT64 |
| Consent | `cookie_preference` STRING | `cookie_preference` STRUCT with booleans |
