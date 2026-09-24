{{ config(
    materialized='table'
) }}

SELECT
    sales_id,
    sales_date,
    customer_id,
    product,
    business_unit,
    region,
    revenue,
    cost,
    gross_profit,
    revenue - cost AS calculated_gross_profit
FROM {{ ref('stg_sales') }}