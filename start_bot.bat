@echo off
title VoltageGPU Bot - Dropshipping GPU Automation
color 0A

echo.
echo ========================================================
echo 🚀 VOLTAGEGPU BOT - DROPSHIPPING GPU AUTOMATION
echo ========================================================
echo 💰 Projet Dropshipping GPU via CeliumCompute
echo 📈 Marge de 25%% sur les prix CeliumCompute
echo 🌍 Ciblage global : US, EU, CN, IN, BR
echo 🤖 IA autonome avec apprentissage automatique
echo ========================================================
echo.

:MENU
echo 🎯 MENU PRINCIPAL:
echo 1. 🔧 Tester la configuration
echo 2. 🧪 Mode test (sans posts réels)
echo 3. 🚀 Lancer le bot en mode production
echo 4. 📊 Voir le statut des APIs
echo 5. 📖 Ouvrir la documentation
echo 6. 🛑 Quitter
echo.

set /p choice="👉 Votre choix (1-6): "

if "%choice%"=="1" goto TEST_CONFIG
if "%choice%"=="2" goto TEST_MODE
if "%choice%"=="3" goto PRODUCTION_MODE
if "%choice%"=="4" goto API_STATUS
if "%choice%"=="5" goto DOCUMENTATION
if "%choice%"=="6" goto EXIT
echo ❌ Choix invalide. Veuillez choisir entre 1 et 6.
goto MENU

:TEST_CONFIG
echo.
echo 🔧 LANCEMENT DU TEST DE CONFIGURATION...
python test_config.py
pause
goto MENU

:TEST_MODE
echo.
echo 🧪 LANCEMENT DU BOT EN MODE TEST...
echo ⚠️  Aucun post réel ne sera effectué
python SHA-256BOT.py --test
pause
goto MENU

:PRODUCTION_MODE
echo.
echo 🚀 LANCEMENT DU BOT EN MODE PRODUCTION...
echo ⚠️  ATTENTION: Le bot va poster sur les réseaux sociaux!
echo.
set /p confirm="Êtes-vous sûr de vouloir continuer? (oui/non): "
if /i "%confirm%"=="oui" goto RUN_PRODUCTION
if /i "%confirm%"=="o" goto RUN_PRODUCTION
if /i "%confirm%"=="yes" goto RUN_PRODUCTION
if /i "%confirm%"=="y" goto RUN_PRODUCTION
echo 🛑 Lancement annulé
pause
goto MENU

:RUN_PRODUCTION
python SHA-256BOT.py
pause
goto MENU

:API_STATUS
echo.
echo 📊 STATUT RAPIDE DES APIs:
echo ------------------------------
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('💰 Code d\'affiliation:', '✅' if os.getenv('AFFILIATE_CODE') else '❌')
print('⚡ VoltageGPU API:', '✅' if os.getenv('VOLTAGE_API_KEY') else '❌')
print('🐦 Twitter Compte 1:', '✅' if os.getenv('TWITTER_API_KEY') else '❌')
print('🐦 Twitter Compte 2:', '✅' if os.getenv('TWITTER_API_KEY_2') else '❌')
print('💬 Telegram Bot:', '✅' if os.getenv('TELEGRAM_BOT_TOKEN') else '❌')
print('📍 Reddit Compte 1:', '✅' if os.getenv('REDDIT_CLIENT_ID') else '❌')
print('📍 Reddit Compte 2:', '✅' if os.getenv('REDDIT_CLIENT_ID_2') else '❌')
if os.getenv('AFFILIATE_CODE'):
    print('\n💰 Votre lien d\'affiliation:')
    print(f'https://voltagegpu.com/?ref={os.getenv(\"AFFILIATE_CODE\")}')
"
pause
goto MENU

:DOCUMENTATION
echo.
echo 📖 Ouverture de la documentation...
start README_CONFIGURATION.md
goto MENU

:EXIT
echo.
echo 👋 Au revoir!
echo 💰 N'oubliez pas votre lien d'affiliation: https://voltagegpu.com/?ref=SHA-256-76360B81D39F
pause
exit

:ERROR
echo ❌ Une erreur s'est produite.
pause
goto MENU
