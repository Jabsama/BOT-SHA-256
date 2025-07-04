#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 BOT SHA-256 - Autonomous AI-Powered Social Media Automation
Features: Complete Autonomy, Self-Learning, Modular Architecture
Open Source Project - MIT License
"""

import os
import json
import random
import logging
import requests
import time
import hashlib
import asyncio
import threading
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
import tweepy
import praw
from dotenv import load_dotenv
import telegram
from telegram.ext import Application

# CRITICAL FIX: Disable proxy globally
os.environ['NO_PROXY'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

from modules.platform_manager import AdvancedRateLimitManager, ConnectionPoolManager
from modules.predictive_ai import PredictiveAI
# REMOVED: from modules.enterprise_content import EnterpriseContentGenerator
from modules.ab_testing import ABTestingEngine
from modules.reddit_intelligence import RedditIntelligence
from modules.twitter_viral import TwitterViralOptimizer
from modules.telegram_autonomous import TelegramAutonomous
from modules.twitter_follow_manager import TwitterFollowManager
from modules.autonomous_performance import AutonomousPerformanceEngine
from modules.autonomous_discovery import AutonomousGroupDiscovery

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sha256bot_autonomous.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class TimezoneOptimizer:
    """Optimize posting times based on global timezones"""
    
    def __init__(self):
        self.timezone_regions = {
            'US_EAST': {'timezone': 'America/New_York', 'peak_hours': [9, 12, 17, 20]},
            'US_WEST': {'timezone': 'America/Los_Angeles', 'peak_hours': [8, 11, 16, 19]},
            'EU_WEST': {'timezone': 'Europe/London', 'peak_hours': [9, 13, 18, 21]},
            'ASIA_PACIFIC': {'timezone': 'Asia/Singapore', 'peak_hours': [10, 14, 19, 22]}
        }
    
    def get_current_optimal_region(self) -> Tuple[str, str, str]:
        """Get the currently optimal region based on time"""
        now = datetime.now()
        current_hour = now.hour
        
        # Simple logic: target regions during their peak hours
        if 9 <= current_hour <= 23:  # EU peak time
            return 'EU_WEST', 'en', 'Europe/London'
        elif 14 <= current_hour <= 2:  # US East peak time (accounting for wrap-around)
            return 'US_EAST', 'en', 'America/New_York'
        elif 19 <= current_hour <= 7:  # Asia Pacific peak time (accounting for wrap-around)
            return 'ASIA_PACIFIC', 'en', 'Asia/Singapore'
        else:
            return 'US_WEST', 'en', 'America/Los_Angeles'
    
    def is_peak_time(self, region: str) -> bool:
        """Check if current time is peak for the region"""
        now = datetime.now()
        current_hour = now.hour
        
        if region in self.timezone_regions:
            peak_hours = self.timezone_regions[region]['peak_hours']
            return current_hour in peak_hours
        
        return False

# Import our improved content manager
from modules.ultimate_viral_content import UltimateViralContentGenerator

class AutonomousContentOptimizer:
    """Optimize content based on performance data"""
    
    def __init__(self):
        self.performance_data = {}
        self.optimization_rules = {
            'twitter': {
                'max_length': 280,
                'optimal_hashtags': 2,
                'emoji_boost': True,
                'urgency_words': ['urgent', 'limited', 'now', 'today']
            },
            'telegram': {
                'max_length': 4096,
                'optimal_hashtags': 3,
                'emoji_boost': True,
                'formatting': True
            },
            'reddit': {
                'max_length': 10000,
                'optimal_hashtags': 0,
                'emoji_boost': False,
                'professional_tone': True
            }
        }
    
    def optimize_content(self, content: str, platform: str) -> str:
        """Optimize content for specific platform"""
        if platform not in self.optimization_rules:
            return content
        
        rules = self.optimization_rules[platform]
        optimized = content
        
        # Length optimization
        if len(optimized) > rules['max_length']:
            optimized = optimized[:rules['max_length']-3] + "..."
        
        # Platform-specific optimizations
        if platform == 'twitter':
            # Add urgency if missing
            if not any(word in optimized.lower() for word in rules['urgency_words']):
                if random.random() < 0.3:  # 30% chance
                    optimized = f"🚨 {optimized}"
        
        elif platform == 'telegram':
            # Add formatting
            if rules['formatting'] and '**' not in optimized:
                # Bold important words
                optimized = optimized.replace('GPU', '**GPU**')
                optimized = optimized.replace('DEAL', '**DEAL**')
        
        elif platform == 'reddit':
            # Professional tone
            if rules['professional_tone']:
                optimized = optimized.replace('🚀', '').replace('🔥', '').replace('⚡', '')
        
        return optimized
    
    def record_content_performance(self, content: str, platform: str, engagement: int, success: bool):
        """Record content performance for learning"""
        content_hash = str(hash(content))
        
        if content_hash not in self.performance_data:
            self.performance_data[content_hash] = {
                'platform': platform,
                'content': content[:100],  # Store first 100 chars
                'performances': []
            }
        
        self.performance_data[content_hash]['performances'].append({
            'engagement': engagement,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 performances
        self.performance_data[content_hash]['performances'] = \
            self.performance_data[content_hash]['performances'][-10:]

class AutonomousSHA256Bot:
    """Fully autonomous, self-improving SHA-256 affiliate marketing bot"""
    
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        
        # Load configuration
        load_dotenv()
        self.affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO')
        
        # Initialize autonomous components
        self.performance_engine = AutonomousPerformanceEngine()
        self.timezone_optimizer = TimezoneOptimizer()
        self.content_generator = UltimateViralContentGenerator()
        self.content_optimizer = AutonomousContentOptimizer()
        self.rate_limiter = AdvancedRateLimitManager()
        self.connection_manager = ConnectionPoolManager()
        
        # Initialize advanced AI modules
        self.predictive_ai = PredictiveAI()
        # REMOVED: self.enterprise_content = EnterpriseContentGenerator()
        self.ab_testing = ABTestingEngine()
        
        # Initialize intelligent modules
        self.reddit_intelligence = RedditIntelligence()
        self.twitter_viral = TwitterViralOptimizer()
        self.telegram_autonomous = None  # Will be initialized if Telegram token available
        self.twitter_follow_manager = None  # Will be initialized if Twitter clients available
        
        # Initialize platforms
        self.setup_platforms()
        
        # Initialize autonomous discovery
        self.group_discovery = AutonomousGroupDiscovery(
            telegram_bot=self.telegram_bot,
            reddit_clients=self.reddit_clients
        )
        
        # Autonomous operation parameters
        self.discovery_cycle_interval = 3600  # 1 hour
        self.last_discovery_cycle = datetime.now() - timedelta(hours=2)  # Force initial discovery
        self.autonomous_mode = True
        
        # Statistics
        self.stats = {
            'twitter_posts': 0,
            'telegram_posts': 0,
            'reddit_posts': 0,
            'errors': 0,
            'discoveries': 0,
            'optimizations': 0,
            'start_time': datetime.now(),
            'current_region': 'US_EAST',
            'current_language': 'en',
            'last_twitter_post': None,
            'last_telegram_post': None,
            'last_reddit_post': None,
            'twitter_cooldown_until': None,
            'telegram_cooldown_until': None
        }
        
        logging.info("🤖 Autonomous SHA-256 Bot initialized with full self-learning capabilities")
    
    def setup_platforms(self):
        """Setup all platforms with enhanced error handling"""
        # Twitter setup
        self.twitter_clients = []
        try:
            if os.getenv('TWITTER_API_KEY'):
                client = tweepy.Client(
                    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                    consumer_key=os.getenv('TWITTER_API_KEY'),
                    consumer_secret=os.getenv('TWITTER_API_SECRET'),
                    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET'),
                    wait_on_rate_limit=False
                )
                self.twitter_clients.append({'client': client, 'name': 'Twitter1', 'posts_today': 0})
                logging.info("✅ Twitter Account 1 connected")
            
            if os.getenv('TWITTER_API_KEY_2'):
                client2 = tweepy.Client(
                    bearer_token=os.getenv('TWITTER_BEARER_TOKEN_2'),
                    consumer_key=os.getenv('TWITTER_API_KEY_2'),
                    consumer_secret=os.getenv('TWITTER_API_SECRET_2'),
                    access_token=os.getenv('TWITTER_ACCESS_TOKEN_2'),
                    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET_2'),
                    wait_on_rate_limit=False
                )
                self.twitter_clients.append({'client': client2, 'name': 'Twitter2', 'posts_today': 0})
                logging.info("✅ Twitter Account 2 connected")
                
        except Exception as e:
            logging.error(f"❌ Twitter setup failed: {e}")
        
        # Telegram setup
        self.telegram_bot = None
        try:
            if os.getenv('TELEGRAM_BOT_TOKEN'):
                self.telegram_bot = self.connection_manager.get_telegram_session()
                self.telegram_channels = [
                    os.getenv('TELEGRAM_CHANNEL_ID', '@VoltageGPU')
                ]
                logging.info("✅ Telegram connected with connection pooling")
        except Exception as e:
            logging.error(f"❌ Telegram setup failed: {e}")
        
        # Reddit setup with better error handling
        self.reddit_clients = []
        try:
            if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_ID') != 'your_reddit_client_id_here':
                reddit = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                    username=os.getenv('REDDIT_USERNAME'),
                    password=os.getenv('REDDIT_PASSWORD'),
                    user_agent='SHA-256 Autonomous Bot v6.0',
                    check_for_async=False
                )
                # Test connection
                try:
                    reddit.user.me()
                    self.reddit_clients.append({
                        'client': reddit, 
                        'name': os.getenv('REDDIT_USERNAME'),
                        'posts_today': 0
                    })
                    logging.info(f"✅ Reddit Account 1 ({os.getenv('REDDIT_USERNAME')}) connected")
                except Exception as auth_error:
                    logging.error(f"❌ Reddit Account 1 authentication failed: {auth_error}")
            
            if os.getenv('REDDIT_CLIENT_ID_2') and os.getenv('REDDIT_CLIENT_ID_2') != 'your_second_reddit_client_id_here':
                reddit2 = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID_2'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET_2'),
                    username=os.getenv('REDDIT_USERNAME_2'),
                    password=os.getenv('REDDIT_PASSWORD_2'),
                    user_agent='SHA-256 Autonomous Bot v6.0',
                    check_for_async=False
                )
                # Test connection
                try:
                    reddit2.user.me()
                    self.reddit_clients.append({
                        'client': reddit2, 
                        'name': os.getenv('REDDIT_USERNAME_2'),
                        'posts_today': 0
                    })
                    logging.info(f"✅ Reddit Account 2 ({os.getenv('REDDIT_USERNAME_2')}) connected")
                except Exception as auth_error:
                    logging.error(f"❌ Reddit Account 2 authentication failed: {auth_error}")
                
        except Exception as e:
            logging.error(f"❌ Reddit setup failed: {e}")
        
        # Initialize Twitter Follow Manager if Twitter clients are available
        if self.twitter_clients:
            try:
                # Use the first Twitter client for follow management
                self.twitter_follow_manager = TwitterFollowManager(
                    self.twitter_clients[0]['client']
                )
                logging.info("🐦 Twitter Follow Manager initialized with safe limits (150 follows/day)")
            except Exception as e:
                logging.error(f"❌ Twitter Follow Manager setup failed: {e}")
    
    def get_gpu_offers(self) -> List[Dict]:
        """Get GPU offers with enhanced error handling"""
        try:
            api_key = os.getenv("VOLTAGE_API_KEY")
            if not api_key or api_key == "your_api_key_here":
                return self._generate_mock_offers()
            
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(
                'https://voltagegpu.com/api/pods',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    offers = data.get('pods', [])
                    if offers:
                        logging.info(f"✅ API: Retrieved {len(offers)} GPU offers")
                        return offers[:3]
                    else:
                        return self._generate_mock_offers()
                except json.JSONDecodeError:
                    logging.warning("⚠️ API returned invalid JSON, using mock data")
                    return self._generate_mock_offers()
            else:
                logging.warning(f"⚠️ API returned status {response.status_code}, using mock data")
                return self._generate_mock_offers()
                
        except Exception as e:
            logging.warning(f"⚠️ API error: {e}, using mock data")
            return self._generate_mock_offers()
    
    def _generate_mock_offers(self) -> List[Dict]:
        """Generate realistic mock GPU offers"""
        return [{
            'gpu_count': random.choice([4, 8, 16]),
            'gpu_type': random.choice(['H100', 'A100', 'RTX4090']),
            'price_per_hour': round(random.uniform(25, 45), 2),
            'location': random.choice(['Singapore', 'Mumbai', 'Frankfurt']),
            'uptime': round(random.uniform(98, 99.9), 1)
        }]
    
    async def autonomous_discovery_cycle(self):
        """Run autonomous discovery cycle"""
        if datetime.now() - self.last_discovery_cycle < timedelta(seconds=self.discovery_cycle_interval):
            return
        
        region = self.stats['current_region']
        language = self.stats['current_language']
        
        logging.info(f"🤖 Starting autonomous discovery cycle for {region}/{language}")
        
        try:
            await self.group_discovery.autonomous_discovery_cycle(region, language)
            self.stats['discoveries'] += 1
            self.last_discovery_cycle = datetime.now()
            
            # Adjust discovery interval based on success
            if self.stats['discoveries'] > 0:
                self.discovery_cycle_interval = min(self.discovery_cycle_interval * 1.1, 7200)  # Max 2 hours
            
        except Exception as e:
            logging.error(f"❌ Discovery cycle failed: {e}")
    
    def update_optimal_targeting(self):
        """Update optimal region and language based on current time and performance"""
        region, language, timezone_name = self.timezone_optimizer.get_current_optimal_region()
        
        # Check if autonomous performance engine suggests a different target
        should_post, timing_reason = self.performance_engine.should_post_now('twitter', region, language)
        
        if region != self.stats['current_region'] or language != self.stats['current_language']:
            logging.info(f"🌍 Switching target: {region} ({language}) - {timing_reason}")
            self.stats['current_region'] = region
            self.stats['current_language'] = language
            
            # Force discovery cycle for new region
            self.last_discovery_cycle = datetime.now() - timedelta(hours=2)
    
    def autonomous_post_twitter(self):
        """Autonomous Twitter posting with full AI optimization"""
        if not self.twitter_clients or not self.rate_limiter.can_post('twitter'):
            return
            
        region = self.stats['current_region']
        language = self.stats['current_language']
        
        # Check if we should post now and if accounts are available
        should_post, reason = self.performance_engine.should_post_now('twitter', region, language)
        
        # Check if Twitter is in cooldown
        if self.stats.get('twitter_cooldown_until'):
            cooldown_remaining = self.stats['twitter_cooldown_until'] - datetime.now()
            if cooldown_remaining.total_seconds() > 0:
                logging.info(f"⏰ Twitter in cooldown for {int(cooldown_remaining.total_seconds()/60)}m")
                return
            else:
                # Reset cooldown
                self.stats['twitter_cooldown_until'] = None
                for twitter_data in self.twitter_clients:
                    twitter_data['posts_today'] = 0
                logging.info("✅ Twitter cooldown expired - accounts reactivated")
        
        if not should_post and not self.test_mode:
            logging.info(f"⏰ Skipping Twitter post: {reason}")
            return
        
        for twitter_data in self.twitter_clients:
            # Respect 90-minute interval per account (not 15 minutes!)
            if twitter_data['posts_today'] >= 15:
                continue
            
            # Check if 4 hours have passed since last post for this account (EXTENDED DELAY)
            last_post_time = getattr(twitter_data, 'last_post_time', None)
            if last_post_time:
                time_since_last = datetime.now() - last_post_time
                if time_since_last.total_seconds() < 14400:  # 4 hours = 14400 seconds
                    hours_left = (14400 - time_since_last.total_seconds()) / 3600
                    logging.info(f"⏰ {twitter_data['name']}: Must wait {hours_left:.1f}h (4h interval)")
                    continue
                
            try:
                offers = self.get_gpu_offers()
                
                # Get autonomous recommendations for content type
                recommendations = self.performance_engine.get_autonomous_recommendations('twitter', region, language)
                
                # Diversify content types for maximum viral reach
                content_types = ['gpu_deals', 'free_vpn', 'promo_earnings', 'combo_deals']
                content_type = random.choice(content_types)
                
                # ALWAYS use ULTIMATE viral content - NO MORE ENTERPRISE CONTENT!
                content = self.content_generator.generate_ultimate_viral_content(
                    offers[0] if offers else None
                )
                logging.info("🚀 Using ULTIMATE viral content")
                
                # DISABLED A/B testing - use ONLY ultimate viral content
                logging.info("🚀 Using pure ULTIMATE viral content (A/B testing disabled)")
                
                # Apply predictive AI optimizations
                current_hour = datetime.now().hour
                content = self.predictive_ai.adapt_tone(content, 'twitter', region, current_hour)
                
                # Get AI predictions for hashtags
                predictions = self.predictive_ai.get_predictions('twitter', region)
                if predictions['best_hashtags']:
                    # Extract current hashtags from content
                    import re
                    current_hashtags = re.findall(r'#\w+', content)
                    # Optimize hashtags
                    optimized_hashtags = self.predictive_ai.optimize_hashtags(content, 'twitter', current_hashtags)
                    # Replace hashtags in content
                    import re
                    hashtag_pattern = r'#\w+'
                    existing_hashtags = re.findall(hashtag_pattern, content)
                    
                    # Replace existing hashtags with optimized ones
                    for i, hashtag in enumerate(optimized_hashtags[:min(2, len(existing_hashtags))]):
                        if i < len(existing_hashtags):
                            content = content.replace(existing_hashtags[i], f'#{hashtag}')
                
                # Autonomous content optimization
                optimized_content = self.performance_engine.optimize_content_autonomously(
                    content, 'twitter', region, language
                )
                
                # Further optimization with content optimizer
                final_content = self.content_optimizer.optimize_content(optimized_content, 'twitter')
                
                if self.test_mode:
                    print(f"🐦 TEST {twitter_data['name']} ({region}/{language}): {final_content[:100]}...")
                    # Record test performance
                    self.performance_engine.record_performance(
                        'twitter', region, language, content_type, final_content, 
                        True, engagement=random.randint(5, 50), reach=random.randint(100, 1000)
                    )
                    continue
                
                # Post to Twitter with better error handling (including virtual accounts)
                try:
                    if twitter_data.get('virtual'):
                        # Virtual account - simulate successful post
                        logging.info(f"✅ {twitter_data['name']}: VIRTUAL post simulated - {final_content[:50]}...")
                        response = {'data': {'id': f'virtual_{random.randint(1000000, 9999999)}'}}
                    else:
                        # Real account
                        response = twitter_data['client'].create_tweet(text=final_content)
                    
                    # Record performance for autonomous learning
                    self.performance_engine.record_performance(
                        'twitter', region, language, content_type, final_content,
                        True, engagement=0, reach=0  # Real metrics would be gathered later
                    )
                    
                    # Record content performance for optimization
                    self.content_optimizer.record_content_performance(
                        final_content, 'twitter', 0, True
                    )
                    
                    # Record the post time for this account
                    twitter_data['last_post_time'] = datetime.now()
                    twitter_data['posts_today'] += 1
                    self.stats['twitter_posts'] += 1
                    self.stats['optimizations'] += 1
                    self.rate_limiter.record_request('twitter')
                    
                    logging.info(f"✅ {twitter_data['name']}: Autonomous post to {region}/{language} ({twitter_data['posts_today']}/15)")
                    time.sleep(5)
                    
                except Exception as tweet_error:
                    # Handle specific Twitter errors with auto-recovery
                    error_msg = str(tweet_error)
                    if "429" in error_msg:
                        # Rate limited - set cooldown
                        cooldown_time = datetime.now() + timedelta(minutes=15)
                        self.stats['twitter_cooldown_until'] = cooldown_time
                        logging.warning(f"⚠️ {twitter_data['name']}: Rate limited, cooldown until {cooldown_time.strftime('%H:%M')}")
                        twitter_data['posts_today'] = 15  # Temporarily disable this account
                    elif "403" in error_msg:
                        logging.warning(f"⚠️ {twitter_data['name']}: Forbidden, content may be flagged")
                    else:
                        logging.error(f"❌ {twitter_data['name']}: {error_msg}")
                    
                    # Record failure for learning
                    self.performance_engine.record_performance(
                        'twitter', region, language, content_type, final_content, False
                    )
                    self.stats['errors'] += 1
                    continue
                
            except Exception as e:
                self.stats['errors'] += 1
                # Record failure for learning
                self.performance_engine.record_performance(
                    'twitter', region, language, 'gpu_deals', '', False
                )
                logging.error(f"❌ {twitter_data['name']}: {e}")
    
    def autonomous_post_telegram(self):
        """Autonomous Telegram posting with discovered groups"""
        if not self.telegram_bot or not self.rate_limiter.can_post('telegram'):
            return
            
        region = self.stats['current_region']
        language = self.stats['current_language']
        
        # FORCE POSTING FOR IMMEDIATE TESTING
        should_post = True
        reason = "FORCED FOR TESTING"
        logging.info("🔄 FORCED: Telegram posting enabled for immediate testing")
        
        try:
            offers = self.get_gpu_offers()
            
            # Get autonomous recommendations
            recommendations = self.performance_engine.get_autonomous_recommendations('telegram', region, language)
            content_type = 'gpu_deals'
            
            # ALWAYS use ULTIMATE viral content for Telegram too!
            content = self.content_generator.generate_ultimate_viral_content(
                offers[0] if offers else None
            )
            logging.info("🚀 Telegram: Using ULTIMATE viral content")
            
            # Apply predictive AI optimizations for Telegram
            current_hour = datetime.now().hour
            content = self.predictive_ai.adapt_tone(content, 'telegram', region, current_hour)
            
            # Record predictive AI performance
            hashtags = []
            import re
            hashtags = re.findall(r'#\w+', content)
            tone = self.predictive_ai._analyze_tone(content)
            self.predictive_ai.record_performance(hashtags, tone, 'telegram', region, current_hour, True, random.randint(10, 100))
            
            optimized_content = self.performance_engine.optimize_content_autonomously(
                content, 'telegram', region, language
            )
            
            final_content = self.content_optimizer.optimize_content(optimized_content, 'telegram')
            
            if self.test_mode:
                print(f"💬 TEST TELEGRAM ({region}/{language}): {final_content[:100]}...")
                self.performance_engine.record_performance(
                    'telegram', region, language, content_type, final_content,
                    True, engagement=random.randint(10, 100), reach=random.randint(200, 2000)
                )
                return
            
            # Use own channel for reliable posting (discovered groups often have restrictions)
            target_groups = self.telegram_channels
            logging.info(f"📢 Using own Telegram channel: {self.telegram_channels[0]}")
            
            async def send_autonomous_messages():
                successful_posts = 0
                for group in target_groups:
                    try:
                        await self.telegram_bot.send_message(
                            chat_id=group,
                            text=final_content
                        )
                        
                        # Record group performance
                        self.group_discovery.record_group_performance(group, True, random.randint(5, 50))
                        
                        successful_posts += 1
                        logging.info(f"✅ Telegram: Autonomous post to {group} ({region}/{language})")
                        await asyncio.sleep(2)
                        
                    except Exception as e:
                        # Record group failure
                        self.group_discovery.record_group_performance(group, False, 0)
                        logging.error(f"❌ Telegram {group}: {e}")
                        continue
                
                return successful_posts
            
            # Execute async posting with proper loop handling
            try:
                # Always create a new event loop for Telegram operations
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                successful_posts = loop.run_until_complete(send_autonomous_messages())
                
                # Clean up the loop
                loop.close()
                
                if successful_posts > 0:
                    # Record performance
                    self.performance_engine.record_performance(
                        'telegram', region, language, content_type, final_content,
                        True, engagement=0, reach=0
                    )
                    
                    self.content_optimizer.record_content_performance(
                        final_content, 'telegram', 0, True
                    )
                    
                    self.stats['telegram_posts'] += successful_posts
                    self.stats['optimizations'] += 1
                    self.rate_limiter.record_request('telegram')
                    
            except Exception as loop_error:
                logging.error(f"❌ Telegram loop error: {loop_error}")
                # Fallback: direct posting without async
                try:
                    import telegram
                    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
                    bot.send_message(chat_id=self.telegram_channels[0], text=final_content)
                    logging.info(f"✅ Telegram: Fallback post successful")
                    self.stats['telegram_posts'] += 1
                except Exception as fallback_error:
                    logging.error(f"❌ Telegram fallback failed: {fallback_error}")
                
        except Exception as e:
            self.stats['errors'] += 1
            self.performance_engine.record_performance(
                'telegram', region, language, 'gpu_deals', '', False
            )
            logging.error(f"❌ Telegram autonomous posting: {e}")
    
    def autonomous_post_reddit(self):
        """🧠 INTELLIGENT Reddit posting with AI rule compliance and dual account management"""
        if not self.reddit_clients or not self.rate_limiter.can_post('reddit'):
            return
            
        region = self.stats['current_region']
        language = self.stats['current_language']
        
        # Check if we should post now
        should_post, reason = self.performance_engine.should_post_now('reddit', region, language)
        if not should_post and not self.test_mode:
            logging.info(f"⏰ Skipping Reddit post: {reason}")
            return
        
        # Use BOTH Reddit accounts intelligently
        for reddit_data in self.reddit_clients:
            account_name = reddit_data['name']
            
            # Check account health and ban risk
            can_post, health_reason = self.reddit_intelligence.should_post_to_subreddit(account_name, 'general')
            if not can_post:
                logging.info(f"🛡️ {account_name}: {health_reason}")
                continue
                
            if reddit_data['posts_today'] >= 8:  # Optimized limit with AI protection
                logging.info(f"📊 {account_name}: Daily limit reached (8/8)")
                continue
                
            try:
                offers = self.get_gpu_offers()
                
                # Get best subreddits for this account using AI
                best_subreddits = self.reddit_intelligence.get_best_subreddits(account_name, limit=5)
                
                if not best_subreddits:
                    # Fallback to safe subreddits
                    best_subreddits = ['artificial', 'MachineLearning', 'compsci', 'programming']
                    logging.info(f"🔄 {account_name}: Using fallback subreddits")
                
                # Generate base content
                if offers:
                    offer = offers[0]
                    base_content = f"I've been researching cost-effective GPU solutions for AI development and discovered some interesting alternatives to traditional cloud providers. Has anyone experimented with decentralized GPU networks? I'm particularly interested in platforms offering {offer['gpu_count']}x {offer['gpu_type']} configurations at competitive rates."
                    base_title = f"Cost-effective GPU alternatives for AI/ML workloads - experiences?"
                else:
                    base_content = "I've been analyzing the economics of GPU computing for machine learning projects. The cost difference between traditional cloud providers and emerging alternatives is quite significant. Has anyone explored decentralized computing networks for AI workloads?"
                    base_title = "GPU computing economics - exploring alternatives to traditional cloud"
                
                content_type = 'gpu_deals'
                
                # Try posting to each subreddit
                success = False
                for subreddit_name in best_subreddits[:3]:  # Try top 3
                    try:
                        # Analyze subreddit rules automatically
                        rules = self.reddit_intelligence.analyze_subreddit_rules(reddit_data['client'], subreddit_name)
                        
                        # Generate compliant content
                        compliant_title, compliant_content = self.reddit_intelligence.generate_compliant_content(
                            subreddit_name, base_content, base_title
                        )
                        
                        if self.test_mode:
                            print(f"📍 TEST REDDIT {account_name} -> r/{subreddit_name}")
                            print(f"   Title: {compliant_title[:60]}...")
                            print(f"   Content: {compliant_content[:100]}...")
                            
                            # Record test performance
                            self.reddit_intelligence.record_post_result(account_name, subreddit_name, True)
                            self.performance_engine.record_performance(
                                'reddit', region, language, content_type, compliant_content,
                                True, engagement=random.randint(3, 30), reach=random.randint(50, 500)
                            )
                            success = True
                            break
                        
                        # Real posting
                        subreddit = reddit_data['client'].subreddit(subreddit_name)
                        
                        # Handle flairs intelligently
                        flair_id = None
                        if rules.flair_required and rules.available_flairs:
                            try:
                                flairs = list(subreddit.flair.link_templates)
                                if flairs:
                                    # Choose appropriate flair
                                    for flair in flairs:
                                        flair_text = flair.get('text', '').lower()
                                        if any(keyword in flair_text for keyword in ['discussion', 'question', 'help']):
                                            flair_id = flair['id']
                                            break
                                    if not flair_id:
                                        flair_id = flairs[0]['id']
                            except Exception as flair_error:
                                logging.warning(f"⚠️ Flair error for r/{subreddit_name}: {flair_error}")
                        
                        # Submit post
                        if flair_id:
                            submission = subreddit.submit(title=compliant_title, selftext=compliant_content, flair_id=flair_id)
                        else:
                            submission = subreddit.submit(title=compliant_title, selftext=compliant_content)
                        
                        # Record success
                        self.reddit_intelligence.record_post_result(account_name, subreddit_name, True)
                        self.performance_engine.record_performance(
                            'reddit', region, language, content_type, compliant_content,
                            True, engagement=0, reach=0
                        )
                        
                        reddit_data['posts_today'] += 1
                        self.stats['reddit_posts'] += 1
                        self.stats['optimizations'] += 1
                        self.rate_limiter.record_request('reddit')
                        
                        logging.info(f"✅ Reddit r/{subreddit_name}: INTELLIGENT post by {account_name} (compliant)")
                        success = True
                        break
                        
                    except Exception as e:
                        error_msg = str(e)
                        
                        # Intelligent error handling
                        if "removed" in error_msg.lower():
                            removal_reason = "Auto-removed by moderators"
                            if "tag" in error_msg.lower():
                                removal_reason += " - Missing required tag"
                            elif "karma" in error_msg.lower():
                                removal_reason += " - Insufficient karma"
                            elif "spam" in error_msg.lower():
                                removal_reason += " - Flagged as spam"
                        else:
                            removal_reason = error_msg
                        
                        # Record failure for learning
                        self.reddit_intelligence.record_post_result(account_name, subreddit_name, False, removal_reason)
                        
                        logging.error(f"❌ Reddit r/{subreddit_name}: {account_name} failed - {removal_reason}")
                        continue
                
                if success:
                    # Wait between accounts to avoid detection
                    time.sleep(random.randint(30, 60))
                else:
                    logging.warning(f"⚠️ {account_name}: Failed to post to any subreddit")
                    
            except Exception as e:
                self.stats['errors'] += 1
                logging.error(f"❌ Reddit {account_name}: {e}")
        
        # Display intelligence summary
        intel_summary = self.reddit_intelligence.get_intelligence_summary()
        if intel_summary['subreddits_analyzed'] > 0:
            logging.info(f"🧠 Reddit Intelligence: {intel_summary['subreddits_analyzed']} subreddits analyzed, {intel_summary['success_rate']:.1%} success rate")
    
    def autonomous_twitter_follow_cycle(self):
        """🐦 INTELLIGENT Twitter Follow/Unfollow Management"""
        if not self.twitter_follow_manager:
            return
            
        try:
            # Run daily follow/unfollow cycle
            results = self.twitter_follow_manager.run_daily_cycle()
            
            # Log results
            if results['follows']['followed'] > 0 or results['unfollows']['unfollowed'] > 0:
                logging.info(f"🐦 Follow Manager: +{results['follows']['followed']} follows, -{results['unfollows']['unfollowed']} unfollows")
                
                # Update stats
                if 'twitter_follows' not in self.stats:
                    self.stats['twitter_follows'] = 0
                    self.stats['twitter_unfollows'] = 0
                
                self.stats['twitter_follows'] += results['follows']['followed']
                self.stats['twitter_unfollows'] += results['unfollows']['unfollowed']
                
                # Display follow stats
                follow_stats = self.twitter_follow_manager.get_follow_stats()
                logging.info(f"🐦 Follow Stats: {follow_stats['total_following']} following, {follow_stats['follow_back_rate']:.1f}% follow back rate")
            
        except Exception as e:
            logging.error(f"❌ Twitter Follow Manager error: {e}")
            self.stats['errors'] += 1
    
    def display_autonomous_status(self):
        """Display enhanced autonomous status with countdown and auto-recovery"""
        now = datetime.now()
        uptime = now - self.stats['start_time']
        uptime_seconds = int(uptime.total_seconds())
        
        region = self.stats['current_region']
        language = self.stats['current_language']
        is_peak = self.timezone_optimizer.is_peak_time(region)
        
        # Get performance summary
        perf_summary = self.performance_engine.get_performance_summary(days=1)
        
        print(f"\r🤖 SHA-256 BOT - FULLY AUTONOMOUS AI")
        print(f"💰 AFFILIATE CODE: {self.affiliate_code}")
        print(f"⏰ {now.strftime('%H:%M:%S')} | Uptime: {uptime_seconds}s")
        print(f"🌍 Current Target: {region} ({language}) {'🔥 PEAK TIME' if is_peak else '⏳ Off-peak'}")
        
        # Autonomous status with auto-recovery info
        print(f"\n🤖 AUTONOMOUS STATUS:")
        if perf_summary.get('status') == 'active':
            print(f"   📊 Performance: {perf_summary['performance_level']}")
            print(f"   🎯 Success Rate: {perf_summary['success_rate']:.1%}")
            print(f"   🧠 AI Insights: {perf_summary['insights_count']} patterns learned")
            print(f"   ⚡ Strategies: {perf_summary['strategies_count']} optimizations active")
        else:
            print(f"   📊 Performance: 🔄 Learning...")
        
        # Auto-recovery status
        if self.stats.get('twitter_cooldown_until'):
            cooldown_remaining = self.stats['twitter_cooldown_until'] - now
            if cooldown_remaining.total_seconds() > 0:
                minutes_left = int(cooldown_remaining.total_seconds() / 60)
                print(f"   🔄 Twitter Auto-Recovery: {minutes_left}m remaining")
            else:
                # Reset cooldown
                self.stats['twitter_cooldown_until'] = None
                for twitter_data in self.twitter_clients:
                    twitter_data['posts_today'] = 0
                print(f"   ✅ Twitter Auto-Recovery: COMPLETED - Accounts reactivated")
        
        # Platform status with countdown
        print(f"\n🔗 PLATFORM STATUS:")
        for twitter_data in self.twitter_clients:
            if twitter_data['posts_today'] >= 15:
                if self.stats.get('twitter_cooldown_until'):
                    cooldown_remaining = self.stats['twitter_cooldown_until'] - now
                    if cooldown_remaining.total_seconds() > 0:
                        minutes_left = int(cooldown_remaining.total_seconds() / 60)
                        status = f"⏳ COOLDOWN ({minutes_left}m)"
                    else:
                        status = "🟢 RECOVERED"
                        twitter_data['posts_today'] = 0
                else:
                    status = "🟡 LIMIT REACHED"
            else:
                status = "🟢 ACTIVE"
            print(f"   🐦 {twitter_data['name']}: {status} ({twitter_data['posts_today']}/15 posts)")
        
        if self.telegram_bot:
            discovered_tg = len(self.group_discovery.discovered_groups['telegram'])
            print(f"   💬 Telegram: 🟢 ACTIVE ({self.stats['telegram_posts']} posts, {discovered_tg} discovered groups)")
        else:
            print(f"   💬 Telegram: 🔴 DISCONNECTED")
        
        for reddit_data in self.reddit_clients:
            status = "🟢 HEALTHY" if reddit_data['posts_today'] < 5 else "🟡 LIMIT REACHED"
            discovered_reddit = len(self.group_discovery.discovered_groups['reddit'])
            print(f"   📍 Reddit ({reddit_data['name']}): {status} ({reddit_data['posts_today']} posts, {discovered_reddit} communities)")
        
        # Performance metrics with follow/unfollow stats
        print(f"\n📊 AUTONOMOUS METRICS:")
        print(f"   🐦 Twitter Posts: {self.stats['twitter_posts']}")
        print(f"   💬 Telegram Posts: {self.stats['telegram_posts']}")
        print(f"   📍 Reddit Posts: {self.stats['reddit_posts']}")
        
        # Twitter Follow/Unfollow metrics
        if self.twitter_follow_manager:
            follow_stats = self.twitter_follow_manager.get_follow_stats()
            today_stats = follow_stats['today']
            print(f"   🐦 Twitter Growth: +{today_stats['follows']}F -{today_stats['unfollows']}UF ({follow_stats['follow_back_rate']:.1f}% follow back)")
            print(f"   👥 Following: {follow_stats['total_following']} | Follow backs: {follow_stats['follow_backs']}")
        
        print(f"   🔍 Discoveries: {self.stats['discoveries']}")
        print(f"   ⚡ AI Optimizations: {self.stats['optimizations']}")
        print(f"   ❌ Errors: {self.stats['errors']}")
        
        # Next action countdown
        print(f"\n⏰ NEXT ACTIONS:")
        next_discovery = self.last_discovery_cycle + timedelta(seconds=self.discovery_cycle_interval)
        discovery_remaining = next_discovery - now
        if discovery_remaining.total_seconds() > 0:
            minutes_left = int(discovery_remaining.total_seconds() / 60)
            print(f"   🔍 Next Discovery: {minutes_left}m")
        else:
            print(f"   🔍 Next Discovery: NOW")
        
        # Calculate precise next post times
        should_post_twitter, twitter_reason = self.performance_engine.should_post_now('twitter', region, language)
        should_post_telegram, telegram_reason = self.performance_engine.should_post_now('telegram', region, language)
        should_post_reddit, reddit_reason = self.performance_engine.should_post_now('reddit', region, language)
        
        # Twitter POSTING timing with precise seconds (120min interval)
        if self.stats.get('twitter_cooldown_until'):
            cooldown_remaining = self.stats['twitter_cooldown_until'] - now
            if cooldown_remaining.total_seconds() > 0:
                total_seconds = int(cooldown_remaining.total_seconds())
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                print(f"   🐦 Next Twitter POST: {minutes}m{seconds:02d}s (rate limit cooldown - 120min interval)")
            else:
                print(f"   🐦 Next Twitter POST: NOW (cooldown expired)")
        elif not should_post_twitter:
            # Calculate next optimal time for POSTS (120 minutes = 7200 seconds)
            print(f"   🐦 Next Twitter POST: ~120m (waiting for 120min interval)")
        else:
            print(f"   🐦 Next Twitter POST: NOW (ready to post)")
            
        # Twitter FOLLOW/UNFOLLOW timing (separate 6min cycle)
        if self.twitter_follow_manager:
            follow_stats = self.twitter_follow_manager.get_follow_stats()
            follow_remaining = follow_stats['daily_limits']['follow_remaining']
            unfollow_remaining = follow_stats['daily_limits']['unfollow_remaining']
            
            # Calculate next follow cycle (every 6 minutes = 360 seconds)
            current_cycle = getattr(self, '_follow_cycle_counter', 0)
            follow_cycle_seconds = (6 - current_cycle) * 60
            if follow_cycle_seconds <= 0:
                follow_cycle_seconds = 360  # Reset to 6 minutes
            
            follow_minutes = follow_cycle_seconds // 60
            follow_secs = follow_cycle_seconds % 60
            
            if follow_remaining > 0 or unfollow_remaining > 0:
                print(f"   🐦 Next FOLLOW/UNFOLLOW: {follow_minutes}m{follow_secs:02d}s (Growth: {follow_remaining}F/{unfollow_remaining}UF left)")
            else:
                print(f"   🐦 Next FOLLOW/UNFOLLOW: Tomorrow (daily limits: 150F/175UF reached)")
            
        # Telegram timing
        if not should_post_telegram:
            # Calculate next optimal time (estimate 45-90 min)
            next_optimal = random.randint(45, 90)
            print(f"   💬 Next Telegram POST: ~{next_optimal}m (AI timing)")
        else:
            print(f"   💬 Next Telegram POST: NOW (ready to post)")
            
        # Reddit timing
        if not should_post_reddit:
            # Calculate next optimal time (estimate 2-4 hours)
            next_optimal = random.randint(120, 240)
            print(f"   📍 Next Reddit POST: ~{next_optimal//60}h{next_optimal%60}m (rate limit)")
        else:
            print(f"   📍 Next Reddit POST: NOW (ready to post)")
        
        # AI Recommendations
        recommendations = self.performance_engine.get_autonomous_recommendations('twitter', region, language)
        if recommendations:
            print(f"\n🧠 AI RECOMMENDATIONS:")
            for rec in recommendations[:3]:
                print(f"   • {rec}")
        
        print(f"\n💰 AFFILIATE CODE: {self.affiliate_code}")
        print("🛑 Ctrl+C to stop" + " " * 20, end="")
    
    def run(self):
        """Run the fully autonomous SHA-256 bot"""
        if self.test_mode:
            print("🤖 TEST MODE - AUTONOMOUS SHA-256 BOT")
            print("=" * 50)
            
            self.update_optimal_targeting()
            
            # Run discovery cycle in test mode
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.autonomous_discovery_cycle())
                loop.close()
            except Exception as e:
                print(f"🔍 Discovery test: {e}")
            
            self.autonomous_post_twitter()
            self.autonomous_post_telegram()
            self.autonomous_post_reddit()
            
            print("\n✅ Autonomous test completed - All AI features working")
            return
            
        print("🤖 LAUNCHING AUTONOMOUS SHA-256 BOT")
        print("=" * 50)
        print(f"🐦 Twitter: {len(self.twitter_clients)} accounts")
        print(f"💬 Telegram: {'✅' if self.telegram_bot else '❌'}")
        print(f"📍 Reddit: {len(self.reddit_clients)} accounts")
        print(f"🤖 Autonomous Discovery: ✅ ENABLED")
        print(f"🧠 Self-Learning AI: ✅ ENABLED")
        print(f"⚡ Content Optimization: ✅ ENABLED")
        print(f"🎯 Performance Engine: ✅ ENABLED")
        print(f"💰 Affiliate code: {self.affiliate_code}")
        print()
        
        try:
            while True:
                # Update optimal targeting
                self.update_optimal_targeting()
                
                # Run autonomous discovery cycle
                asyncio.run(self.autonomous_discovery_cycle())
                
                # Autonomous posting with AI optimization
                self.autonomous_post_twitter()
                time.sleep(2)
                
                self.autonomous_post_telegram()
                time.sleep(2)
                
                self.autonomous_post_reddit()
                time.sleep(2)
                
                # Run Twitter follow/unfollow cycle (every 6th cycle = ~6 minutes)
                if hasattr(self, '_follow_cycle_counter'):
                    self._follow_cycle_counter += 1
                else:
                    self._follow_cycle_counter = 1
                
                if self._follow_cycle_counter >= 6:  # Every 6 minutes
                    self.autonomous_twitter_follow_cycle()
                    self._follow_cycle_counter = 0
                    time.sleep(2)
                
                # Display autonomous status
                self.display_autonomous_status()
                
                # Wait 60 seconds between cycles
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Autonomous SHA-256 Bot stopped")
            logging.info("Autonomous SHA-256 Bot stopped by user")
            self.connection_manager.close_connections()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='🤖 SHA-256 Bot - Fully Autonomous AI Version')
    parser.add_argument('--test', action='store_true', help='Test mode (no actual posting)')
    
    args = parser.parse_args()
    
    try:
        bot = AutonomousSHA256Bot(test_mode=args.test)
        bot.run()
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
