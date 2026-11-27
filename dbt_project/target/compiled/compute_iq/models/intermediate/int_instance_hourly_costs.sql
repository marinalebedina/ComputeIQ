

SELECT
    m.instance_id,
    m.timestamp,
    i.instance_type,
    i.cpu_count,
    i.gpu_count,
    i.hourly_cost
FROM "computeiq"."analytics"."stg_instance_metrics" AS m
LEFT JOIN "computeiq"."analytics"."stg_instances" AS i
    ON m.instance_id = i.instance_id

