from .cv import CV
from .export_config import get_cvs
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convertir le fichier Markdown en fichier HTML ou PDF."
    )
    parser.add_argument(
        "-i",
        "--inputYAML",
        type=str,
        help="Entrer le répertoire du fichier.yaml",  # noqa:
    )
    parser.add_argument(
        "-style",
        "--liencss",
        type=str,
        help="Entrer le répertoire du fichier.css",  # noqa:
    )
    parser.add_argument(
        "-a",
        "--anonimize",
        action="store_true",
        help="sortir le fichier anonyme",
        default=False,
    )
    parser.add_argument(
        "-html",
        "--toHtml",
        action="store_true",
        help="sortir le fichier html",
        default=False,
    )
    parser.add_argument(
        "-pdf",
        "--toPdf",
        action="store_true",
        help="sortir le fichier pdf",
        default=False,
    )
    parser.add_argument(
        "-all",
        "--toAll",
        action="store_true",
        help="sortir tous les fichiers",
        default=False,
    )
    args = parser.parse_args()
    return args


def creer_dossier(nom_dossier: str):
    if not os.path.exists(nom_dossier):
        os.makedirs(nom_dossier)


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


def get_trigrammer(input_yaml: str) -> str:
    """Récupérez la partie à trigrammer du input

    :example :
    >>> get_trigrammer("yao.xin/export.yaml")
    yao.xin
    """
    try:
        a_trigrammer = input_yaml.split("/")[-2]
    except IndexError:
        raise TrigrammerError(
            "wrong format, need to use firstname.name/metier.md"
        )  # noqa:
    return a_trigrammer


def get_output_name(input_yaml: str, nom_metier: str, anonimized: bool):
    trigramme = trigrammer(get_trigrammer(input_yaml))
    creer_dossier(trigramme)
    if anonimized is True:
        output_name = trigramme + "/" + nom_metier + "_a"
    else:
        output_name = trigramme + "/" + nom_metier
    return output_name


def main():
    args = parse_args()
    cvs = get_cvs(args.inputYAML, args.liencss)
    for cv_contenu in cvs:
        metier = cv_contenu[0]
        cv = CV(cv_contenu[1])
        cv_anonimized = CV(cv_contenu[1]).anonimize()
        if args.toAll:
            cv_anonimized.to_html_file(
                get_output_name(args.inputYAML, metier, anonimized=True),
                args.liencss,  # noqa:
            )
            cv_anonimized.to_pdf_file(
                get_output_name(args.inputYAML, metier, anonimized=True),
                args.liencss,  # noqa:
            )
            cv.to_html_file(
                get_output_name(args.inputYAML, metier, anonimized=False),
                args.liencss,  # noqa:
            )  # noqa:
            cv.to_pdf_file(
                get_output_name(args.inputYAML, metier, anonimized=False),
                args.liencss,  # noqa:
            )  # noqa:
        if args.anonimize:
            if args.toHtml:
                cv_anonimized.to_html_file(
                    get_output_name(args.inputYAML, metier, anonimized=True),
                    args.liencss,
                )
            if args.toPdf:
                cv_anonimized.to_pdf_file(
                    get_output_name(args.inputYAML, metier, anonimized=True),
                    args.liencss,
                )
        else:
            if args.toHtml:
                cv.to_html_file(
                    get_output_name(args.inputYAML, metier, anonimized=False),
                    args.liencss,
                )
            if args.toPdf:
                cv.to_pdf_file(
                    get_output_name(args.inputYAML, metier, anonimized=False),
                    args.liencss,
                )


if __name__ == "__main__":
    main()
