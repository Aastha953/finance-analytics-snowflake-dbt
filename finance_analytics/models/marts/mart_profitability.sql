{{ config(
    materialized='table'
) }}

SELECT
    DATE_TRUNC('month', sales_date) AS month,
    product,
    business_unit,
    region,

    SUM(revenue) AS revenue,
    SUM(cost) AS cost,
    SUM(gross_profit) AS gross_profit,

    CASE
        WHEN SUM(revenue) = 0 THEN 0
        ELSE SUM(gross_profit) / SUM(revenue)
    END AS gross_margin

FROM {{ ref('core_sales') }}

GROUP BY
    DATE_TRUNC('month', sales_date),
    product,
    business_unit,
    region