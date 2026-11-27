
    
    

with child as (
    select instance_id as from_field
    from "computeiq"."analytics"."stg_instance_metrics"
    where instance_id is not null
),

parent as (
    select instance_id as to_field
    from "computeiq"."analytics"."stg_instances"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


