{{ config(
    materialized='table'
) }}

WITH sales AS (
    SELECT
        sales_date,
        business_unit,
        region,
        revenue,
        cost,
        gross_profit
    FROM {{ ref('core_sales') }}
),

monthly_pnl AS (
    SELECT
        DATE_TRUNC('month', sales_date) AS month,
        business_unit,
        region,

        SUM(revenue) AS revenue,
        SUM(cost) AS cost,
        SUM(gross_profit) AS gross_profit,

        CASE
            WHEN SUM(revenue) = 0 THEN 0
            ELSE SUM(gross_profit) / SUM(revenue)
        END AS gross_margin

    FROM sales
    GROUP BY
        DATE_TRUNC('month', sales_date),
        business_unit,
        region
)

SELECT
    month,
    business_unit,
    region,
    revenue,
    cost,
    gross_profit,
    gross_margin
FROM monthly_pnl