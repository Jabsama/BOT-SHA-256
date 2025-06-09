#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VoltageGPU Bot Final Optimisé - Version stable
Rotation subreddits, timing optimal, stratégies avancées
"""

import os
import json
import random
import logging
import requests
import schedule
import time
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Optional
import tweepy
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

error_logger = logging.getLogger('errors')
error_handler = logging.FileHandler('errors.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

class FinalOptimizedBot:
    def __init__(self, test_mode=False):
        """Initialise le bot final optimisé"""
        self.test_mode = test_mode
        self.load_config()
        self.setup_platforms()
        self.load_templates()
        self.init_optimization_data()
        
    def load_config(self):
        """Charge la configuration"""
        load_dotenv()
        
        self.voltage_api_key = os.getenv('VOLTAGE_API_KEY')
        self.voltage_base_url = "https://voltagegpu.com/api"
        self.affiliate_code = "SHA-256-76360B81D39F"
        
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
        """Configure les plateformes"""
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
                    logging.info(f"✅ Twitter connecté: @{me.data.username}")
            except Exception as e:
                error_logger.error(f"❌ Erreur Twitter: {e}")
                
        # Telegram
        if self.platform_configs['telegram']['enabled']:
            try:
                import telegram
                self.platforms['telegram'] = telegram.Bot(
                    token=self.platform_configs['telegram']['bot_token']
                )
                logging.info("✅ Telegram configuré")
            except ImportError:
                logging.warning("⚠️  python-telegram-bot non installé")
            except Exception as e:
                error_logger.error(f"❌ Erreur Telegram: {e}")
                
        # Reddit
        if self.platform_configs['reddit']['enabled']:
            try:
                import praw
                self.platforms['reddit'] = praw.Reddit(
                    client_id=self.platform_configs['reddit']['client_id'],
                    client_secret=self.platform_configs['reddit']['client_secret'],
                    username=self.platform_configs['reddit']['username'],
                    password=self.platform_configs['reddit']['password'],
                    user_agent="VoltageGPU Final Bot v1.0"
                )
                logging.info("✅ Reddit configuré")
            except ImportError:
                logging.warning("⚠️  praw non installé")
            except Exception as e:
                error_logger.error(f"❌ Erreur Reddit: {e}")
                
        logging.info(f"🚀 Plateformes actives: {list(self.platforms.keys())}")
        
    def load_templates(self):
        """Charge les templates"""
        try:
            with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
            logging.info("✅ Templates multilingues chargés")
        except Exception as e:
            error_logger.error(f"❌ Erreur chargement templates: {e}")
            raise
            
    def init_optimization_data(self):
        """Initialise les données d'optimisation"""
        # Rotation des subreddits optimisée
        self.subreddit_rotation = [
            'MachineLearning',    # 2.8M - Tier 1
            'artificial',         # 180k - Tier 1  
            'LocalLLaMA',        # 150k - Tier 1
            'deeplearning',      # 120k - Tier 2
            'ChatGPT',           # 300k - Tier 2
            'entrepreneur'       # 1.2M - Tier 2
        ]
        self.current_subreddit_index = 0
        
        # Compteurs pour stratégies
        self.twitter_last_type = 'affiliate'  # Commence par GPU deal
        self.telegram_post_count = 0
        
        # Langues avec pondération optimale
        self.language_weights = {'en': 0.7, 'zh': 0.3}
        
        # Statistiques
        self.stats = {
            'twitter_posts': 0,
            'telegram_posts': 0,
            'reddit_posts': 0,
            'last_post_times': {}
        }
        
    def get_gpu_offers(self) -> Optional[List[Dict]]:
        """Récupère les offres GPU"""
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
                    logging.info(f"✅ {len(offers)} offres GPU récupérées")
                    return offers
                except json.JSONDecodeError:
                    return self.get_mock_offers()
            else:
                return self.get_mock_offers()
                
        except Exception as e:
            error_logger.error(f"❌ Erreur API VoltageGPU: {e}")
            return self.get_mock_offers()
            
    def get_mock_offers(self) -> Optional[List[Dict]]:
        """Récupère les offres mock"""
        try:
            with open('mock_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            offers = self.filter_and_sort_offers(data)
            logging.info(f"⚠️  Utilisation des données mock: {len(offers)} offres")
            return offers
        except Exception as e:
            error_logger.error(f"❌ Erreur données mock: {e}")
            return None
            
    def filter_and_sort_offers(self, data: Dict) -> List[Dict]:
        """Filtre et trie les offres GPU"""
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
        
    def choose_language(self) -> str:
        """Choisit une langue selon la pondération"""
        return random.choices(
            list(self.language_weights.keys()),
            weights=list(self.language_weights.values())
        )[0]
        
    def get_next_subreddit(self) -> str:
        """Récupère le prochain subreddit dans la rotation"""
        subreddit = self.subreddit_rotation[self.current_subreddit_index]
        self.current_subreddit_index = (self.current_subreddit_index + 1) % len(self.subreddit_rotation)
        return subreddit
        
    def generate_optimized_content(self, platform: str, content_type: str, language: str, offer: Optional[Dict] = None) -> str:
        """Génère du contenu optimisé"""
        templates = self.templates[platform][language][content_type]
        template = random.choice(templates)
        
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
        
        content = template
        for key, value in variables.items():
            content = content.replace(f'{{{key}}}', str(value))
            
        return content
        
    def post_to_platform(self, platform: str, content: str, subreddit: str = None) -> bool:
        """Poste du contenu sur une plateforme"""
        if self.test_mode:
            print(f"🧪 MODE TEST - {platform.upper()}:")
            if subreddit:
                print(f"📍 Subreddit: r/{subreddit}")
            print(f"📄 Contenu ({len(content)} caractères):")
            print(content)
            print("-" * 50)
            return True
            
        try:
            if platform == 'twitter' and 'twitter' in self.platforms:
                if len(content) > 280:
                    content = content[:277] + "..."
                response = self.platforms['twitter'].create_tweet(text=content)
                logging.info(f"✅ Tweet posté - ID: {response.data['id']}")
                self.stats['twitter_posts'] += 1
                return True
                
            elif platform == 'telegram' and 'telegram' in self.platforms:
                # Version synchrone pour Telegram
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
                logging.info("✅ Message Telegram envoyé")
                self.stats['telegram_posts'] += 1
                return True
                
            elif platform == 'reddit' and 'reddit' in self.platforms:
                if not subreddit:
                    subreddit = self.get_next_subreddit()
                    
                subreddit_obj = self.platforms['reddit'].subreddit(subreddit)
                title = f"VoltageGPU - GPU Rentals 70% Cheaper Than AWS"
                
                submission = subreddit_obj.submit(title=title, selftext=content)
                logging.info(f"✅ Post Reddit créé dans r/{subreddit} - {submission.permalink}")
                self.stats['reddit_posts'] += 1
                return True
                
            else:
                logging.warning(f"⚠️  Plateforme {platform} non configurée")
                return False
                
        except Exception as e:
            error_logger.error(f"❌ Erreur {platform}: {e}")
            return False
            
    def twitter_post(self):
        """Post Twitter optimisé"""
        try:
            offers = self.get_gpu_offers()
            best_offer = offers[0] if offers else None
            
            # Alternance GPU deals ↔ Affiliation
            content_type = 'gpu_deals' if self.twitter_last_type == 'affiliate' else 'affiliate'
            self.twitter_last_type = content_type
            
            language = 'en'  # Twitter principalement en anglais
            content = self.generate_optimized_content('twitter', content_type, language, best_offer)
            
            success = self.post_to_platform('twitter', content)
            if success:
                logging.info(f"✅ Twitter {content_type} publié")
                self.stats['last_post_times']['twitter'] = datetime.now()
                
        except Exception as e:
            error_logger.error(f"❌ Erreur Twitter post: {e}")
            
    def telegram_post(self):
        """Post Telegram optimisé"""
        try:
            offers = self.get_gpu_offers()
            best_offer = offers[0] if offers else None
            
            # 80% affiliation, 20% GPU deals
            content_type = 'affiliate' if self.telegram_post_count % 5 != 0 else 'gpu_deals'
            self.telegram_post_count += 1
            
            language = self.choose_language()
            content = self.generate_optimized_content('telegram', content_type, language, best_offer)
            
            success = self.post_to_platform('telegram', content)
            if success:
                logging.info(f"✅ Telegram {content_type} en {language} publié")
                self.stats['last_post_times']['telegram'] = datetime.now()
                
        except Exception as e:
            error_logger.error(f"❌ Erreur Telegram post: {e}")
            
    def reddit_post(self):
        """Post Reddit optimisé"""
        try:
            offers = self.get_gpu_offers()
            best_offer = offers[0] if offers else None
            
            # 90% GPU deals, 10% affiliation
            content_type = 'gpu_deals' if random.random() < 0.9 else 'affiliate'
            
            language = self.choose_language()
            subreddit = self.get_next_subreddit()
            
            content = self.generate_optimized_content('reddit', content_type, language, best_offer)
            
            success = self.post_to_platform('reddit', content, subreddit)
            if success:
                logging.info(f"✅ Reddit {content_type} en {language} publié sur r/{subreddit}")
                self.stats['last_post_times']['reddit'] = datetime.now()
                
        except Exception as e:
            error_logger.error(f"❌ Erreur Reddit post: {e}")
            
    def setup_optimized_scheduler(self):
        """Configure le planificateur optimisé"""
        # Twitter : 1x/jour à 14h UTC (optimal)
        schedule.every().day.at("14:00").do(self.twitter_post)
        
        # Telegram : 2x/jour à 10h et 18h UTC
        schedule.every().day.at("10:00").do(self.telegram_post)
        schedule.every().day.at("18:00").do(self.telegram_post)
        
        # Reddit : 1x tous les 2 jours à 15h UTC
        schedule.every(2).days.at("15:00").do(self.reddit_post)
        
        logging.info("✅ Planificateur optimisé configuré")
        
    def run_test(self):
        """Lance un test complet"""
        print("🧪 TEST COMPLET DU BOT FINAL OPTIMISÉ")
        print("=" * 50)
        
        print("\n🐦 TEST TWITTER (Alternance):")
        self.twitter_post()
        
        print("\n📱 TEST TELEGRAM (80% Affiliation):")
        self.telegram_post()
        
        print("\n🔴 TEST REDDIT (Rotation Subreddits):")
        self.reddit_post()
        
        print(f"\n📊 STATISTIQUES:")
        print(f"   🐦 Twitter posts: {self.stats['twitter_posts']}")
        print(f"   📱 Telegram posts: {self.stats['telegram_posts']}")
        print(f"   🔴 Reddit posts: {self.stats['reddit_posts']}")
        print(f"   📍 Prochain subreddit: r/{self.subreddit_rotation[self.current_subreddit_index]}")
        
    def run(self):
        """Lance le bot optimisé"""
        if self.test_mode:
            self.run_test()
            return
            
        print("🚀 Lancement du bot VoltageGPU FINAL OPTIMISÉ...")
        self.setup_optimized_scheduler()
        
        print("⏰ PLANIFICATION OPTIMISÉE ACTIVE:")
        print("   🐦 Twitter: 14h UTC (1x/jour) - Alternance GPU/Affiliation")
        print("   📱 Telegram: 10h et 18h UTC (2x/jour) - 80% Affiliation")
        print("   🔴 Reddit: 15h UTC (1x/2 jours) - Rotation 6 subreddits")
        print("   🌍 Langues: 70% EN + 30% ZH")
        print("🛑 Ctrl+C pour arrêter")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n🛑 Bot final optimisé arrêté")
            print(f"📊 Statistiques finales: {self.stats}")
            logging.info("Bot final optimisé arrêté")

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='VoltageGPU Final Optimized Bot')
    parser.add_argument('--test', action='store_true', 
                       help='Lance le bot en mode test')
    
    args = parser.parse_args()
    
    try:
        bot = FinalOptimizedBot(test_mode=args.test)
        bot.run()
    except Exception as e:
        error_logger.error(f"❌ Erreur fatale: {e}")
        print(f"❌ Erreur fatale: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
