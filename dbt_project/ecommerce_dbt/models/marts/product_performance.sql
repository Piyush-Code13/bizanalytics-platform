SELECT
    p.product_category_name,
    COUNT(oi.order_id) AS total_sales,
    SUM(oi.price) AS revenue
FROM {{ ref('stg_order_items') }} oi
JOIN {{ ref('stg_products') }} p
ON oi.product_id = p.product_id
GROUP BY 1