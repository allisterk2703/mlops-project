import os
import shutil
import requests
import re
from datetime import datetime
import boto3
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
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


def save_dataset(name, source, new) -> None:
    dt = datetime.now().strftime("%Y-%m-%d_%H-%M")
    directory = f"datas/{name}"

    os.makedirs(directory, exist_ok=True)

    version = 1 if new else get_next_version(directory, name)
    filename = f"{name}_v{version}_{dt}.csv"
    file_path = os.path.join(directory, filename)

    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)
    if source.startswith("http"):
        try:
            response = requests.get(source, stream=True)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Dataset téléchargé et enregistré sous : {file_path}")
            s3.upload_file(f"{directory}/{filename}",
                           S3_BUCKET_NAME, f"{name}/{filename}")
            print(
                f"Fichier uploadé sur S3 : s3://{S3_BUCKET_NAME}/{name}/{filename}")
        except Exception as e:
            print(f"Erreur de téléchargement depuis {source} : {e}")
        except Exception as e:
            print("Erreur d'import du dataset sur S3")
    else:
        if not os.path.exists(source):
            print(f"Erreur : Le fichier '{source}' n'existe pas.")
            return
        shutil.copy(source, file_path)
        print(f"Dataset copié sous : {file_path}")
        try:
            s3.upload_file(f"{directory}/{filename}",
                           S3_BUCKET_NAME, f"{name}/{filename}")
            print(
                f"Fichier uploadé sur S3 : s3://{S3_BUCKET_NAME}/{name}/{filename}")
        except Exception as e:
            print("Erreur d'import du dataset sur S3")


def list_dataset_versions(name) -> list[str]:
    directory = f"datas/{name}"
    print(f"Available versions for dataset '{name}':")
    for file in sorted(os.listdir(directory)):
        print(f"-", file)


def list_datasets_ids() -> list[str]:
    return os.listdir("datas")
