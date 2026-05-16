# 🏠 Immo-Analyzer — Plugin Claude Code

> Agent expert en analyse d'investissement immobilier locatif en Belgique. Analyse une annonce Immoweb, chiffre les travaux, calcule le rendement, génère des visualisations IA de rénovation (DALL-E 3) et produit un rapport complet pour la banque.

## ✨ Ce qu'il fait

Tu colles un lien Immoweb dans ton terminal, il te sort :

- 📊 **Rapport HTML interactif** avec graphiques (prix, rendement, scénarios)
- 🎨 **Images IA "après rénovation"** générées par DALL-E 3 pour chaque pièce clé
- 💰 **Chiffrage travaux** poste par poste basé sur les prix du marché liégeois 2026
- 🏦 **Dossier PDF formel pour la banque** avec plan d'amortissement, ratios, scénarios
- ⚖️ **Comparaison automatique** entre plusieurs biens (table de scoring)
- 🚩 **Pièges et red flags** spécifiques au marché belge (PEB, RC, division, primes)

## 🚀 Installation rapide

### 1. Cloner le plugin

```bash
git clone https://github.com/samuelbiancola/immo-analyzer.git ~/.claude/plugins/immo-analyzer
# ou télécharger ce zip et le décompresser dans ~/.claude/plugins/
```

### 2. Installer les dépendances Python

```bash
cd ~/.claude/plugins/immo-analyzer
pip install -r requirements.txt
```

Sur macOS, pour weasyprint (PDF) :
```bash
brew install pango cairo libffi
```

Sur Ubuntu :
```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libcairo2
```

### 3. Choisir le mode de génération d'images

Le plugin propose **deux modes** pour les images "après rénovation" :

**🆓 Mode MANUEL (par défaut, gratuit)** — Recommandé

Le plugin écrit pour toi un fichier `prompts.txt` avec 6 prompts pros prêts à copier-coller. Tu génères les images dans **ton outil préféré** :
- **ChatGPT Plus** (DALL-E 3 inclus dans l'abo)
- **Bing Image Creator** (https://www.bing.com/create — DALL-E 3 gratuit)
- **Midjourney**, **Stable Diffusion local**, **Leonardo.ai**, **Pollinations.ai**...

Tu télécharges chaque image, tu la renommes selon le manifest (cuisine.png, salon.png, etc.) et tu la déposes dans le dossier `renderings/`. Le rapport les intègre automatiquement.

**💸 Mode AUTO (DALL-E 3 via API, ~0,30 €/bien)** — Optionnel

Si tu veux que ça soit 100 % automatisé, ajoute ta clé OpenAI :

```bash
cp .env.example .env
# Édite .env et ajoute ta clé OPENAI_API_KEY
```

Récupère ta clé sur https://platform.openai.com/api-keys.

**⚠️ Important** : ton abonnement ChatGPT Plus à 20 €/mois ne donne **pas** accès à l'API. Si tu veux éviter la double facturation, reste sur le mode MANUEL.

### 4. Activer le plugin dans Claude Code

```bash
claude
> /plugin install immo-analyzer
```

## 📖 Utilisation

### Analyser une annonce

```bash
claude
> /analyse-immo https://www.immoweb.be/fr/annonce/maison/a-vendre/verviers/4800/21538755
```

Demande optionnelle de précisions :
- Ton revenu net mensuel
- Apport disponible
- Usage prévu (locatif pur / habitation propre puis location)

→ Sortie : `~/Documents/immo-analyzer/<reference>/rapport.html` + images dans `/renderings/`

### Comparer plusieurs biens

```bash
> /compare-immo https://...annonce1 https://...annonce2 https://...annonce3
```

→ Tableau de scoring (prix/m², rendement, travaux, faisabilité) + recommandation.

### Générer le dossier PDF pour la banque

```bash
> /rapport-banque https://www.immoweb.be/...
```

→ PDF formel `dossier-banque-<adresse>.pdf` avec :
- Page de garde avec photos
- Synthèse exécutive
- Plan de financement détaillé
- Tableau d'amortissement
- Projections locatives sur 10 ans
- Photos avant/après rénovation IA

## 🧠 Comment ça marche

```
┌─────────────────┐
│  URL Immoweb    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  fetch_immoweb  │─────▶│  Extraction      │
│      .py        │      │  - Prix, m², ch  │
└─────────────────┘      │  - PEB, RC       │
                         │  - Photos        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  market_research │  → recherche web
                         │      .py         │     prix Verviers/Liège
                         └────────┬─────────┘
                                  │
                ┌─────────────────┴─────────────────┐
                │                                   │
                ▼                                   ▼
       ┌─────────────────┐                ┌─────────────────┐
       │ generate_       │                │  build_report   │
       │ renovations.py  │                │      .py        │
       │  (DALL-E 3)     │                │   (HTML +       │
       └─────────────────┘                │   Chart.js)     │
                │                         └─────────────────┘
                └─────────────┬────────────────────┘
                              ▼
                     ┌─────────────────┐
                     │ rapport.html    │
                     │ + dossier.pdf   │
                     └─────────────────┘
```

## 📁 Structure du plugin

```
immo-analyzer/
├── .claude-plugin/
│   └── plugin.json              # Manifest
├── commands/
│   ├── analyse-immo.md          # /analyse-immo
│   ├── compare-immo.md          # /compare-immo
│   └── rapport-banque.md        # /rapport-banque
├── skills/
│   └── immo-analyzer/
│       └── SKILL.md             # Cerveau du skill
├── scripts/
│   ├── fetch_immoweb.py         # Scraper Immoweb
│   ├── market_research.py       # Recherche prix marché
│   ├── generate_renovations.py  # DALL-E 3 integration
│   ├── build_report.py          # Génération HTML
│   ├── build_bank_pdf.py        # Génération PDF banque
│   └── utils.py                 # Helpers (calculs financiers)
├── templates/
│   ├── report.html              # Template Jinja2 rapport
│   └── bank_report.html         # Template Jinja2 PDF
├── examples/
│   └── sample-output/           # Exemple de rapport
├── requirements.txt
├── .env.example
└── README.md
```

## 💰 Coûts d'utilisation

| Composant | Mode manuel | Mode auto |
|-----------|-------------|-----------|
| Claude Code | 