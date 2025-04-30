select * from {{ source('dbo', 'fact_taxi_trips') }}
