SELECT
    c.customer_state,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    COUNT(o.order_id) AS total_orders
FROM {{ ref('stg_customers') }} c
JOIN {{ ref('stg_orders') }} o
ON c.customer_id = o.customer_id
GROUP BY 1