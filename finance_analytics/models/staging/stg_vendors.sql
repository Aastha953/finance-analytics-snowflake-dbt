{{ config(
    materialized='view'
) }}

SELECT
    vendor_id,
    vendor_name,
    vendor_category,
    city,
    state,
    payment_terms
FROM {{ source('raw', 'RAW_VENDORS') }}