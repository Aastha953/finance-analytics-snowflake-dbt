{{ config(
    materialized='view'
) }}

SELECT
    cost_center_id,
    cost_center_name,
    department,
    region,
    manager
FROM {{ source('raw', 'RAW_COST_CENTERS') }}