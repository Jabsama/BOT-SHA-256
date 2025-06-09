#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Setup Multi-Bots VoltageGPU
Crée automatiquement plusieurs bots avec configurations séparées
"""

import os
import shutil
import sys

def create_multi_bots(num_bots=3):
    """Crée plusieurs instances de bots"""
    
    print(f"🚀 Création de {num_bots} bots VoltageGPU...")
    
    # Fichiers à copier dans chaque bot
    files_to_copy = [
        'final_optimized_bot.py',
        'multilingual_templates.json',
        'mock_data.json',
        'requirements.txt'
    ]
    
    # Vérifier que les fichiers existent
    missing_files = []
    for file in files_to_copy:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants : {missing_files}")
        return False
    
    # Créer les dossiers et copier les fichiers
    for i in range(1, num_bots + 1):
        bot_dir = f"bot{i}"
        
        print(f"\n📁 Création du {bot_dir}...")
        
        # Créer le dossier
        if not os.path.exists(bot_dir):
            os.makedirs(bot_dir)
            print(f"✅ Dossier {bot_dir} créé")
        
        # Copier les fichiers
        for file in files_to_copy:
            dest_file = os.path.join(bot_dir, file)
            try:
                shutil.copy2(file, dest_file)
                print(f"✅ {file} copié dans {bot_dir}")
            except Exception as e:
                print(f"❌ Erreur copie {file}: {e}")
        
        # Créer le fichier .env template
        env_content = f"""# 🔧 Bot {i} - Configuration VoltageGPU
# Remplacez par vos vraies clés API

# ⚡ VoltageGPU API (Partagée)
VOLTAGE_API_KEY=NAKAMOTO_live_8682a9d8bb97f0bac706532e7b3f0a5f223a260eb2b45b40585b9d92bfbc2704

# 🐦 Twitter Configuration Bot {i}
TWITTER_ENABLED=true
TWITTER_API_KEY=votre_api_key_bot{i}
TWITTER_API_SECRET=votre_api_secret_bot{i}
TWITTER_BEARER_TOKEN=votre_bearer_token_bot{i}
TWITTER_ACCESS_TOKEN=votre_access_token_bot{i}
TWITTER_ACCESS_SECRET=votre_access_secret_bot{i}

# 📱 Telegram Configuration Bot {i}
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=votre_bot_token_{i}
TELEGRAM_CHANNEL_ID=@VoltageGPU{i}

# 🔴 Reddit Configuration Bot {i}
REDDIT_ENABLED=true
REDDIT_CLIENT_ID=votre_client_id_bot{i}
REDDIT_CLIENT_SECRET=votre_client_secret_bot{i}
REDDIT_USERNAME=votre_username_bot{i}
REDDIT_PASSWORD=votre_password_bot{i}

# 💰 Code d'affiliation Bot {i}
AFFILIATE_CODE=SHA-256-VOTRE_CODE_BOT{i}

# 🌍 Langue Bot {i}
DEFAULT_LANGUAGE=en
"""
        
        env_file = os.path.join(bot_dir, '.env')
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print(f"✅ Fichier .env créé pour {bot_dir}")
        except Exception as e:
            print(f"❌ Erreur création .env: {e}")
    
    print(f"\n🎉 {num_bots} bots créés avec succès !")
    return True

def create_launch_script(num_bots=3):
    """Crée un script de lancement pour tous les bots"""
    
    print("\n📝 Création du script de lancement...")
    
    # Script PowerShell
    ps_content = f"""# Script de lancement multi-bots VoltageGPU
Write-Host "🚀 Lancement de {num_bots} bots VoltageGPU..." -ForegroundColor Green

"""
    
    for i in range(1, num_bots + 1):
        ps_content += f"""
# Lancement Bot {i}
if (Test-Path "bot{i}/final_optimized_bot.py") {{
    Set-Location "bot{i}"
    Start-Process python -ArgumentList "final_optimized_bot.py" -WindowStyle Hidden
    Write-Host "✅ Bot {i} lancé" -ForegroundColor Green
    Set-Location ".."
}} else {{
    Write-Host "❌ Bot {i} non trouvé" -ForegroundColor Red
}}
"""
    
    ps_content += f"""
Write-Host "🎉 Tous les bots sont lancés !" -ForegroundColor Green
Write-Host "📊 Vérification des processus..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue

Write-Host "💰 Vos {num_bots} bots génèrent maintenant des revenus 24/7 !" -ForegroundColor Cyan
Read-Host "Appuyez sur Entrée pour continuer"
"""
    
    try:
        with open('launch_all_bots.ps1', 'w', encoding='utf-8') as f:
            f.write(ps_content)
        print("✅ Script PowerShell créé : launch_all_bots.ps1")
    except Exception as e:
        print(f"❌ Erreur création script PS: {e}")
    
    # Script Batch
    bat_content = f"""@echo off
