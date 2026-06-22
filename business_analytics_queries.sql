-- =========================================================
-- BUSINESS ANALYTICS PROJECT
-- Dataset: ecommerce_raw
-- Project: bizanalytics-project
-- =========================================================

------------------------------------------------------------
-- STEP 1: Total Revenue
------------------------------------------------------------
SELECT
    ROUND(SUM(payment_value),2) AS total_revenue
FROM `bizanalytics-project.ecommerce_raw.order_payments`;

------------------------------------------------------------
-- STEP 2: Average Order Value
------------------------------------------------------------
SELECT
    ROUND(AVG(payment_value),2) AS average_order_value
FROM `bizanalytics-project.ecommerce_raw.order_payments`;

------------------------------------------------------------
-- STEP 3: Orders by Status
------------------------------------------------------------
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM `bizanalytics-project.ecommerce_raw.orders`
GROUP BY order_status
ORDER BY total_orders DESC;

------------------------------------------------------------
-- STEP 4: Monthly Revenue Trend
------------------------------------------------------------
SELECT
    FORMAT_DATE('%Y-%m', DATE(o.order_purchase_timestamp)) AS month,
    ROUND(SUM(p.payment_value),2) AS revenue
FROM `bizanalytics-project.ecommerce_raw.orders` o
JOIN `bizanalytics-project.ecommerce_raw.order_payments` p
ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;

------------------------------------------------------------
-- STEP 5: Top 10 Product Categories by Revenue
------------------------------------------------------------
SELECT
    p.product_category_name,
    ROUND(SUM(pay.payment_value),2) AS revenue
FROM `bizanalytics-project.ecommerce_raw.products` p
JOIN `bizanalytics-project.ecommerce_raw.order_items` oi
ON p.product_id = oi.product_id
JOIN `bizanalytics-project.ecommerce_raw.order_payments` pay
ON oi.order_id = pay.order_id
GROUP BY p.product_category_name
ORDER BY revenue DESC
LIMIT 10;

------------------------------------------------------------
-- STEP 6: Top 10 Sellers by Revenue
------------------------------------------------------------
SELECT
    seller_id,
    ROUND(SUM(payment_value),2) AS revenue
FROM `bizanalytics-project.ecommerce_raw.order_items` oi
JOIN `bizanalytics-project.ecommerce_raw.order_payments` op
ON oi.order_id = op.order_id
GROUP BY seller_id
ORDER BY revenue DESC
LIMIT 10;

------------------------------------------------------------
-- STEP 7: Average Delivery Time
------------------------------------------------------------
SELECT
    AVG(
        DATE_DIFF(
            DATE(order_delivered_customer_date),
            DATE(order_purchase_timestamp),
            DAY
        )
    ) AS avg_delivery_days
FROM `bizanalytics-project.ecommerce_raw.orders`
WHERE order_delivered_customer_date IS NOT NULL;

------------------------------------------------------------
-- STEP 8: Customer Distribution by State
------------------------------------------------------------
SELECT
    customer_state,
    COUNT(*) AS customers
FROM `bizanalytics-project.ecommerce_raw.customers`
GROUP BY customer_state
ORDER BY customers DESC;

------------------------------------------------------------
-- STEP 9: Payment Type Distribution
------------------------------------------------------------
SELECT
    payment_type,
    COUNT(*) AS transactions
FROM `bizanalytics-project.ecommerce_raw.order_payments`
GROUP BY payment_type
ORDER BY transactions DESC;

------------------------------------------------------------
-- STEP 10: Orders by Weekday
------------------------------------------------------------
SELECT
    FORMAT_DATE('%A', DATE(order_purchase_timestamp)) AS weekday,
    COUNT(*) AS total_orders
FROM `bizanalytics-project.ecommerce_raw.orders`
GROUP BY weekday
ORDER BY total_orders DESC;

------------------------------------------------------------
-- STEP 11: Top 10 Most Sold Products
------------------------------------------------------------
SELECT
    p.product_category_name,
    COUNT(*) AS total_sales
FROM `bizanalytics-project.ecommerce_raw.order_items` oi
JOIN `bizanalytics-project.ecommerce_raw.products` p
ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_sales DESC
LIMIT 10;

------------------------------------------------------------
-- STEP 12: Repeat Customers
------------------------------------------------------------
SELECT
    COUNT(*) AS repeat_customers
FROM (
    SELECT
        customer_id,
        COUNT(order_id) AS orders_count
    FROM `bizanalytics-project.ecommerce_raw.orders`
    GROUP BY customer_id
    HAVING COUNT(order_id) > 1
);