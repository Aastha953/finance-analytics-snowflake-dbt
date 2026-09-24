{{ config(
    materialized='view'
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
    gross_profit
FROM {{ source('raw', 'RAW_SALES') }}