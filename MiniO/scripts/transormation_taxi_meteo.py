from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, when, unix_timestamp, hour, date_format, from_unixtime

def init_spark():
    return SparkSession.builder \
        .appName("TaxiMeteoTransformation") \
        .config("spark.driver.host", "127.0.0.1") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.jars", ",".join([
            "C:/Users/naell/OneDrive - univ-lyon2.fr/Documents/Epsi/MiniO/jar/hadoop-aws-3.3.2.jar",
            "C:/Users/naell/OneDrive - univ-lyon2.fr/Documents/Epsi/MiniO/jar/aws-java-sdk-bundle-1.11.1026.jar",
            "C:/Users/naell/OneDrive - univ-lyon2.fr/Documents/Epsi/MiniO/jar/mssql-jdbc-12.8.1.jre8.jar"
        ])) \
        .getOrCreate()

def process_taxi_data(spark):
    df = spark.read.parquet("s3a://taxi/taxi/yellow_tripdata_2025-01.parquet")
    return df.withColumn(
        "trip_duration_minutes",
        (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 60
    ).withColumn(
        "distance_range",
        when(col("trip_distance") <= 2, "0-2 km")
        .when((col("trip_distance") > 2) & (col("trip_distance") <= 5), "2-5 km")
        .otherwise(">5 km")
    ).withColumn(
        "tip_percentage",
        when(col("fare_amount") > 0, (col("tip_amount") / col("fare_amount")) * 100).otherwise(0)
    ).withColumn(
        "pickup_hour", hour(col("tpep_pickup_datetime"))
    ).withColumn(
        "pickup_weekday", date_format(col("tpep_pickup_datetime"), "EEEE")
    )

def process_weather_data(spark):
    df_raw = spark.read.option("multiline", "true").json("s3a://meteo/weather/")
    df = df_raw.select(
        from_unixtime(col("data.dt")).cast("timestamp").alias("timestamp"),
        col("data.coord.lat").alias("latitude"),
        col("data.coord.lon").alias("longitude"),
        col("data.main.temp").alias("temperature"),
        col("data.main.feels_like").alias("ressenti"),
        col("data.main.humidity").alias("humidite"),
        col("data.wind.speed").alias("vent_vitesse"),
        col("data.weather")[0]["main"].alias("condition_meteo"),
        col("data.clouds.all").alias("nuages"),
        col("data.name").alias("ville")
    )
    return df.withColumn(
        "weather_category",
        when(col("condition_meteo") == "Clear", "Clair")
        .when(col("condition_meteo") == "Rain", "Pluvieux")
        .when(col("condition_meteo") == "Storm", "Orageux")
        .otherwise("Autre")
    )

def write_to_sql(df, table_name, jdbc_url, jdbc_props, coalesce=False):
    writer = df.coalesce(1) if coalesce else df
    writer.write \
        .mode("overwrite") \
        .jdbc(
            url=jdbc_url,
            table=table_name,
            properties=jdbc_props
        )

def main():
    spark = init_spark()

    taxi_df = process_taxi_data(spark)
    meteo_df = process_weather_data(spark)

    jdbc_url = "jdbc:sqlserver://localhost;databaseName=MiniO_server;encrypt=false"
    jdbc_properties = {
        "user": "ohma69",
        "password": "ohma69",
        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    }

    write_to_sql(taxi_df, "fact_taxi_trips", jdbc_url, jdbc_properties)
    write_to_sql(meteo_df, "dim_weather", jdbc_url, jdbc_properties, coalesce=True)

    print("✅ Données taxi et météo écrites avec succès !")

if __name__ == "__main__":
    main()



