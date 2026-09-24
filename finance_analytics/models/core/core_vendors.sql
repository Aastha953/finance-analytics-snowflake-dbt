{{ config(
    materialized='table'
) }}

SELECT
    vendor_id,
    vendor_name,
    vendor_category,
    city,
    state,
    payment_terms
FROM {{ ref('stg_vendors') }}