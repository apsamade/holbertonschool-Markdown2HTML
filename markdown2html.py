import os
import sys
import markdown

if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

fichier_markdown = sys.argv[1]
fichier_sortie = sys.argv[2]

if not os.path.exists(fichier_markdown):
    print(f"Missing {fichier_markdown}", file=sys.stderr)
    sys.exit(1)

try:
    with open(fichier_markdown, 'r', encoding='utf-8', errors='ignore') as f:
        contenu_markdown = f.read()
except UnicodeDecodeError as e:
    print(f"Erreur de décodage dans {fichier_markdown}: {e}", file=sys.stderr)
    sys.exit(1)

contenu_html = markdown.markdown(contenu_markdown)

with open(fichier_sortie, 'w', encoding='utf-8') as f:
    f.write(contenu_html)

sys.exit(0)
