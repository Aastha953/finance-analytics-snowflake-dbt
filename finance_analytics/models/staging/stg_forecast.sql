{{ config(
    materialized='view'
) }}

SELECT
    budget_month,
    account_id,
    cost_center_id,
    forecast_amount,
    forecast_version
FROM {{ source('raw', 'RAW_FORECAST') }}