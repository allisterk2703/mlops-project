import os
import shutil
import requests
import re
from datetime import datetime


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

    if source.startswith("http"):
        try:
            response = requests.get(source, stream=True)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Dataset téléchargé et enregistré sous : {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de téléchargement : {e}")

    else:
        if not os.path.exists(source):
            print(f"❌ Erreur : Le fichier '{source}' n'existe pas.")
            return
        shutil.copy(source, file_path)
        print(f"✅ Dataset copié sous : {file_path}")


def list_dataset_versions(name) -> list[str]:
    directory = f"datas/{name}"
    print(sorted(os.listdir(directory)))


def list_datasets_ids() -> list[str]:
    return os.listdir("datas")
