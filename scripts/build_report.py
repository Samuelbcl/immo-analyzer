#!/usr/bin/env python3
"""build_report.py - Genere le rapport HTML."""

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def format_eur(value, decimals=0):
    if value is None:
        return "-"
    try:
        if decimals == 0:
            return f"{int(round(float(value))):,}".replace(",", " ") + " EUR"
        return f"{float(value):,.{decimals}f}".replace(",", " ").replace(".", ",") + " EUR"
    except (ValueError, TypeError):
        return str(value)


def format_pct(value, decimals=1):
    if value is None:
        return "-"
    try:
        return f"{float(value):.{decimals}f} %".replace(".", ",")
    except (ValueError, TypeError):
        return str(value)


def format_int(value):
    if value is None:
        return "-"
    try:
        return f"{int(float(value)):,}".replace(",", " ")
    except (ValueError, TypeError):
        return str(value)


def get_renderings(renderings_dir):
    manifest_path = renderings_dir / "manifest.json"
    accepted_exts = {".png", ".jpg", ".jpeg", ".webp"}

    if manifest_path.exists():
        entries = json.loads(manifest_path.read_text(encoding="utf-8"))
        result = []
        for entry in entries:
            base = Path(entry.get("file", "")).stem
            for ext in accepted_exts:
                candidate = renderings_dir / f"{base}{ext}"
                if candidate.exists():
                    entry["file"] = candidate.name
                    result.append(entry)
                    break
        return result

    return [
        {"room": p.stem, "file": p.name, "prompt": ""}
        for p in renderings_dir.iterdir()
        if p.suffix.lower() in accepted_exts
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--listing", required=True)
    parser.add_argument("--analyse", required=True)
    parser.add_argument("--renderings", default=None)
    parser.add_argument("--template-dir", default=None)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    listing = json.loads(Path(args.listing).read_text(encoding="utf-8"))
    analyse = json.loads(Path(args.analyse).read_text(encoding="utf-8"))

    renderings = []
    renderings_rel = None
    if args.renderings:
        rdir = Path(args.renderings).expanduser()
        if rdir.exists():
            renderings = get_renderings(rdir)
            try:
                renderings_rel = rdir.relative_to(Path(args.output).parent)
            except ValueError:
                renderings_rel = rdir

    if args.template_dir:
        template_dir = Path(args.template_dir)
    else:
        template_dir = Path(__file__).parent.parent / "templates"

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["eur"] = format_eur
    env.filters["pct"] = format_pct
    env.filters["intf"] = format_int

    template = env.get_template("report.html")
    html = template.render(
        listing=listing,
        analyse=analyse,
        renderings=renderings,
        renderings_dir=str(renderings_rel) if renderings_rel else None,
    )

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"OK Rapport genere: {output_path}", file=sys.stderr)
    print(str(output_path))


if __name__ == "__main__":
    main()
