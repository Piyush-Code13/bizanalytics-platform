SELECT
    order_id,
    product_id,
    seller_id,
    price,
    freight_value
FROM {{ source('ecommerce_raw', 'order_items') }}