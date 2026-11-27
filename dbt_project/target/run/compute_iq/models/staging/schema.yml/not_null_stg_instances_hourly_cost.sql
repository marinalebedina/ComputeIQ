
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select hourly_cost
from "computeiq"."analytics"."stg_instances"
where hourly_cost is null



  
  
      
    ) dbt_internal_test