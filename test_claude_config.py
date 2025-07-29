#!/usr/bin/env python3
"""Test de la configuration exacte utilisée par Claude Desktop."""

import asyncio
import subprocess
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def test_claude_desktop_config():
    """Test avec la configuration exacte de Claude Desktop."""
    print("🧪 Test configuration Claude Desktop...")
    
    # Configuration exacte de Claude Desktop
    server_params = StdioServerParameters(
        command="/Users/joel/Dropbox/mcp-wikidata/claude_desktop_launcher.py",
        args=[],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialiser
                await session.initialize()
                print("✅ Session MCP initialisée")
                
                # Lister les outils
                tools = await session.list_tools()
                print(f"✅ {len(tools.tools)} outils disponibles:")
                for tool in tools.tools:
                    print(f"  - {tool.name}")
                
                # Test simple
                result = await session.call_tool(
                    "search_entities",
                    {"query": "Python", "limit": 1}
                )
                print("✅ Test search_entities réussi")
                
                return True
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_claude_desktop_config())
    if success:
        print("\n🎉 Configuration Claude Desktop fonctionne !")
        print("Redémarrez Claude Desktop et le serveur devrait être disponible.")
    else:
        print("\n❌ Problème avec la configuration Claude Desktop")
    sys.exit(0 if success else 1)