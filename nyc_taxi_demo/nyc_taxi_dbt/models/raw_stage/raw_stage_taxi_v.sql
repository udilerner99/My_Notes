-- << import CTE >>
with raw_source as
    (select
        *
    from {{ source ('taxi_src', 'raw_nyc_yellow_taxi_t') }} as t
    {% if target.name == 'dev' %}
    -- sample (40)
    {% endif %}
),
-- << logical CTE >>
transform as
    (select
        t.vendorid as id_vendor,
        t.ratecodeid as id_rate_code,
        t.pulocationid as id_pu_location,
        t.dolocationid as id_do_location,
        nvl(t.payment_type, -1) as id_payment_type,
        nvl(cast(t.store_and_fwd_flag as boolean), false) as ind_store_and_fwd_flag,
        t.fare_amount as msr_fare_amount,
        t.extra as msr_extra,
        t.mta_tax as msr_mta_tax,
        t.tip_amount as msr_tip_amount,
        t.tolls_amount as msr_tolls_amount,
        t.improvement_surcharge as msr_improvement_surcharge,
        t.total_amount as msr_total_amount,
        t.congestion_surcharge as msr_congestion_surcharge,
        t.airport_fee as msr_airport_fee,
        t.passenger_count as msr_passenger_count,
        t.trip_distance as msr_trip_distance,
        cast(nvl(t.tpep_pickup_datetime, '1900-01-01' ) as date) as dt_tpep_pickup,
        cast(nvl(t.tpep_dropoff_datetime, '1900-01-01' ) as date) as dt_pep_dropoff_datetime,
        cast(nvl(t.tpep_pickup_datetime, '1900-01-01 00:00:00' ) as timestamp) as tm_pep_pickup_datetime,
        cast(nvl(t.tpep_dropoff_datetime, '1900-01-01 00:00:00' ) as timestamp) as tm_pep_dropoff_datetime
    from raw_source as t),
-- << final CTE >>
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
        '{{ invocation_id }}' as fk_audit
    from transform t)
select * from final