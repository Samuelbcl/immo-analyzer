# CLAUDE.md — Contexte projet pour Claude Code

Ce fichier est lu automatiquement par Claude Code quand tu ouvres ce repo dans VS Code. Il donne à l'agent tout le contexte nécessaire pour bosser efficacement sur le projet.

## Projet

**immo-analyzer** est un plugin Claude Code (CLI terminal) qui analyse une annonce immobilière belge (Immoweb) et produit :
- Un rapport HTML d'investissement locatif (prix, travaux, rendement, scénarios)
- Des prompts pour générer des images "après rénovation" (mode manuel par défaut, DALL-E API en option)
- Un PDF formel pour rendez-vous bancaire
- Une comparaison multi-biens

Marché ciblé : **Wallonie** (Liège, Verviers, Namur, Charleroi). Tous les calculs fiscaux (droits d'enregistrement, précompte immobilier, primes) sont spécifiques à la région wallonne.

## Stack technique

- **Python 3.10+** pour tous les scripts (`scripts/`)
- **Jinja2** pour les templates HTML/PDF (`templates/`)
- **Chart.js** (CDN) pour les graphiques dans le rapport HTML
- **WeasyPrint** pour la génération PDF banque
- **OpenAI Python SDK** pour le mode auto DALL-E (optionnel)
- **BeautifulSoup4 + requests** pour le scraping Immoweb

## Architecture

```
immo-analyzer/
├── .claude-plugin/plugin.json    ← Manifest reconnu par Claude Code
├── skills/immo-analyzer/SKILL.md ← Brief principal de l'agent
├── commands/                     ← Slash commands (analyse-immo, compare-immo, rapport-banque)
├── scripts/                      ← Pipeline Python
│   ├── fetch_immoweb.py          → Scraping
│   ├── market_data.py            → Constants marché belge 2026
│   ├── utils.py                  → Helpers calculs financiers
│   ├── analyze_listing.py        → Orchestrateur analyse complète
│   ├── generate_renovations.py   → Images (mode manuel/auto)
│   ├── build_report.py           → Génération HTML
│   ├── build_bank_pdf.py         → Génération PDF banque
│   └── build_comparison.py       → Comparaison multi-biens
└── templates/                    ← Jinja2 (report.html, bank_report.html, comparison.html)
```

## Conventions de code

- **Pas d'emoji dans le code source.** L'environnement de l'utilisateur a planté avec certains emojis sur les écritures de fichiers, donc on évite. Garde les emojis pour le HTML rendu seulement.
- **Sortie console en ASCII** (`OK`, `ERREUR`, `ATTENTION`) au lieu de `✓`, `✗`, `⚠️`.
- **F-strings imbriquées** : éviter d'imbriquer deux f-strings avec le même type de quote (compatibilité Python 3.10). Utiliser `.append()` + `"\n".join()` pour les longs blocs de texte plutôt que des triple f-strings avec interpolations multiples.
- **Pas de fonctions trop longues** : si un script dépasse 200 lignes, le splitter en helpers.
- **Toutes les valeurs de marché** vont dans `scripts/market_data.py`, jamais hardcodées ailleurs.
- **Tous les calculs financiers** vont dans `scripts/utils.py`, jamais dupliqués.

## Données du marché belge à jour (2026)

Voir `scripts/market_data.py` pour les valeurs sourcées :
- **Droits d'enregistrement Wallonie** : 3 % habitation propre et unique / 12,5 % autre (réforme 01/01/2025)
- **Quotité max BNB** : 90 % résidence principale / 80 % investissement locatif
- **Taux fixe 25 ans 2026** : 3,77 % bons dossiers (DirectFin baromètre)
- **TVA travaux logement > 10 ans** : 6 %
- **Indexation RC 2026** : 2,18 (publié au MB)
- **Précompte additionnels Verviers** : 28× communaux, 15× provincial

À mettre à jour annuellement.

## Pour itérer

### Ajouter une nouvelle ville
Édite `scripts/market_data.py` → ajouter dans `PRIX_M2_VENTE`, `LOYER_MOYEN`, `PRECOMPTE_COMMUNES`.

### Modifier le design du rapport
Édite `templates/report.html`. Les variables Jinja2 disponibles sont définies dans `scripts/build_report.py` (`listing`, `analyse`, `renderings`).

Couleurs du design system :
- `--accent: #c2410c` (terracotta — couleur principale)
- `--ink: #1a1a1a` (texte)
- `--paper: #fafaf7` (fond)
- `--green: #15803d` (succès)
- `--red: #b91c1c` (alerte)
- `--amber: #b45309` (attention)

### Ajouter un scénario de rentabilité
Édite `scripts/analyze_listing.py` → fonction `calculer_scenarios()`. Le scénario doit retourner les clés standard du dict de rendement (cf. `utils.rendement_locatif_net()`).

### Ajouter une source de scraping (Realo, Zimmo)
Créer `scripts/fetch_realo.py` sur le même modèle que `fetch_immoweb.py`. Output JSON doit respecter le même schéma (voir `examples/sample-listing.json`).

## À NE PAS faire

- ❌ Ne jamais commit `.env` (il contient la clé OpenAI)
- ❌ Ne pas hardcoder de chiffres financiers dans les templates Jinja2 — passer par `analyse.json`
- ❌ Ne pas modifier les calculs fiscaux sans citer la source (notaire.be, wallonie.be)
- ❌ Ne pas mélanger les UI strings (qui peuvent contenir des emojis) et les fichiers générés (qui doivent rester en ASCII)

## Tests

Pas de framework de test pour l'instant (à ajouter). En attendant :
```bash
# Test scraping
python3 scripts/fetch_immoweb.py <url> --output /tmp/test.json

# Test analyse (avec sample)
python3 scripts/analyze_listing.py examples/sample-listing.json --revenu-net 2200 --apport 13000 --output /tmp/analyse.json

# Test génération rapport
python3 scripts/build_report.py --listing examples/sample-listing.json --analyse /tmp/analyse.json --output /tmp/test-report.html
```

## Roadmap (idées en attente)

- [ ] Tests unitaires (pytest) sur `utils.py` et `analyze_listing.py`
- [ ] Support Realo + Zimmo en plus d'Immoweb
- [ ] Intégration carte d'aléa inondation (CIGER Wallonie)
- [ ] Mode `--watch` qui surveille de nouvelles annonces selon critères
- [ ] Adaptation Flandre + Bruxelles (droits d'enregistrement différents)
- [ ] Mode "estimation pré-acquisition" (générer le PDF banque sans rapport HTML)
- [ ] Export Excel pour le banquier (en complément du PDF)
- [ ] Stress test scénario "départ locataire au mois 6 + 4 mois de vacance"

## Conventions de commit

```
feat:     nouvelle fonctionnalité
fix:      correction de bug
docs:     documentation seulement
refactor: refactoring sans changement de comportement
chore:    maintenance, dépendances, config
data:     mise à jour des valeurs de marché
```

Exemple : `feat: ajouter scénario division horizontale 3 logements`

## Contact

samuelbiancola@gmail.com
