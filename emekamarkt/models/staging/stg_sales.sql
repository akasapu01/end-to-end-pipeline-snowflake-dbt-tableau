-- Cleaned, typed sales order lines from the raw seed.

with source as (

    select * from {{ ref('raw_sales') }}

)

select
    cast(order_id as varchar)          as order_id,
    cast(order_date as date)           as order_date,
    cast(customer_id as varchar)       as customer_id,
    trim(customer_name)                as customer_name,
    trim(customer_city)                as customer_city,
    cast(product_id as varchar)        as product_id,
    trim(product_name)                 as product_name,
    trim(category)                     as category,
    cast(unit_price as {{ dbt.type_numeric() }})   as unit_price,
    cast(quantity as integer)          as quantity,
    cast(unit_price as {{ dbt.type_numeric() }}) * cast(quantity as integer) as line_total
from source
