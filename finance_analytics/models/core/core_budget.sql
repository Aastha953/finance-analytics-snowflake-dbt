{{ config(
    materialized='table'
) }}

SELECT
    budget_month,
    account_id,
    cost_center_id,
    budget_amount
FROM {{ ref('stg_budget') }}