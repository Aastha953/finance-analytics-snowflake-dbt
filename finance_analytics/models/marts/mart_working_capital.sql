{{ config(
    materialized='table'
) }}

WITH ar AS (

    SELECT
        DATE_TRUNC('month', invoice_date) AS month,
        SUM(invoice_amount) AS ar_invoiced,
        SUM(payment_amount) AS ar_collected,
        SUM(outstanding_amount) AS ar_outstanding
    FROM {{ ref('core_accounts_receivable') }}
    GROUP BY DATE_TRUNC('month', invoice_date)

),

ap AS (

    SELECT
        DATE_TRUNC('month', invoice_date) AS month,
        SUM(invoice_amount) AS ap_invoiced,
        SUM(payment_amount) AS ap_paid,
        SUM(outstanding_amount) AS ap_outstanding
    FROM {{ ref('core_accounts_payable') }}
    GROUP BY DATE_TRUNC('month', invoice_date)

)

SELECT
    COALESCE(ar.month, ap.month) AS month,

    COALESCE(ar.ar_invoiced, 0) AS ar_invoiced,
    COALESCE(ar.ar_collected, 0) AS ar_collected,
    COALESCE(ar.ar_outstanding, 0) AS ar_outstanding,

    COALESCE(ap.ap_invoiced, 0) AS ap_invoiced,
    COALESCE(ap.ap_paid, 0) AS ap_paid,
    COALESCE(ap.ap_outstanding, 0) AS ap_outstanding,

    COALESCE(ar.ar_outstanding, 0)
        - COALESCE(ap.ap_outstanding, 0) AS working_capital

FROM ar

FULL OUTER JOIN ap
    ON ar.month = ap.month