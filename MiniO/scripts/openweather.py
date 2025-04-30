import requests
import boto3
import json
import time
import os

from datetime import datetime, timezone
from botocore.exceptions import ClientError
from botocore.client import Config

API_KEY = "9d1816e1bb6115e8059fe87779b95446"
CITY = "New York"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
MINIO_BUCKET = "meteo"
MINIO_PREFIX = "weather/"

s3 = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:9000/',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    config=Config(signature_version='s3v4')
)

def ensure_bucket_exists(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Le bucket '{bucket_name}' existe déjà.")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Le bucket '{bucket_name}' n'existe pas, création en cours...")
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' créé avec succès.")
        else:
            raise

def fetch_weather():
    print("Récupération météo...")
    response = requests.get(URL)
    return response.json()

def save_and_upload(all_data, filename):
    with open(filename, 'w') as f:
        json.dump(all_data, f, indent=2)
    s3.upload_file(filename, MINIO_BUCKET, MINIO_PREFIX + filename)
    print(f"Upload de {filename} terminé.")

def main():
    ensure_bucket_exists(MINIO_BUCKET)

    all_weather_data = []
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    filename = f"weather_{today}.json"

    while True:
        data = fetch_weather()
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        data_with_timestamp = {
            "timestamp": timestamp,
            "data": data
        }
        all_weather_data.append(data_with_timestamp)

        save_and_upload(all_weather_data, filename)

        print(f"Mesure ajoutée à {filename}. Total : {len(all_weather_data)} enregistrements.")

        time.sleep(60)  # Modifier à 3600 pour une exécution toutes les heures

if __name__ == "__main__":
    main()
