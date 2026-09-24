{{ config(
    materialized='view'
) }}

SELECT
    invoice_id,
    customer_id,
    invoice_date,
    due_date,
    payment_date,
    invoice_amount,
    payment_amount,
    currency,
    status
FROM {{ source('raw', 'RAW_ACCOUNTS_RECEIVABLE') }}