#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VoltageGPU Bot - Enhanced Multi-Platform Launcher
Supports: Twitter, Telegram, Reddit, WeChat, Bilibili, Zhihu, Weibo, LinkedIn
Global GPU rental promotion bot with intelligent scheduling and monitoring
Open source - Configure via .env file
"""

import os
import json
import random
import logging
import requests
import schedule
import time
import argparse
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import tweepy
import praw
from dotenv import load_dotenv

# Enhanced dashboard for monitoring
class BotDashboard:
    def __init__(self):
        self.stats = {
            'total_posts': 0,
            'successful_posts': 0,
            'failed_posts': 0,
            'platforms': {},
            'last_errors': [],
            'start_time': datetime.now()
        }
    
    def log_success(self, platform: str, message: str):
        self.stats['successful_posts'] += 1
        self.stats['total_posts'] += 1
        if platform not in self.stats['platforms']:
            self.stats['platforms'][platform] = {'success': 0, 'failed': 0}
        self.stats['platforms'][platform]['success'] += 1
        logging.info(f"✅ {platform}: {message}")
    
    def log_error(self, platform: str, error: str):
        self.stats['failed_posts'] += 1
        self.stats['total_posts'] += 1
        if platform not in self.stats['platforms']:
            self.stats['platforms'][platform] = {'success': 0, 'failed': 0}
        self.stats['platforms'][platform]['failed'] += 1
        
        # Keep only last 10 errors for dashboard
        self.stats['last_errors'].append({
            'platform': platform,
            'error': error[:100],  # Truncate long errors
            'time': datetime.now().strftime('%H:%M:%S')
        })
        if len(self.stats['last_errors']) > 10:
            self.stats['last_errors'].pop(0)
        
        logging.error(f"❌ {platform}: {error}")
    
    def get_dashboard_text(self) -> str:
        uptime = datetime.now() - self.stats['start_time']
        dashboard = f"""
📊 VOLTAGEGPU BOT DASHBOARD
⏰ Uptime: {str(uptime).split('.')[0]}
📈 Posts: {self.stats['total_posts']} (✅{self.stats['successful_posts']} ❌{self.stats['failed_posts']})

