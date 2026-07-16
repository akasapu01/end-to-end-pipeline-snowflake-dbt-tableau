-- Singular data test: the sales fact must never contain a negative quantity.
-- dbt fails the test if this query returns any rows.

select *
from {{ ref('fact_sales') }}
where quantity < 0
