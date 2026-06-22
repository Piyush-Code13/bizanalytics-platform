SELECT
    seller_id,
    seller_city,
    seller_state
FROM {{ source('ecommerce_raw', 'sellers') }}