select
    avg(
        date_diff(
            date(order_delivered_customer_date),
            date(order_purchase_timestamp),
            day
        )
    ) as avg_delivery_days
from {{ source('ecommerce_raw','orders') }}
where order_delivered_customer_date is not null