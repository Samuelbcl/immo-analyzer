#!/usr/bin/env bash
# install.sh — Installation rapide d'immo-analyzer

set -e

PLUGIN_DIR="${HOME}/.claude/plugins/immo-analyzer"

echo "🏠 Installation d'immo-analyzer..."

# 1. Copier les fichiers
if [ -d "$PLUGIN_DIR" ]; then
  echo "⚠️  Plugin déjà installé dans $PLUGIN_DIR"
  read -p "Écraser ? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 1; fi
  rm -rf "$PLUGIN_DIR"
fi

mkdir -p "$PLUGIN_DIR"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -r "$SCRIPT_DIR"/. "$PLUGIN_DIR/"

# 2. Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r "$PLUGIN_DIR/requirements.txt" --user

# 3. Setup .env
if [ ! -f "$PLUGIN_DIR/.env" ]; then
  cp "$PLUGIN_DIR/.env.example" "$PLUGIN_DIR/.env"
  echo "📝 Fichier .env créé. Édite-le pour ajouter ta clé OPENAI_API_KEY :"
  echo "   $PLUGIN_DIR/.env"
fi

# 4. Vérification weasyprint (PDF)
echo "🔍 Vérification de weasyprint (PDF)..."
if ! python3 -c "import weasyprint" 2>/dev/null; then
  echo "⚠️  WeasyPrint nécessite des libs système :"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   brew install pango cairo libffi"
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "   sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libcairo2"
  fi
fi

echo ""
echo "✅ Installation terminée !"
echo ""
echo "Utilisation :"
echo "  $ claude"
echo "  > /analyse-immo https://www.immoweb.be/fr/annonce/..."
echo "  > /compare-immo <url1> <url2>"
echo "  > /rapport-banque <url>"
echo ""
echo "N'oublie pas d'éditer $PLUGIN_DIR/.env pour ta clé OpenAI."
