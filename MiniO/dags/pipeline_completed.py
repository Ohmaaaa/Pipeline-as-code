from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))


default_args = {
    'start_date': datetime(2025, 4, 30),
    'retries': 1,
}

# === Appels avec les bons noms de scripts ===

def run_openweather():
    import openweather as ow
    ow.main()

def run_taxi():
    import taxi as tx
    tx.main()

def run_transformation():
    import transformation_taxi_meteo as tf
    tf.main()

def run_dbt():
    import dbt_run as dbt
    dbt.main()


# === DAG principal ===

with DAG(
    dag_id='pipeline_full',
    schedule_interval="0 2 * * *",  # Tous les jours à 2h du matin
    default_args=default_args,
    catchup=False,
    tags=['etl', 'dbt'],
) as dag:

    extract_weather = PythonOperator(
        task_id='extract_weather',
        python_callable=run_openweather,
    )

    extract_taxi = PythonOperator(
        task_id='extract_taxi',
        python_callable=run_taxi,
    )

    transform_and_load = PythonOperator(
        task_id='transform_and_load',
        python_callable=run_transformation,
    )

    dbt_run = PythonOperator(
        task_id='dbt_run',
        python_callable=run_dbt,
    )

    [extract_weather, extract_taxi] >> transform_and_load >> dbt_run
