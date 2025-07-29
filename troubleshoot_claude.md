# Diagnostic Claude Desktop - MCP Wikidata

## 🔍 Problème
Claude Desktop affiche "server disconnected" pour mcp-wikidata

## ✅ Tests réussis
1. **Serveur fonctionne** : `uv run mcp-wikidata` démarre sans erreur
2. **MCP client** : Test client réussi avec tous les outils
3. **MCP Inspector** : Fonctionne parfaitement
4. **Configuration** : claude_desktop_config.json est correcte

## 🛠️ Solutions à essayer

### 1. Redémarrer Claude Desktop
- Quitter complètement Claude Desktop
- Relancer l'application
- Les changements de configuration nécessitent un redémarrage

### 2. Vérifier la configuration finale
```json
{
  "mcpServers": {
    "mcp-wikidata": {
      "command": "uv",
      "args": ["run", "mcp-wikidata"],
      "cwd": "/Users/joel/Dropbox/mcp-wikidata",
      "env": {
        "WIKIDATA_USER_AGENT": "Claude-Desktop-MCP-Wikidata/0.1.0"
      }
    }
  }
}
```

### 3. Test manuel de la commande
```bash
cd "/Users/joel/Dropbox/mcp-wikidata"
uv run mcp-wikidata
# Doit démarrer sans erreur et attendre l'input
```

### 4. Alternative avec chemin absolu
Si le problème persiste, essayer avec le chemin absolu :
```json
{
  "command": "/Users/joel/.local/bin/uv",
  "args": ["run", "mcp-wikidata"],
  "cwd": "/Users/joel/Dropbox/mcp-wikidata"
}
```

### 5. Mode debug
Pour plus de logs, ajouter :
```json
{
  "args": ["run", "mcp-wikidata", "--log-level", "DEBUG"]
}
```

## 📝 Étapes de diagnostic
1. ✅ Serveur se lance correctement
2. ✅ Outils MCP définis (5 outils)
3. ✅ Réponse JSON-RPC correcte
4. ✅ Configuration JSON valide
5. 🔄 **À tester** : Redémarrage Claude Desktop

## 🎯 Prochaine étape
**Redémarrer Claude Desktop** puis tester à nouveau.