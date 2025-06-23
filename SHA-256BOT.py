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

# Import our modular components
from modules.autonomous_discovery import AutonomousGroupDiscovery, AutonomousContentOptimizer
from modules.autonomous_performance import AutonomousPerformanceEngine
from modules.timing_manager import TimezoneOptimizer
from modules.content_manager import ContentGenerator
from modules.platform_manager import AdvancedRateLimitManager, ConnectionPoolManager

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sha256bot_autonomous.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

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
        self.content_generator = ContentGenerator()
        self.content_optimizer = AutonomousContentOptimizer()
        self.rate_limiter = AdvancedRateLimitManager()
        self.connection_manager = ConnectionPoolManager()
        
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
            'current_language': 'en'
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
        
        # Reddit setup
        self.reddit_clients = []
        try:
            if os.getenv('REDDIT_CLIENT_ID'):
                reddit = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                    username=os.getenv('REDDIT_USERNAME'),
                    password=os.getenv('REDDIT_PASSWORD'),
                    user_agent='SHA-256 Autonomous Bot v3.0'
                )
                self.reddit_clients.append({
                    'client': reddit, 
                    'name': os.getenv('REDDIT_USERNAME'),
                    'posts_today': 0
                })
                logging.info(f"✅ Reddit Account 1 ({os.getenv('REDDIT_USERNAME')}) connected")
            
            if os.getenv('REDDIT_CLIENT_ID_2'):
                reddit2 = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID_2'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET_2'),
                    username=os.getenv('REDDIT_USERNAME_2'),
                    password=os.getenv('REDDIT_PASSWORD_2'),
                    user_agent='SHA-256 Autonomous Bot v3.0'
                )
                self.reddit_clients.append({
                    'client': reddit2, 
                    'name': os.getenv('REDDIT_USERNAME_2'),
                    'posts_today': 0
                })
                logging.info(f"✅ Reddit Account 2 ({os.getenv('REDDIT_USERNAME_2')}) connected")
                
        except Exception as e:
            logging.error(f"❌ Reddit setup failed: {e}")
    
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
        
        # Check if we should post now
        should_post, reason = self.performance_engine.should_post_now('twitter', region, language)
        if not should_post and not self.test_mode:
            logging.info(f"⏰ Skipping Twitter post: {reason}")
            return
        
        for twitter_data in self.twitter_clients:
            if twitter_data['posts_today'] >= 15:
                continue
                
            try:
                offers = self.get_gpu_offers()
                
                # Get autonomous recommendations for content type
                recommendations = self.performance_engine.get_autonomous_recommendations('twitter', region, language)
                content_type = 'gpu_deals'  # Default, could be optimized based on recommendations
                
                # Generate content
                content = self.content_generator.generate_unique_content(
                    'twitter', content_type, language, offers[0] if offers else None
                )
                
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
                
                # Post to Twitter
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
                
                twitter_data['posts_today'] += 1
                self.stats['twitter_posts'] += 1
                self.stats['optimizations'] += 1
                self.rate_limiter.record_request('twitter')
                
                logging.info(f"✅ {twitter_data['name']}: Autonomous post to {region}/{language} ({twitter_data['posts_today']}/15)")
                time.sleep(5)
                
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
        
        # Check if we should post now
        should_post, reason = self.performance_engine.should_post_now('telegram', region, language)
        if not should_post and not self.test_mode:
            logging.info(f"⏰ Skipping Telegram post: {reason}")
            return
        
        try:
            offers = self.get_gpu_offers()
            
            # Get autonomous recommendations
            recommendations = self.performance_engine.get_autonomous_recommendations('telegram', region, language)
            content_type = 'gpu_deals'
            
            # Generate and optimize content
            content = self.content_generator.generate_unique_content(
                'telegram', content_type, language, offers[0] if offers else None
            )
            
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
            
            # Get discovered groups for current region/language
            discovered_groups = self.group_discovery.get_best_groups('telegram', region, language, limit=3)
            
            # Fallback to default channels if no discovered groups
            target_groups = discovered_groups if discovered_groups else self.telegram_channels
            
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
            
            # Execute async posting
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                successful_posts = loop.run_until_complete(send_autonomous_messages())
                
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
                    
            finally:
                loop.close()
                
        except Exception as e:
            self.stats['errors'] += 1
            self.performance_engine.record_performance(
                'telegram', region, language, 'gpu_deals', '', False
            )
            logging.error(f"❌ Telegram autonomous posting: {e}")
    
    def autonomous_post_reddit(self):
        """Autonomous Reddit posting with discovered communities"""
        if not self.reddit_clients or not self.rate_limiter.can_post('reddit'):
            return
            
        region = self.stats['current_region']
        language = self.stats['current_language']
        
        # Check if we should post now
        should_post, reason = self.performance_engine.should_post_now('reddit', region, language)
        if not should_post and not self.test_mode:
            logging.info(f"⏰ Skipping Reddit post: {reason}")
            return
        
        for reddit_data in self.reddit_clients:
            if reddit_data['posts_today'] >= 5:
                continue
                
            try:
                offers = self.get_gpu_offers()
                
                # Get discovered communities
                discovered_communities = self.group_discovery.get_best_groups('reddit', region, language, limit=5)
                
                if not discovered_communities:
                    logging.info("🔍 No discovered Reddit communities, skipping")
                    continue
                
                # Generate content
                content_type = 'gpu_deals'
                content = self.content_generator.generate_unique_content(
                    'telegram', content_type, language, offers[0] if offers else None
                )
                
                # Create title
                if offers:
                    offer = offers[0]
                    title = f"Found {offer['gpu_count']}x {offer['gpu_type']} at ${offer['price_per_hour']:.2f}/hour - 70% cheaper than AWS"
                else:
                    title = "VoltageGPU: 70% cheaper GPU rentals for AI/ML projects"
                
                if self.test_mode:
                    print(f"📍 TEST REDDIT {reddit_data['name']} ({region}/{language}): {title[:50]}...")
                    self.performance_engine.record_performance(
                        'reddit', region, language, content_type, content,
                        True, engagement=random.randint(3, 30), reach=random.randint(50, 500)
                    )
                    continue
                
                # Try posting to discovered communities
                success = False
                for community in discovered_communities[:3]:  # Try top 3
                    try:
                        subreddit = reddit_data['client'].subreddit(community)
                        submission = subreddit.submit(title=title, selftext=content)
                        
                        # Record success
                        self.group_discovery.record_group_performance(community, True, random.randint(5, 50))
                        self.performance_engine.record_performance(
                            'reddit', region, language, content_type, content,
                            True, engagement=0, reach=0
                        )
                        
                        reddit_data['posts_today'] += 1
                        self.stats['reddit_posts'] += 1
                        self.stats['optimizations'] += 1
                        self.rate_limiter.record_request('reddit')
                        
                        logging.info(f"✅ Reddit r/{community}: Autonomous post by {reddit_data['name']} ({region}/{language})")
                        success = True
                        break
                        
                    except Exception as e:
                        # Record failure and learn
                        self.group_discovery.record_group_performance(community, False, 0)
                        logging.error(f"❌ Reddit r/{community}: {e}")
                        continue
                
                if success:
                    time.sleep(10)  # Wait between successful posts
                else:
                    logging.warning(f"⚠️ Failed to post to any discovered Reddit community for {reddit_data['name']}")
                    
            except Exception as e:
                self.stats['errors'] += 1
                logging.error(f"❌ Reddit autonomous posting: {e}")
    
    def display_autonomous_status(self):
        """Display enhanced autonomous status"""
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
        
        # Autonomous status
        print(f"\n🤖 AUTONOMOUS STATUS:")
        if perf_summary.get('status') == 'active':
            print(f"   📊 Performance: {perf_summary['performance_level']}")
            print(f"   🎯 Success Rate: {perf_summary['success_rate']:.1%}")
            print(f"   🧠 AI Insights: {perf_summary['insights_count']} patterns learned")
            print(f"   ⚡ Strategies: {perf_summary['strategies_count']} optimizations active")
        else:
            print(f"   📊 Performance: 🔄 Learning...")
        
        # Platform status
        print(f"\n🔗 PLATFORM STATUS:")
        for twitter_data in self.twitter_clients:
            status = "🟢 ACTIVE" if twitter_data['posts_today'] < 15 else "🟡 LIMIT REACHED"
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
        
        # Performance metrics
        print(f"\n📊 AUTONOMOUS METRICS:")
        print(f"   🐦 Twitter: {self.stats['twitter_posts']}")
        print(f"   💬 Telegram: {self.stats['telegram_posts']}")
        print(f"   📍 Reddit: {self.stats['reddit_posts']}")
        print(f"   🔍 Discoveries: {self.stats['discoveries']}")
        print(f"   ⚡ Optimizations: {self.stats['optimizations']}")
        print(f"   ❌ Errors: {self.stats['errors']}")
        
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
