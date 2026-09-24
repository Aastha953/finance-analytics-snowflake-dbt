{{ config(
    materialized='table'
) }}

WITH sales AS (

    SELECT
        DATE_TRUNC('month', sales_date) AS month,
        SUM(revenue) AS revenue,
        SUM(cost) AS cost,
        SUM(gross_profit) AS gross_profit
    FROM {{ ref('core_sales') }}
    GROUP BY DATE_TRUNC('month', sales_date)

),

ar AS (

    SELECT
        DATE_TRUNC('month', invoice_date) AS month,
        SUM(outstanding_amount) AS ar_outstanding
    FROM {{ ref('core_accounts_receivable') }}
    GROUP BY DATE_TRUNC('month', invoice_date)

),

ap AS (

    SELECT
        DATE_TRUNC('month', invoice_date) AS month,
        SUM(outstanding_amount) AS ap_outstanding
    FROM {{ ref('core_accounts_payable') }}
    GROUP BY DATE_TRUNC('month', invoice_date)

)

SELECT
    s.month,

    s.revenue,
    s.cost,
    s.gross_profit,

    CASE
        WHEN s.revenue = 0 THEN 0
        ELSE s.gross_profit / s.revenue
    END AS gross_margin,

    COALESCE(ar.ar_outstanding, 0) AS ar_outstanding,
    COALESCE(ap.ap_outstanding, 0) AS ap_outstanding,

    COALESCE(ar.ar_outstanding, 0)
        - COALESCE(ap.ap_outstanding, 0) AS working_capital

FROM sales s

LEFT JOIN ar
    ON s.month = ar.month

LEFT JOIN ap
    ON s.month = ap.month