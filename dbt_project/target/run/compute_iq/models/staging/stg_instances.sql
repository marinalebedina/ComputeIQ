
  create view "computeiq"."analytics"."stg_instances__dbt_tmp"
    
    
  as (
    SELECT
    instance_id,
    instance_type,
    cpu_count,
    gpu_count,
    hourly_cost
FROM "computeiq"."raw"."instances"
  );