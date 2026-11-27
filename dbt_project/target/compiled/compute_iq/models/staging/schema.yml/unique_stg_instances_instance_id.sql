
    
    

select
    instance_id as unique_field,
    count(*) as n_records

from "computeiq"."analytics"."stg_instances"
where instance_id is not null
group by instance_id
having count(*) > 1


