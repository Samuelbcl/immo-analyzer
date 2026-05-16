#!/usr/bin/env python3
"""
build_comparison.py — Génère un rapport HTML comparatif entre plusieurs biens.

Usage:
    python3 build_comparison.py --listings l1.json l2.json l3.json \
        --analyses a1.json a2.json a3.json --output comparaison.html
"""

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


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
    parser = argparse.ArgumentParser(description="Comparaison de plusieurs biens")
    parser.add_argument("--listings", nargs="+", required=True)
    parser.add_argument("--analyses", nargs="+", required=True)
    parser.add_argument("--template-dir", default=None)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    if len(args.listings) != len(args.analyses):
        print("❌ Nombre de listings != nombre d'analyses", file=sys.stderr)
        sys.exit(1)

    biens = []
    for lpath, apath in zip(args.listings, args.analyses):
        listing = json.loads(Path(lpath).read_text(encoding="utf-8"))
        analyse = json.loads(Path(apath).read_text(encoding="utf-8"))
        biens.append({"listing": listing, "analyse": analyse})

    # Trier par score décroissant
    biens.sort(key=lambda b: b["analyse"]["score"]["total"], reverse=True)

    template_dir = Path(args.template_dir) if args.template_dir else Path(__file__).parent.parent / "templates"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["eur"] = format_eur
    env.filters["pct"] = format_pct

    template = env.get_template("comparison.html")
    html = template.render(biens=biens)

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"✓ Comparaison générée : {output_path}", file=sys.stderr)
    print(str(output_path))


if __name__ == "__main__":
    main()
