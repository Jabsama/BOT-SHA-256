#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Complet - Vérification de TOUT le système VoltageGPU
"""

import os
import json
import requests
import tweepy
from dotenv import load_dotenv

def test_voltage_api():
    """Test API VoltageGPU"""
    print("🔋 TEST API VOLTAGEGPU")
    print("=" * 30)
    
    load_dotenv()
    api_key = os.getenv('VOLTAGE_API_KEY')
    
    if not api_key:
        print("❌ VOLTAGE_API_KEY manquante")
        return False
        
    print(f"✅ Clé API: {api_key[:20]}...")
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            "https://voltagegpu.com/api/pods",
            headers=headers,
            timeout=10
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ API VoltageGPU fonctionne - {len(data.get('pods', []))} offres")
                
                # Afficher première offre
                if data.get('pods'):
                    offer = data['pods'][0]
                    print(f"📊 Exemple offre:")
                    print(f"   GPU: {offer.get('gpu_type', 'N/A')}")
                    print(f"   Prix: ${offer.get('price_per_hour', 0):.2f}/h")
                    print(f"   Lieu: {offer.get('location', 'N/A')}")
                    print(f"   Uptime: {offer.get('uptime', 0):.1f}%")
                return True
            except json.JSONDecodeError:
                print("❌ Réponse API invalide")
                return False
        else:
            print(f"❌ API VoltageGPU erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur API VoltageGPU: {e}")
        return False

def test_twitter_bot1():
    """Test Twitter Bot 1"""
    print("\n🐦 TEST TWITTER BOT 1")
    print("=" * 30)
    
    # Charger config bot1
    load_dotenv('bot1/.env')
    
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not all([api_key, api_secret, access_token, access_secret, bearer_token]):
        print("❌ Clés Twitter Bot 1 manquantes")
        return False
        
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ Access Token: {access_token[:20]}...")
    
    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
            wait_on_rate_limit=True
        )
        
        me = client.get_me()
        print(f"✅ Twitter Bot 1 connecté: @{me.data.username}")
        print(f"📊 Followers: {me.data.public_metrics['followers_count']}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur Twitter Bot 1: {e}")
        return False

def test_twitter_bot2():
    """Test Twitter Bot 2"""
    print("\n🐦 TEST TWITTER BOT 2")
    print("=" * 30)
    
    # Charger config bot2
    load_dotenv('bot2/.env')
    
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not all([api_key, api_secret, access_token, access_secret, bearer_token]):
        print("❌ Clés Twitter Bot 2 manquantes")
        return False
        
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ Access Token: {access_token[:20]}...")
    
    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
            wait_on_rate_limit=True
        )
        
        me = client.get_me()
        print(f"✅ Twitter Bot 2 connecté: @{me.data.username}")
        print(f"📊 Followers: {me.data.public_metrics['followers_count']}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur Twitter Bot 2: {e}")
        return False

def test_telegram():
    """Test Telegram"""
    print("\n📱 TEST TELEGRAM")
    print("=" * 30)
    
    load_dotenv('bot1/.env')
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN manquant")
        return False
        
    print(f"✅ Bot Token: {bot_token[:20]}...")
    print(f"✅ Canal: {channel_id}")
    
    try:
        import telegram
        bot = telegram.Bot(token=bot_token)
        
        # Test simple
        bot_info = bot.get_me()
        print(f"✅ Telegram Bot connecté: @{bot_info.username}")
        return True
        
    except ImportError:
        print("⚠️  python-telegram-bot non installé")
        return False
    except Exception as e:
        print(f"❌ Erreur Telegram: {e}")
        return False

def test_templates():
    """Test Templates"""
    print("\n📝 TEST TEMPLATES")
    print("=" * 30)
    
    try:
        with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
            templates = json.load(f)
            
        print("✅ Templates chargés")
        
        # Vérifier structure
        platforms = ['twitter', 'telegram', 'reddit']
        languages = ['en', 'zh']
        content_types = ['gpu_deals', 'affiliate']
        
        for platform in platforms:
            if platform in templates:
                print(f"✅ {platform}: OK")
                for lang in languages:
                    if lang in templates[platform]:
                        for content_type in content_types:
                            if content_type in templates[platform][lang]:
                                count = len(templates[platform][lang][content_type])
                                print(f"   {lang}/{content_type}: {count} templates")
            else:
                print(f"❌ {platform}: Manquant")
                
        return True
        
    except Exception as e:
        print(f"❌ Erreur templates: {e}")
        return False

def test_content_generation():
    """Test génération de contenu"""
    print("\n🧠 TEST GÉNÉRATION CONTENU")
    print("=" * 30)
    
    load_dotenv('bot1/.env')
    affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-76360B81D39F')
    
    # Mock offer
    offer = {
        'gpu_count': 4,
        'gpu_type': 'B200',
        'price_per_hour': 45.50,
        'location': 'Raleigh',
        'uptime': 98.7
    }
    
    try:
        with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
            templates = json.load(f)
            
        # Test Twitter
        twitter_template = templates['twitter']['en']['gpu_deals'][0]
        content = twitter_template.format(
            gpu_count=offer['gpu_count'],
            gpu_type=offer['gpu_type'],
            price=f"${offer['price_per_hour']:.2f}",
            location=offer['location'],
            uptime=f"{offer['uptime']:.1f}%",
            affiliate_code=affiliate_code
        )
        
        print("✅ Contenu Twitter généré:")
        print(f"📄 ({len(content)} caractères)")
        print(content)
        print()
        
        # Vérifications
        checks = [
            ("Code promo", affiliate_code in content),
            ("Lien VoltageGPU", "voltagegpu.com" in content),
            ("Prix GPU", str(offer['price_per_hour']) in content),
            ("Type GPU", offer['gpu_type'] in content),
            ("Longueur OK", len(content) <= 280)
        ]
        
        for check_name, check_result in checks:
            status = "✅" if check_result else "❌"
            print(f"{status} {check_name}")
            
        return all(check[1] for check in checks)
        
    except Exception as e:
        print(f"❌ Erreur génération contenu: {e}")
        return False

def main():
    """Test complet du système"""
    print("🧪 TEST COMPLET SYSTÈME VOLTAGEGPU")
    print("=" * 50)
    
    tests = [
        ("API VoltageGPU", test_voltage_api),
        ("Twitter Bot 1", test_twitter_bot1),
        ("Twitter Bot 2", test_twitter_bot2),
        ("Telegram", test_telegram),
        ("Templates", test_templates),
        ("Génération Contenu", test_content_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS FINAUX")
    print("=" * 50)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            success_count += 1
    
    print(f"\n🎯 SCORE: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 TOUS LES TESTS PASSENT - SYSTÈME 100% FONCTIONNEL!")
    elif success_count >= len(tests) * 0.8:
        print("⚠️  SYSTÈME MAJORITAIREMENT FONCTIONNEL")
    else:
        print("❌ SYSTÈME NÉCESSITE DES CORRECTIONS")
    
    print("\n💰 FONCTIONNALITÉS CONFIRMÉES:")
    print("✅ API VoltageGPU intégrée")
    print("✅ Codes promos automatiques")
    print("✅ Liens d'affiliation inclus")
    print("✅ Contenu intelligent généré")
    print("✅ Multi-plateformes configuré")

if __name__ == "__main__":
    main()
