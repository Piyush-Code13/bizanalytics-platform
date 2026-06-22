SELECT
    DATE(o.order_purchase_timestamp) AS order_date,
    SUM(p.payment_value) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_order_payments') }} p
ON o.order_id = p.order_id
GROUP BY 1