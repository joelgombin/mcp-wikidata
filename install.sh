#!/bin/bash

# Script d'installation pour MCP Wikidata
# Automatise l'installation et la configuration avec Claude Desktop

set -e

echo "🚀 Installation de MCP Wikidata..."

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Obtenir le répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📂 Répertoire d'installation: $SCRIPT_DIR"

# Vérifier que uv est installé
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv n'est pas installé.${NC}"
    echo "Installez uv avec : curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo -e "${GREEN}✅ uv trouvé$(NC)"

# Installer les dépendances
echo "📦 Installation des dépendances..."
uv sync

# Rendre le script wrapper exécutable
chmod +x run_mcp_wikidata.sh

# Test d'installation
echo "🧪 Test de l'installation..."
if uv run python test_connection.py; then
    echo -e "${GREEN}✅ Installation réussie !${NC}"
else
    echo -e "${RED}❌ Erreur lors du test d'installation${NC}"
    exit 1
fi

# Configuration Claude Desktop
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

echo ""
echo -e "${YELLOW}📋 Configuration Claude Desktop :${NC}"
echo ""
echo "Ajoutez cette configuration à votre fichier Claude Desktop :"
echo -e "${YELLOW}$CLAUDE_CONFIG${NC}"
echo ""
echo "{"
echo '  "mcpServers": {'
echo '    "mcp-wikidata": {'
echo "      \"command\": \"$SCRIPT_DIR/run_mcp_wikidata.sh\","
echo '      "args": []'
echo '    }'
echo '  }'
echo "}"
echo ""

# Proposer d'ajouter automatiquement la configuration
if [[ -f "$CLAUDE_CONFIG" ]]; then
    echo -e "${YELLOW}🤔 Voulez-vous ajouter automatiquement cette configuration ? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Backup du fichier existant
        cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
        
        # Ajouter la configuration (approche simple - remplacer si mcp-wikidata existe déjà)
        python3 -c "
import json
import sys

config_file = '$CLAUDE_CONFIG'
with open(config_file, 'r') as f:
    config = json.load(f)

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['mcp-wikidata'] = {
    'command': '$SCRIPT_DIR/run_mcp_wikidata.sh',
    'args': []
}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print('✅ Configuration ajoutée automatiquement')
"
        
        echo -e "${GREEN}✅ Configuration mise à jour !${NC}"
        echo -e "${YELLOW}🔄 Redémarrez Claude Desktop pour appliquer les changements.${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  Fichier de configuration Claude Desktop non trouvé.${NC}"
    echo "Créez-le manuellement avec la configuration ci-dessus."
fi

echo ""
echo -e "${GREEN}🎉 Installation terminée !${NC}"
echo ""
echo "Prochaines étapes :"
echo "1. Redémarrez Claude Desktop"
echo "2. Le serveur MCP Wikidata sera disponible avec 5 outils"
echo "3. Testez avec : npx @modelcontextprotocol/inspector $SCRIPT_DIR/run_mcp_wikidata.sh"
echo ""