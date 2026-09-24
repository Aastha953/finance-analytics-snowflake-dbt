{{ config(
    materialized='table'
) }}

SELECT
    cost_center_id,
    cost_center_name,
    department,
    region,
    manager
FROM {{ ref('stg_cost_centers') }}