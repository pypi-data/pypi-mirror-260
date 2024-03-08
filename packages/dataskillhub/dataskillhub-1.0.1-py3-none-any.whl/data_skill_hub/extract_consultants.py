from pydantic import BaseModel
from typing import List
import yaml


class Section(BaseModel):
    titre: str = "Mon titre"
    file: str = "fichier.md"


class Poste(BaseModel):
    poste: str
    structure: str = "standard"
    sections: List[Section]


"""
    @validator('structure')
    def sections(self, sections, standard):
        if sections == []:
            if structure=="standard":
                return [
                    Section("Valeur ajoutée sur votre mission","valeur.md"),
                    Section("Compétences clés","competence.md"),
                    Section("Diplômes et certifications","diplome.md"),
                    Section("Langues parlées","langague.md"),
                    Section("Formations suivies","formation.md"),
                    Section("Expériences significatives","experience_s.md"),
                    Section("Expériences de formateur","experience_f.md")
                ]
            if structure == "formation":
                return [
                    Section("Compétences clés","competence.md"),
                    Section("Valeur ajoutée sur votre mission","valeur.md")
                ]
"""


class ExportConfig(BaseModel):
    nom_prenom: str
    dossiers: List[Poste]


class DossierCompetencePret(BaseModel):
    name: str
    poste: str
    sections: list[Section]
    # ex:[Section(titre='Compétences', file='valeur_ajoute.md'), Section(titre='Expériences', file='diplome.md')] # noqa:


class DossierCompetence(BaseModel):
    name: str
    poste: str
    sections: list[Section]
    # ex:section=[Section(titre='Compétences', file='# valeur_ajoute'), Section(titre='Expériences', file='#diplome')] # noqa:


"""
class StandardPoste(Poste):
    nom_poste: str
    sections = [
        Section("Valeur ajoutée sur votre mission","valeur.md"),
        Section("Compétences clés","competence.md"),
        Section("Diplômes et certifications","diplome.md"),
        Section("Langues parlées","langague.md"),
        Section("Formations suivies","formation.md"),
        Section("Expériences significatives","experience_s.md"),
        Section("Expériences de formateur","experience_f.md")
    ]
class FormateurPoste(Poste):
    nom_poste: str
    sections = [
        Section("Valeur ajoutée sur votre mission","valeur.md"),
        Section("Compétences clés","competence.md"),
        Section("Diplômes et certifications","diplome.md"),
        Section("Langues parlées","langague.md"),
        Section("Formations suivies","formation.md"),
        Section("Expériences de formateur","experience_f.md"),
        Section("Expériences significatives","experience_s.md")
    ]
class CustomPoste(Poste):
    nom_poste: str
    sections: List[Section]
"""


def get_source_content(source: str) -> str:
    """read le fichier selon la source"""
    with open(source, "r") as content:
        content_str = content.read()
    return content_str


def read_yaml(file_path: str) -> ExportConfig:
    """Lire le le fichier yaml"""
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)
    return ExportConfig(**config)


def flat_export(config: ExportConfig) -> list:
    """exporter en list[DC]"""
    name = config.nom_prenom
    dc_liste = []
    for dossier in config.dossiers:
        dc_liste.append(
            DossierCompetencePret(
                name=name, poste=dossier.poste, sections=dossier.sections
            )
        )
    return dc_liste


def extract_contenue(
    consultant_path: str, dcp: DossierCompetencePret
) -> DossierCompetence:
    """extract le contenue md"""
    name = dcp.name
    poste = dcp.poste
    liste_Section = []
    for section in dcp.sections:
        md = get_source_content(consultant_path + "/" + section.file)
        liste_Section.append(Section(titre=section.titre, file=md))
    return DossierCompetence(name=name, poste=poste, sections=liste_Section)


def get_dc_contenue(
    consultant_path: str, liste_dcp: list[DossierCompetencePret]
) -> list[DossierCompetence]:
    liste_dc = []
    for dcp in liste_dcp:
        liste_dc.append(extract_contenue(consultant_path, dcp))
    return liste_dc


def get_cvs(consultant: str, consultants_path: str) -> list:
    consultant_path = f"{consultants_path}/{consultant}"
    config = read_yaml(f"{consultant_path}/export.yaml")
    liste_dcp = flat_export(config)
    dc_liste = get_dc_contenue(consultant_path, liste_dcp)
    return dc_liste
