{{ config(
    materialized='table'
) }}

SELECT
    entity_id,
    entity_name,
    country,
    currency
FROM {{ ref('stg_entities') }}