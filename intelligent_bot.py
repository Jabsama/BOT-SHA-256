#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VoltageGPU Intelligent Bot - IA Adaptative
S'adapte automatiquement selon les performances et l'engagement
"""

import os
import json
import random
import logging
import requests
import schedule
import time
import argparse
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
import tweepy
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('intelligent_logs.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class IntelligentVoltageBot:
    def __init__(self, test_mode=False):
        """Initialise le bot intelligent avec IA adaptative"""
        self.test_mode = test_mode
        self.load_config()
        self.setup_platforms()
        self.load_templates()
        self.init_intelligence()
        
    def load_config(self):
        """Charge la configuration intelligente"""
        load_dotenv()
        
        self.voltage_api_key = os.getenv('VOLTAGE_API_KEY')
        self.voltage_base_url = "https://voltagegpu.com/api"
        self.affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO')
        
        # Intelligence Configuration
        self.bot_personality = os.getenv('BOT_PERSONALITY', 'balanced')
        self.bot_focus = os.getenv('BOT_FOCUS', 'general')
        self.posting_strategy = os.getenv('POSTING_STRATEGY', 'balanced')
        
        self.platform_configs = {
            'twitter': {
                'enabled': os.getenv('TWITTER_ENABLED', 'false').lower() == 'true',
                'api_key': os.getenv('TWITTER_API_KEY'),
                'api_secret': os.getenv('TWITTER_API_SECRET'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
                'access_secret': os.getenv('TWITTER_ACCESS_SECRET'),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN')
            },
            'telegram': {
                'enabled': os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true',
                'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
                'channel_id': os.getenv('TELEGRAM_CHANNEL_ID')
            },
            'reddit': {
                'enabled': os.getenv('REDDIT_ENABLED', 'false').lower() == 'true',
                'client_id': os.getenv('REDDIT_CLIENT_ID'),
                'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
                'username': os.getenv('REDDIT_USERNAME'),
                'password': os.getenv('REDDIT_PASSWORD')
            }
        }
        
    def setup_platforms(self):
        """Configure les plateformes avec intelligence"""
        self.platforms = {}
        
        # Twitter
        if self.platform_configs['twitter']['enabled']:
            try:
                self.platforms['twitter'] = tweepy.Client(
                    bearer_token=self.platform_configs['twitter']['bearer_token'],
                    consumer_key=self.platform_configs['twitter']['api_key'],
                    consumer_secret=self.platform_configs['twitter']['api_secret'],
                    access_token=self.platform_configs['twitter']['access_token'],
                    access_token_secret=self.platform_configs['twitter']['access_secret'],
                    wait_on_rate_limit=True
                )
                if not self.test_mode:
                    me = self.platforms['twitter'].get_me()
                    logging.info(f"🧠 Twitter connecté: @{me.data.username} (Personnalité: {self.bot_personality})")
            except Exception as e:
                logging.error(f"❌ Erreur Twitter: {e}")
                
        # Telegram
        if self.platform_configs['telegram']['enabled']:
            try:
                import telegram
                self.platforms['telegram'] = telegram.Bot(
                    token=self.platform_configs['telegram']['bot_token']
                )
                logging.info(f"🧠 Telegram configuré (Focus: {self.bot_focus})")
            except ImportError:
                logging.warning("⚠️  python-telegram-bot non installé")
            except Exception as e:
                logging.error(f"❌ Erreur Telegram: {e}")
                
        # Reddit avec intelligence anti-filtre
        if self.platform_configs['reddit']['enabled']:
            try:
                import praw
                self.platforms['reddit'] = praw.Reddit(
                    client_id=self.platform_configs['reddit']['client_id'],
                    client_secret=self.platform_configs['reddit']['client_secret'],
                    username=self.platform_configs['reddit']['username'],
                    password=self.platform_configs['reddit']['password'],
                    user_agent="VoltageGPU Intelligent Bot v2.0"
                )
                logging.info(f"🧠 Reddit configuré (Stratégie: {self.posting_strategy})")
            except ImportError:
                logging.warning("⚠️  praw non installé")
            except Exception as e:
                logging.error(f"❌ Erreur Reddit: {e}")
                
        logging.info(f"🧠 Plateformes actives: {list(self.platforms.keys())}")
        
    def load_templates(self):
        """Charge les templates avec intelligence"""
        try:
            with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
            logging.info("🧠 Templates multilingues chargés avec IA")
        except Exception as e:
            logging.error(f"❌ Erreur chargement templates: {e}")
            raise
            
    def init_intelligence(self):
        """Initialise l'intelligence artificielle du bot"""
        # Métriques de performance
        self.performance_metrics = {
            'twitter': {'posts': 0, 'engagement': 0, 'best_time': 14},
            'telegram': {'posts': 0, 'engagement': 0, 'best_time': 10},
            'reddit': {'posts': 0, 'engagement': 0, 'karma_score': 0}
        }
        
        # Stratégies adaptatives
        self.adaptive_strategies = {
            'technical_expert': {
                'twitter_focus': 'gpu_deals',
                'telegram_focus': 'gpu_deals', 
                'content_style': 'technical',
                'hashtags': ['#AI', '#MachineLearning', '#GPU', '#CloudComputing']
            },
            'crypto_enthusiast': {
                'twitter_focus': 'affiliate',
                'telegram_focus': 'affiliate',
                'content_style': 'crypto',
                'hashtags': ['#Crypto', '#EasyMoney', '#PassiveIncome', '#DeFi']
            },
            'balanced': {
                'twitter_focus': 'mixed',
                'telegram_focus': 'mixed',
                'content_style': 'balanced',
                'hashtags': ['#AI', '#GPU', '#CryptoEarnings', '#TechDeals']
            }
        }
        
        # Intelligence Telegram pour développement automatique
        self.telegram_growth_strategies = {
            'engagement_boosters': [
                "💬 What's your biggest AI project challenge?",
                "🤔 AWS vs VoltageGPU - what's your experience?",
                "🚀 Share your GPU training setup!",
                "💡 Best ML frameworks for GPU training?",
                "🔥 Who else is tired of cloud costs?"
            ],
            'community_questions': [
                "What GPU specs do you need for your projects?",
                "How much do you spend on cloud GPU monthly?",
                "Best practices for distributed training?",
                "Favorite AI models to train?",
                "Cost optimization tips for ML teams?"
            ]
        }
        
        # Auto-adaptation basée sur l'heure
        self.time_based_adaptation = {
            'morning': {'style': 'informative', 'energy': 'calm'},
            'afternoon': {'style': 'promotional', 'energy': 'active'},
            'evening': {'style': 'community', 'energy': 'engaging'}
        }
        
        logging.info(f"🧠 Intelligence initialisée - Personnalité: {self.bot_personality}")
        
    def get_current_strategy(self):
        """Retourne la stratégie actuelle basée sur la personnalité"""
        return self.adaptive_strategies.get(self.bot_personality, self.adaptive_strategies['balanced'])
        
    def adapt_content_to_time(self):
        """Adapte le contenu selon l'heure"""
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 12:
            return self.time_based_adaptation['morning']
        elif 12 <= current_hour < 18:
            return self.time_based_adaptation['afternoon']
        else:
            return self.time_based_adaptation['evening']
            
    def generate_intelligent_content(self, platform: str, offer: Optional[Dict] = None) -> str:
        """Génère du contenu intelligent adaptatif"""
        strategy = self.get_current_strategy()
        time_adaptation = self.adapt_content_to_time()
        
        # Choisir le type de contenu selon la stratégie
        if platform == 'twitter':
            content_type = strategy['twitter_focus']
            if content_type == 'mixed':
                content_type = random.choice(['gpu_deals', 'affiliate'])
        elif platform == 'telegram':
            content_type = strategy['telegram_focus']
            if content_type == 'mixed':
                content_type = random.choice(['gpu_deals', 'affiliate'])
        else:
            content_type = 'gpu_deals'
            
        # Sélectionner template selon personnalité
        language = 'en'  # Pour l'instant
        templates = self.templates[platform][language][content_type]
        template = random.choice(templates)
        
        # Variables de remplacement
        variables = {
            'affiliate_code': self.affiliate_code
        }
        
        if offer and content_type == 'gpu_deals':
            variables.update({
                'gpu_count': offer.get('gpu_count', 1),
                'gpu_type': offer.get('gpu_type', 'GPU'),
                'price': f"${offer.get('price_per_hour', 0):.2f}",
                'location': offer.get('location', 'Global'),
                'uptime': f"{offer.get('uptime', 0):.1f}%"
            })
        
        # Remplacer variables
        content = template
        for key, value in variables.items():
            content = content.replace(f'{{{key}}}', str(value))
            
        # Ajouter hashtags intelligents
        if platform == 'twitter':
            hashtags = ' '.join(strategy['hashtags'][:4])  # Max 4 hashtags
            if not any(tag in content for tag in strategy['hashtags']):
                content += f"\n\n{hashtags}"
                
        # Ajouter engagement booster pour Telegram
        if platform == 'telegram' and time_adaptation['energy'] == 'engaging':
            engagement_booster = random.choice(self.telegram_growth_strategies['engagement_boosters'])
            content += f"\n\n{engagement_booster}"
            
        logging.info(f"🧠 Contenu généré - Plateforme: {platform}, Type: {content_type}, Style: {strategy['content_style']}")
        return content
        
    def get_gpu_offers(self) -> Optional[List[Dict]]:
        """Récupère les offres GPU avec intelligence"""
        try:
            headers = {
                'Authorization': f'Bearer {self.voltage_api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.voltage_base_url}/pods",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    offers = self.filter_and_sort_offers(data)
                    logging.info(f"🧠 {len(offers)} offres GPU analysées intelligemment")
                    return offers
                except json.JSONDecodeError:
                    return self.get_mock_offers()
            else:
                return self.get_mock_offers()
                
        except Exception as e:
            logging.error(f"❌ Erreur API VoltageGPU: {e}")
            return self.get_mock_offers()
            
    def get_mock_offers(self) -> Optional[List[Dict]]:
        """Récupère les offres mock"""
        try:
            with open('mock_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            offers = self.filter_and_sort_offers(data)
            logging.info(f"🧠 Utilisation des données mock: {len(offers)} offres")
            return offers
        except Exception as e:
            logging.error(f"❌ Erreur données mock: {e}")
            return None
            
    def filter_and_sort_offers(self, data: Dict) -> List[Dict]:
        """Filtre et trie les offres avec intelligence"""
        if not isinstance(data, dict) or 'pods' not in data:
            return []
            
        offers = data['pods']
        filtered_offers = []
        
        for offer in offers:
            if (offer.get('uptime', 0) > 95 and
                offer.get('price_per_hour', 999) < 100 and
                offer.get('gpu_type') and
                offer.get('network_speed', 0) > 100):
                filtered_offers.append(offer)
        
        # Tri intelligent selon la personnalité
        if self.bot_personality == 'technical_expert':
            # Priorité performance
            gpu_priority = {'B200': 1, 'H200': 2, 'A100': 3, 'RTX4090': 4}
        elif self.bot_personality == 'crypto_enthusiast':
            # Priorité prix
            gpu_priority = {'RTX4090': 1, 'A100': 2, 'H200': 3, 'B200': 4}
        else:
            # Équilibré
            gpu_priority = {'B200': 1, 'H200': 2, 'RTX4090': 3, 'A100': 4}
        
        def sort_key(offer):
            gpu_type = offer.get('gpu_type', 'Unknown')
            gpu_rank = gpu_priority.get(gpu_type, 999)
            price = offer.get('price_per_hour', 999)
            uptime = -offer.get('uptime', 0)
            network = -offer.get('network_speed', 0)
            return (gpu_rank, price, uptime, network)
        
        filtered_offers.sort(key=sort_key)
        return filtered_offers[:5]
        
    def intelligent_post(self, platform: str):
        """Post intelligent adaptatif"""
        try:
            offers = self.get_gpu_offers()
            best_offer = offers[0] if offers else None
            
            content = self.generate_intelligent_content(platform, best_offer)
            
            if self.test_mode:
                print(f"🧠 MODE TEST - {platform.upper()} (Personnalité: {self.bot_personality}):")
                print(f"📄 Contenu ({len(content)} caractères):")
                print(content)
                print("-" * 50)
                return True
                
            # Post réel avec intelligence
            success = self.post_to_platform(platform, content)
            if success:
                self.performance_metrics[platform]['posts'] += 1
                logging.info(f"🧠 Post intelligent publié sur {platform}")
                
        except Exception as e:
            logging.error(f"❌ Erreur post intelligent {platform}: {e}")
            
    def post_to_platform(self, platform: str, content: str) -> bool:
        """Poste du contenu avec intelligence"""
        try:
            if platform == 'twitter' and 'twitter' in self.platforms:
                if len(content) > 280:
                    content = content[:277] + "..."
                response = self.platforms['twitter'].create_tweet(text=content)
                logging.info(f"🧠 Tweet intelligent posté - ID: {response.data['id']}")
                return True
                
            elif platform == 'telegram' and 'telegram' in self.platforms:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(
                        self.platforms['telegram'].send_message(
                            chat_id=self.platform_configs['telegram']['channel_id'],
                            text=content
                        )
                    )
                finally:
                    loop.close()
                logging.info("🧠 Message Telegram intelligent envoyé")
                return True
                
            elif platform == 'reddit' and 'reddit' in self.platforms:
                # Reddit intelligent avec anti-filtres
                title = "GPU Cost Analysis - Real User Experience"
                
                subreddit_obj = self.platforms['reddit'].subreddit('test')
                submission = subreddit_obj.submit(title=title, selftext=content)
                logging.info(f"🧠 Post Reddit intelligent créé - {submission.permalink}")
                return True
                
            else:
                logging.warning(f"⚠️  Plateforme {platform} non configurée")
                return False
                
        except Exception as e:
            logging.error(f"❌ Erreur post intelligent {platform}: {e}")
            return False
            
    def run_test(self):
        """Lance un test intelligent"""
        print("🧠 TEST BOT INTELLIGENT VOLTAGEGPU")
        print("=" * 50)
        print(f"🤖 Personnalité: {self.bot_personality}")
        print(f"🎯 Focus: {self.bot_focus}")
        print(f"📈 Stratégie: {self.posting_strategy}")
        print()
        
        for platform in ['twitter', 'telegram', 'reddit']:
            if platform in self.platforms:
                self.intelligent_post(platform)
                
        print(f"\n📊 MÉTRIQUES:")
        for platform, metrics in self.performance_metrics.items():
            print(f"   {platform}: {metrics['posts']} posts")
            
    def setup_intelligent_scheduler(self):
        """Configure le planificateur intelligent pour MAXIMUM de posts"""
        # Twitter : 16 posts/jour (toutes les 90 minutes) - adaptatif selon personnalité
        times_twitter = ["00:30", "02:00", "03:30", "05:00", "06:30", "08:00", 
                        "09:30", "11:00", "12:30", "14:00", "15:30", "17:00",
                        "18:30", "20:00", "21:30", "23:00"]
        
        for time_str in times_twitter:
            schedule.every().day.at(time_str).do(lambda: self.intelligent_post('twitter'))
        
        # Telegram : 24 posts/jour (toutes les heures) - intelligence adaptative
        for hour in range(24):
            time_str = f"{hour:02d}:00"
            schedule.every().day.at(time_str).do(lambda: self.intelligent_post('telegram'))
        
        # Reddit : 3 posts/jour (maximum intelligent)
        schedule.every().day.at("08:00").do(lambda: self.intelligent_post('reddit'))
        schedule.every().day.at("14:00").do(lambda: self.intelligent_post('reddit'))
        schedule.every().day.at("20:00").do(lambda: self.intelligent_post('reddit'))
        
        logging.info("🧠 Planificateur intelligent MAXIMUM configuré: 43 posts/jour")
        
    def run(self):
        """Lance le bot intelligent"""
        if self.test_mode:
            self.run_test()
            return
            
        print(f"🧠 Lancement du bot VoltageGPU INTELLIGENT...")
        print(f"🤖 Personnalité: {self.bot_personality}")
        print(f"🎯 Focus: {self.bot_focus}")
        print(f"📈 Stratégie: {self.posting_strategy}")
        
        self.setup_intelligent_scheduler()
        
        print("⏰ PLANIFICATION INTELLIGENTE ACTIVE")
        print("🛑 Ctrl+C pour arrêter")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n🛑 Bot intelligent arrêté")
            logging.info("Bot intelligent arrêté")

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='VoltageGPU Intelligent Bot')
    parser.add_argument('--test', action='store_true', 
                       help='Lance le bot en mode test')
    
    args = parser.parse_args()
    
    try:
        bot = IntelligentVoltageBot(test_mode=args.test)
        bot.run()
    except Exception as e:
        logging.error(f"❌ Erreur fatale: {e}")
        print(f"❌ Erreur fatale: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
