-- Sales fact table: grain = one order line (order_id + product_id).

with sales as (

    select * from {{ ref('stg_sales') }}

)

select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'product_id']) }} as sales_key,
    order_id,
    order_date,
    customer_id,
    product_id,
    quantity,
    unit_price,
    line_total
from sales
