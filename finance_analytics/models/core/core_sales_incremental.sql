{{ config(
    materialized='incremental',
    unique_key='sales_id',
    on_schema_change='sync_all_columns'
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
FROM {{ ref('stg_sales') }}

{% if is_incremental() %}

WHERE sales_date >= (
    SELECT COALESCE(MAX(sales_date), '1900-01-01'::DATE)
    FROM {{ this }}
)

{% endif %}