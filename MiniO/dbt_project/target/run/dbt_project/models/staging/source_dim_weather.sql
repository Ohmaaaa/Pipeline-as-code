USE [MiniO_server];
    
    

    

    
    USE [MiniO_server];
    EXEC('
        create view "dbo"."source_dim_weather__dbt_tmp" as select * from "MiniO_server"."dbo"."dim_weather";
    ')

