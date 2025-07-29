"""Wikidata API client implementation."""

import asyncio
import json
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx

from .config import Config


class WikidataClient:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.session = httpx.AsyncClient(
            headers={"User-Agent": config.user_agent},
            timeout=config.timeout,
        )
        self._rate_limiter = asyncio.Semaphore(config.rate_limit)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.aclose()

    async def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        async with self._rate_limiter:
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def search_entities(
        self, 
        query: str, 
        language: str = "en",
        limit: int = 10,
        type: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {
            "action": "wbsearchentities",
            "search": query,
            "language": language,
            "limit": min(limit, self.config.max_results),
            "format": "json",
        }
        
        if type:
            params["type"] = type

        data = await self._make_request(self.config.wikibase_api_url, params)
        
        entities = []
        for item in data.get("search", []):
            entities.append({
                "id": item.get("id"),
                "label": item.get("label"),
                "description": item.get("description", ""),
                "url": f"https://www.wikidata.org/entity/{item.get('id')}"
            })

        return {"entities": entities}

    async def get_entity(
        self,
        entity_id: str,
        language: str = "en",
        properties: Optional[List[str]] = None,
        simplified: bool = False
    ) -> Dict[str, Any]:
        params = {
            "action": "wbgetentities",
            "ids": entity_id,
            "languages": language,
            "format": "json",
        }

        if properties:
            params["props"] = "|".join(properties)

        data = await self._make_request(self.config.wikibase_api_url, params)
        
        if "entities" not in data or entity_id not in data["entities"]:
            raise ValueError(f"Entity {entity_id} not found")

        entity_data = data["entities"][entity_id]
        
        if simplified:
            return self._simplify_entity(entity_data, language)
        
        return {"entity": entity_data}

    def _simplify_entity(self, entity_data: Dict[str, Any], language: str) -> Dict[str, Any]:
        entity = {
            "id": entity_data.get("id"),
            "labels": {},
            "descriptions": {},
            "properties": {}
        }

        if "labels" in entity_data:
            entity["labels"] = {
                lang: label["value"] 
                for lang, label in entity_data["labels"].items()
            }

        if "descriptions" in entity_data:
            entity["descriptions"] = {
                lang: desc["value"] 
                for lang, desc in entity_data["descriptions"].items()
            }

        if "claims" in entity_data:
            for prop_id, claims in entity_data["claims"].items():
                prop_values = []
                for claim in claims:
                    if "mainsnak" in claim and "datavalue" in claim["mainsnak"]:
                        value = claim["mainsnak"]["datavalue"]["value"]
                        if isinstance(value, dict) and "id" in value:
                            prop_values.append({
                                "value": value["id"],
                                "label": value.get("label", value["id"])
                            })
                        else:
                            prop_values.append({"value": str(value)})
                
                if prop_values:
                    entity["properties"][prop_id] = prop_values

        return {"entity": entity}

    async def sparql_query(
        self,
        query: str,
        format: str = "json",
        limit: int = 100
    ) -> Dict[str, Any]:
        if "LIMIT" not in query.upper():
            query += f" LIMIT {min(limit, 1000)}"

        params = {
            "query": query,
            "format": format
        }

        response = await self.session.get(
            self.config.sparql_endpoint,
            params=params,
            headers={
                "Accept": f"application/sparql-results+{format}",
                "User-Agent": self.config.user_agent
            }
        )
        response.raise_for_status()

        if format == "json":
            return response.json()
        else:
            return {"result": response.text}

    async def get_relations(
        self,
        entity_id: str,
        relation_type: str = "outgoing",
        property_filter: Optional[List[str]] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        if relation_type == "outgoing":
            query = f"""
            SELECT ?property ?propertyLabel ?target ?targetLabel WHERE {{
              wd:{entity_id} ?property ?target .
              ?prop wikibase:directClaim ?property .
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
            }}
            LIMIT {limit}
            """
        elif relation_type == "incoming":
            query = f"""
            SELECT ?property ?propertyLabel ?source ?sourceLabel WHERE {{
              ?source ?property wd:{entity_id} .
              ?prop wikibase:directClaim ?property .
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
            }}
            LIMIT {limit}
            """
        else:
            raise ValueError(f"Invalid relation_type: {relation_type}")

        result = await self.sparql_query(query)
        
        relations = []
        for binding in result.get("results", {}).get("bindings", []):
            relation = {
                "property": binding.get("property", {}).get("value", "").split("/")[-1],
                "property_label": binding.get("propertyLabel", {}).get("value", ""),
                "direction": relation_type
            }
            
            if relation_type == "outgoing":
                relation["target"] = {
                    "id": binding.get("target", {}).get("value", "").split("/")[-1],
                    "label": binding.get("targetLabel", {}).get("value", "")
                }
            else:
                relation["source"] = {
                    "id": binding.get("source", {}).get("value", "").split("/")[-1],
                    "label": binding.get("sourceLabel", {}).get("value", "")
                }
            
            relations.append(relation)

        return {"relations": relations}

    async def find_by_property(
        self,
        property: str,
        value: str,
        language: str = "en",
        limit: int = 10
    ) -> Dict[str, Any]:
        query = f"""
        SELECT ?item ?itemLabel WHERE {{
          ?item wdt:{property} "{value}" .
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{language}" . }}
        }}
        LIMIT {limit}
        """

        result = await self.sparql_query(query)
        
        entities = []
        for binding in result.get("results", {}).get("bindings", []):
            entities.append({
                "id": binding.get("item", {}).get("value", "").split("/")[-1],
                "label": binding.get("itemLabel", {}).get("value", "")
            })

        return {"entities": entities}