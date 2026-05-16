---
description: Compare 2 à 5 annonces Immoweb dans un tableau de scoring avec recommandation finale
allowed-tools: ["Read", "Write", "Edit", "Bash", "WebFetch", "WebSearch", "AskUserQuestion"]
argument-hint: "<url1> <url2> [<url3> <url4> <url5>]"
---

# /compare-immo

Compare jusqu'à 5 annonces Immoweb et produit un tableau de scoring.

## Arguments

- `$1, $2, ..., $5` : URLs Immoweb à comparer (2 minimum, 5 maximum)

## Workflow

1. **Valider toutes les URLs**. Si moins de 2 ou plus de 5, signaler.

2. **Charger le skill `immo-analyzer`**.

3. **Briefing utilisateur** (AskUserQuestion) : revenu, apport, usage prévu, critères prioritaires (rendement / prix / état / localisation).

4. **Pour chaque URL** :
   ```bash
   python3 scripts/fetch_immoweb.py "$URL" --output /tmp/listing_$i.json
   python3 scripts/analyze_listing.py /tmp/listing_$i.json \
     --revenu-net <r> --apport <a> --usage <u> \
     --output /tmp/analyse_$i.json
   ```

5. **Score chaque bien sur 100** (script `compute_score.py`) basé sur :
   - Prix /m² vs marché (25 points)
   - Rendement net projeté (30 points)
   - État technique (élec, chauffage, toiture, PEB) (20 points)
   - Localisation (transports, services, demande locative) (15 points)
   - Potentiel de division / extension (10 points)

6. **Construire le tableau comparatif** :
   ```bash
   python3 scripts/build_comparison.py \
     --listings /tmp/listing_*.json \
     --analyses /tmp/analyse_*.json \
     --output ~/Documents/immo-analyzer/comparaison-<date>.html
   ```

7. **Présenter** :
   - Tableau côte-à-côte (mini-cartes pour chaque bien)
   - Tableau de scoring avec barres horizontales
   - Recommandation finale claire ("Va sur le bien X parce que…")
   - Lien rapport HTML complet

## Exemple

```
> /compare-immo \
    https://www.immoweb.be/fr/annonce/.../21538755 \
    https://www.immoweb.be/fr/annonce/.../21998877 \
    https://www.immoweb.be/fr/annonce/.../21111222
```

## Note

Pour économiser des appels DALL-E, le mode comparaison **ne génère pas d'images IA** par défaut. Si l'utilisateur le souhaite, suggérer `/analyse-immo <url-du-gagnant>` ensuite pour avoir les images du bien retenu.
