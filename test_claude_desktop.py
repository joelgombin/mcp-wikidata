#!/usr/bin/env python3
"""Test pour reproduire l'environnement Claude Desktop."""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

async def test_claude_desktop_env():
    """Teste le serveur dans les mêmes conditions que Claude Desktop."""
    print("🔍 Test de l'environnement Claude Desktop...")
    
    # Changer vers le bon répertoire
    os.chdir("/Users/joel/Dropbox/mcp-wikidata")
    print(f"📂 Répertoire courant: {os.getcwd()}")
    
    # Tester la commande exacte de Claude Desktop
    cmd = ["uv", "run", "mcp-wikidata"]
    print(f"🚀 Commande: {' '.join(cmd)}")
    
    try:
        # Créer un processus avec stdin/stdout pipes comme Claude Desktop
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/joel/Dropbox/mcp-wikidata"
        )
        
        print("✅ Processus lancé avec succès")
        
        # Tenter de parler MCP (message d'initialisation basique)
        init_message = '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n'
        
        try:
            process.stdin.write(init_message)
            process.stdin.flush()
            print("📤 Message d'initialisation envoyé")
            
            # Attendre une réponse (timeout 5s)
            import select
            import time
            
            start_time = time.time()
            while time.time() - start_time < 5:
                if process.poll() is not None:
                    print(f"❌ Processus terminé avec code: {process.returncode}")
                    break
                    
                # Vérifier s'il y a une sortie
                ready, _, _ = select.select([process.stdout], [], [], 0.1)
                if ready:
                    output = process.stdout.readline()
                    if output:
                        print(f"📥 Réponse: {output.strip()}")
                        print("✅ Le serveur répond correctement!")
                        break
            else:
                print("⏰ Timeout - pas de réponse du serveur")
                
        except Exception as e:
            print(f"❌ Erreur lors de la communication: {e}")
            
        finally:
            process.terminate()
            process.wait()
            stderr = process.stderr.read()
            if stderr:
                print(f"❌ Erreurs stderr: {stderr}")
                
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_claude_desktop_env())