{% snapshot snap_customers %}

{{
    config(
        target_schema='CORE',
        unique_key='customer_id',
        strategy='check',
        check_cols=[
            'customer_name',
            'city',
            'state',
            'customer_segment'
        ]
    )
}}

SELECT
    customer_id,
    customer_name,
    city,
    state,
    customer_segment,
    signup_date

FROM {{ ref('stg_customers') }}

{% endsnapshot %}
