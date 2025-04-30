import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os

# === CONFIGURATION ===
TLC_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"
LOCAL_FILE = "yellow_tripdata_2025-01.parquet"
MINIO_BUCKET = "taxi"
MINIO_OBJECT = "taxi/yellow_tripdata_2025-01.parquet"

# === MinIO S3 client (sur le port 9001) ===
s3 = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:9000/',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
)

def download_taxi_data():
    print("Téléchargement des données Yellow Taxi...")
    response = requests.get(TLC_URL)
    if response.status_code == 200:
        with open(LOCAL_FILE, 'wb') as f:
            f.write(response.content)
        print(f" Fichier téléchargé localement : {LOCAL_FILE}")
    else:
        print(f"Erreur de téléchargement (code {response.status_code})")

def create_bucket_if_not_exists(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        print(f"ℹ Bucket '{bucket_name}' non trouvé. Création...")
        try:
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' créé avec succès.")
        except Exception as e:
            print(f"Impossible de créer le bucket : {e}")
            raise

def upload_to_minio():
    print("Upload vers MinIO...")
    try:
        create_bucket_if_not_exists(MINIO_BUCKET)
        s3.upload_file(LOCAL_FILE, MINIO_BUCKET, MINIO_OBJECT)
        print(f"Upload réussi dans MinIO : s3://{MINIO_BUCKET}/{MINIO_OBJECT}")
    except NoCredentialsError:
        print("Identifiants MinIO invalides.")
    except Exception as e:
        print("Erreur pendant l'upload :", str(e))

def main():
    download_taxi_data()
    if os.path.exists(LOCAL_FILE):
        upload_to_minio()
    else:
        print("Le fichier n'existe pas, upload annulé.")

if __name__ == "__main__":
    main()