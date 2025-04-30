USE [MiniO_server];
    
    

    

    
    USE [MiniO_server];
    EXEC('
        create view "dbo"."high_value_customers__dbt_tmp" as with base as (
    select * from "MiniO_server"."dbo"."trip_enriched"
),
agg as (
    select 
        passenger_count as client_id,
        count(*) as nb_trajets,
        sum(total_amount) as total_depense,
        avg(tip_percentage) as avg_tip
    from base
    group by passenger_count
),
filtre as (
    select *
    from agg
    where nb_trajets > 10
      and total_depense > 300
      and avg_tip > 15
)

select * from filtre;
    ')

