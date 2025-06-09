#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Final VoltageGPU avec Timer - 1810 Posts/Mois
Compteur en temps réel avant chaque prochain post
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
        logging.FileHandler('bot_final_timer.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class BotFinalAvecTimer:
    def __init__(self, test_mode=False):
        """Bot final avec timer et compteur"""
        self.test_mode = test_mode
        self.load_config()
        self.setup_platforms()
        self.load_templates()
        self.init_counters()
        self.init_timers()
        
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
                'handle': '@Account1',
                'api_key': os.getenv('TWITTER_API_KEY'),
                'api_secret': os.getenv('TWITTER_API_SECRET'),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
                'access_secret': os.getenv('TWITTER_ACCESS_SECRET'),
                'posts_today': 0,
                'posts_month': 0,
                'next_post_time': None
            },
            {
                'name': 'Account2',
                'handle': '@Account2',
                'api_key': os.getenv('TWITTER_API_KEY_2'),
                'api_secret': os.getenv('TWITTER_API_SECRET_2'),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN_2'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN_2'),
                'access_secret': os.getenv('TWITTER_ACCESS_SECRET_2'),
                'posts_today': 0,
                'posts_month': 0,
                'next_post_time': None
            }
        ]
        
        self.telegram_config = {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'channel_id': os.getenv('TELEGRAM_CHANNEL_ID', '@YourChannel'),
            'posts_today': 0,
            'posts_month': 0,
            'next_post_time': None
        }
        
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
                    logging.info(f"🚀 Twitter {config['handle']}: Connecté")
                
                self.twitter_clients.append({
                    'client': client,
                    'config': config
                })
                
            except Exception as e:
                logging.error(f"❌ Erreur Twitter {config['handle']}: {e}")
        
        # Setup Telegram
        try:
            import telegram
            self.telegram_bot = telegram.Bot(token=self.telegram_config['bot_token'])
            logging.info("🚀 Telegram @VoltageGPU: Connecté")
        except Exception as e:
            logging.error(f"❌ Erreur Telegram: {e}")
            self.telegram_bot = None
            
        logging.info(f"🚀 Bot Final initialisé: {len(self.twitter_clients)} comptes Twitter + Telegram")
        
    def load_templates(self):
        """Charge les templates"""
        try:
            with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
            logging.info("🚀 Templates chargés")
        except Exception as e:
            logging.error(f"❌ Erreur templates: {e}")
            raise
            
    def init_counters(self):
        """Initialise les compteurs"""
        self.daily_stats = {
            'twitter_posts': 0,
            'telegram_posts': 0,
            'total_posts': 0,
            'start_time': datetime.now()
        }
        
    def init_timers(self):
        """Initialise les timers pour prochains posts"""
        now = datetime.now()
        
        # Prochains posts Twitter (toutes les 90 minutes)
        for i, twitter_data in enumerate(self.twitter_clients):
            config = twitter_data['config']
            # Décaler de 45 minutes entre les comptes
            next_time = now + timedelta(minutes=45 * (i + 1))
            config['next_post_time'] = next_time
            
        # Prochain post Telegram (toutes les heures)
        self.telegram_config['next_post_time'] = now + timedelta(hours=1)
        
    def get_gpu_offers(self) -> List[Dict]:
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
            return self.get_mock_offers()
            
    def get_mock_offers(self) -> List[Dict]:
        """Offres mock pour fallback"""
        return [{
            'gpu_count': random.choice([4, 8, 16]),
            'gpu_type': random.choice(['B200', 'H200', 'RTX4090']),
            'price_per_hour': round(random.uniform(35, 55), 2),
            'location': random.choice(['Mumbai', 'Raleigh', 'Singapore']),
            'uptime': round(random.uniform(97, 99.5), 1)
        }]
            
    def filter_offers(self, data: Dict) -> List[Dict]:
        """Filtre les meilleures offres"""
        if not isinstance(data, dict) or 'pods' not in data:
            return self.get_mock_offers()
            
        offers = data['pods'][:3]
        return offers if offers else self.get_mock_offers()
        
    def generate_content(self, platform: str, content_type: str, offer: Optional[Dict] = None) -> str:
        """Génère du contenu"""
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
    
    def post_twitter(self, twitter_index: int):
        """Post Twitter avec timer"""
        twitter_data = self.twitter_clients[twitter_index]
        client = twitter_data['client']
        config = twitter_data['config']
        
        # Vérifier limite quotidienne (16 posts/jour max)
        if config['posts_today'] >= 16:
            logging.info(f"⏰ {config['handle']}: Limite quotidienne atteinte (16/16)")
            return
            
        offers = self.get_gpu_offers()
        best_offer = offers[0] if offers else None
        
        # Alterner GPU deals et affiliation
        content_type = 'gpu_deals' if config['posts_today'] % 2 == 0 else 'affiliate'
        content = self.generate_content('twitter', content_type, best_offer)
        
        if self.test_mode:
            print(f"🚀 TEST {config['handle']} - {content_type.upper()}:")
            print(f"📄 {content}")
            return
            
        try:
            response = client.create_tweet(text=content)
            tweet_id = response.data['id']
            
            config['posts_today'] += 1
            config['posts_month'] += 1
            self.daily_stats['twitter_posts'] += 1
            self.daily_stats['total_posts'] += 1
            
            # Programmer prochain post dans 90 minutes
            config['next_post_time'] = datetime.now() + timedelta(minutes=90)
            
            logging.info(f"🚀 Tweet posté - {config['handle']} - Post {config['posts_today']}/16")
            logging.info(f"🔗 https://twitter.com/i/status/{tweet_id}")
            
        except Exception as e:
            logging.error(f"❌ Erreur tweet {config['handle']}: {e}")
    
    def post_telegram(self):
        """Post Telegram avec timer"""
        if not self.telegram_bot:
            return
            
        if self.telegram_config['posts_today'] >= 24:
            logging.info("⏰ Telegram: Limite quotidienne atteinte (24/24)")
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
            return
            
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                message = loop.run_until_complete(
                    self.telegram_bot.send_message(
                        chat_id=self.telegram_config['channel_id'],
                        text=content
                    )
                )
                
                self.telegram_config['posts_today'] += 1
                self.telegram_config['posts_month'] += 1
                self.daily_stats['telegram_posts'] += 1
                self.daily_stats['total_posts'] += 1
                
                # Programmer prochain post dans 1 heure
                self.telegram_config['next_post_time'] = datetime.now() + timedelta(hours=1)
                
                logging.info(f"🚀 Message Telegram posté - Post {self.telegram_config['posts_today']}/24")
                
            finally:
                loop.close()
                
        except Exception as e:
            logging.error(f"❌ Erreur Telegram: {e}")
    
    def check_and_post(self):
        """Vérifie les timers et poste si nécessaire"""
        now = datetime.now()
        
        # Vérifier Twitter
        for i, twitter_data in enumerate(self.twitter_clients):
            config = twitter_data['config']
            if config['next_post_time'] and now >= config['next_post_time']:
                self.post_twitter(i)
        
        # Vérifier Telegram
        if (self.telegram_config['next_post_time'] and 
            now >= self.telegram_config['next_post_time']):
            self.post_telegram()
    
    def display_timer_status(self):
        """Affiche le statut avec timer"""
        now = datetime.now()
        uptime = now - self.daily_stats['start_time']
        
        print(f"\r🚀 BOT FINAL VOLTAGEGPU - TIMER LIVE", end="")
        print(f"\n⏰ {now.strftime('%H:%M:%S')} | Uptime: {str(uptime).split('.')[0]}")
        
        print(f"\n📊 STATS AUJOURD'HUI:")
        print(f"   🐦 Twitter: {self.daily_stats['twitter_posts']} posts")
        print(f"   💬 Telegram: {self.daily_stats['telegram_posts']} posts")
        print(f"   📈 Total: {self.daily_stats['total_posts']} posts")
        
        print(f"\n⏰ PROCHAINS POSTS:")
        
        # Timer Twitter
        for twitter_data in self.twitter_clients:
            config = twitter_data['config']
            if config['next_post_time']:
                time_left = config['next_post_time'] - now
                if time_left.total_seconds() > 0:
                    minutes = int(time_left.total_seconds() // 60)
                    seconds = int(time_left.total_seconds() % 60)
                    print(f"   🐦 {config['handle']}: {minutes:02d}:{seconds:02d} ({config['posts_today']}/16)")
                else:
                    print(f"   🐦 {config['handle']}: PRÊT À POSTER ({config['posts_today']}/16)")
        
        # Timer Telegram
        if self.telegram_config['next_post_time']:
            time_left = self.telegram_config['next_post_time'] - now
            if time_left.total_seconds() > 0:
                minutes = int(time_left.total_seconds() // 60)
                seconds = int(time_left.total_seconds() % 60)
                print(f"   💬 Telegram: {minutes:02d}:{seconds:02d} ({self.telegram_config['posts_today']}/24)")
            else:
                print(f"   💬 Telegram: PRÊT À POSTER ({self.telegram_config['posts_today']}/24)")
        
        print(f"\n💰 CODE: {self.affiliate_code} | 🎯 OBJECTIF: 1810 posts/mois")
        print("🛑 Ctrl+C pour arrêter" + " " * 20, end="")
        
    def reset_daily_counters(self):
        """Reset les compteurs quotidiens"""
        for twitter_data in self.twitter_clients:
            twitter_data['config']['posts_today'] = 0
        self.telegram_config['posts_today'] = 0
        
        logging.info(f"🚀 Compteurs reset - Stats hier: {self.daily_stats}")
        self.daily_stats = {
            'twitter_posts': 0, 
            'telegram_posts': 0, 
            'total_posts': 0,
            'start_time': datetime.now()
        }
        
    def run(self):
        """Lance le bot final avec timer"""
        if self.test_mode:
            print("🚀 TEST BOT FINAL AVEC TIMER")
            print("=" * 60)
            self.post_twitter(0)
            self.post_twitter(1)
            self.post_telegram()
            return
            
        print("🚀 LANCEMENT BOT FINAL VOLTAGEGPU AVEC TIMER")
        print("=" * 60)
        print("📊 STRATÉGIE: 1810 posts/mois automatiques")
        print("⏰ TIMER: Compteur en temps réel")
        print(f"💰 CODE: {self.affiliate_code} dans chaque post")
        print()
        
        # Reset quotidien à minuit
        schedule.every().day.at("00:00").do(self.reset_daily_counters)
        
        try:
            while True:
                # Vérifier et poster si nécessaire
                self.check_and_post()
                
                # Vérifier tâches programmées
                schedule.run_pending()
                
                # Afficher timer
                self.display_timer_status()
                
                # Attendre 1 seconde
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot final arrêté")
            logging.info("Bot final avec timer arrêté")

def main():
    """Point d'entrée"""
    parser = argparse.ArgumentParser(description='Bot Final VoltageGPU avec Timer')
    parser.add_argument('--test', action='store_true', help='Mode test')
    
    args = parser.parse_args()
    
    try:
        bot = BotFinalAvecTimer(test_mode=args.test)
        bot.run()
    except Exception as e:
        logging.error(f"❌ Erreur fatale: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
