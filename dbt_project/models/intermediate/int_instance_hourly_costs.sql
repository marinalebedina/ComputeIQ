
{{ config(
    materialized='incremental',
    unique_key=['instance_id', 'timestamp'],
    incremental_strategy='delete+insert'
) }}

SELECT
    m.instance_id,
    m.timestamp,
    i.instance_type,
    i.cpu_count,
    i.gpu_count,
    i.hourly_cost
FROM {{ ref('stg_instance_metrics') }} AS m
LEFT JOIN {{ ref('stg_instances') }} AS i ON m.instance_id = i.instance_id

{% if is_incremental() %}
WHERE m.timestamp >= (
    SELECT COALESCE(MAX(timestamp) - INTERVAL '3 days', '1900-01-01'::timestamptz)
    FROM {{ this }}
                    )
{% endif %}
