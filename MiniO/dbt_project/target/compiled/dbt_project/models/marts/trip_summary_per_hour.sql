with base as (
    select * from "MiniO_server"."dbo"."trip_enriched"
),
agg as (
    select 
        datepart(hour, tpep_pickup_datetime) as pickup_hour,
        weather_category,
        count(*) as nb_trajets,
        avg(trip_duration_minutes) as duree_moyenne,
        avg(tip_percentage) as pourboire_moyen
    from base
    group by datepart(hour, tpep_pickup_datetime), weather_category
)

select * from agg