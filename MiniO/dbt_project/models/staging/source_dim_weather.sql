select * from {{ source('dbo', 'dim_weather') }}
