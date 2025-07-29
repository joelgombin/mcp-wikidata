#!/usr/bin/env python3
"""
Lanceur MCP Wikidata spécifiquement pour Claude Desktop
Utilise l'environnement virtuel créé par uv
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Répertoire du projet
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Environnement virtuel uv
    venv_python = project_dir / ".venv" / "bin" / "python"
    
    if not venv_python.exists():
        print("Erreur: Environnement virtuel non trouvé. Exécutez 'uv sync' d'abord.", file=sys.stderr)
        sys.exit(1)
    
    # Variables d'environnement
    env = os.environ.copy()
    env["WIKIDATA_USER_AGENT"] = "Claude-Desktop-MCP-Wikidata/0.1.0"
    env["VIRTUAL_ENV"] = str(project_dir / ".venv")
    env["PATH"] = f"{project_dir / '.venv' / 'bin'}:{env.get('PATH', '')}"
    
    # Arguments filtrés (enlever les redondants)
    args = [arg for arg in sys.argv[1:] if arg not in ["run", "mcp-wikidata"]]
    
    # Commande finale
    cmd = [str(venv_python), "-m", "mcp_wikidata.server"] + args
    
    # Exécuter
    try:
        os.execve(str(venv_python), cmd, env)
    except Exception as e:
        print(f"Erreur lors du lancement: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()