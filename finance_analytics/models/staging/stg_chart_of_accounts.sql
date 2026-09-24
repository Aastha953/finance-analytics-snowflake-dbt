{{ config(
    materialized='view'
) }}

SELECT
    account_id,
    account_number,
    account_name,
    account_type,
    financial_statement
FROM {{ source('raw', 'RAW_CHART_OF_ACCOUNTS') }}