{{ config(
    materialized='incremental'
    ) }}
-- << import CTE >>
with source_fact as
    (select
        *
    from {{ ref('f_taxi_rides_t') }} as t    
    {% if is_incremental() %}
    -- << this filter will only be applied on an incremental run >>
    where 
        dt_tpep_pickup > (select max(dt_tpep_pickup) from {{ this }})
    {% endif %}),
-- final fact select
final as
    (select
        t.dt_tpep_pickup,
        t.id_vendor,
        t.id_rate_code,
        t.id_pu_location,
        t.id_do_location,
        t.id_payment_type,
        t.ind_store_and_fwd_flag,
        t.fk_audit,
        sum(t.msr_fare_amount) as msr_fare_amount_daily,
        sum(t.msr_extra) as msr_extra_daily,
        sum(t.msr_mta_tax) as msr_mta_tax_daily,
        sum(t.msr_tip_amount) as msr_tip_amount_daily,
        sum(t.msr_tolls_amount) as msr_tolls_amount_daily,
        sum(t.msr_improvement_surcharge) as msr_improvement_surcharge_daily,
        sum(t.msr_total_amount) as msr_total_amount_daily,
        sum(t.msr_congestion_surcharge) as msr_congestion_surcharge_daily,
        sum(t.msr_airport_fee) as msr_airport_fee_daily,
        sum(t.msr_passenger_count) as msr_passenger_count_daily,
        sum(t.msr_trip_distance) as msr_trip_distance_daily
    from source_fact t
    group by 1,2,3,4,5,6,7,8)
select * from final