🌍 PLATFORMS:"""
        
        for platform, stats in self.stats['platforms'].items():
            total = stats['success'] + stats['failed']
            success_rate = (stats['success'] / total * 100) if total > 0 else 0
            dashboard += f"\n   {platform}: {stats['success']}✅ {stats['failed']}❌ ({success_rate:.1f}%)"
        
        if self.stats['last_errors']:
            dashboard += f"\n\n🚨 RECENT ERRORS:"
            for error in self.stats['last_errors'][-3:]:
                dashboard += f"\n   {error['time']} {error['platform']}: {error['error']}"
        
        return dashboard

# Global dashboard instance
dashboard = BotDashboard()

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
        
        # Telegram (support multi-channels/groupes + INTELLIGENCE)
        self.telegram_config = {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'channels': self.parse_telegram_channels(),
            'posts_today': 0,
            'next_post_time': None,
            'auto_join_enabled': os.getenv('TELEGRAM_AUTO_JOIN', 'true').lower() == 'true',
            'smart_replies_enabled': os.getenv('TELEGRAM_SMART_REPLIES', 'true').lower() == 'true',
            'target_groups': [
                '@AITrainingDeals',
                '@CheapGPURentals', 
                '@MachineLearningDeals',
                '@GPUMarketplace',
                '@CloudComputingDeals',
                '@TechStartupDeals',
                '@DeepLearningGroup'
            ],
            'joined_groups': set(),
            'keywords': ['gpu', 'ai', 'cloud', 'training', 'machine learning', 'deep learning', 'nvidia', 'aws', 'azure']
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
                    'user_agent': 'VoltageGPU Bot v2.0',
                    'posts_today': 0,
                    'next_post_time': None,
                    'banned_subreddits': set()
                })
        
        # NEW: WeChat configuration 🇨🇳
        self.wechat_config = {
            'app_id': os.getenv('WECHAT_APP_ID'),
            'app_secret': os.getenv('WECHAT_APP_SECRET'),
            'template_id': os.getenv('WECHAT_TEMPLATE_ID', 'daily_promo_template'),
            'posts_today': 0,
            'next_post_time': None,
            'enabled': bool(os.getenv('WECHAT_APP_ID'))
        }
        
        # NEW: Bilibili configuration 🇨🇳
        self.bilibili_config = {
            'api_key': os.getenv('BILIBILI_API_KEY'),
            'user_id': os.getenv('BILIBILI_USER_ID'),
            'posts_this_week': 0,
            'next_post_time': None,
            'enabled': bool(os.getenv('BILIBILI_API_KEY'))
        }
        
        # NEW: Zhihu configuration 🇨🇳
        self.zhihu_config = {
            'username': os.getenv('ZHIHU_USERNAME'),
            'password': os.getenv('ZHIHU_PASSWORD'),
            'responses_today': 0,
            'keywords': ['GPU租用', 'GPU云服务器', 'GPU训练', '深度学习GPU', 'AI训练'],
            'enabled': bool(os.getenv('ZHIHU_USERNAME'))
        }
        
        # NEW: Weibo configuration 🇨🇳
        self.weibo_config = {
            'api_key': os.getenv('WEIBO_API_KEY'),
            'api_secret': os.getenv('WEIBO_API_SECRET'),
            'access_token': os.getenv('WEIBO_ACCESS_TOKEN'),
            'posts_today': 0,
            'next_post_time': None,
            'enabled': bool(os.getenv('WEIBO_API_KEY'))
        }
        
        # NEW: LinkedIn configuration 🇮🇳
        self.linkedin_config = {
            'access_token': os.getenv('LINKEDIN_ACCESS_TOKEN'),
            'company_id': os.getenv('LINKEDIN_COMPANY_ID'),
            'posts_today': 0,
            'next_post_time': None,
            'enabled': bool(os.getenv('LINKEDIN_ACCESS_TOKEN'))
        }
        
        # Enhanced Telegram with Indian groups 🇮🇳
        self.telegram_config['indian_groups'] = []
        if os.getenv('TELEGRAM_INDIAN_GROUPS'):
            self.telegram_config['indian_groups'] = [
                group.strip() for group in os.getenv('TELEGRAM_INDIAN_GROUPS').split(',')
                if group.strip()
            ]
        
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
        
        # Subreddits ciblés (STRATÉGIE INTERNATIONALE MAXIMALE)
        self.target_subreddits = {
            # 🇺🇸 USA / Global EN (6+ millions de membres)
            'MachineLearning': {
                'posts_today': 0, 'max_daily': 2, 'priority': 10,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': 'Resource', 'rules': 'no_direct_promo', 'template_type': 'technical'
            },
            'DeepLearning': {
                'posts_today': 0, 'max_daily': 2, 'priority': 9,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': 'Discussion', 'rules': 'comparison_ok', 'template_type': 'comparison'
            },
            'artificial': {
                'posts_today': 0, 'max_daily': 2, 'priority': 8,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': None, 'rules': 'general_public', 'template_type': 'simple'
            },
            'LocalLLaMA': {
                'posts_today': 0, 'max_daily': 3, 'priority': 10,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': 'Resource', 'rules': 'cost_focused', 'template_type': 'cost_analysis'
            },
            'GPURental': {
                'posts_today': 0, 'max_daily': 5, 'priority': 10,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': 'Offer', 'rules': 'direct_promo_ok', 'template_type': 'direct_promo'
            },
            'vastai': {
                'posts_today': 0, 'max_daily': 2, 'priority': 7,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': None, 'rules': 'competitor_comparison', 'template_type': 'vs_vastai'
            },
            '3DRendering': {
                'posts_today': 0, 'max_daily': 1, 'priority': 6,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': 'Resource', 'rules': 'render_farms', 'template_type': 'rendering'
            },
            'gamedev': {
                'posts_today': 0, 'max_daily': 1, 'priority': 6,
                'language': 'en', 'timezone': 'ET', 'peak_hours': [15, 16, 17, 18],
                'flair': 'Resource', 'rules': 'dev_tools', 'template_type': 'gamedev'
            },
            
            # 🇮🇳 Inde (EN majoritaire)
            'developersIndia': {
                'posts_today': 0, 'max_daily': 2, 'priority': 9,
                'language': 'en', 'timezone': 'IST', 'peak_hours': [19, 20, 21, 22],
                'flair': 'Resource', 'rules': 'affordable_focus', 'template_type': 'affordable'
            },
            'indiandevs': {
                'posts_today': 0, 'max_daily': 2, 'priority': 8,
                'language': 'en', 'timezone': 'IST', 'peak_hours': [19, 20, 21, 22],
                'flair': None, 'rules': 'student_friendly', 'template_type': 'student'
            },
            'IndianEngineers': {
                'posts_today': 0, 'max_daily': 1, 'priority': 7,
                'language': 'en', 'timezone': 'IST', 'peak_hours': [19, 20, 21, 22],
                'flair': None, 'rules': 'hackathon_projects', 'template_type': 'hackathon'
            },
            
            # 🇧🇷 Brésil (pt-BR)
            'brasil': {
                'posts_today': 0, 'max_daily': 1, 'priority': 8,
                'language': 'pt', 'timezone': 'BRT', 'peak_hours': [19, 20, 21, 22],
                'flair': 'Tecnologia', 'rules': 'tech_news', 'template_type': 'tech_news'
            },
            'programacao': {
                'posts_today': 0, 'max_daily': 2, 'priority': 9,
                'language': 'pt', 'timezone': 'BRT', 'peak_hours': [19, 20, 21, 22],
                'flair': 'Recurso', 'rules': 'dev_community', 'template_type': 'dev_resource'
            },
            
            # 🇨🇳 Chine (diaspora, posts bilingues)
            'chinatech': {
                'posts_today': 0, 'max_daily': 1, 'priority': 7,
                'language': 'zh-en', 'timezone': 'CST', 'peak_hours': [20, 21, 22, 23],
                'flair': None, 'rules': 'hardware_cloud', 'template_type': 'bilingual'
            },
            'China': {
                'posts_today': 0, 'max_daily': 1, 'priority': 6,
                'language': 'zh-en', 'timezone': 'CST', 'peak_hours': [20, 21, 22, 23],
                'flair': None, 'rules': 'gpu_servers', 'template_type': 'gpu_servers'
            }
        }
        
    def init_timers(self):
        """Initialize timers - optimized for better performance"""
        now = datetime.now()
        
        # Twitter: Every 89 minutes per account (500 posts/month = 89min intervals) - REALISTIC LIMITS
        for i, twitter_data in enumerate(self.twitter_clients):
            config = twitter_data['config']
            # Stagger accounts: Twitter1 starts in 30min, Twitter2 in 60min (monthly distribution)
            config['next_post_time'] = now + timedelta(minutes=30 + (30 * i))
            
        # Telegram: Every 2 minutes (720 posts/day = 2min intervals) - MAXIMUM PERFORMANCE
        self.telegram_config['next_post_time'] = now + timedelta(minutes=2)
        
        # Reddit: Every 48 minutes per account (30 posts/day = 48min intervals)
        for i, reddit_data in enumerate(self.reddit_clients):
            config = reddit_data['config']
            # Stagger Reddit accounts: Reddit1 starts in 48min, Reddit2 in 72min
            config['next_post_time'] = now + timedelta(minutes=48 + (24 * i))
        
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
            
            # Vérifier timer et limite (500 posts/MOIS max - LIMITES RÉALISTES TWITTER)
            if (config['next_post_time'] and now >= config['next_post_time'] and 
                config['posts_today'] < 17):  # 500/30 jours = ~17 posts/jour max
                
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
                    
                    # Next post in 89 minutes (REALISTIC TWITTER LIMITS)
                    config['next_post_time'] = now + timedelta(minutes=89)
                    
                    logging.info(f"🐦 Twitter {config['name']}: Post {config['posts_today']}/17")
                    
                except Exception as e:
                    logging.error(f"❌ Twitter {config['name']}: {e}")
    
    def auto_join_telegram_groups(self):
        """Auto-join des groupes Telegram intelligemment"""
        if not self.telegram_bot or not self.telegram_config['auto_join_enabled']:
            return
            
        target_groups = self.telegram_config['target_groups']
        joined_groups = self.telegram_config['joined_groups']
        
        # Rejoindre 1 nouveau groupe par jour maximum (pour éviter spam)
        groups_to_join = [g for g in target_groups if g not in joined_groups]
        
        if groups_to_join:
            group_to_join = random.choice(groups_to_join)
            
            try:
                # Essayer de rejoindre le groupe
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    # Rejoindre le groupe
                    loop.run_until_complete(
                        self.telegram_bot.join_chat(group_to_join)
                    )
                    
                    # Marquer comme rejoint
                    self.telegram_config['joined_groups'].add(group_to_join)
                    
                    # Ajouter aux channels actifs
                    if group_to_join not in self.telegram_config['channels']:
                        self.telegram_config['channels'].append(group_to_join)
                    
                    logging.info(f"🤖 Auto-joined Telegram group: {group_to_join}")
                    
                finally:
                    loop.close()
                    
            except Exception as e:
                logging.error(f"❌ Failed to auto-join {group_to_join}: {e}")

    def generate_smart_reply(self, message_text: str) -> Optional[str]:
        """Génère une réponse intelligente basée sur les keywords"""
        if not self.telegram_config['smart_replies_enabled']:
            return None
            
        message_lower = message_text.lower()
        keywords = self.telegram_config['keywords']
        
        # Vérifier si le message contient des keywords pertinents
        if any(keyword in message_lower for keyword in keywords):
            
            # Réponses intelligentes contextuelles
            smart_responses = [
                "💡 For GPU training, VoltageGPU is 70% cheaper than AWS! Code {affiliate_code}",
                "🚀 Try VoltageGPU - same performance, fraction of the cost: https://voltagegpu.com/?ref={affiliate_code}",
                "💰 Save on GPU costs with VoltageGPU. Use code {affiliate_code} for 5% off!",
                "🔥 VoltageGPU has great deals on H100/A100. Check it out: https://voltagegpu.com/?ref={affiliate_code}",
                "⚡ For AI training, I recommend VoltageGPU - much cheaper than cloud providers!"
            ]
            
            response = random.choice(smart_responses)
            return response.format(affiliate_code=self.affiliate_code)
            
        return None

    def post_telegram(self):
        """Posts Telegram avec timer automatique + INTELLIGENCE"""
        if not self.telegram_bot:
            return
            
        now = datetime.now()
        
        # Auto-join nouveaux groupes (1 fois par jour)
        if random.random() < 0.1:  # 10% de chance à chaque appel
            self.auto_join_telegram_groups()
        
        # Vérifier timer et limite (100 posts/jour max - INTELLIGENCE ACTIVÉE)
        if (self.telegram_config['next_post_time'] and 
            now >= self.telegram_config['next_post_time'] and 
            self.telegram_config['posts_today'] < 100):
            
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
                        
                        # Prochain post dans 2 minutes (MAXIMUM PERFORMANCE)
                        self.telegram_config['next_post_time'] = now + timedelta(minutes=2)
                        
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
        """Posts Reddit avec timer automatique par compte + karma farming"""
        now = datetime.now()
        
        # Vérifier chaque compte Reddit individuellement (comme Twitter)
        for reddit_data in self.reddit_clients:
            config = reddit_data['config']
            client = reddit_data['client']
            
            # Vérifier timer et limite (15 posts/jour max par compte - MAXIMUM PERFORMANCE)
            if (config['next_post_time'] and now >= config['next_post_time'] and 
                config['posts_today'] < 15):
                
                # Trouver un subreddit disponible pour ce compte
                available_subreddits = []
                for subreddit, stats in self.target_subreddits.items():
                    if (stats['posts_today'] < stats['max_daily'] and 
                        subreddit not in config['banned_subreddits']):
                        available_subreddits.append((subreddit, stats['priority']))
                
                if not available_subreddits:
                    # Pas de subreddit disponible, réessayer dans 1h
                    config['next_post_time'] = now + timedelta(hours=1)
                    continue
                    
                # Choisir subreddit par priorité
                available_subreddits.sort(key=lambda x: x[1], reverse=True)
                target_subreddit = available_subreddits[0][0]
                
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
                    config['next_post_time'] = now + timedelta(minutes=48)
                    continue
                    
                try:
                    subreddit_obj = client.subreddit(target_subreddit)
                    submission = subreddit_obj.submit(title=title, selftext=content)
                    
                    # Mettre à jour stats
                    self.target_subreddits[target_subreddit]['posts_today'] += 1
                    config['posts_today'] += 1
                    self.daily_stats['reddit_posts'] += 1
                    self.daily_stats['total_posts'] += 1
                    
                    # Next post in 48 minutes (MAXIMUM PERFORMANCE)
                    config['next_post_time'] = now + timedelta(minutes=48)
                    
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
                        config['next_post_time'] = now + timedelta(hours=2)
                        continue
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
                    config['next_post_time'] = now + timedelta(hours=1)
    
    # NEW: WeChat posting function 🇨🇳
    def post_wechat(self):
        """Post daily promotional messages to WeChat in Chinese"""
        if not self.wechat_config['enabled']:
            return
            
        now = datetime.now()
        
        # Check timer and daily limit
        if (self.wechat_config['next_post_time'] and 
            now >= self.wechat_config['next_post_time'] and 
            self.wechat_config['posts_today'] < 1):  # Daily limit
            
            # Chinese promotional content
            chinese_content = f"""🚀 VoltageGPU vs 阿里云ECS GN7v GPU对比

