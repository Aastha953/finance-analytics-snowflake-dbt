{{ config(
    materialized='view'
) }}

SELECT
    transaction_id,
    transaction_date,
    account_id,
    cost_center_id,
    entity_id,
    debit,
    credit,
    currency,
    description,
    source_system
FROM {{ source('raw', 'RAW_GENERAL_LEDGER') }}