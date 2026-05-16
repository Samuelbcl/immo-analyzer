# 🚀 Setup GitHub + Claude Code dans VS Code

Guide pas-à-pas pour pousser le projet sur GitHub et continuer à développer dans VS Code avec Claude Code.

## 1. Créer le repo sur GitHub

1. Va sur https://github.com/new
2. **Repository name** : `immo-analyzer`
3. **Description** : `Agent expert en analyse d'investissement immobilier locatif belge — plugin Claude Code`
4. **Visibility** : Private (recommandé tant que tu ajustes les valeurs financières) ou Public
5. **NE coche PAS** "Add a README" ni "Add .gitignore" ni "Choose a license" — on les a déjà
6. Clique "Create repository"

GitHub te montre les commandes à exécuter. Ignore-les, voilà les bonnes :

## 2. Pousser le code depuis ton terminal

```bash
# Va dans le dossier décompressé du plugin
cd ~/Downloads/immo-analyzer-plugin   # adapte le chemin

# Initialise git
git init
git add .
git commit -m "feat: initial commit - plugin immo-analyzer v1"

# Connecte au repo GitHub (remplace TON_USERNAME)
git branch -M main
git remote add origin https://github.com/TON_USERNAME/immo-analyzer.git

# Push
git push -u origin main
```

Si Git te demande tes credentials : utilise un **Personal Access Token** GitHub (Settings → Developer settings → Personal access tokens → Generate new token), pas ton mot de passe.

## 3. Ouvrir le projet dans VS Code avec Claude Code

### Prérequis VS Code

1. Installer VS Code : https://code.visualstudio.com/
2. Installer l'extension **Claude Code** depuis le Marketplace VS Code :
   - `Cmd/Ctrl+Shift+X` → cherche "Claude Code" → Install
   - Plus d'info : https://docs.claude.com/claude-code

### Cloner et ouvrir

```bash
git clone https://github.com/TON_USERNAME/immo-analyzer.git
cd immo-analyzer
code .
```

VS Code s'ouvre. L'extension Claude Code lit automatiquement le fichier `CLAUDE.md` à la racine et a tout le contexte du projet en mémoire.

### Premiers tests

Dans le terminal intégré VS Code :

```bash
# 1. Installer les deps
pip install -r requirements.txt

# 2. Copier .env.example en .env (optionnel, seulement pour mode DALL-E auto)
cp .env.example .env

# 3. Tester le scraping
python3 scripts/fetch_immoweb.py "https://www.immoweb.be/fr/annonce/maison/a-vendre/verviers/4800/21538755" --output /tmp/test.json
cat /tmp/test.json

# 4. Tester l'analyse complète
python3 scripts/analyze_listing.py /tmp/test.json --revenu-net 2200 --apport 13000 --output /tmp/analyse.json

# 5. Générer le rapport HTML
python3 scripts/generate_renovations.py /tmp/test.json --manual --output-dir /tmp/renderings/
python3 scripts/build_report.py --listing /tmp/test.json --analyse /tmp/analyse.json --renderings /tmp/renderings/ --output /tmp/rapport.html

# 6. Ouvrir le rapport
open /tmp/rapport.html  # macOS
xdg-open /tmp/rapport.html  # Linux
```

## 4. Workflow de dev avec Claude Code

Dans VS Code, ouvre la palette Claude Code (`Cmd/Ctrl+Shift+P` → "Claude Code: Open chat") et demande par exemple :

- *"Ajoute le support de Realo.be comme deuxième source de scraping en plus d'Immoweb"*
- *"Crée des tests pytest pour `utils.py` qui couvrent les calculs de mensualité et rendement"*
- *"Modifie le template HTML pour ajouter un graphique radar des points forts/faibles du bien"*
- *"Adapte les calculs fiscaux pour la Région flamande (droits d'enregistrement, primes)"*

Claude Code lit le `CLAUDE.md`, comprend l'architecture, et fait les modifications cohérentes avec les conventions.

## 5. Installer le plugin localement pour le tester

```bash
mkdir -p ~/.claude/plugins/
ln -s "$(pwd)" ~/.claude/plugins/immo-analyzer

# Vérifier
claude
> /plugin list   # tu dois voir immo-analyzer
> /analyse-immo https://www.immoweb.be/...
```

Avec le symlink, chaque modification dans VS Code est immédiatement active dans Claude Code — pas besoin de réinstaller.

## 6. Workflow git classique

```bash
# Travailler sur une feature
git checkout -b feat/ajouter-source-realo
# ... modifs ...
git add .
git commit -m "feat: ajouter scraper Realo.be"
git push origin feat/ajouter-source-realo
# → ouvrir PR sur GitHub
```

## 7. Conseil : créer un alias pour aller vite

Dans ton `.zshrc` ou `.bashrc` :

```bash
alias immo='cd ~/dev/immo-analyzer && code .'
alias immo-test='cd ~/dev/immo-analyzer && python3 scripts/analyze_listing.py'
```

## 8. Trois extensions VS Code utiles pour ce projet

- **Python** (Microsoft) : autocomplétion, linting
- **Jinja2** (wholroyd) : syntax highlighting des templates
- **Live Preview** (Microsoft) : prévisualiser le rapport HTML directement

## En cas de souci

- **`pip install` échoue sur weasyprint** : `brew install pango cairo libffi` (macOS) ou `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libcairo2` (Linux)
- **Le rapport HTML est cassé** : ouvre `templates/report.html` et regarde si les filtres Jinja2 utilisés correspondent à ceux définis dans `build_report.py` (eur, pct, intf)
- **Le scraper Immoweb renvoie vide** : Immoweb a probablement changé sa structure HTML. Édite `scripts/fetch_immoweb.py` → fonction `extract_classified_json()`.

Bon dev ! 🛠️
