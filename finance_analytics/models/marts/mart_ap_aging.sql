{{ config(
    materialized='table'
) }}

SELECT
    invoice_id,
    vendor_id,
    invoice_date,
    due_date,
    payment_date,
    invoice_amount,
    payment_amount,
    outstanding_amount,
    currency,
    status,
    days_overdue,
    aging_bucket,

    CASE
        WHEN outstanding_amount > 0 THEN 1
        ELSE 0
    END AS is_outstanding

FROM {{ ref('core_accounts_payable') }}