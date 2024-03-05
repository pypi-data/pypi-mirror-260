from pydantic import BaseModel
from typing import List
import yaml
import markdown
from jinja2 import Template
import os


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
    source: str, dcp: DossierCompetencePret
) -> DossierCompetence:  # noqa:
    """extract le contenue (md->str->html_contenu)"""
    name = dcp.name
    poste = dcp.poste
    liste_Section = []
    chemin_relatif = os.path.dirname(source)
    for section in dcp.sections:
        md = get_source_content(chemin_relatif + "/" + section.file)
        md_contenue = markdown.markdown(md)
        liste_Section.append(Section(titre=section.titre, file=md_contenue))
    return DossierCompetence(name=name, poste=poste, sections=liste_Section)


def get_dc_contenue(
    source: str, liste_dcp: list[DossierCompetencePret]
) -> list[DossierCompetence]:
    liste_dc = []
    for dcp in liste_dcp:
        liste_dc.append(extract_contenue(source, dcp))
    return liste_dc


def get_cvs(source_yaml: str, source_css: str) -> list:
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(
        os.path.dirname(current_path) + os.path.sep + ".."
    )  # noqa:
    html_template = os.path.join(
        father_path, "dossier_competence/temp_cv.html"
    )  # noqa:
    html_content = get_source_content(html_template)
    template = Template(html_content)
    config = read_yaml(source_yaml)
    liste_dcp = flat_export(config)
    dc_liste = get_dc_contenue(source_yaml, liste_dcp)
    cvs = {}
    for dc in dc_liste:
        a = template.render(
            name=dc.name,
            poste=dc.poste,
            sections=dc.sections,
            LIEN_CSS="LIEN_CSS",
            LOGO_TETE="LOGO_TETE",
            LOGO_PIED="LOGO_PIED",
        )
        cvs[dc.poste] = a
    return list(cvs.items())
