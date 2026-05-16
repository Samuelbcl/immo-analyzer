---
description: Analyse complète d'une annonce Immoweb (prix, travaux, rendement, scénarios, images IA de rénovation)
allowed-tools: ["Read", "Write", "Edit", "Bash", "WebFetch", "WebSearch", "AskUserQuestion"]
argument-hint: "<url-immoweb>"
---

# /analyse-immo

Lance l'analyse complète d'une annonce Immoweb.

## Arguments

- `$1` : URL de l'annonce Immoweb (obligatoire)

## Workflow

1. **Vérifier que `$1` est une URL Immoweb valide.** Format attendu :
   `https://www.immoweb.be/fr/annonce/maison/a-vendre/<ville>/<code-postal>/<reference>`
   Si non, demander à l'utilisateur de coller le bon lien.

2. **Charger le skill `immo-analyzer`** (voir `skills/immo-analyzer/SKILL.md`).

3. **Briefing utilisateur (AskUserQuestion)** : revenu net, apport, usage prévu, expérience.

4. **Extraire les données** :
   ```bash
   cd $CLAUDE_PLUGIN_ROOT
   python3 scripts/fetch_immoweb.py "$1" --output /tmp/listing.json
   ```

5. **Recherche marché** via WebSearch sur la ville :
   - `prix moyen maison <ville> /m² 2026`
   - `loyer moyen <ville> appartement 2026`
   - `quartier <rue> <ville> investissement`

6. **Chiffrage travaux + scénarios** :
   ```bash
   python3 scripts/analyze_listing.py /tmp/listing.json \
     --revenu-net <revenu> \
     --apport <apport> \
     --usage <usage> \
     --output /tmp/analyse.json
   ```

7. **Préparation images de rénovation** (mode manuel par défaut) :
   ```bash
   # Mode manuel (recommandé) : génère prompts.txt + instructions
   python3 scripts/generate_renovations.py /tmp/listing.json \
     --manual \
     --output-dir ~/Documents/immo-analyzer/<ref>/renderings/ \
     --count 6
   ```

   En sortie, l'utilisateur reçoit :
   - `prompts.txt` : 6 prompts prêts à copier-coller dans ChatGPT Plus / Bing / Midjourney
   - `COMMENT_FAIRE.md` : instructions pas-à-pas
   - `manifest.json` : référence des noms de fichiers attendus

   L'utilisateur génère lui-même les images via son outil préféré et les dépose dans
   le dossier `renderings/` avec les noms exacts indiqués. Le rapport HTML les détecte
   automatiquement et les intègre — il peut être régénéré sans tout relancer.

   Si l'utilisateur a une clé OpenAI API et veut l'automatisation complète :
   ```bash
   python3 scripts/generate_renovations.py /tmp/listing.json --auto ...
   ```

8. **Génération rapport HTML** :
   ```bash
   python3 scripts/build_report.py \
     --listing /tmp/listing.json \
     --analyse /tmp/analyse.json \
    