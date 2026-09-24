{{ config(
    materialized='view'
) }}

SELECT
    budget_month,
    account_id,
    cost_center_id,
    budget_amount
FROM {{ source('raw', 'RAW_BUDGET') }}