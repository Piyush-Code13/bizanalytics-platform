SELECT
    order_id,
    review_score
FROM {{ source('ecommerce_raw', 'order_reviews') }}