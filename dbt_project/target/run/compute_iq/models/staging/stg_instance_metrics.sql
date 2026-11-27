
  create view "computeiq"."analytics"."stg_instance_metrics__dbt_tmp"
    
    
  as (
    SELECT
    instance_id,
    timestamp,
    cpu_util,
    gpu_util
FROM "computeiq"."raw"."instance_metrics"
  );