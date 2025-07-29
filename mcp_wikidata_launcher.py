#!/usr/bin/env python3
"""
Lanceur Python pour MCP Wikidata
Alternative robuste au script bash pour éviter les problèmes d'arguments
"""

import os
import sys
import subprocess
from pathlib import Path

def find_uv():
    """Trouve le chemin vers uv."""
    possible_paths = [
        Path.home() / ".local" / "bin" / "uv",
        Path.home() / ".cargo" / "bin" / "uv", 
        Path("/usr/local/bin/uv"),
        Path("/opt/homebrew/bin/uv"),
    ]
    
    # Essayer which/where
    try:
        result = subprocess.run(["which", "uv"], capture_output=True, text=True)
        if result.returncode == 0:
            possible_paths.insert(0, Path(result.stdout.strip()))
    except:
        pass
    
    for path in possible_paths:
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
    
    return None

def main():
    # Aller dans le répertoire du script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Configurer l'environnement
    os.environ.setdefault("WIKIDATA_USER_AGENT", "Claude-Desktop-MCP-Wikidata/0.1.0")
    
    # Trouver uv
    uv_path = find_uv()
    if not uv_path:
        print("Erreur: uv n'est pas trouvé.", file=sys.stderr)
        print("Installez uv: https://docs.astral.sh/uv/getting-started/installation/", file=sys.stderr)
        sys.exit(1)
    
    # Construire la commande
    cmd = [uv_path, "run", "mcp-wikidata"]
    
    # Ajouter les arguments, en filtrant les redondants
    for arg in sys.argv[1:]:
        if arg not in ["run", "mcp-wikidata"]:
            cmd.append(arg)
    
    # Exécuter
    try:
        os.execv(uv_path, cmd)
    except Exception as e:
        print(f"Erreur lors du lancement: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()