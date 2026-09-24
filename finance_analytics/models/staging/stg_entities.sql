{{ config(
    materialized='view'
) }}

SELECT
    entity_id,
    entity_name,
    country,
    currency
FROM {{ source('raw', 'RAW_ENTITIES') }}