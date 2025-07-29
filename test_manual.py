#!/usr/bin/env python3
"""Script de test manuel pour MCP Wikidata."""

import asyncio
import json
from mcp_wikidata.config import Config
from mcp_wikidata.wikidata_client import WikidataClient


async def test_search():
    """Test de recherche d'entités."""
    print("=== Test search_entities ===")
    config = Config.from_env()
    client = WikidataClient(config)
    
    try:
        result = await client.search_entities("Douglas Adams", limit=3)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        await client.session.aclose()


async def test_get_entity():
    """Test de récupération d'entité."""
    print("\n=== Test get_entity ===")
    config = Config.from_env()
    client = WikidataClient(config)
    
    try:
        result = await client.get_entity("Q42", simplified=True)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        await client.session.aclose()


async def test_sparql():
    """Test de requête SPARQL."""
    print("\n=== Test SPARQL ===")
    config = Config.from_env()
    client = WikidataClient(config)
    
    query = """
    SELECT ?item ?itemLabel WHERE {
      ?item wdt:P31 wd:Q5 .
      ?item wdt:P106 wd:Q36180 .
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
    }
    LIMIT 5
    """
    
    try:
        result = await client.sparql_query(query)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        await client.session.aclose()


async def main():
    """Lance tous les tests."""
    await test_search()
    await test_get_entity()
    await test_sparql()


if __name__ == "__main__":
    asyncio.run(main())