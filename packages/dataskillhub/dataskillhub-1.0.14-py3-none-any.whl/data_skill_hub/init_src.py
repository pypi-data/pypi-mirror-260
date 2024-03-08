import shutil
from pathlib import Path


def creer_dossier(nom_dossier: str):
    folder_path = Path(nom_dossier)
    folder_path.mkdir(parents=True, exist_ok=True)


def copy_file(source_dossier, cible_dossier, file_name):
    path = Path(__file__).parent
    path_copier = path.parent / source_dossier / file_name
    path_coller = cible_dossier + "/" + file_name
    shutil.copyfile(path_copier, path_coller)
