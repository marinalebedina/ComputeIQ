
SELECT
    instance_id,
    instance_type,
    cpu_count,
    gpu_count,
    hourly_cost
FROM {{ source('raw', 'instances') }}
