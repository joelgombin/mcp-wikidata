#!/usr/bin/env python3
"""Test client MCP pour vérifier le serveur."""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def test_mcp_server():
    """Test le serveur MCP avec un vrai client."""
    print("🚀 Démarrage du test MCP client...")
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "mcp-wikidata"],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialiser la session
                await session.initialize()
                print("✅ Session MCP initialisée")
                
                # Lister les outils disponibles
                tools = await session.list_tools()
                print(f"✅ {len(tools.tools)} outils disponibles:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test search_entities
                print("\n🔍 Test search_entities...")
                result = await session.call_tool(
                    "search_entities",
                    {"query": "Einstein", "limit": 2}
                )
                print("✅ search_entities:", result.content[0].text[:100] + "...")
                
                # Test get_entity
                print("\n📖 Test get_entity...")
                result = await session.call_tool(
                    "get_entity",
                    {"entity_id": "Q937", "simplified": True}
                )
                print("✅ get_entity:", result.content[0].text[:100] + "...")
                
                print("\n🎉 Tous les tests sont passés !")
                return True
                
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)