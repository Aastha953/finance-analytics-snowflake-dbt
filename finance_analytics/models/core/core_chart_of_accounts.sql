{{ config(
    materialized='table'
) }}

SELECT
    account_id,
    account_number,
    account_name,
    account_type,
    financial_statement
FROM {{ ref('stg_chart_of_accounts') }}