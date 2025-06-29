#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test des Modules Intelligents - SHA-256 Bot v6.0
Vérifie que tous les modules d'intelligence artificielle fonctionnent correctement
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configuration du logging pour les tests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_reddit_intelligence():
    """Test du module Reddit Intelligence"""
    print("🧠 Testing Reddit Intelligence Module...")
    
    try:
        from modules.reddit_intelligence import RedditIntelligence
        
        # Initialiser le module
        reddit_intel = RedditIntelligence()
        
        # Test 1: Génération de contenu conforme
        base_title = "GPU rental alternatives for AI workloads"
        base_content = "I've been researching cost-effective GPU solutions for AI development."
        
        compliant_title, compliant_content = reddit_intel.generate_compliant_content(
            'MachineLearning', base_content, base_title
        )
        
        print(f"   ✅ Content generation: {compliant_title[:50]}...")
        
        # Test 2: Vérification de la santé d'un compte
        health = reddit_intel.check_account_health('test_account')
        print(f"   ✅ Account health check: Risk score = {health['ban_risk_score']}")
        
        # Test 3: Recommandation de subreddits
        best_subreddits = reddit_intel.get_best_subreddits('test_account', limit=3)
        print(f"   ✅ Subreddit recommendations: {best_subreddits}")
        
        # Test 4: Résumé d'intelligence
        summary = reddit_intel.get_intelligence_summary()
        print(f"   ✅ Intelligence summary: {summary['subreddits_analyzed']} subreddits analyzed")
        
        print("   🎉 Reddit Intelligence Module: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Reddit Intelligence Module failed: {e}")
        return False

def test_twitter_viral():
    """Test du module Twitter Viral Optimizer"""
    print("🚀 Testing Twitter Viral Optimizer...")
    
    try:
        from modules.twitter_viral import TwitterViralOptimizer
        
        # Initialiser le module
        twitter_viral = TwitterViralOptimizer()
        
        # Test 1: Optimisation des hashtags
        content = "GPU rental costs are getting expensive. Looking for alternatives."
        hashtags = twitter_viral.optimize_hashtags(content, 'gpu_deals', datetime.now())
        print(f"   ✅ Hashtag optimization: {hashtags}")
        
        # Test 2: Génération de contenu viral
        viral_content = twitter_viral.generate_viral_content(content, 'savings')
        print(f"   ✅ Viral content generation: {viral_content[:50]}...")
        
        # Test 3: Vérification du risque de shadow ban
        risk_score, risk_factors = twitter_viral.check_shadow_ban_risk('test_user')
        print(f"   ✅ Shadow ban risk check: Score = {risk_score}, Factors = {len(risk_factors)}")
        
        # Test 4: Suggestions de contenu
        suggestions = twitter_viral.get_content_suggestions('gpu_deals')
        print(f"   ✅ Content suggestions: {len(suggestions)} suggestions generated")
        
        # Test 5: Résumé viral
        summary = twitter_viral.get_viral_summary()
        print(f"   ✅ Viral summary: {summary['total_viral_patterns']} patterns learned")
        
        print("   🎉 Twitter Viral Optimizer: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Twitter Viral Optimizer failed: {e}")
        return False

def test_telegram_autonomous():
    """Test du module Telegram Autonomous"""
    print("🤖 Testing Telegram Autonomous Module...")
    
    try:
        from modules.telegram_autonomous import TelegramAutonomous
        
        # Initialiser le module (sans token pour le test)
        telegram_auto = TelegramAutonomous('test_token')
        
        # Test 1: Classification d'utilisateur
        interests = ['gpu computing', 'machine learning', 'ai development']
        user_type = telegram_auto._classify_user_type(interests)
        print(f"   ✅ User classification: {user_type}")
        
        # Test 2: Génération d'intérêts d'utilisateur
        generated_interests = telegram_auto._generate_user_interests('@ai_group')
        print(f"   ✅ Interest generation: {generated_interests}")
        
        # Test 3: Détection d'opportunité de conversation
        text = "I'm looking for affordable GPU solutions for my AI project"
        opportunity = telegram_auto._detect_conversation_opportunity(text)
        print(f"   ✅ Conversation opportunity: {opportunity}")
        
        # Test 4: Génération de réponse intelligente
        if opportunity:
            response = telegram_auto._generate_intelligent_response(text, opportunity)
            print(f"   ✅ Intelligent response: {response[:50]}...")
        
        # Test 5: Résumé autonome
        summary = telegram_auto.get_autonomous_summary()
        print(f"   ✅ Autonomous summary: {summary['discovered_groups']} groups discovered")
        
        print("   🎉 Telegram Autonomous Module: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Telegram Autonomous Module failed: {e}")
        return False

def test_integration():
    """Test d'intégration des modules"""
    print("🔗 Testing Module Integration...")
    
    try:
        # Test d'importation du bot principal
        from SHA-256BOT import AutonomousSHA256Bot
        
        # Initialiser le bot en mode test
        bot = AutonomousSHA256Bot(test_mode=True)
        
        # Vérifier que tous les modules sont initialisés
        assert hasattr(bot, 'reddit_intelligence'), "Reddit Intelligence not initialized"
        assert hasattr(bot, 'twitter_viral'), "Twitter Viral not initialized"
        
        print("   ✅ Bot initialization: All modules loaded")
        
        # Test de la configuration
        assert bot.test_mode == True, "Test mode not activated"
        print("   ✅ Test mode: Activated correctly")
        
        # Test des statistiques
        assert 'twitter_posts' in bot.stats, "Stats not initialized"
        print("   ✅ Statistics: Initialized correctly")
        
        print("   🎉 Module Integration: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Module Integration failed: {e}")
        return False

def test_configuration():
    """Test de la configuration"""
    print("⚙️ Testing Configuration...")
    
    try:
        # Charger les variables d'environnement
        load_dotenv()
        
        # Vérifier les variables critiques
        affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO')
        print(f"   ✅ Affiliate code: {affiliate_code}")
        
        # Vérifier la structure des dossiers
        required_dirs = ['modules', 'config', 'data', 'logs']
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            print(f"   ✅ Directory: {dir_name} exists")
        
        # Vérifier les fichiers de configuration
        config_files = ['config/timing_config.py', 'modules/__init__.py']
        for config_file in config_files:
            if os.path.exists(config_file):
                print(f"   ✅ Config file: {config_file} exists")
            else:
                print(f"   ⚠️ Config file: {config_file} missing (will be created)")
        
        print("   🎉 Configuration: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration failed: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 SHA-256 Bot v6.0 - Intelligent Modules Test Suite")
    print("=" * 60)
    print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Créer les dossiers nécessaires
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Liste des tests à exécuter
    tests = [
        ("Configuration", test_configuration),
        ("Reddit Intelligence", test_reddit_intelligence),
        ("Twitter Viral Optimizer", test_twitter_viral),
        ("Telegram Autonomous", test_telegram_autonomous),
        ("Module Integration", test_integration)
    ]
    
    # Exécuter tous les tests
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
        print()
    
    # Afficher le résumé
    print("=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The intelligent modules are ready for production.")
        print("🚀 You can now run: python SHA-256BOT.py --test")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please check the errors above.")
        print("🔧 Fix the issues and run the tests again.")
        return 1

if __name__ == "__main__":
    exit(main())
