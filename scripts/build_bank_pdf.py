#!/usr/bin/env python3
"""
build_bank_pdf.py — Génère un dossier PDF formel pour rendez-vous bancaire.

Utilise WeasyPrint pour convertir un template HTML en PDF de qualité impression.

Usage:
    python3 build_bank_pdf.py --analyse analyse.json --listing listing.json \
        --borrower-info borrower.json --renderings ./renderings/ \
        --output ./dossier-banque.pdf
"""

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS


def format_eur(value, decimals=0):
    if value is None:
        return "—"
    try:
        if decimals == 0:
            return f"{int(round(float(value))):,} €".replace(",", " ")
        return f"{float(value):,.{decimals}f} €".replace(",", " ").replace(".", ",")
    except (ValueError, TypeError):
        return str(value)


def format_pct(value, decimals=1):
    if value is None:
        return "—"
    try:
        return f"{float(value):.{decimals}f} %".replace(".", ",")
    except (ValueError, TypeError):
        return str(value)


def main():
    parser = argparse.ArgumentParser(description="Génère un dossier PDF banque")
    parser.add_argument("--listing", required=True)
    parser.add_argument("--analyse", required=True)
    parser.add_argument("--borrower-info", help="JSON avec infos emprunteur")
    parser.add_argument("--renderings", help="Dossier images IA")
    parser.add_argument("--template-dir", default=None)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    listing = json.loads(Path(args.listing).read_text(encoding="utf-8"))
    analyse = json.loads(Path(args.analyse).read_text(encoding="utf-8"))
    borrower = {}
    if args.borrower_info:
        borrower = json.loads(Path(args.borrower_info).read_text(encoding="utf-8"))

    renderings = []
    if args.renderings:
        rdir = Path(args.renderings).expanduser()
        manifest = rdir / "manifest.json"
        if manifest.exists():
            renderings = json.loads(manifest.read_text(encoding="utf-8"))
            # Résoudre les chemins absolus pour WeasyPrint
            for r in renderings:
                r["file_abs"] = str((rdir / r["file"]).resolve())

    # Setup Jinja2
    template_dir = Path(args.template_dir) if args.template_dir else Path(__file__).parent.parent / "templates"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["eur"] = format_eur
    env.filters["pct"] = format_pct

    template = env.get_template("bank_report.html")
    html_content = template.render(
        listing=listing,
        analyse=analyse,
        borrower=borrower,
        renderings=renderings,
    )

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🖨️  Génération PDF...", file=sys.stderr)
    HTML(string=html_content, base_url=str(template_dir)).write_pdf(str(output_path))
    print(f"✓ PDF généré : {output_path}", file=sys.stderr)
    print(str(output_path))


if __name__ == "__main__":
    main()
