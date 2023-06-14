{{ config(
    materialized='incremental'
    ) }}
-- << import CTE >>
with source_fact as
    (select
        *
    from {{ ref('stage_f_taxi_rides_v') }} as t    
    {% if is_incremental() %}
    -- << this filter will only be applied on an incremental run >>
    where 
        tm_pep_pickup_datetime > (select max(tm_pep_pickup_datetime) from {{ this }})
    {% endif %}),
-- final fact select
final as
    (select
        t.id_vendor,
        t.id_rate_code,
        t.id_pu_location,
        t.id_do_location,
        t.id_payment_type,
        t.ind_store_and_fwd_flag,
        t.msr_fare_amount,
        t.msr_extra,
        t.msr_mta_tax,
        t.msr_tip_amount,
        t.msr_tolls_amount,
        t.msr_improvement_surcharge,
        t.msr_total_amount,
        t.msr_congestion_surcharge,
        t.msr_airport_fee,
        t.msr_passenger_count,
        t.msr_trip_distance,
        t.dt_tpep_pickup,
        t.dt_pep_dropoff_datetime,
        t.tm_pep_pickup_datetime,
        t.tm_pep_dropoff_datetime,
        t.fk_audit
    from source_fact t)
select * from final