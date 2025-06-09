#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Explosif VoltageGPU - 1810 Posts/Mois
Stratégie maximale : 500 tweets/compte + 720 Telegram + 90 Reddit
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
        logging.FileHandler('bot_explosif.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class BotExplosif:
    def __init__(self, test_mode=False):
        """Bot explosif avec 1810 posts/mois"""
        self.test_mode = test_mode
        self.load_config()
        self.setup_platforms()
        self.load_templates()
        self.init_counters()
        
    def load_config(self):
        """Charge la configuration"""
        load_dotenv()
        
        self.voltage_api_key = os.getenv('VOLTAGE_API_KEY')
        self.voltage_base_url = "https://voltagegpu.com/api"
        self.affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO')
        
        # Configuration multi-comptes depuis variables d'environnement
        self.twitter_configs = [
            {
                'name': 'Account1',
                'api_key': os.getenv('TWITTER_API_KEY'),
                'api_secret': os.getenv('TWITTER_API_SECRET'),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
                'access_secret': os.getenv('TWITTER_ACCESS_SECRET'),
                'posts_today': 0,
                'posts_month': 0
            },
            {
                'name': 'Account2',
                'api_key': os.getenv('TWITTER_API_KEY_2'),
                'api_secret': os.getenv('TWITTER_API_SECRET_2'),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN_2'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN_2'),
                'access_secret': os.getenv('TWITTER_ACCESS_SECRET_2'),
                'posts_today': 0,
                'posts_month': 0
            }
        ]
        
        self.telegram_config = {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'channel_id': os.getenv('TELEGRAM_CHANNEL_ID', '@YourChannel'),
            'posts_today': 0,
            'posts_month': 0
        }
        
        self.reddit_subreddits = [
            'MachineLearning', 'artificial', 'LocalLLaMA', 
            'deeplearning', 'ChatGPT', 'ArtificialIntelligence'
        ]
        
    def setup_platforms(self):
        """Configure les plateformes"""
        self.twitter_clients = []
        
        # Setup Twitter clients
        for config in self.twitter_configs:
            try:
                client = tweepy.Client(
                    bearer_token=config['bearer_token'],
                    consumer_key=config['api_key'],
                    consumer_secret=config['api_secret'],
                    access_token=config['access_token'],
                    access_token_secret=config['access_secret'],
                    wait_on_rate_limit=True
                )
                
                if not self.test_mode:
                    me = client.get_me()
                    logging.info(f"🚀 Twitter {config['name']}: @{me.data.username}")
                
                self.twitter_clients.append({
                    'client': client,
                    'config': config
                })
                
            except Exception as e:
                logging.error(f"❌ Erreur Twitter {config['name']}: {e}")
        
        # Setup Telegram
        try:
            import telegram
            self.telegram_bot = telegram.Bot(token=self.telegram_config['bot_token'])
            logging.info("🚀 Telegram configuré pour posts explosifs")
        except Exception as e:
            logging.error(f"❌ Erreur Telegram: {e}")
            self.telegram_bot = None
            
        logging.info(f"🚀 Bot Explosif initialisé: {len(self.twitter_clients)} comptes Twitter")
        
    def load_templates(self):
        """Charge les templates"""
        try:
            with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
            logging.info("🚀 Templates explosifs chargés")
        except Exception as e:
            logging.error(f"❌ Erreur templates: {e}")
            raise
            
    def init_counters(self):
        """Initialise les compteurs"""
        self.daily_stats = {
            'twitter_posts': 0,
            'telegram_posts': 0,
            'reddit_posts': 0,
            'total_posts': 0
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
                data = response.json()
                return self.filter_offers(data)
            else:
                return self.get_mock_offers()
                
        except Exception as e:
            logging.error(f"❌ Erreur API VoltageGPU: {e}")
            return self.get_mock_offers()
            
    def get_mock_offers(self) -> List[Dict]:
        """Offres mock pour fallback"""
        try:
            with open('mock_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.filter_offers(data)
        except:
            return [{
                'gpu_count': 4,
                'gpu_type': 'B200',
                'price_per_hour': 45.50,
                'location': 'Raleigh',
                'uptime': 98.7
            }]
            
    def filter_offers(self, data: Dict) -> List[Dict]:
        """Filtre les meilleures offres"""
        if not isinstance(data, dict) or 'pods' not in data:
            return self.get_mock_offers()
            
        offers = data['pods'][:5]  # Top 5 offres
        return offers if offers else self.get_mock_offers()
        
    def generate_content(self, platform: str, content_type: str, offer: Optional[Dict] = None) -> str:
        """Génère du contenu explosif"""
        language = random.choice(['en', 'zh']) if random.random() < 0.3 else 'en'
        
        try:
            templates = self.templates[platform][language][content_type]
            template = random.choice(templates)
            
            variables = {'affiliate_code': self.affiliate_code}
            
            if offer and content_type == 'gpu_deals':
                variables.update({
                    'gpu_count': offer.get('gpu_count', 4),
                    'gpu_type': offer.get('gpu_type', 'B200'),
                    'price': f"${offer.get('price_per_hour', 45.50):.2f}",
                    'location': offer.get('location', 'Global'),
                    'uptime': f"{offer.get('uptime', 98.7):.1f}%"
                })
            
            content = template
            for key, value in variables.items():
                content = content.replace(f'{{{key}}}', str(value))
                
            # Raccourcir pour Twitter si nécessaire
            if platform == 'twitter' and len(content) > 280:
                content = content[:277] + "..."
                
            return content
            
        except Exception as e:
            logging.error(f"❌ Erreur génération contenu: {e}")
            return f"🚀 VoltageGPU - 70% cheaper than AWS! Use code {self.affiliate_code}: https://voltagegpu.com/?ref={self.affiliate_code}"
    
    def post_twitter_explosif(self):
        """Posts Twitter explosifs (16 par jour par compte)"""
        offers = self.get_gpu_offers()
        best_offer = offers[0] if offers else None
        
        for twitter_data in self.twitter_clients:
            client = twitter_data['client']
            config = twitter_data['config']
            
            # Vérifier limite quotidienne (16 posts/jour max)
            if config['posts_today'] >= 16:
                continue
                
            # Alterner GPU deals et affiliation
            content_type = 'gpu_deals' if config['posts_today'] % 2 == 0 else 'affiliate'
            content = self.generate_content('twitter', content_type, best_offer)
            
            if self.test_mode:
                print(f"🚀 TEST TWITTER {config['name']}:")
                print(f"📄 {content}")
                print("-" * 50)
                continue
                
            try:
                response = client.create_tweet(text=content)
                config['posts_today'] += 1
                config['posts_month'] += 1
                self.daily_stats['twitter_posts'] += 1
                
                logging.info(f"🚀 Tweet explosif posté - {config['name']} - Post {config['posts_today']}/16")
                
            except Exception as e:
                logging.error(f"❌ Erreur tweet {config['name']}: {e}")
    
    def post_telegram_explosif(self):
        """Posts Telegram explosifs (24 par jour)"""
        if not self.telegram_bot:
            return
            
        if self.telegram_config['posts_today'] >= 24:
            return
            
        offers = self.get_gpu_offers()
        best_offer = offers[0] if offers else None
        
        # 80% affiliation, 20% GPU deals
        content_type = 'affiliate' if random.random() < 0.8 else 'gpu_deals'
        content = self.generate_content('telegram', content_type, best_offer)
        
        # Ajouter question engageante
        questions = [
            "\n\n💬 What's your biggest AI project challenge?",
            "\n\n🤔 AWS vs VoltageGPU - what's your experience?",
            "\n\n🚀 Share your GPU training setup!",
            "\n\n💡 Best ML frameworks for GPU training?",
            "\n\n🔥 Who else is tired of cloud costs?"
        ]
        content += random.choice(questions)
        
        if self.test_mode:
            print(f"🚀 TEST TELEGRAM:")
            print(f"📄 {content}")
            print("-" * 50)
            return
            
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(
                    self.telegram_bot.send_message(
                        chat_id=self.telegram_config['channel_id'],
                        text=content
                    )
                )
            finally:
                loop.close()
                
            self.telegram_config['posts_today'] += 1
            self.telegram_config['posts_month'] += 1
            self.daily_stats['telegram_posts'] += 1
            
            logging.info(f"🚀 Message Telegram explosif - Post {self.telegram_config['posts_today']}/24")
            
        except Exception as e:
            logging.error(f"❌ Erreur Telegram: {e}")
    
    def post_reddit_explosif(self):
        """Posts Reddit explosifs (3 par jour)"""
        # Reddit sera implémenté quand les comptes seront prêts
        logging.info("🚀 Reddit explosif - En attente comptes matures")
        
    def setup_explosive_schedule(self):
        """Configure la planification explosive"""
        logging.info("🚀 Configuration planification EXPLOSIVE")
        
        # Twitter Bot 1 - 16 posts/jour (toutes les 90 minutes)
        times_bot1 = ["00:30", "02:00", "03:30", "05:00", "06:30", "08:00", 
                      "09:30", "11:00", "12:30", "14:00", "15:30", "17:00",
                      "18:30", "20:00", "21:30", "23:00"]
        
        for time_str in times_bot1:
            schedule.every().day.at(time_str).do(self.post_twitter_explosif)
        
        # Telegram - 24 posts/jour (toutes les heures)
        for hour in range(24):
            time_str = f"{hour:02d}:00"
            schedule.every().day.at(time_str).do(self.post_telegram_explosif)
        
        # Reddit - 3 posts/jour
        schedule.every().day.at("08:00").do(self.post_reddit_explosif)
        schedule.every().day.at("14:00").do(self.post_reddit_explosif)
        schedule.every().day.at("20:00").do(self.post_reddit_explosif)
        
        # Reset compteurs quotidiens à minuit
        schedule.every().day.at("00:00").do(self.reset_daily_counters)
        
        logging.info("🚀 Planification explosive configurée:")
        logging.info("   🐦 Twitter: 32 posts/jour (16 par compte)")
        logging.info("   💬 Telegram: 24 posts/jour")
        logging.info("   🔴 Reddit: 3 posts/jour")
        logging.info("   📊 TOTAL: 59 posts/jour = 1810 posts/mois")
        
    def reset_daily_counters(self):
        """Reset les compteurs quotidiens"""
        for config in self.twitter_configs:
            config['posts_today'] = 0
        self.telegram_config['posts_today'] = 0
        
        logging.info(f"🚀 Compteurs reset - Stats hier: {self.daily_stats}")
        self.daily_stats = {'twitter_posts': 0, 'telegram_posts': 0, 'reddit_posts': 0, 'total_posts': 0}
        
    def run_test(self):
        """Test explosif"""
        print("🚀 TEST BOT EXPLOSIF - 1810 POSTS/MOIS")
        print("=" * 60)
        
        print("🐦 TEST TWITTER EXPLOSIF:")
        self.post_twitter_explosif()
        
        print("💬 TEST TELEGRAM EXPLOSIF:")
        self.post_telegram_explosif()
        
        print("🔴 TEST REDDIT EXPLOSIF:")
        self.post_reddit_explosif()
        
        print(f"\n📊 STRATÉGIE EXPLOSIVE:")
        print(f"   🐦 Twitter: 1000 posts/mois (500 par compte)")
        print(f"   💬 Telegram: 720 posts/mois")
        print(f"   🔴 Reddit: 90 posts/mois")
        print(f"   📈 TOTAL: 1810 posts/mois")
        print(f"   💰 Revenus estimés: $270+/mois")
        
    def run(self):
        """Lance le bot explosif"""
        if self.test_mode:
            self.run_test()
            return
            
        print("🚀 LANCEMENT BOT EXPLOSIF VOLTAGEGPU")
        print("=" * 60)
        print("📊 STRATÉGIE: 1810 posts/mois automatiques")
        print("💰 OBJECTIF: Revenus passifs maximisés")
        print(f"🎯 CODE: {self.affiliate_code} dans chaque post")
        
        self.setup_explosive_schedule()
        
        print("\n⏰ PLANIFICATION EXPLOSIVE ACTIVE")
        print("🛑 Ctrl+C pour arrêter")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n🛑 Bot explosif arrêté")
            logging.info("Bot explosif arrêté")

def main():
    """Point d'entrée"""
    parser = argparse.ArgumentParser(description='Bot Explosif VoltageGPU')
    parser.add_argument('--test', action='store_true', help='Mode test')
    
    args = parser.parse_args()
    
    try:
        bot = BotExplosif(test_mode=args.test)
        bot.run()
    except Exception as e:
        logging.error(f"❌ Erreur fatale: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
