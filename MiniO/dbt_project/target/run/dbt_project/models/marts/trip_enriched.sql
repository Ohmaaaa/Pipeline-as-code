USE [MiniO_server];
    
    

    

    
    USE [MiniO_server];
    EXEC('
        create view "dbo"."trip_enriched__dbt_tmp" as with trips as (
    select * from "MiniO_server"."dbo"."fact_taxi_trips"
),
weather as (
    select * from "MiniO_server"."dbo"."dim_weather"
),
trip_enriched as (
    select 
    t.tpep_pickup_datetime,
    t.tpep_dropoff_datetime,
    t.passenger_count,
    t.trip_distance,
    t.total_amount,
    t.tip_amount,
    t.fare_amount,
    t.payment_type,
    datediff(minute, t.tpep_pickup_datetime, t.tpep_dropoff_datetime) as trip_duration_minutes,
    w.weather_category,
    w.temperature,
    w.vent_vitesse,
    t.tip_amount / nullif(t.fare_amount, 0) * 100 as tip_percentage


    from trips t
    left join weather w 
        on cast(t.tpep_pickup_datetime as date) = cast(w.timestamp as date)
        and datepart(hour, t.tpep_pickup_datetime) = datepart(hour, w.timestamp)
)

select * from trip_enriched;
    ')