echo 🚀 Lancement de {num_bots} bots VoltageGPU...

"""
    
    for i in range(1, num_bots + 1):
        bat_content += f"""
if exist "bot{i}\\final_optimized_bot.py" (
    cd bot{i}
    start /B python final_optimized_bot.py
    echo ✅ Bot {i} lancé
    cd ..
) else (
    echo ❌ Bot {i} non trouvé
)
"""
    
    bat_content += f"""
echo 🎉 Tous les bots sont lancés !
echo 💰 Vos {num_bots} bots génèrent maintenant des revenus 24/7 !
pause
"""
    
    try:
        with open('launch_all_bots.bat', 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print("✅ Script Batch créé : launch_all_bots.bat")
    except Exception as e:
        print(f"❌ Erreur création script BAT: {e}")

def create_monitoring_script(num_bots=3):
    """Crée un script de monitoring"""
    
    print("\n📊 Création du script de monitoring...")
    
    monitor_content = f"""#!/usr/bin/env python3
# Script de monitoring multi-bots VoltageGPU

import os
import subprocess
import time
from datetime import datetime

def check_bots():
    \"\"\"Vérifie le statut de tous les bots\"\"\"
    
    print("📊 MONITORING MULTI-BOTS VOLTAGEGPU")
    print("=" * 50)
    print(f"🕐 Heure : {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
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
        print(f"❌ Erreur vérification processus: {{e}}")
    
    print()
    
    # Vérifier les logs de chaque bot
    for i in range(1, {num_bots + 1}):
        bot_dir = f"bot{{i}}"
        logs_file = os.path.join(bot_dir, "logs.txt")
        
        print(f"📁 BOT {{i}} STATUS:")
        
        if os.path.exists(logs_file):
            try:
                # Lire les dernières lignes du log
                with open(logs_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        last_lines = lines[-3:] if len(lines) >= 3 else lines
                        for line in last_lines:
                            print(f"   {{line.strip()}}")
                    else:
                        print("   📝 Fichier log vide")
            except Exception as e:
                print(f"   ❌ Erreur lecture log: {{e}}")
        else:
            print("   ❌ Fichier log non trouvé")
        
        print()
    
    # Statistiques globales
    print("📈 STATISTIQUES GLOBALES:")
    print(f"   🤖 Bots configurés : {num_bots}")
    print(f"   📅 Posts/mois estimés : {{105 * {num_bots}}}")
    print(f"   💰 Clics/mois estimés : {{100 * {num_bots}}}+")
    print()

if __name__ == "__main__":
    while True:
        check_bots()
        print("🔄 Actualisation dans 60 secondes... (Ctrl+C pour arrêter)")
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print("\\n🛑 Monitoring arrêté")
            break
"""
    
    try:
        with open('monitor_bots.py', 'w', encoding='utf-8') as f:
            f.write(monitor_content)
        print("✅ Script monitoring créé : monitor_bots.py")
    except Exception as e:
        print(f"❌ Erreur création monitoring: {e}")

def main():
    """Fonction principale"""
    
    print("🤖 SETUP MULTI-BOTS VOLTAGEGPU")
    print("=" * 40)
    
    # Demander le nombre de bots
    try:
        num_bots = int(input("Combien de bots voulez-vous créer ? (défaut: 3) : ") or "3")
        if num_bots < 1 or num_bots > 10:
            print("❌ Nombre de bots invalide (1-10)")
            return
    except ValueError:
        print("❌ Veuillez entrer un nombre valide")
        return
    
    # Créer les bots
    if create_multi_bots(num_bots):
        create_launch_script(num_bots)
        create_monitoring_script(num_bots)
        
        print(f"\\n🎉 SETUP MULTI-BOTS TERMINÉ !")
        print("=" * 40)
        print(f"✅ {num_bots} bots créés")
        print("✅ Scripts de lancement créés")
        print("✅ Script de monitoring créé")
        
        print(f"\\n🚀 PROCHAINES ÉTAPES:")
        print(f"1. Configurez les fichiers .env dans chaque dossier bot1/, bot2/, etc.")
        print(f"2. Lancez tous les bots : .\\launch_all_bots.bat")
        print(f"3. Surveillez l'activité : python monitor_bots.py")
        print(f"4. Profitez de vos revenus multipliés par {num_bots} ! 💰")
    else:
        print("❌ Échec du setup multi-bots")

if __name__ == "__main__":
    main()
