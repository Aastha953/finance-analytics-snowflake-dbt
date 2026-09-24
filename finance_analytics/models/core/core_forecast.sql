{{ config(
    materialized='table'
) }}

SELECT
    budget_month,
    account_id,
    cost_center_id,
    forecast_amount,
    forecast_version
FROM {{ ref('stg_forecast') }}