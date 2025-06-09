#!/usr/bin/env python3
# Script de monitoring multi-bots VoltageGPU

import os
import subprocess
import time
from datetime import datetime

def check_bots():
    """Vérifie le statut de tous les bots"""
    
    print("📊 MONITORING MULTI-BOTS VOLTAGEGPU")
    print("=" * 50)
    print(f"🕐 Heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Vérifier les processus Python
    try:
        result = subprocess.run(['powershell', 'Get-Process python -ErrorAction SilentlyContinue'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("🤖 PROCESSUS PYTHON ACTIFS:")
            print(result.stdout)
        else:
            print("❌ Aucun processus Python trouvé")
    except Exception as e:
        print(f"❌ Erreur vérification processus: {e}")
    
    print()
    
    # Vérifier les logs de chaque bot
    for i in range(1, 4):
        bot_dir = f"bot{i}"
        logs_file = os.path.join(bot_dir, "logs.txt")
        
        print(f"📁 BOT {i} STATUS:")
        
        if os.path.exists(logs_file):
            try:
                # Lire les dernières lignes du log
                with open(logs_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        last_lines = lines[-3:] if len(lines) >= 3 else lines
                        for line in last_lines:
                            print(f"   {line.strip()}")
                    else:
                        print("   📝 Fichier log vide")
            except Exception as e:
                print(f"   ❌ Erreur lecture log: {e}")
        else:
            print("   ❌ Fichier log non trouvé")
        
        print()
    
    # Statistiques globales
    print("📈 STATISTIQUES GLOBALES:")
    print(f"   🤖 Bots configurés : 3")
    print(f"   📅 Posts/mois estimés : {105 * 3}")
    print(f"   💰 Clics/mois estimés : {100 * 3}+")
    print()

if __name__ == "__main__":
    while True:
        check_bots()
        print("🔄 Actualisation dans 60 secondes... (Ctrl+C pour arrêter)")
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring arrêté")
            break
