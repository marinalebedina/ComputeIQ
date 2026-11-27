
SELECT
    instance_id,
    timestamp,
    cpu_util,
    gpu_util
FROM {{ source('raw','instance_metrics')}}