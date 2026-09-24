{{ config(
    materialized='table'
) }}

SELECT
    customer_id,
    customer_name,
    city,
    state,
    customer_segment,
    signup_date
FROM {{ ref('stg_customers') }}