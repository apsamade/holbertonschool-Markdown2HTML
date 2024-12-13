#!/usr/bin/env python3
import os
import sys
import re

# Vérifier si le nombre d'arguments est inférieur à 2
if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

# Récupérer les fichiers d'entrée et de sortie
fichier_markdown = sys.argv[1]
fichier_sortie = sys.argv[2]

# Vérifier si le fichier markdown existe
if not os.path.exists(fichier_markdown):
    print(f"Missing {fichier_markdown}", file=sys.stderr)
    sys.exit(1)

# Lire le contenu du fichier markdown avec l'encodage UTF-8
try:
    with open(fichier_markdown, 'r', encoding='utf-8') as f:
        contenu_markdown = f.read()
except UnicodeDecodeError:
    # Si l'UTF-8 échoue, essayer avec ISO-8859-1
    try:
        with open(fichier_markdown, 'r', encoding='ISO-8859-1') as f:
            contenu_markdown = f.read()
    except UnicodeDecodeError as e:
        print(f"Erreur de décodage dans {fichier_markdown}: {e}", file=sys.stderr)
        sys.exit(1)

# Fonction pour convertir les titres Markdown en HTML
def convertir_titres(contenu):
    contenu = re.sub(r"###### (.*)", r"<h6>\1</h6>", contenu)
    contenu = re.sub(r"##### (.*)", r"<h5>\1</h5>", contenu)
    contenu = re.sub(r"#### (.*)", r"<h4>\1</h4>", contenu)
    contenu = re.sub(r"### (.*)", r"<h3>\1</h3>", contenu)
    contenu = re.sub(r"## (.*)", r"<h2>\1</h2>", contenu)
    contenu = re.sub(r"# (.*)", r"<h1>\1</h1>", contenu)
    return contenu

# Fonction pour convertir les listes non ordonnées
def convertir_listes_non_ordonnees(contenu):
    contenu = re.sub(r"^\s*- (.*)$", r"<ul>\n<li>\1</li>\n</ul>", contenu, flags=re.MULTILINE)
    return contenu

# Fonction pour convertir les listes ordonnées
def convertir_listes_ordonnees(contenu):
    contenu = re.sub(r"^\s*\* (.*)$", r"<ol>\n<li>\1</li>\n</ol>", contenu, flags=re.MULTILINE)
    return contenu

# Fonction pour convertir les paragraphes
def convertir_paragraphes(contenu):
    contenu = re.sub(r"([^#\*\-_]+)(?=\n|$)", r"<p>\1</p>", contenu)
    return contenu

# Fonction pour convertir le texte en gras et en italique
def convertir_gras_italique(contenu):
    contenu = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", contenu)
    contenu = re.sub(r"__(.*?)__", r"<em>\1</em>", contenu)
    return contenu

# Appliquer toutes les conversions sur le contenu Markdown
contenu_html = contenu_markdown
contenu_html = convertir_titres(contenu_html)
contenu_html = convertir_listes_non_ordonnees(contenu_html)
contenu_html = convertir_listes_ordonnees(contenu_html)
contenu_html = convertir_paragraphes(contenu_html)
contenu_html = convertir_gras_italique(contenu_html)

# Écrire le résultat dans le fichier HTML de sortie avec l'encodage UTF-8
with open(fichier_sortie, 'w', encoding='utf-8') as f:
    f.write(contenu_html)

# Si tout va bien, rien n'est affiché et le script termine avec un code de sortie 0
sys.exit(0)
