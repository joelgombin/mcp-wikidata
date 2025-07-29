#!/bin/bash

# Script de debug spécifique pour Claude Desktop
# Enregistre tous les détails d'exécution pour diagnostiquer les problèmes

set -e

# Fichier de log avec timestamp
LOG_FILE="/tmp/mcp_wikidata_claude_debug_$(date +%Y%m%d_%H%M%S).log"

# Fonction de log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== DEBUT DEBUG CLAUDE DESKTOP ==="
log "Script appelé: $0"
log "Arguments: $@"
log "Nombre d'arguments: $#"
log "PWD: $(pwd)"
log "USER: $USER"
log "HOME: $HOME"
log "PATH: $PATH"

# Log détaillé des arguments
for i in $(seq 1 $#); do
    log "Arg[$i]: '${!i}'"
done

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log "SCRIPT_DIR: $SCRIPT_DIR"

# Aller dans le bon répertoire
cd "$SCRIPT_DIR"
log "Changed to: $(pwd)"

# Variables d'environnement pour Wikidata
export WIKIDATA_USER_AGENT="${WIKIDATA_USER_AGENT:-Claude-Desktop-MCP-Wikidata/0.1.0}"
log "WIKIDATA_USER_AGENT: $WIKIDATA_USER_AGENT"

# Chercher uv
UV_PATHS=(
    "$HOME/.local/bin/uv"
    "$HOME/.cargo/bin/uv" 
    "/usr/local/bin/uv"
    "/opt/homebrew/bin/uv"
    "$(which uv 2>/dev/null)"
)

UV_CMD=""
for uv_path in "${UV_PATHS[@]}"; do
    log "Checking uv path: '$uv_path'"
    if [[ -n "$uv_path" && -x "$uv_path" ]]; then
        UV_CMD="$uv_path"
        log "Found uv: $UV_CMD"
        break
    fi
done

if [[ -z "$UV_CMD" ]]; then
    log "ERROR: uv not found"
    echo "Erreur: uv n'est pas trouvé. Consultez le log: $LOG_FILE" >&2
    exit 1
fi

# Vérifier les fichiers nécessaires
if [[ ! -f "pyproject.toml" ]]; then
    log "ERROR: pyproject.toml not found in $(pwd)"
    exit 1
fi

if [[ ! -d "mcp_wikidata" ]]; then
    log "ERROR: mcp_wikidata directory not found in $(pwd)"
    exit 1
fi

# Filtrer les arguments
FILTERED_ARGS=()
for arg in "$@"; do
    if [[ "$arg" != "run" && "$arg" != "mcp-wikidata" ]]; then
        FILTERED_ARGS+=("$arg")
        log "Including arg: '$arg'"
    else
        log "Filtering out arg: '$arg'"
    fi
done

# Commande finale
CMD=("$UV_CMD" "run" "mcp-wikidata" "${FILTERED_ARGS[@]}")
log "Final command: ${CMD[*]}"

# Test préliminaire (sans exec)
log "Testing uv sync..."
if "$UV_CMD" sync --quiet 2>>"$LOG_FILE"; then
    log "uv sync successful"
else
    log "uv sync failed - check log"
fi

log "Testing basic command..."
if "$UV_CMD" run mcp-wikidata --help >>"$LOG_FILE" 2>&1; then
    log "Basic command test successful"
else
    log "Basic command test failed - check log"
fi

# Lancer le serveur MCP
log "Executing: ${CMD[*]}"
log "Log file: $LOG_FILE"

# Rediriger stderr vers le log aussi
exec 2> >(tee -a "$LOG_FILE" >&2)

exec "${CMD[@]}"