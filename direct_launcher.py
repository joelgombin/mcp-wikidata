#!/usr/bin/env python3
"""
Lanceur direct MCP Wikidata - Similaire au pattern basecamp
Point d'entrée direct sans dépendance uv
"""

import os
import sys
import asyncio
from pathlib import Path

# Ajouter le répertoire du projet au PYTHONPATH
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Import direct du serveur
try:
    from mcp_wikidata.server import main
except ImportError as e:
    print(f"Erreur d'import: {e}", file=sys.stderr)
    print("Assurez-vous que les dépendances sont installées avec 'uv sync'", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    # Configurer l'environnement
    os.environ.setdefault("WIKIDATA_USER_AGENT", "Claude-Desktop-MCP-Wikidata/0.1.0")
    
    # Changer vers le répertoire du projet
    os.chdir(project_dir)
    
    # Lancer le serveur MCP directement
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Erreur lors du lancement du serveur: {e}", file=sys.stderr)
        sys.exit(1)