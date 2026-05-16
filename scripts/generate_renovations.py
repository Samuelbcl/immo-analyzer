#!/usr/bin/env python3
"""generate_renovations.py - Generation d'images apres renovation.

Deux modes :
  --manual (defaut) : genere prompts.txt + structure dossier (gratuit)
  --auto            : appelle DALL-E 3 via OpenAI API
"""

import argparse
import json
import os
import sys
from pathlib import Path


PROMPTS_TEMPLATES = {
    "cuisine": "Photorealistic real estate photo of a fully renovated Belgian townhouse kitchen, approximately {surface} square meters. Modern minimalist style: matte white cabinets, oak wooden countertop, terracotta or beige floor tiles, brass fixtures, integrated stainless steel appliances, natural daylight from a window with white frame, no people, wide angle, high-end interior magazine quality.",
    "salon": "Photorealistic real estate photo of a renovated living room in a Belgian townhouse, approximately {surface} square meters, contemporary scandinavian style: light oak parquet floor, white walls with subtle wainscoting, large window with natural light, neutral fabric sofa, small coffee table, minimalist art, no people, wide angle, real estate photography, warm afternoon light.",
    "chambre": "Photorealistic real estate photo of a renovated bedroom in a Belgian townhouse, approximately {surface} square meters, calm minimalist: light oak floor, soft greige walls, double bed with linen bedding, small bedside table, large window with linen curtains, no people, wide angle, natural soft morning light.",
    "salle_de_bain": "Photorealistic real estate photo of a renovated bathroom in a Belgian townhouse, approximately {surface} square meters, modern clean: white subway tile shower wall, terrazzo or matte concrete floor tiles, wall-hung vanity with double sink, large round mirror, matte black fixtures, warm towel rail, natural light, no people, wide angle.",
    "facade": "Photorealistic exterior photo of a renovated Belgian townhouse facade, traditional 19th century Walloon architecture, brick or stone, repointed brick, refurbished sash windows with white frames, freshly painted dark grey or anthracite front door, daylight, no people, real estate photography, ground level perspective.",
    "terrasse": "Photorealistic real estate photo of a renovated rooftop terrace on a Belgian townhouse, approximately {surface} square meters, wood deck composite, small bistro table with two chairs, potted plants and lavender, view over rooftops, soft golden hour light, no people, wide angle, real estate photography.",
    "studio": "Photorealistic real estate photo of a converted ground floor studio apartment in a Belgian townhouse, approximately {surface} square meters, open plan with kitchenette: white cabinets, small dining table, single bed area, neutral floor tiles, large window, no people, wide angle.",
}


def choisir_pieces(listing, count):
    bedrooms = listing.get("bedrooms") or 3
    surface = listing.get("surface") or 100
    features = listing.get("features") or []
    selections = []
    selections.append(("facade", {"surface": surface}))
    selections.append(("cuisine", {"surface": 8}))
    selections.append(("salon", {"surface": 22}))
    selections.append(("salle_de_bain", {"surface": 6}))
    if bedrooms >= 1:
        selections.append(("chambre", {"surface": 12}))
    if "terrasse" in features:
        selections.append(("terrasse", {"surface": 16}))
    if bedrooms >= 3 and surface >= 100:
        selections.append(("studio", {"surface": 30}))
    return selections[:count]


