SELECT
    s.seller_state,
    COUNT(DISTINCT s.seller_id) AS total_sellers,
    SUM(oi.price) AS seller_revenue
FROM {{ ref('stg_sellers') }} s
JOIN {{ ref('stg_order_items') }} oi
ON s.seller_id = oi.seller_id
GROUP BY 1