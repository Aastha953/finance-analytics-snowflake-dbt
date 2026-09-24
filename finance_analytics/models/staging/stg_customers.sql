{{ config(
    materialized='view'
) }}

SELECT
    customer_id,
    customer_name,
    city,
    state,
    customer_segment,
    signup_date
FROM {{ source('raw', 'RAW_CUSTOMERS') }}
