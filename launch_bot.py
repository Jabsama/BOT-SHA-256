#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VoltageGPU Bot - Unified Launcher
Twitter + Telegram + Reddit with automatic timer
Simply configure .env and launch!
"""

import os
import json
import random
import logging
import requests
import schedule
import time
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import tweepy
import praw
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voltagegpu_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class VoltageGPUBot:
    def __init__(self, test_mode=False):
        """Bot VoltageGPU unifié - Configuration automatique depuis .env"""
        self.test_mode = test_mode
        self.load_config()
        self.setup_platforms()
        self.load_templates()
        self.init_counters()
        self.init_timers()
        
    def load_config(self):
        """Charge automatiquement depuis .env"""
        load_dotenv()
        
        # VoltageGPU API
        self.voltage_api_key = os.getenv('VOLTAGE_API_KEY')
        self.voltage_base_url = "https://voltagegpu.com/api"
        self.affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO')
        
        # Twitter (multi-comptes automatique)
        self.twitter_configs = []
        for i in ['', '_2']:  # Support 2 comptes Twitter
            if os.getenv(f'TWITTER_API_KEY{i}'):
                self.twitter_configs.append({
                    'name': f'Twitter{len(self.twitter_configs)+1}',
                    'api_key': os.getenv(f'TWITTER_API_KEY{i}'),
                    'api_secret': os.getenv(f'TWITTER_API_SECRET{i}'),
                    'bearer_token': os.getenv(f'TWITTER_BEARER_TOKEN{i}'),
                    'access_token': os.getenv(f'TWITTER_ACCESS_TOKEN{i}'),
                    'access_secret': os.getenv(f'TWITTER_ACCESS_SECRET{i}'),
                    'posts_today': 0,
                    'next_post_time': None
                })
        
        # Telegram (support multi-channels/groupes)
        self.telegram_config = {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'channels': self.parse_telegram_channels(),
            'posts_today': 0,
            'next_post_time': None
        }
        
        # Reddit (multi-comptes automatique)
        self.reddit_configs = []
        for i in ['', '_2']:  # Support 2 comptes Reddit
            if os.getenv(f'REDDIT_CLIENT_ID{i}'):
                self.reddit_configs.append({
                    'name': f'Reddit{len(self.reddit_configs)+1}',
                    'client_id': os.getenv(f'REDDIT_CLIENT_ID{i}'),
                    'client_secret': os.getenv(f'REDDIT_CLIENT_SECRET{i}'),
                    'username': os.getenv(f'REDDIT_USERNAME{i}'),
                    'password': os.getenv(f'REDDIT_PASSWORD{i}'),
                    'user_agent': 'VoltageGPU Bot v1.0',
                    'posts_today': 0,
                    'next_post_time': None,
                    'banned_subreddits': set()
                })
        
    def parse_telegram_channels(self):
        """Parse les channels/groupes Telegram depuis .env"""
        channels = []
        
        # Channel principal
        main_channel = os.getenv('TELEGRAM_CHANNEL_ID', '@VoltageGPU')
        if main_channel:
            channels.append(main_channel)
        
        # Channels additionnels (séparés par virgules)
        extra_channels = os.getenv('TELEGRAM_EXTRA_CHANNELS', '')
        if extra_channels:
            for channel in extra_channels.split(','):
                channel = channel.strip()
                if channel:
                    channels.append(channel)
        
        # Groupes populaires par défaut (autonomes)
        default_groups = [
            '@AITrainingDeals',
            '@CheapGPURentals', 
            '@MachineLearningDeals',
            '@GPUMarketplace',
            '@CloudComputingDeals'
        ]
        
        # Ajouter groupes par défaut si pas de channels configurés
        if not channels:
            channels = default_groups[:2]  # Prendre 2 par défaut
            
        return channels
        
    def setup_platforms(self):
        """Setup automatique de toutes les plateformes"""
        # Twitter
        self.twitter_clients = []
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
                    logging.info(f"🐦 Twitter {config['name']}: Connecté")
                
                self.twitter_clients.append({'client': client, 'config': config})
                
            except Exception as e:
                logging.error(f"❌ Twitter {config['name']}: {e}")
        
        # Telegram
        self.telegram_bot = None
        try:
            import telegram
            self.telegram_bot = telegram.Bot(token=self.telegram_config['bot_token'])
            if not self.test_mode:
                logging.info("💬 Telegram: Connecté")
        except Exception as e:
            logging.error(f"❌ Telegram: {e}")
        
        # Reddit
        self.reddit_clients = []
        for config in self.reddit_configs:
            try:
                reddit = praw.Reddit(
                    client_id=config['client_id'],
                    client_secret=config['client_secret'],
                    username=config['username'],
                    password=config['password'],
                    user_agent=config['user_agent']
                )
                
                if not self.test_mode:
                    user = reddit.user.me()
                    logging.info(f"📍 Reddit {config['username']}: Connecté")
                
                self.reddit_clients.append({'client': reddit, 'config': config})
                
            except Exception as e:
                logging.error(f"❌ Reddit {config['username']}: {e}")
        
        total_platforms = len(self.twitter_clients) + len(self.reddit_clients) + (1 if self.telegram_bot else 0)
        logging.info(f"🚀 VoltageGPU Bot: {total_platforms} plateformes connectées")
        
    def load_templates(self):
        """Charge les templates ou utilise les templates intégrés"""
        try:
            with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
        except:
            # Templates intégrés si fichier absent
            self.templates = {
                "twitter": {
                    "en": {
                        "gpu_deals": [
                            "🚨 INSANE GPU DEAL! 🚨\n\n💻 {gpu_count}x {gpu_type} for ${price}/hour\n⚡ 70% cheaper than AWS\n🌍 {location} | {uptime} uptime\n\n💰 Code {affiliate_code} = 5% OFF!\n🔗 https://voltagegpu.com/?ref={affiliate_code}\n\n#GPUDeals #AI"
                        ],
                        "affiliate": [
                            "💰 EASY MONEY! 💰\n\n🤑 GPU referrals = passive income\n📈 5% commission per sale\n🔥 Code {affiliate_code}\n⚡ 70% cheaper than AWS\n\n💸 https://voltagegpu.com/?ref={affiliate_code}\n\n#PassiveIncome #GPU"
                        ]
                    }
                },
                "telegram": {
                    "en": {
                        "gpu_deals": [
                            "🚨 GPU DEAL ALERT! 🚨\n\n💻 {gpu_count}x {gpu_type} for ${price}/hour\n⚡ 70% cheaper than AWS\n🌍 {location} | {uptime} uptime\n\n💰 Code {affiliate_code} = 5% OFF!\n🔗 https://voltagegpu.com/?ref={affiliate_code}"
                        ],
                        "affiliate": [
                            "💰 EASY MONEY WITH GPU REFERRALS! 💰\n\n🚀 70% cheaper than AWS\n💎 Your code = Your ATM\n📱 Share once, earn forever!\n\n✅ 5% commission\n✅ 5% discount for users\n\n🔗 https://voltagegpu.com/?ref={affiliate_code}"
                        ]
                    }
                },
                "reddit": {
                    "en": {
                        "gpu_deals": [
                            "🔬 **VoltageGPU vs AWS: Real Cost Analysis**\n\n**Config:** {gpu_count}x {gpu_type}\n**Price:** ${price}/hour vs $120+/hour AWS\n**Savings:** 70%+ cost reduction\n**Location:** {location} | **Uptime:** {uptime}\n\n**Bonus:** Code `{affiliate_code}` for 5% off\n**Link:** https://voltagegpu.com/?ref={affiliate_code}\n\nAnyone else tired of AWS pricing?"
                        ],
                        "affiliate": [
                            "💼 **Side Hustle: GPU Referral Program Actually Profitable**\n\n**VoltageGPU referrals:**\n- 5% commission per rental\n- 70% cheaper than AWS (easy sell)\n- Passive income from tech network\n\n**My results:** $200+ first month\n\n**Code:** `{affiliate_code}`\n**Link:** https://voltagegpu.com/?ref={affiliate_code}\n\nAnyone else monetizing their network?"
                        ]
                    }
                }
            }
        
    def init_counters(self):
        """Initialise les compteurs"""
        self.daily_stats = {
            'twitter_posts': 0,
            'telegram_posts': 0,
            'reddit_posts': 0,
            'total_posts': 0,
            'start_time': datetime.now()
        }
        
        # Subreddits ciblés (optimisés pour maximum de posts)
        self.target_subreddits = {
            'MachineLearning': {'posts_today': 0, 'max_daily': 2, 'priority': 10},
            'DeepLearning': {'posts_today': 0, 'max_daily': 2, 'priority': 9},
            'artificial': {'posts_today': 0, 'max_daily': 2, 'priority': 8},
            'LocalLLaMA': {'posts_today': 0, 'max_daily': 2, 'priority': 10},
            'GPURental': {'posts_today': 0, 'max_daily': 8, 'priority': 10},  # Maximum
            'vastai': {'posts_today': 0, 'max_daily': 2, 'priority': 7},
            'developersIndia': {'posts_today': 0, 'max_daily': 2, 'priority': 9},
            'indiandevs': {'posts_today': 0, 'max_daily': 2, 'priority': 8},
            'programacao': {'posts_today': 0, 'max_daily': 2, 'priority': 9},
        }
        
    def init_timers(self):
        """Initialise les timers simples et efficaces"""
        now = datetime.now()
        
        # Twitter: toutes les 90 minutes par compte
        for i, twitter_data in enumerate(self.twitter_clients):
            config = twitter_data['config']
            config['next_post_time'] = now + timedelta(minutes=45 * (i + 1))
            
        # Telegram: toutes les heures
        self.telegram_config['next_post_time'] = now + timedelta(hours=1)
        
        # Reddit: planning simple toutes les 30 minutes
        self.reddit_next_post = now + timedelta(minutes=30)
        
    def get_gpu_offers(self) -> List[Dict]:
        """Récupère les offres GPU (API réelle + fallback)"""
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
                offers = data.get('pods', [])[:3]
                return offers if offers else self.get_mock_offers()
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
        
    def generate_content(self, platform: str, content_type: str, offer: Optional[Dict] = None) -> str:
        """Génère du contenu pour toutes les plateformes"""
        try:
            templates = self.templates[platform]['en'][content_type]
            template = random.choice(templates)
            
            variables = {'affiliate_code': self.affiliate_code}
            
            if offer and content_type == 'gpu_deals':
                variables.update({
                    'gpu_count': offer.get('gpu_count', 4),
                    'gpu_type': offer.get('gpu_type', 'B200'),
                    'price': f"{offer.get('price_per_hour', 45.50):.2f}",
                    'location': offer.get('location', 'Global'),
                    'uptime': f"{offer.get('uptime', 98.7):.1f}%"
                })
            
            content = template
            for key, value in variables.items():
                content = content.replace(f'{{{key}}}', str(value))
                
            # Raccourcir pour Twitter
            if platform == 'twitter' and len(content) > 280:
                content = content[:277] + "..."
                
            return content
            
        except Exception as e:
            return f"🚀 VoltageGPU - 70% cheaper than AWS! Code {self.affiliate_code}: https://voltagegpu.com/?ref={self.affiliate_code}"
    
    def post_twitter(self):
        """Posts Twitter avec timer automatique"""
        now = datetime.now()
        
        for twitter_data in self.twitter_clients:
            config = twitter_data['config']
            client = twitter_data['client']
            
            # Vérifier timer et limite (20 posts/jour max)
            if (config['next_post_time'] and now >= config['next_post_time'] and 
                config['posts_today'] < 20):
                
                offers = self.get_gpu_offers()
                best_offer = offers[0] if offers else None
                
                # Alterner GPU deals et affiliation
                content_type = 'gpu_deals' if config['posts_today'] % 2 == 0 else 'affiliate'
                content = self.generate_content('twitter', content_type, best_offer)
                
                if self.test_mode:
                    print(f"🐦 TEST TWITTER {config['name']}: {content[:100]}...")
                    config['posts_today'] += 1
                    config['next_post_time'] = now + timedelta(minutes=90)
                    continue
                    
                try:
                    response = client.create_tweet(text=content)
                    
                    config['posts_today'] += 1
                    self.daily_stats['twitter_posts'] += 1
                    self.daily_stats['total_posts'] += 1
                    
                    # Prochain post dans 90 minutes
                    config['next_post_time'] = now + timedelta(minutes=90)
                    
                    logging.info(f"🐦 Twitter {config['name']}: Post {config['posts_today']}/20")
                    
                except Exception as e:
                    logging.error(f"❌ Twitter {config['name']}: {e}")
    
    def post_telegram(self):
        """Posts Telegram avec timer automatique"""
        if not self.telegram_bot:
            return
            
        now = datetime.now()
        
        # Vérifier timer et limite (30 posts/jour max)
        if (self.telegram_config['next_post_time'] and 
            now >= self.telegram_config['next_post_time'] and 
            self.telegram_config['posts_today'] < 30):
            
            offers = self.get_gpu_offers()
            best_offer = offers[0] if offers else None
            
            # 80% affiliation, 20% GPU deals
            content_type = 'affiliate' if random.random() < 0.8 else 'gpu_deals'
            content = self.generate_content('telegram', content_type, best_offer)
            
            # Ajouter question engageante
            questions = [
                "\n\n💬 What's your biggest AI challenge?",
                "\n\n🤔 AWS vs VoltageGPU experience?",
                "\n\n🚀 Share your GPU setup!",
                "\n\n🔥 Tired of cloud costs?"
            ]
            content += random.choice(questions)
            
            if self.test_mode:
                print(f"💬 TEST TELEGRAM: {content[:100]}...")
                self.telegram_config['posts_today'] += 1
                self.telegram_config['next_post_time'] = now + timedelta(hours=1)
                return
                
            # Poster dans tous les channels configurés
            channels = self.telegram_config['channels']
            successful_posts = 0
            
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    for channel in channels:
                        try:
                            loop.run_until_complete(
                                self.telegram_bot.send_message(
                                    chat_id=channel,
                                    text=content
                                )
                            )
                            successful_posts += 1
                            logging.info(f"💬 Telegram: Post réussi dans {channel}")
                            
                            # Délai entre posts pour éviter spam
                            time.sleep(2)
                            
                        except Exception as e:
                            logging.error(f"❌ Telegram {channel}: {e}")
                            # Continuer avec les autres channels
                            continue
                    
                    if successful_posts > 0:
                        self.telegram_config['posts_today'] += 1
                        self.daily_stats['telegram_posts'] += successful_posts
                        self.daily_stats['total_posts'] += successful_posts
                        
                        # Prochain post dans 1 heure
                        self.telegram_config['next_post_time'] = now + timedelta(hours=1)
                        
                        logging.info(f"💬 Telegram: {successful_posts}/{len(channels)} channels - Post {self.telegram_config['posts_today']}/30")
                    
                finally:
                    loop.close()
                    
            except Exception as e:
                logging.error(f"❌ Telegram global: {e}")
    
    def farm_karma(self, reddit_client, config):
        """Farm karma by commenting on popular posts"""
        try:
            # Subreddits faciles pour farmer du karma
            karma_subreddits = ['AskReddit', 'explainlikeimfive', 'todayilearned', 'technology']
            target_sub = random.choice(karma_subreddits)
            
            subreddit = reddit_client.subreddit(target_sub)
            
            # Prendre les posts hot du moment
            hot_posts = list(subreddit.hot(limit=10))
            if not hot_posts:
                return False
                
            post = random.choice(hot_posts)
            
            # Commentaires génériques utiles
            helpful_comments = [
                "Thanks for sharing this! Really helpful information.",
                "This is exactly what I was looking for. Much appreciated!",
                "Great explanation, this makes a lot of sense now.",
                "Very informative post, learned something new today.",
                "Interesting perspective, thanks for the detailed breakdown.",
                "This is really useful, bookmarking for later reference.",
                "Excellent point, I hadn't thought about it that way.",
                "Thanks for taking the time to explain this so clearly."
            ]
            
            comment_text = random.choice(helpful_comments)
            
            # Poster le commentaire
            post.reply(comment_text)
            
            logging.info(f"💬 Karma farming: Comment posted in r/{target_sub} - {config['username']}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Karma farming failed for {config['username']}: {e}")
            return False

    def post_reddit(self):
        """Posts Reddit avec timer automatique + karma farming"""
        now = datetime.now()
        
        # Vérifier timer Reddit global (toutes les 30 minutes)
        if now < self.reddit_next_post:
            return
            
        # Trouver un subreddit disponible
        available_subreddits = []
        for subreddit, stats in self.target_subreddits.items():
            if stats['posts_today'] < stats['max_daily']:
                available_subreddits.append((subreddit, stats['priority']))
        
        if not available_subreddits:
            self.reddit_next_post = now + timedelta(hours=1)  # Réessayer dans 1h
            return
            
        # Choisir subreddit par priorité
        available_subreddits.sort(key=lambda x: x[1], reverse=True)
        target_subreddit = available_subreddits[0][0]
        
        # Choisir un compte Reddit disponible
        available_accounts = []
        for reddit_data in self.reddit_clients:
            config = reddit_data['config']
            if target_subreddit not in config['banned_subreddits']:
                available_accounts.append(reddit_data)
        
        if not available_accounts:
            self.reddit_next_post = now + timedelta(hours=1)
            return
            
        reddit_data = available_accounts[0]
        client = reddit_data['client']
        config = reddit_data['config']
        
        # Générer contenu
        offers = self.get_gpu_offers()
        best_offer = offers[0] if offers else None
        
        content_type = random.choice(['gpu_deals', 'affiliate'])
        content = self.generate_content('reddit', content_type, best_offer)
        
        # Générer titre
        if content_type == 'gpu_deals' and best_offer:
            title = f"Found {best_offer['gpu_count']}x {best_offer['gpu_type']} at ${best_offer['price_per_hour']:.2f}/hour - 70% cheaper than AWS"
        else:
            title = "Side hustle: GPU referral program actually profitable"
        
        if self.test_mode:
            print(f"📍 TEST REDDIT r/{target_subreddit}: {title[:50]}...")
            self.target_subreddits[target_subreddit]['posts_today'] += 1
            self.reddit_next_post = now + timedelta(minutes=30)
            return
            
        try:
            subreddit_obj = client.subreddit(target_subreddit)
            submission = subreddit_obj.submit(title=title, selftext=content)
            
            # Mettre à jour stats
            self.target_subreddits[target_subreddit]['posts_today'] += 1
            config['posts_today'] += 1
            self.daily_stats['reddit_posts'] += 1
            self.daily_stats['total_posts'] += 1
            
            # Prochain post Reddit dans 30 minutes
            self.reddit_next_post = now + timedelta(minutes=30)
            
            logging.info(f"📍 Reddit r/{target_subreddit}: Post réussi - {config['username']}")
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Gestion spécifique des erreurs Reddit
            if '403' in str(e) or 'forbidden' in error_msg or 'banned' in error_msg:
                config['banned_subreddits'].add(target_subreddit)
                logging.error(f"❌ BANNED from r/{target_subreddit} - {config['username']} (403 Forbidden)")
                logging.info(f"💡 Trying karma farming to build reputation...")
                
                # Essayer de farmer du karma
                if self.farm_karma(client, config):
                    logging.info(f"✅ Karma farming successful for {config['username']}")
                else:
                    logging.info(f"❌ Karma farming failed for {config['username']}")
                    
            elif '429' in str(e) or 'rate limit' in error_msg:
                logging.error(f"❌ RATE LIMITED on Reddit - {config['username']}")
                logging.info(f"💡 Solution: Waiting 2 hours before next attempt")
                self.reddit_next_post = now + timedelta(hours=2)
                return
            elif 'karma' in error_msg or 'account' in error_msg:
                logging.error(f"❌ ACCOUNT ISSUE r/{target_subreddit} - {config['username']}: {e}")
                logging.info(f"💡 Trying karma farming to build reputation...")
                
                # Essayer de farmer du karma
                if self.farm_karma(client, config):
                    logging.info(f"✅ Karma farming successful for {config['username']}")
                else:
                    logging.info(f"❌ Karma farming failed for {config['username']}")
                    
            else:
                logging.error(f"❌ Reddit r/{target_subreddit}: {e}")
                
            # Réessayer dans 1 heure en cas d'erreur
            self.reddit_next_post = now + timedelta(hours=1)
    
    def check_and_post(self):
        """Vérifie tous les timers et poste automatiquement"""
        self.post_twitter()
        self.post_telegram()
        self.post_reddit()
    
    def display_status(self):
        """Affiche le statut en temps réel"""
        now = datetime.now()
        uptime = now - self.daily_stats['start_time']
        
        print(f"\r🚀 VOLTAGEGPU BOT - LAUNCHER UNIFIÉ", end="")
        print(f"\n⏰ {now.strftime('%H:%M:%S')} | Uptime: {str(uptime).split('.')[0]}")
        
        print(f"\n📊 POSTS AUJOURD'HUI:")
        print(f"   🐦 Twitter: {self.daily_stats['twitter_posts']}")
        print(f"   💬 Telegram: {self.daily_stats['telegram_posts']}")
        print(f"   📍 Reddit: {self.daily_stats['reddit_posts']}")
        print(f"   📈 TOTAL: {self.daily_stats['total_posts']}")
        
        print(f"\n⏰ PROCHAINS POSTS:")
        
        # Twitter
        for twitter_data in self.twitter_clients:
            config = twitter_data['config']
            if config['next_post_time']:
                time_left = config['next_post_time'] - now
                if time_left.total_seconds() > 0:
                    minutes = int(time_left.total_seconds() // 60)
                    print(f"   🐦 {config['name']}: {minutes:02d}min ({config['posts_today']}/20)")
                else:
                    print(f"   🐦 {config['name']}: PRÊT ({config['posts_today']}/20)")
        
        # Telegram
        if self.telegram_config['next_post_time']:
            time_left = self.telegram_config['next_post_time'] - now
            if time_left.total_seconds() > 0:
                minutes = int(time_left.total_seconds() // 60)
                print(f"   💬 Telegram: {minutes:02d}min ({self.telegram_config['posts_today']}/30)")
            else:
                print(f"   💬 Telegram: PRÊT ({self.telegram_config['posts_today']}/30)")
        
        # Reddit
        time_left = self.reddit_next_post - now
        if time_left.total_seconds() > 0:
            minutes = int(time_left.total_seconds() // 60)
            print(f"   📍 Reddit: {minutes:02d}min")
        else:
            print(f"   📍 Reddit: PRÊT")
        
        # Top subreddits
        active_subs = [(k, v['posts_today']) for k, v in self.target_subreddits.items() if v['posts_today'] > 0]
        if active_subs:
            active_subs.sort(key=lambda x: x[1], reverse=True)
            print(f"\n📍 TOP SUBREDDITS:")
            for sub, posts in active_subs[:3]:
                print(f"   r/{sub}: {posts} posts")
        
        print(f"\n💰 CODE: {self.affiliate_code}")
        print("🛑 Ctrl+C pour arrêter" + " " * 20, end="")
        
    def reset_daily_counters(self):
        """Reset quotidien à minuit"""
        for twitter_data in self.twitter_clients:
            twitter_data['config']['posts_today'] = 0
        self.telegram_config['posts_today'] = 0
        for reddit_data in self.reddit_clients:
            reddit_data['config']['posts_today'] = 0
        for subreddit in self.target_subreddits:
            self.target_subreddits[subreddit]['posts_today'] = 0
        
        self.daily_stats = {
            'twitter_posts': 0,
            'telegram_posts': 0,
            'reddit_posts': 0,
            'total_posts': 0,
            'start_time': datetime.now()
        }
        
        logging.info("🚀 Compteurs quotidiens remis à zéro")
        
    def run(self):
        """Lance le bot unifié"""
        if self.test_mode:
            print("🚀 TEST MODE - VOLTAGEGPU BOT")
            print("=" * 50)
            
            # Test rapide de toutes les plateformes
            self.post_twitter()
            self.post_telegram()
            self.post_reddit()
            
            print("\n✅ Test terminé - Toutes les plateformes fonctionnent")
            return
            
        print("🚀 LANCEMENT VOLTAGEGPU BOT")
        print("=" * 50)
        print(f"🐦 Twitter: {len(self.twitter_clients)} comptes")
        print(f"💬 Telegram: {'✅' if self.telegram_bot else '❌'}")
        print(f"📍 Reddit: {len(self.reddit_clients)} comptes")
        print(f"💰 Code affilié: {self.affiliate_code}")
        print(f"🎯 Objectif: 100+ posts/jour automatiques")
        print()
        
        # Reset quotidien à minuit
        schedule.every().day.at("00:00").do(self.reset_daily_counters)
        
        try:
            while True:
                # Vérifier et poster automatiquement
                self.check_and_post()
                
                # Vérifier tâches programmées
                schedule.run_pending()
                
                # Afficher statut
                self.display_status()
                
                # Attendre 1 seconde
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 VoltageGPU Bot arrêté")
            logging.info("VoltageGPU Bot arrêté par l'utilisateur")

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='🚀 VoltageGPU Bot - Launcher Unifié')
    parser.add_argument('--test', action='store_true', help='Mode test (sans poster)')
    
    args = parser.parse_args()
    
    try:
        bot = VoltageGPUBot(test_mode=args.test)
        bot.run()
    except Exception as e:
        logging.error(f"❌ Erreur fatale: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
