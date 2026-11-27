
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select instance_id
from "computeiq"."analytics"."stg_instance_metrics"
where instance_id is null



  
  
      
    ) dbt_internal_test