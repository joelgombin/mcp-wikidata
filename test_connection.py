#!/usr/bin/env python3
"""Test de connexion MCP simple."""

import asyncio
import sys
from mcp_wikidata.server import WikidataServer
from mcp_wikidata.config import Config


async def test_server_init():
    """Test que le serveur s'initialise correctement."""
    try:
        config = Config.from_env()
        server = WikidataServer(config)
        print("✅ Serveur initialisé avec succès")
        
        # Test des définitions d'outils
        tools = server.tools.get_tool_definitions()
        print(f"✅ {len(tools)} outils définis:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_server_init())
    sys.exit(0 if success else 1)