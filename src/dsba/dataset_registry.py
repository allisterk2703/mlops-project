import os
import logging
import shutil
import requests
import re
import zipfile
from datetime import datetime
import boto3
from dotenv import load_dotenv

load_dotenv(override=True)
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def get_next_version(directory, name):
    existing_files = [f for f in os.listdir(
        directory) if re.search(rf"{name}_v(\d+)_", f)]
    if existing_files:
        last_version = sorted(existing_files)[-1]
        match = re.search(r"_v(\d+)_", last_version)
        return int(match.group(1)) + 1 if match else 1
    return 1


def save_dataset(name: str, source: str, new: bool, upload_on_s3: bool = False) -> None:
    dt = datetime.now().strftime("%Y-%m-%d_%H-%M")
    directory = f"datas/{name}"

    os.makedirs(directory, exist_ok=True)

    version = 1 if new else get_next_version(directory, name)
    zip_name = f"{name}_v{version}_{dt}.zip"
    filename = f"{name}_v{version}_{dt}.csv"
    file_path = os.path.join(directory, filename)
    zip_file_path = os.path.join(directory, zip_name)

    # Connection à S3
    if upload_on_s3:
        try:
            s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)
            response = s3.list_buckets() # Test de la connexion
            logging.info("✅ Connection to S3 successful")
        except Exception as e:
            logging.warning(f"⚠️  Connection error to S3: {e}")

    # Récupération des données depuis l'URL fourni
    if source.startswith("http"):
        try:
            response = requests.get(source, stream=True)
            response.raise_for_status()
            with open(zip_file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logging.info(f"✅ ZIP file downloaded and saved as: {zip_file_path}")
        except Exception as e:
            logging.error(f"❌ Download error from {source}: {e}")

        try:
            temporary_directory = "datas/temp"
            os.makedirs(temporary_directory, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(temporary_directory)
        except Exception as e:
            logging.error(f"❌ Error extracting ZIP file: {e}")

        try:
            os.rename(f"{temporary_directory}/{zip_ref.namelist()[0]}", file_path)
            logging.info(f"✅ Dataset extracted to: {file_path}")
        except Exception as e:
            logging.error(f"❌ Error extracting dataset: {e}")

        try:     
            os.rmdir(temporary_directory)  
            os.remove(zip_file_path)
            logging.info(f"✅ Temporary files removed")
        except Exception as e:
            logging.error(f"❌ Error removing temporary files: {e}")

    else: # Récupération des données depuis le chemin fourni
        try:
            shutil.copy(source, file_path)
            logging.info(f"✅ Dataset copied to: {file_path}")
        except Exception as e:
            logging.error(f"❌ The file '{source}' does not exist.")
        
        # Upload du dataset vers S3 si demandé
    if upload_on_s3:
        try:
            s3.upload_file(f"{directory}/{filename}",
                        S3_BUCKET_NAME, f"{name}/{filename}")
            logging.info(f"✅ File uploaded to S3: s3://{S3_BUCKET_NAME}/{name}/{filename}")
        except Exception as e:
            logging.warning("⚠️  Error importing dataset to S3...")


def list_dataset_versions(name: str) -> None:
    try:
        directory = f"datas/{name}"
        files = sorted(os.listdir(directory))
        print(f"Available versions for dataset '{name}':")
        for file in files:
            print(f"-", file)
    except Exception as e:
        logging.error(f"❌ Error listing dataset versions: {e}")


def list_datasets_ids() -> list[str]:
    return os.listdir("datas")
