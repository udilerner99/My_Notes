-- << import CTE >>
with raw_source as
    (select
        *
    from {{ ref ('raw_stage_taxi_v') }} as t),
-- << logical CTE >>
transform as
    (select
        *
    from raw_source t),
-- << final CTE >>
final as
    (select
        *
    from transform)
select * from final