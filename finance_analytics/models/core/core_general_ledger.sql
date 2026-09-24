{{ config(
    materialized='table'
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
    source_system,

    COALESCE(debit, 0) - COALESCE(credit, 0) AS net_amount,

    CASE
        WHEN COALESCE(debit, 0) > 0 THEN 'Debit'
        WHEN COALESCE(credit, 0) > 0 THEN 'Credit'
        ELSE 'Zero'
    END AS transaction_type

FROM {{ ref('stg_general_ledger') }}