from jinja2 import Template
import markdown
from weasyprint import HTML, CSS
import yaml


def get_source_content(srouce: str) -> str:
    """read le fichier selon la source"""
    with open(srouce, "r") as content:
        content_str = content.read()
    return content_str


def get_yaml_content(source_yaml: str) -> dict:
    """read yaml et transformer en dictionnary"""
    content_str = get_source_content(source_yaml)
    content_dict = yaml.load(content_str, Loader=yaml.FullLoader)
    return content_dict


def get_name(source_yaml: str) -> str:
    """Obtenir le nom sur le fichier yaml"""
    content_dict = get_yaml_content(source_yaml)
    name = content_dict.get("nom_prenom")
    return name


def get_poste_liste(source_yaml: str) -> str:
    """Obtenir les postes sur le fichier yaml, mettre le format list"""
    content_dict = get_yaml_content(source_yaml)
    dossier_liste = content_dict.get("dossiers")
    poste_liste = []
    for d in dossier_liste:
        poste_liste.append(d.get("poste"))
    return poste_liste


def get_structure(source_yaml: str) -> str:
    content_dict = get_yaml_content(source_yaml)
    dossier_liste = content_dict.get("dossiers")
    for d in dossier_liste:
        print(d.get("structure"))


def get_section_liste_dic(source_yaml: str) -> list:
    content_dict = get_yaml_content(source_yaml)
    dossier_liste = content_dict.get("dossiers")
    section_liste_dic = []
    for d in dossier_liste:
        section_liste_dic.append(d.get("sections"))
    return section_liste_dic


def get_section_liste_liste(source_yaml: str) -> list:
    section_liste_dic = get_section_liste_dic(source_yaml)
    section_liste_liste = []
    l_temporaire = []
    for s in section_liste_dic:
        for i in range(0, len(s)):
            s[i]["file"] = get_source_content(s[i].get("file"))
            l_temporaire.append(list(s[i].values()))
        section_liste_liste.append(l_temporaire)
        l_temporaire = []
    return section_liste_liste


class DossierCompetence:
    def __init__(self, name: str, poste: str, section: list) -> None:
        """initialise le model du DossierCompetence"""
        self.name = name
        self.poste = poste
        self.section = section


def get_dc_liste(source_yaml: str):
    name = get_name(source_yaml)
    poste_liste = get_poste_liste(source_yaml)
    section_liste = get_section_liste_liste(source_yaml)
    dc_liste = []
    for i in range(0, len(poste_liste)):
        p = poste_liste[i]
        s = section_liste[i]
        dc_liste.append(DossierCompetence(name, p, s))
    return dc_liste


def make_html_content(source_html: str, source_yaml: str):
    html_content = get_source_content(source_html)
    template = Template(html_content)
    dc_liste = get_dc_liste(source_yaml)
    LIEN_CSS = "../file_static/test.css"
    LOGO_TETE = "../file_static/Datalyo_logo_rvb.png"
    LOGO_PIED = "../file_static/pied.png"
    css = get_source_content("../file_static/test.css")
    for dc in dc_liste:
        output_pdf_file = dc.name + dc.poste + ".pdf"
        outtput_html_file = dc.name + dc.poste + ".html"
        for s in dc.section:
            x = markdown.markdown(s[1])
            s[1] = x
        a = template.render(
            name=dc.name,
            poste=dc.poste,
            sections=dc.section,
            LIEN_CSS=LIEN_CSS,
            LOGO_TETE=LOGO_TETE,
            LOGO_PIED=LOGO_PIED,
        )
        with open(outtput_html_file, "w", encoding="utf-8") as html_file:
            html_file.write(a)
        HTML(string=a).write_pdf(
            output_pdf_file,
            stylesheets=[CSS(string=css)],
            presentational_hints=True,  # noqa:
        )


if __name__ == "__main__":
    # get_section_liste_liste("../exemple/plop.pipo/ppl_export.yaml")
    make_html_content(
        "../templates/temp_cv.html", "../exemple/plop.pipo/ppl_export.yaml"
    )
