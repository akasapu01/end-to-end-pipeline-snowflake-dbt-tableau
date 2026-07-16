-- Product dimension: one row per product.

with sales as (

    select * from {{ ref('stg_sales') }}

)

select
    product_id,
    max(product_name)       as product_name,
    max(category)           as category,
    max(unit_price)         as unit_price,
    sum(quantity)           as units_sold,
    sum(line_total)         as revenue
from sales
group by product_id
