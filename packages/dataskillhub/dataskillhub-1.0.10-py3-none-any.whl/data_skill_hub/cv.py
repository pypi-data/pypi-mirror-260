from weasyprint import HTML, CSS
import json
from .extract_consultants import DossierCompetence
from jinja2 import Template
import markdown


def get_content(source: str) -> str:
    """read le fichier selon la source"""
    with open(source, "r") as content:
        content_str = content.read()
    return content_str


class CV:
    """class pour manipuler un contenu du cv

    :example :
    >>> cv = CV("name='Bob Pipo'
                 poste='Data Scientist'
                sections=[
                    Section(titre='Compétences1', file='### A '),
                    Section(titre='Diplôme1', file='### Diplômes')
                ]")

    """

    def __init__(
        self,
        dossier_competence: DossierCompetence,
        template_path="src/templates/temp_cv.html",
        fileAnomyme="src/config/anonyme.json",
        logo_tete="src/assets/Datalyo_logo_rvb.png",
        logo_pied="src/assets/logo_pied.png",
    ) -> None:
        """initialise le contenu du cv"""
        html_template = template_path
        html_content = get_content(html_template)
        self.dossier_competence = dossier_competence
        self.template = Template(html_content)
        self.fileAnomyme = fileAnomyme
        self.logo_tete_html = "../../../" + logo_tete
        self.logo_pied_html = "../../../" + logo_pied
        self.logo_tete_pdf = logo_tete
        self.logo_pied_pdf = logo_pied

    def to_html_content(self, css_lien, for_pdf: bool):
        """transformer le format md en html"""
        if for_pdf:
            logo_tete = self.logo_tete_pdf
            logo_pied = self.logo_pied_pdf
        else:
            logo_tete = self.logo_tete_html
            logo_pied = self.logo_pied_html
        css_lien = "../../../" + css_lien
        for section in self.dossier_competence.sections:
            section.file = markdown.markdown(section.file)
        html = self.template.render(
            name=self.dossier_competence.name,
            poste=self.dossier_competence.poste,
            sections=self.dossier_competence.sections,
            LIEN_CSS=css_lien,
            LOGO_TETE=logo_tete,
            LOGO_PIED=logo_pied,
        )
        return html

    def anonimize(self, cv: str) -> str:
        """anonimiser le contenu du cv"""
        with open(self.fileAnomyme, "r") as anonimizeFile:
            dictAnonimizd = json.loads(anonimizeFile.read())
        for key in dictAnonimizd:
            cv = cv.replace(key, dictAnonimizd[key])
        return cv

    def to_html_file(self, output_html_file, css_lien, anonimize: bool):
        """transformer le format md en html et sorti la fichier.html"""
        html_content = self.to_html_content(css_lien, for_pdf=False)
        if anonimize:
            html_content = self.anonimize(html_content)
        output_html_file = output_html_file + ".html"
        with open(output_html_file, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

    def to_pdf_file(self, output_pdf_file, css_lien, anonimize: bool):
        """transformer le format html en pdf et sorti la fichier.pdf"""
        html_content = self.to_html_content(css_lien, for_pdf=True)
        if anonimize:
            html_content = self.anonimize(html_content)
        html = HTML(string=html_content, base_url="")
        output_pdf_file = output_pdf_file + ".pdf"
        with open(css_lien, "rb") as f:
            css = f.read()
        html.write_pdf(
            output_pdf_file,
            stylesheets=[CSS(string=css)],
            presentational_hints=True,
        )
