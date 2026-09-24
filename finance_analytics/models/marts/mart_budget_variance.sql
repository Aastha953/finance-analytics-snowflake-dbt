{{ config(
    materialized='table'
) }}

WITH actuals AS (

    SELECT
        DATE_TRUNC('month', transaction_date) AS month,
        account_id,
        cost_center_id,
        SUM(net_amount) AS actual_amount
    FROM {{ ref('core_general_ledger') }}
    GROUP BY
        DATE_TRUNC('month', transaction_date),
        account_id,
        cost_center_id

),

budget AS (

    SELECT
        DATE_TRUNC('month', budget_month) AS month,
        account_id,
        cost_center_id,
        SUM(budget_amount) AS budget_amount
    FROM {{ ref('core_budget') }}
    GROUP BY
        DATE_TRUNC('month', budget_month),
        account_id,
        cost_center_id

)

SELECT
    COALESCE(a.month, b.month) AS month,
    COALESCE(a.account_id, b.account_id) AS account_id,
    COALESCE(a.cost_center_id, b.cost_center_id) AS cost_center_id,

    COALESCE(a.actual_amount, 0) AS actual_amount,
    COALESCE(b.budget_amount, 0) AS budget_amount,

    COALESCE(a.actual_amount, 0)
        - COALESCE(b.budget_amount, 0) AS variance_amount,

    CASE
        WHEN COALESCE(b.budget_amount, 0) = 0 THEN NULL
        ELSE
            (
                COALESCE(a.actual_amount, 0)
                - COALESCE(b.budget_amount, 0)
            ) / ABS(b.budget_amount)
    END AS variance_percentage

FROM actuals a

FULL OUTER JOIN budget b
    ON a.month = b.month
    AND a.account_id = b.account_id
    AND a.cost_center_id = b.cost_center_id