-- Customer dimension: one row per customer.

with sales as (

    select * from {{ ref('stg_sales') }}

)

select
    customer_id,
    max(customer_name)              as customer_name,
    max(customer_city)              as customer_city,
    min(order_date)                 as first_order_date,
    max(order_date)                 as last_order_date,
    count(distinct order_id)        as order_count,
    sum(line_total)                 as lifetime_value
from sales
group by customer_id