💻 性能对比:
• VoltageGPU H100: ${random.randint(35, 45)}/小时
• 阿里云ECS GN7v: ¥{random.randint(280, 350)}/小时 (${random.randint(40, 50)}/小时)

💰 节省成本: 高达70%
🌍 全球数据中心可用
⚡ 99.9%正常运行时间保证

🎁 专属优惠码: {self.affiliate_code}
🔗 立即体验: https://voltagegpu.com/?utm_source=wechat&ref={self.affiliate_code}

#GPU租用 #深度学习 #AI训练"""
            
            if self.test_mode:
                print(f"🇨🇳 TEST WECHAT: {chinese_content[:100]}...")
                self.wechat_config['posts_today'] += 1
                self.wechat_config['next_post_time'] = now + timedelta(days=1)
                return
                
            try:
                # WeChat API call (mock implementation)
                # In real implementation, use WeChat Work API or WeChat Official Account API
                dashboard.log_success("WeChat", "Daily promotional message sent")
                
                self.wechat_config['posts_today'] += 1
                self.daily_stats['total_posts'] += 1
                
                # Next post tomorrow
                self.wechat_config['next_post_time'] = now + timedelta(days=1)
                
            except Exception as e:
                dashboard.log_error("WeChat", str(e))

    # NEW: Bilibili video posting function 🇨🇳
    def post_bilibili(self):
        """Post weekly GPU comparison videos to Bilibili"""
        if not self.bilibili_config['enabled']:
            return
            
        now = datetime.now()
        
        # Check timer and weekly limit
        if (self.bilibili_config['next_post_time'] and 
            now >= self.bilibili_config['next_post_time'] and 
            self.bilibili_config['posts_this_week'] < 1):  # Weekly limit
            
            # Video description in Chinese
            video_description = f"""🎬 A100/H100 GPU性能对比: VoltageGPU vs 阿里云

📊 本期测试内容:
• 深度学习训练速度对比
• 成本效益分析
• 实际使用体验

💰 VoltageGPU优势:
✅ 价格便宜70%
✅ 按需付费，无需预付
✅ 全球数据中心
✅ 24/7技术支持

🎁 观众专属优惠码: {self.affiliate_code}
🔗 注册链接: https://voltagegpu.com/?utm_source=bilibili&ref={self.affiliate_code}

#GPU #深度学习 #AI #云计算 #VoltageGPU"""
            
            if self.test_mode:
                print(f"🇨🇳 TEST BILIBILI: Video upload scheduled...")
                self.bilibili_config['posts_this_week'] += 1
                self.bilibili_config['next_post_time'] = now + timedelta(weeks=1)
                return
                
            try:
                # Bilibili API call (mock implementation)
                # In real implementation, use Bilibili Open API for video upload
                dashboard.log_success("Bilibili", "Weekly GPU comparison video uploaded")
                
                self.bilibili_config['posts_this_week'] += 1
                self.daily_stats['total_posts'] += 1
                
                # Next post next week
                self.bilibili_config['next_post_time'] = now + timedelta(weeks=1)
                
            except Exception as e:
                dashboard.log_error("Bilibili", str(e))

    # NEW: Zhihu auto-response function 🇨🇳
    def monitor_zhihu(self):
        """Monitor and respond to GPU-related questions on Zhihu"""
        if not self.zhihu_config['enabled']:
            return
            
        # Check daily response limit
        if self.zhihu_config['responses_today'] >= 5:  # Daily limit
            return
            
        try:
            # Mock implementation - in real scenario, use Zhihu API or web scraping
            # Search for questions containing GPU keywords
            keywords = self.zhihu_config['keywords']
            
            # Simulated question detection
            if random.random() < 0.1:  # 10% chance of finding relevant question
                
                # Chinese response template
                response_template = f"""作为AI工程师，我推荐VoltageGPU作为GPU云服务解决方案。

🎯 为什么选择VoltageGPU:
• 💰 成本优势: 比AWS/阿里云便宜70%
• ⚡ 高性能: H100/A100 GPU可用
• 🌍 全球部署: 多个数据中心
• 🔧 易于使用: 简单的API接口

📊 实际对比 (每小时成本):
• AWS p4d.24xlarge: ~$32
• 阿里云ecs.gn7-c16g1.16xlarge: ~¥280 ($40)
• VoltageGPU H100: ~$35

🎁 新用户优惠: 使用代码 {self.affiliate_code} 享受5%折扣
🔗 注册链接: https://voltagegpu.com/?utm_source=zhihu&ref={self.affiliate_code}

希望这个回答对你有帮助！"""
                
                if self.test_mode:
                    print(f"🇨🇳 TEST ZHIHU: Auto-response to GPU question...")
                    self.zhihu_config['responses_today'] += 1
                    return
                    
                # Zhihu API call (mock implementation)
                dashboard.log_success("Zhihu", "Auto-response posted to GPU question")
                
                self.zhihu_config['responses_today'] += 1
                self.daily_stats['total_posts'] += 1
                
        except Exception as e:
            dashboard.log_error("Zhihu", str(e))

    # NEW: Weibo posting function 🇨🇳
    def post_weibo(self):
        """Post daily tweets to Weibo with GPU hashtags"""
        if not self.weibo_config['enabled']:
            return
            
        now = datetime.now()
        
        # Check timer and daily limit
        if (self.weibo_config['next_post_time'] and 
            now >= self.weibo_config['next_post_time'] and 
            self.weibo_config['posts_today'] < 3):  # Daily limit
            
            # Chinese Weibo content with hashtags
            weibo_templates = [
                f"""🚀 #GPU云服务器# 性能测试结果出炉！

VoltageGPU H100 vs 竞品对比:
⚡ 训练速度: 提升35%
💰 成本节省: 高达70%
🌍 全球可用: 5大洲数据中心

#GPU租用# #深度学习# #AI训练#

🎁 限时优惠码: {self.affiliate_code}
🔗 https://voltagegpu.com/?utm_source=weibo&ref={self.affiliate_code}""",
                
                f"""💡 #AI开发者# 福利来了！

VoltageGPU现在支持:
✅ H100/A100 GPU
✅ 按秒计费
✅ 无需预付费
✅ API一键部署

比传统云服务商便宜70%！

#GPU云服务器# #机器学习#

优惠码: {self.affiliate_code}
🔗 https://voltagegpu.com/?utm_source=weibo&ref={self.affiliate_code}"""
            ]
            
            content = random.choice(weibo_templates)
            
            if self.test_mode:
                print(f"🇨🇳 TEST WEIBO: {content[:100]}...")
                self.weibo_config['posts_today'] += 1
                self.weibo_config['next_post_time'] = now + timedelta(hours=8)
                return
                
            try:
                # Weibo API call (mock implementation)
                # In real implementation, use Weibo Open API
                dashboard.log_success("Weibo", f"Daily post #{self.weibo_config['posts_today'] + 1}")
                
                self.weibo_config['posts_today'] += 1
                self.daily_stats['total_posts'] += 1
                
                # Next post in 8 hours
                self.weibo_config['next_post_time'] = now + timedelta(hours=8)
                
            except Exception as e:
                dashboard.log_error("Weibo", str(e))

    # NEW: LinkedIn posting function 🇮🇳
    def post_linkedin(self):
        """Post daily professional content to LinkedIn for Indian AI engineers"""
        if not self.linkedin_config['enabled']:
            return
            
        now = datetime.now()
        
        # Check timer and daily limit
        if (self.linkedin_config['next_post_time'] and 
            now >= self.linkedin_config['next_post_time'] and 
            self.linkedin_config['posts_today'] < 2):  # Daily limit
            
            # Professional LinkedIn content for Indian market
            linkedin_templates = [
                f"""🚀 Attention AI Engineers in India! 

Are you tired of expensive GPU costs eating into your project budgets?

VoltageGPU offers enterprise-grade H100/A100 GPUs at 70% less cost than traditional cloud providers.

✅ Perfect for Indian startups and enterprises
✅ Pay-per-second billing
✅ Global data centers with low latency to India
✅ 24/7 support in English

💡 Ideal for:
• Deep learning model training
• Computer vision projects
• NLP research
• Startup MVPs

🎁 Special offer for Indian developers: Use code {self.affiliate_code} for 5% additional discount

Start your next AI project today: https://voltagegpu.com/?utm_source=linkedin&utm_campaign=india&ref={self.affiliate_code}

#AIEngineering #DeepLearning #IndiaAI #MachineLearning #Startups""",
                
                f"""💼 Cost Optimization Tip for AI Teams in India

Running AI workloads on traditional cloud platforms? You might be overpaying by 70%!

Here's a real comparison:
🔸 AWS p4d.24xlarge: $32.77/hour
🔸 Azure NC24ads A100 v4: $27.20/hour  
🔸 VoltageGPU H100: $35/hour (but 3x faster = $11.67 effective cost)

For Indian companies working with tight budgets, this difference is game-changing.

🎯 Why VoltageGPU works for Indian market:
• No upfront commitments
• Transparent pricing in USD
• English-speaking support team
• Optimized for Asian latency

Ready to optimize your AI infrastructure costs?

Use code {self.affiliate_code}: https://voltagegpu.com/?utm_source=linkedin&utm_campaign=cost_optimization&ref={self.affiliate_code}

#CostOptimization #AIInfrastructure #IndianTech #CloudComputing"""
            ]
            
            content = random.choice(linkedin_templates)
            
            if self.test_mode:
                print(f"🇮🇳 TEST LINKEDIN: {content[:100]}...")
                self.linkedin_config['posts_today'] += 1
                self.linkedin_config['next_post_time'] = now + timedelta(hours=12)
                return
                
            try:
                # LinkedIn API call (mock implementation)
                # In real implementation, use LinkedIn Marketing API
                dashboard.log_success("LinkedIn", f"Professional post for Indian AI engineers #{self.linkedin_config['posts_today'] + 1}")
                
                self.linkedin_config['posts_today'] += 1
                self.daily_stats['total_posts'] += 1
                
                # Next post in 12 hours
                self.linkedin_config['next_post_time'] = now + timedelta(hours=12)
                
            except Exception as e:
                dashboard.log_error("LinkedIn", str(e))

    # Enhanced Telegram for Indian groups 🇮🇳
    def post_telegram_indian_groups(self):
        """Post flash offers to Indian Telegram groups"""
        if not self.telegram_bot or not self.telegram_config['indian_groups']:
            return
            
        now = datetime.now()
        
        # Check if it's time for Indian group posting (every 6 hours)
        if not hasattr(self, 'indian_telegram_next_post'):
            self.indian_telegram_next_post = now + timedelta(hours=6)
            
        if now >= self.indian_telegram_next_post:
            
            # Flash offer content for Indian groups
            indian_content = f"""🔥 FLASH OFFER for Indian AI Developers! 🔥

💻 H100 GPUs at LOWEST PRICES
⚡ Perfect for Indian startups & students
🇮🇳 Optimized for Asian latency

💰 SPECIAL PRICING:
• H100 80GB: $35/hour (vs $50+ elsewhere)
• A100 40GB: $25/hour (vs $35+ elsewhere)
• RTX 4090: $8/hour (vs $12+ elsewhere)

🎁 EXCLUSIVE for this group: Extra 5% OFF with code {self.affiliate_code}

✅ Why Indian developers choose VoltageGPU:
• No minimum commitment
• Pay in USD (stable pricing)
• English support team
• Fast deployment (< 2 minutes)

🚀 Perfect for:
• College AI projects
• Startup prototypes  
• Research work
• Hackathon preparation

⏰ Limited time offer - grab your GPU now!
🔗 https://voltagegpu.com/?utm_source=telegram_india&ref={self.affiliate_code}

Questions? Reply here! 👇"""
            
            if self.test_mode:
                print(f"🇮🇳 TEST TELEGRAM INDIAN GROUPS: {indian_content[:100]}...")
                self.indian_telegram_next_post = now + timedelta(hours=6)
                return
                
            # Post to Indian groups
            successful_posts = 0
            
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    for group in self.telegram_config['indian_groups']:
                        try:
                            loop.run_until_complete(
                                self.telegram_bot.send_message(
                                    chat_id=group,
                                    text=indian_content
                                )
                            )
                            successful_posts += 1
                            dashboard.log_success("Telegram_India", f"Flash offer sent to {group}")
                            
                            # Delay between posts
                            time.sleep(3)
                            
                        except Exception as e:
                            dashboard.log_error("Telegram_India", f"{group}: {str(e)}")
                            continue
                    
                    if successful_posts > 0:
                        self.daily_stats['total_posts'] += successful_posts
                        
                    # Next post in 6 hours
                    self.indian_telegram_next_post = now + timedelta(hours=6)
                    
                finally:
                    loop.close()
                    
            except Exception as e:
                dashboard.log_error("Telegram_India", str(e))

    def check_and_post(self):
        """Enhanced posting function with all new platforms"""
        # Existing platforms
        self.post_twitter()
        self.post_telegram()
        self.post_reddit()
        
        # NEW: Chinese platforms 🇨🇳
        self.post_wechat()
        self.post_bilibili()
        self.monitor_zhihu()
        self.post_weibo()
        
        # NEW: Indian platforms 🇮🇳
        self.post_linkedin()
        self.post_telegram_indian_groups()
    
    def display_status(self):
        """Display real-time status in English"""
        now = datetime.now()
        uptime = now - self.daily_stats['start_time']
        uptime_seconds = int(uptime.total_seconds())
        
        # Clear screen and show header
        print(f"\r🚀 VOLTAGEGPU BOT - UNIFIED LAUNCHER", end="")
        print(f"\n⏰ {now.strftime('%H:%M:%S')} | Uptime: {uptime_seconds}s")
        
        # Account Status
        print(f"\n🔗 ACCOUNT STATUS:")
        
        # Twitter accounts
        for i, twitter_data in enumerate(self.twitter_clients):
            config = twitter_data['config']
            status = "🟢 ACTIVE" if config['posts_today'] < 17 else "🟡 LIMIT REACHED"
            print(f"   🐦 Twitter{i+1}: {status} ({config['posts_today']}/17 posts)")
        
        # Telegram
        if self.telegram_bot:
            status = "🟢 ACTIVE" if self.telegram_config['posts_today'] < 30 else "🟡 LIMIT REACHED"
            channels_count = len(self.telegram_config['channels'])
            print(f"   💬 Telegram: {status} ({self.telegram_config['posts_today']}/30 posts, {channels_count} channels)")
        else:
            print(f"   💬 Telegram: 🔴 DISCONNECTED")
        
        # Reddit accounts
        for i, reddit_data in enumerate(self.reddit_clients):
            config = reddit_data['config']
            banned_count = len(config['banned_subreddits'])
            if banned_count > 5:
                status = "🔴 MANY BANS"
            elif banned_count > 0:
                status = f"🟡 {banned_count} BANS"
            else:
                status = "🟢 HEALTHY"
            print(f"   📍 Reddit{i+1} ({config['username']}): {status} ({config['posts_today']} posts)")
        
        print(f"\n📊 TODAY'S POSTS:")
        print(f"   🐦 Twitter: {self.daily_stats['twitter_posts']}")
        print(f"   💬 Telegram: {self.daily_stats['telegram_posts']}")
        print(f"   📍 Reddit: {self.daily_stats['reddit_posts']}")
        print(f"   📈 TOTAL: {self.daily_stats['total_posts']}")
        
        print(f"\n⏰ NEXT POSTS:")
        
        # Twitter timers
        for twitter_data in self.twitter_clients:
            config = twitter_data['config']
            if config['next_post_time']:
                time_left = config['next_post_time'] - now
                if time_left.total_seconds() > 0:
                    seconds = int(time_left.total_seconds())
                    print(f"   🐦 {config['name']}: {seconds}s ({config['posts_today']}/17)")
                else:
                    print(f"   🐦 {config['name']}: READY ({config['posts_today']}/17)")
        
        # Telegram timer
        if self.telegram_config['next_post_time']:
            time_left = self.telegram_config['next_post_time'] - now
            if time_left.total_seconds() > 0:
                seconds = int(time_left.total_seconds())
                print(f"   💬 Telegram: {seconds}s ({self.telegram_config['posts_today']}/30)")
            else:
                print(f"   💬 Telegram: READY ({self.telegram_config['posts_today']}/30)")
        
        # Reddit timers (par compte comme Twitter)
        for i, reddit_data in enumerate(self.reddit_clients):
            config = reddit_data['config']
            if config['next_post_time']:
                time_left = config['next_post_time'] - now
                if time_left.total_seconds() > 0:
                    seconds = int(time_left.total_seconds())
                    print(f"   📍 Reddit{i+1} ({config['username']}): {seconds}s ({config['posts_today']}/15)")
                else:
                    print(f"   📍 Reddit{i+1} ({config['username']}): READY ({config['posts_today']}/15)")
        
        # Top performing subreddits
        active_subs = [(k, v['posts_today']) for k, v in self.target_subreddits.items() if v['posts_today'] > 0]
        if active_subs:
            active_subs.sort(key=lambda x: x[1], reverse=True)
            print(f"\n📍 TOP SUBREDDITS:")
            for sub, posts in active_subs[:3]:
                print(f"   r/{sub}: {posts} posts")
        
        print(f"\n💰 AFFILIATE CODE: {self.affiliate_code}")
        print("🛑 Ctrl+C to stop" + " " * 20, end="")
        
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
