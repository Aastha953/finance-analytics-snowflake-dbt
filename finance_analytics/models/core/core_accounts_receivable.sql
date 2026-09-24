{{ config(
    materialized='table'
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
    status,

    invoice_amount - payment_amount AS outstanding_amount,

    CASE
        WHEN payment_date IS NOT NULL THEN 0
        WHEN CURRENT_DATE() <= due_date THEN 0
        ELSE DATEDIFF('day', due_date, CURRENT_DATE())
    END AS days_overdue,

    CASE
        WHEN payment_date IS NOT NULL THEN 'Paid'
        WHEN CURRENT_DATE() <= due_date THEN 'Current'
        WHEN DATEDIFF('day', due_date, CURRENT_DATE()) BETWEEN 1 AND 30 THEN '1-30'
        WHEN DATEDIFF('day', due_date, CURRENT_DATE()) BETWEEN 31 AND 60 THEN '31-60'
        WHEN DATEDIFF('day', due_date, CURRENT_DATE()) BETWEEN 61 AND 90 THEN '61-90'
        ELSE '90+'
    END AS aging_bucket

FROM {{ ref('stg_accounts_receivable') }}