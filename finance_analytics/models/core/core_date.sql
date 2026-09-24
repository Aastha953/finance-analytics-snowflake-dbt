{{ config(
    materialized='table'
) }}

WITH dates AS (
    SELECT
        DATEADD(
            'day',
            SEQ4(),
            '2024-01-01'::DATE
        ) AS date_day
    FROM TABLE(
        GENERATOR(ROWCOUNT => 1096)
    )
)

SELECT
    date_day,
    YEAR(date_day) AS year,
    MONTH(date_day) AS month,
    MONTHNAME(date_day) AS month_name,
    QUARTER(date_day) AS quarter,
    DAY(date_day) AS day,
    DAYOFWEEK(date_day) AS day_of_week,
    DAYNAME(date_day) AS day_name,
    DATE_TRUNC('month', date_day) AS month_start,
    DATE_TRUNC('quarter', date_day) AS quarter_start,
    DATE_TRUNC('year', date_day) AS year_start
FROM dates