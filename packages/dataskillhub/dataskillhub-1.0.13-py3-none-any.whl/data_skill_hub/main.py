import click
from .extract_consultants import get_cvs
from .export import write_exports
from .init_src import creer_dossier, copy_file

BASE_PATH = "sources_exemple"
DESTINATION_PATH = "src"
OUTPUT_PATH = "src/outputs"


@click.group()
def main():
    pass


@main.command()
def init():
    list_dossier = ["assets", "templates", "config", "consultants"]
    for dossier in list_dossier:
        creer_dossier(f"{DESTINATION_PATH}/{dossier}/")
    print("dossier créé")
    copy_file(f"{BASE_PATH}/assets", f"{DESTINATION_PATH}/assets", "logo_pied.png")  # noqa:
    copy_file(f"{BASE_PATH}/assets", f"{DESTINATION_PATH}/assets", "Datalyo_logo_rvb.png") # noqa:
    copy_file(f"{BASE_PATH}/assets", f"{DESTINATION_PATH}/assets", "test.css")
    copy_file(f"{BASE_PATH}/templates", f"{DESTINATION_PATH}/templates", "temp_cv.html")  # noqa:
    copy_file(f"{BASE_PATH}/config", f"{DESTINATION_PATH}/config", "anonyme.json")  # noqa:
    print("fichiers prêt")


@main.group()
def consultant():
    pass


@consultant.command()
@click.argument("consultant")
def export(consultant):
    consultants_path = f"{DESTINATION_PATH}/consultants/"
    cvs = get_cvs(consultant, consultants_path)
    write_exports(cvs, OUTPUT_PATH, consultant)

@consultant.command()
def list():
    print("ok list")


@consultant.command()
@click.argument("consultant")
def new(consultant):
    print(f"new {consultant}")


@consultant.command()
@click.argument("consultant")
def check(consultant):
    print(f"check {consultant}")


if __name__ == "__main__":
    main()