def write_prompts_file(prompts_path, listing, pieces):
    address = listing.get("address") or "-"
    reference = listing.get("reference") or "-"
    lines = []
    lines.append("# Prompts pour generation d'images - mode manuel")
    lines.append("")
    lines.append(f"## Bien : {address}")
    lines.append(f"## Reference : {reference}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("INSTRUCTIONS :")
    lines.append("1. Ouvre ChatGPT (Plus = DALL-E 3) ou Bing Image Creator (gratuit) ou Midjourney")
    lines.append("2. Pour chaque prompt, genere l'image")
    lines.append("3. Telecharge chaque image et place-la dans CE dossier")
    lines.append("4. NOMS DE FICHIERS attendus :")
    for room, _ in pieces:
        lines.append(f"   - {room}.png ou {room}.jpg")
    lines.append("")
    lines.append("Une fois en place, relance la generation du rapport.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("# Prompts a copier-coller")
    lines.append("")
    for i, (room, params) in enumerate(pieces, 1):
        prompt = PROMPTS_TEMPLATES[room].format(**params)
        lines.append(f"## {i}. {room.replace('_', ' ').title()}")
        lines.append(f"Nom de fichier attendu : {room}.png")
        lines.append("")
        lines.append("```")
        lines.append(prompt)
        lines.append("```")
        lines.append("")
    prompts_path.write_text("\n".join(lines), encoding="utf-8")


def write_instructions(instructions_path, output_dir, manifest, reference):
    file_list_items = []
    for p in manifest:
        file_list_items.append("- " + p["file"])
    file_list = "\n".join(file_list_items)

    text_parts = []
    text_parts.append("# Mode manuel - Comment placer tes images")
    text_parts.append("")
    text_parts.append(f"Le plugin a genere {len(manifest)} prompts dans prompts.txt.")
    text_parts.append("")
    text_parts.append("## Etape 1 - Genere les images")
    text_parts.append("")
    text_parts.append("Choisis ton outil :")
    text_parts.append("- ChatGPT Plus (DALL-E 3)")
    text_parts.append("- Bing Image Creator (https://www.bing.com/create) - gratuit")
    text_parts.append("- Midjourney")
    text_parts.append("- Stable Diffusion local")
    text_parts.append("- Pollinations.ai - gratuit sans inscription")
    text_parts.append("")
    text_parts.append("## Etape 2 - Place les fichiers")
    text_parts.append("")
    text_parts.append("Renomme tes images :")
    text_parts.append("")
    text_parts.append(file_list)
    text_parts.append("")
    text_parts.append(f"Mets-les dans : {output_dir}")
    text_parts.append("")
    text_parts.append("## Etape 3 - Regenere le rapport")
    text_parts.append("")
    text_parts.append("Relance /analyse-immo ou directement :")
    text_parts.append("```")
    text_parts.append("python3 scripts/build_report.py \\")
    text_parts.append("  --listing /tmp/listing.json \\")
    text_parts.append("  --analyse /tmp/analyse.json \\")
    text_parts.append(f"  --renderings {output_dir} \\")
    text_parts.append(f"  --output ~/Documents/immo-analyzer/{reference}/rapport.html")
    text_parts.append("```")
    text_parts.append("")
    text_parts.append("Le rapport HTML detectera les images presentes et les inserera.")
    text_parts.append("")
    text_parts.append("## Astuces")
    text_parts.append("- Pas obligatoire de tout generer. Le rapport affiche ce qu'il trouve.")
    text_parts.append("- Formats acceptes : .png, .jpg, .jpeg, .webp")
    text_parts.append("- Tu peux regenerer une seule image sans toucher aux autres.")

    instructions_path.write_text("\n".join(text_parts), encoding="utf-8")


def mode_manual(listing, output_dir, count):
    output_dir.mkdir(parents=True, exist_ok=True)
    pieces = choisir_pieces(listing, count)
    manifest = []
    for room, params in pieces:
        prompt = PROMPTS_TEMPLATES[room].format(**params)
        manifest.append({"room": room, "file": f"{room}.png", "prompt": prompt, "status": "pending"})

    prompts_path = output_dir / "prompts.txt"
    write_prompts_file(prompts_path, listing, pieces)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    instructions_path = output_dir / "COMMENT_FAIRE.md"
    write_instructions(instructions_path, output_dir, manifest, listing.get("reference") or "bien")

    print(f"OK Mode manuel active. {len(pieces)} prompts dans :", file=sys.stderr)
    print(f"  {prompts_path}", file=sys.stderr)
    print(f"  {instructions_path}", file=sys.stderr)
    print(f"Depose tes images dans : {output_dir}", file=sys.stderr)
    print("\nNoms de fichiers attendus :", file=sys.stderr)
    for p in manifest:
        print(f"  - {p['file']}", file=sys.stderr)
    print(json.dumps({"mode": "manual", "manifest": manifest, "directory": str(output_dir)}))
    return 0


def mode_auto(listing, output_dir, count):
    try:
        import requests
        from openai import OpenAI
        from dotenv import load_dotenv
    except ImportError as e:
        print(f"ERREUR dependance manquante: {e}", file=sys.stderr)
        return 1

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERREUR OPENAI_API_KEY manquante. Utilise --manual a la place.", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    pieces = choisir_pieces(listing, count)
    client = OpenAI(api_key=api_key)
    size = os.getenv("DALLE_SIZE", "1792x1024")
    quality = os.getenv("DALLE_QUALITY", "standard")
    generated = []

    print(f"Generation {len(pieces)} images via DALL-E 3...", file=sys.stderr)
    for room, params in pieces:
        prompt = PROMPTS_TEMPLATES[room].format(**params)
        print(f"  -> {room}...", file=sys.stderr)
        try:
            response = client.images.generate(
                model=os.getenv("DALLE_MODEL", "dall-e-3"),
                prompt=prompt, size=size, quality=quality, n=1,
            )
            url = response.data[0].url
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            dest = output_dir / f"{room}.png"
            dest.write_bytes(r.content)
            generated.append({"room": room, "file": dest.name, "prompt": prompt, "status": "ok"})
            print(f"    OK {dest.name}", file=sys.stderr)
        except Exception as e:
            print(f"    ATTENTION {e}", file=sys.stderr)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(generated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nOK {len(generated)} images generees. Cout ~{len(generated) * 0.04:.2f} USD", file=sys.stderr)
    print(json.dumps({"mode": "auto", "renderings": generated, "directory": str(output_dir)}))
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("listing")
    parser.add_argument("--output-dir", "-o", required=True)
    parser.add_argument("--count", type=int, default=6)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--manual", action="store_true")
    mode.add_argument("--auto", action="store_true")
    args = parser.parse_args()

    listing = json.loads(Path(args.listing).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir).expanduser()

    if args.auto:
        return mode_auto(listing, output_dir, args.count)
    return mode_manual(listing, output_dir, args.count)


if __name__ == "__main__":
    sys.exit(main())
