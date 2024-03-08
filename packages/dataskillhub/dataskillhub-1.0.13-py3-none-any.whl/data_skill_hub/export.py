from .cv import CV
from pathlib import Path


def creer_dossier(nom_dossier: str):
    folder_path = Path(nom_dossier)
    folder_path.mkdir(parents=True, exist_ok=True)


class TrigrammerError(Exception):
    pass


def trigrammer(nom_prenom: str):
    """Trigrammer le nom et prenom et creer une dossier named trigramme

    :example :
    >>> print(trigrammer("yao.xin"))
    xya
    """
    try:
        nom = nom_prenom.split(".")[0]
        prenom = nom_prenom.split(".")[1]
        t_nom = nom[0] + nom[1]
        t_prenom = prenom[0]
    except IndexError:
        raise TrigrammerError("wrong format, need to use firstname.name")
    trigramme = t_prenom + t_nom
    return trigramme


def get_output_name(consultant: str, nom_metier: str, anonimized: bool):
    trigramme = trigrammer(consultant)
    if anonimized is True:
        output_name = trigramme + "/" + nom_metier + "_a"
    else:
        output_name = trigramme + "/" + nom_metier
    return output_name


def write_exports(dossiercompetences, output_path, consultant):
    trigramme = trigrammer(consultant)
    creer_dossier(f"{output_path}/{trigramme}")
    for dc in dossiercompetences:
        metier = dc.poste
        cv = CV(
            dossier_competence=dc,
            template_path="src/templates/temp_cv.html",
            fileAnomyme="src/config/anonyme.json",
            logo_tete="src/assets/Datalyo_logo_rvb.png",
            logo_pied="src/assets/logo_pied.png",
        )
        output_name = get_output_name(consultant, metier, anonimized=False)
        output_name_anonimized = get_output_name(
            consultant, metier, anonimized=True
        )  # noqa:
        output_p = f"{output_path}/{output_name}"
        output_p_a = f"{output_path}/{output_name_anonimized}"
        cv.to_html_file(
            output_p,
            "src/assets/test.css",
            anonimize=False,
        )
        cv.to_pdf_file(
            output_p,
            "src/assets/test.css",
            anonimize=False,
        )
        cv.to_html_file(
            output_p_a,
            "src/assets/test.css",
            anonimize=True,
        )
        cv.to_pdf_file(
            output_p_a,
            "src/assets/test.css",
            anonimize=True,
        )
