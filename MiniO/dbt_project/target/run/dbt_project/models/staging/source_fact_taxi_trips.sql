USE [MiniO_server];
    
    

    

    
    USE [MiniO_server];
    EXEC('
        create view "dbo"."source_fact_taxi_trips__dbt_tmp" as select * from "MiniO_server"."dbo"."fact_taxi_trips";
    ')

