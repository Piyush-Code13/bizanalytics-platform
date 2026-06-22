SELECT
    order_id,
    payment_type,
    payment_value
FROM {{ source('ecommerce_raw', 'order_payments') }}