#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VoltageGPU Bot Launcher
Simple launcher with menu options
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def display_banner():
    """Display bot banner"""
    print("🚀 VOLTAGEGPU BOT - DROPSHIPPING GPU AUTOMATION")
    print("=" * 55)
    print("💰 Projet Dropshipping GPU via CeliumCompute")
    print("📈 Marge de 25% sur les prix CeliumCompute")
    print("🌍 Ciblage global : US, EU, CN, IN, BR")
    print("🤖 IA autonome avec apprentissage automatique")
    print("=" * 55)

def display_menu():
    """Display main menu"""
    print("\n🎯 MENU PRINCIPAL:")
    print("1. 🔧 Tester la configuration")
    print("2. 🧪 Mode test (sans posts réels)")
    print("3. 🚀 Lancer le bot en mode production")
    print("4. 📊 Voir le statut des APIs")
    print("5. 🛑 Quitter")

def test_configuration():
    """Run configuration test"""
    print("\n🔧 LANCEMENT DU TEST DE CONFIGURATION...")
    try:
        result = subprocess.run([sys.executable, "test_config.py"], 
                              capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def run_test_mode():
    """Run bot in test mode"""
    print("\n🧪 LANCEMENT DU BOT EN MODE TEST...")
    print("⚠️  Aucun post réel ne sera effectué")
    try:
        subprocess.run([sys.executable, "SHA-256BOT.py", "--test"])
    except KeyboardInterrupt:
        print("\n🛑 Test arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def run_production_mode():
    """Run bot in production mode"""
    print("\n🚀 LANCEMENT DU BOT EN MODE PRODUCTION...")
    print("⚠️  ATTENTION: Le bot va poster sur les réseaux sociaux!")
    
    confirm = input("Êtes-vous sûr de vouloir continuer? (oui/non): ").lower()
    if confirm in ['oui', 'o', 'yes', 'y']:
        try:
            subprocess.run([sys.executable, "SHA-256BOT.py"])
        except KeyboardInterrupt:
            print("\n🛑 Bot arrêté par l'utilisateur")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print("🛑 Lancement annulé")

def show_api_status():
    """Show quick API status"""
    load_dotenv()
    
    print("\n📊 STATUT RAPIDE DES APIs:")
    print("-" * 30)
    
    # Check environment variables
    affiliate_code = os.getenv('AFFILIATE_CODE')
    voltage_api = os.getenv('VOLTAGE_API_KEY')
    twitter_api = os.getenv('TWITTER_API_KEY')
    twitter_api_2 = os.getenv('TWITTER_API_KEY_2')
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    reddit_client = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_2 = os.getenv('REDDIT_CLIENT_ID_2')
    
    print(f"💰 Code d'affiliation: {'✅' if affiliate_code else '❌'}")
    print(f"⚡ VoltageGPU API: {'✅' if voltage_api else '❌'}")
    print(f"🐦 Twitter Compte 1: {'✅' if twitter_api else '❌'}")
    print(f"🐦 Twitter Compte 2: {'✅' if twitter_api_2 else '❌'}")
    print(f"💬 Telegram Bot: {'✅' if telegram_token else '❌'}")
    print(f"📍 Reddit Compte 1: {'✅' if reddit_client else '❌'}")
    print(f"📍 Reddit Compte 2: {'✅' if reddit_client_2 else '❌'}")
    
    if affiliate_code:
        print(f"\n💰 Votre lien d'affiliation:")
        print(f"https://voltagegpu.com/?ref={affiliate_code}")

def main():
    """Main launcher function"""
    display_banner()
    
    while True:
        display_menu()
        
        try:
            choice = input("\n👉 Votre choix (1-5): ").strip()
            
            if choice == '1':
                test_configuration()
            elif choice == '2':
                run_test_mode()
            elif choice == '3':
                run_production_mode()
            elif choice == '4':
                show_api_status()
            elif choice == '5':
                print("\n👋 Au revoir!")
                break
            else:
                print("❌ Choix invalide. Veuillez choisir entre 1 et 5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        input("\n📱 Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
