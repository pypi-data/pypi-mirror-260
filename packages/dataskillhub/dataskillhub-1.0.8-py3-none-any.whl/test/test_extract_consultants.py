from data_skill_hub.extract_consultants import (
    ExportConfig,
    Poste,
    Section,
    DossierCompetencePret,
    flat_export,
)


# part test


def test_flat_export():
    config = ExportConfig(
        nom_prenom="Bob pipo",
        dossiers=[
            Poste(
                poste="Data Scientist",
                sections=[
                    Section(titre="Compétences1", file="competence.md"),
                    Section(titre="Diplôme1", file="diplome.md"),
                ],
            ),
            Poste(
                poste="Data Engineer",
                sections=[
                    Section(titre="Expérience2", file="experience.md"),
                    Section(titre="Langue2", file="langue.md"),
                ],
            ),
        ],
    )
    liste_dcp = [
        DossierCompetencePret(
            name="Bob pipo",
            poste="Data Scientist",
            sections=[
                Section(titre="Compétences1", file="competence.md"),
                Section(titre="Diplôme1", file="diplome.md"),
            ],
        ),
        DossierCompetencePret(
            name="Bob pipo",
            poste="Data Engineer",
            sections=[
                Section(titre="Expérience2", file="experience.md"),
                Section(titre="Langue2", file="langue.md"),
            ],
        ),
    ]
    assert flat_export(config) == liste_dcp
