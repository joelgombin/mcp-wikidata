#!/usr/bin/env python3
"""Script de debug pour les problèmes MCP avec Claude Desktop."""

import json
import logging
import sys
from mcp_wikidata.server import WikidataServer
from mcp_wikidata.config import Config

# Configuration du logging détaillé
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('/tmp/mcp_wikidata_debug.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("=== DEBUT DEBUG MCP WIKIDATA ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Arguments: {sys.argv}")
    
    try:
        # Test de configuration
        config = Config.from_env()
        logger.info(f"Configuration chargée: {config}")
        
        # Test d'initialisation du serveur
        server = WikidataServer(config)
        logger.info("Serveur initialisé avec succès")
        
        # Test des outils
        tools = server.tools.get_tool_definitions()
        logger.info(f"Outils disponibles: {[t.name for t in tools]}")
        
        # Lancer le serveur normalement
        logger.info("Lancement du serveur MCP...")
        import asyncio
        asyncio.run(server.run())
        
    except Exception as e:
        logger.error(f"ERREUR CRITIQUE: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()