#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 UNIFIED ENGINE - SHA-256 BOT
Centralized architecture to resolve module inconsistencies
"""

import os
import json
import sqlite3
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import threading

@dataclass
class UnifiedConfig:
    """Centralized configuration management"""
    
    def __init__(self):
        # Rate limiting configuration
        self.rate_limits = {
            'twitter': {
                'posts_per_hour': 3,
                'daily_limit': 20,
                'min_interval': 1200,  # 20 minutes
                'follow_limit': 150,
                'unfollow_limit': 175
            },
            'telegram': {
                'posts_per_hour': 2,
                'daily_limit': 15,
                'min_interval': 1800,  # 30 minutes
                'invitation_chance': 0.3
            },
            'reddit': {
                'posts_per_hour': 1,
                'daily_limit': 5,
                'min_interval': 3600,  # 60 minutes
                'max_posts_per_account': 8
            }
        }
        
        # Timezone configuration
        self.timezone_regions = {
            'US_EAST': {'timezone': 'America/New_York', 'peak_hours': [9, 12, 17, 20]},
            'US_WEST': {'timezone': 'America/Los_Angeles', 'peak_hours': [8, 11, 16, 19]},
            'EU_WEST': {'timezone': 'Europe/London', 'peak_hours': [9, 13, 18, 21]},
            'ASIA_PACIFIC': {'timezone': 'Asia/Singapore', 'peak_hours': [10, 14, 19, 22]}
        }
        
        # Content configuration
        self.hashtag_pools = {
            'ai_ml': ['#AI', '#MachineLearning', '#DeepLearning', '#NeuralNetworks', '#DataScience', '#MLOps'],
            'gpu_tech': ['#GPU', '#CUDA', '#Computing', '#HighPerformance', '#ParallelComputing', '#TechDeals'],
            'crypto': ['#Crypto', '#Mining', '#Blockchain', '#Bitcoin', '#Ethereum', '#DeFi'],
            'cloud': ['#Cloud', '#AWS', '#Azure', '#GCP', '#CloudComputing', '#Infrastructure'],
            'dev': ['#Developer', '#Programming', '#Tech', '#Innovation', '#Startup', '#SaaS']
        }
        
        # Region switching configuration
        self.region_switch_interval = 4 * 3600  # 4 hours
        
        # Database configuration
        self.db_path = 'data/unified_bot_data.db'
        
        # Cache configuration
        self.cache_ttl = {
            'api_data': 3600,      # 1 hour
            'user_data': 7200,     # 2 hours
            'content_data': 1800   # 30 minutes
        }

class UnifiedDataManager:
    """Centralized data management with proper concurrency handling"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.db_path = config.db_path
        self.lock = threading.Lock()
        self._init_unified_database()
    
    def _init_unified_database(self):
        """Initialize unified database schema"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Unified performance tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    platform TEXT NOT NULL,
                    region TEXT NOT NULL,
                    language TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    engagement_count INTEGER DEFAULT 0,
                    reach_count INTEGER DEFAULT 0,
                    performance_score REAL DEFAULT 0.0,
                    module_source TEXT NOT NULL
                )
            ''')
            
            # Unified rate limiting tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rate_limit_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    account_id TEXT,
                    last_post TIMESTAMP,
                    posts_today INTEGER DEFAULT 0,
                    daily_reset TIMESTAMP,
                    UNIQUE(platform, account_id)
                )
            ''')
            
            # Unified content tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_hash TEXT UNIQUE NOT NULL,
                    platform TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    hashtags TEXT,
                    performance_score REAL DEFAULT 0.0,
                    usage_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP
                )
            ''')
            
            # Unified user tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    username TEXT,
                    relevance_score REAL DEFAULT 0.0,
                    last_interaction TIMESTAMP,
                    interaction_type TEXT,
                    UNIQUE(platform, user_id)
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def execute_query(self, query: str, params: tuple = (), fetch: bool = False) -> Any:
        """Thread-safe database query execution"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute(query, params)
                
                if fetch:
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount
                
                conn.commit()
                return result
                
            except Exception as e:
                conn.rollback()
                logging.error(f"Database error: {e}")
                raise
            finally:
                conn.close()
    
    def record_performance(self, platform: str, region: str, language: str, 
                          content_type: str, content_hash: str, success: bool,
                          engagement: int = 0, reach: int = 0, score: float = 0.0,
                          module_source: str = 'unified'):
        """Record performance data from any module"""
        query = '''
            INSERT INTO performance_data 
            (platform, region, language, content_type, content_hash, success, 
             engagement_count, reach_count, performance_score, module_source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (platform, region, language, content_type, content_hash, 
                 success, engagement, reach, score, module_source)
        
        self.execute_query(query, params)
    
    def get_performance_data(self, platform: str = None, days: int = 7) -> List[Dict]:
        """Get unified performance data"""
        query = '''
            SELECT * FROM performance_data 
            WHERE timestamp > datetime('now', '-{} days')
        '''.format(days)
        
        if platform:
            query += ' AND platform = ?'
            params = (platform,)
        else:
            params = ()
        
        results = self.execute_query(query, params, fetch=True)
        
        return [
            {
                'platform': row[2], 'region': row[3], 'language': row[4],
                'content_type': row[5], 'success': bool(row[7]),
                'engagement': row[8], 'reach': row[9], 'score': row[10],
                'module_source': row[11], 'timestamp': row[1]
            }
            for row in results
        ]

class UnifiedRateLimiter:
    """Centralized rate limiting with single source of truth"""
    
    def __init__(self, config: UnifiedConfig, data_manager: UnifiedDataManager):
        self.config = config
        self.data_manager = data_manager
        self.limits = config.rate_limits
    
    def can_post(self, platform: str, account_id: str = None) -> Tuple[bool, str, int]:
        """Check if posting is allowed with unified logic"""
        now = datetime.now()
        limit_config = self.limits.get(platform, {})
        
        # Get current rate limit data
        query = '''
            SELECT last_post, posts_today, daily_reset 
            FROM rate_limit_data 
            WHERE platform = ? AND account_id = ?
        '''
        params = (platform, account_id or 'default')
        results = self.data_manager.execute_query(query, params, fetch=True)
        
        if results:
            last_post_str, posts_today, daily_reset_str = results[0]
            last_post = datetime.fromisoformat(last_post_str) if last_post_str else None
            daily_reset = datetime.fromisoformat(daily_reset_str) if daily_reset_str else None
        else:
            last_post = None
            posts_today = 0
            daily_reset = None
        
        # Reset daily counter if needed
        if not daily_reset or now >= daily_reset:
            posts_today = 0
            daily_reset = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        # Check daily limit
        daily_limit = limit_config.get('daily_limit', 999)
        if posts_today >= daily_limit:
            return False, f"Daily limit reached ({posts_today}/{daily_limit})", 0
        
        # Check minimum interval
        min_interval = limit_config.get('min_interval', 0)
        if last_post and min_interval > 0:
            time_since_last = (now - last_post).total_seconds()
            if time_since_last < min_interval:
                wait_time = int(min_interval - time_since_last)
                return False, f"Rate limited", wait_time
        
        return True, "OK", 0
    
    def record_post(self, platform: str, account_id: str = None):
        """Record a post with unified tracking"""
        now = datetime.now()
        daily_reset = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        query = '''
            INSERT OR REPLACE INTO rate_limit_data 
            (platform, account_id, last_post, posts_today, daily_reset)
            VALUES (?, ?, ?, 
                    COALESCE((SELECT posts_today FROM rate_limit_data 
                             WHERE platform = ? AND account_id = ?), 0) + 1,
                    ?)
        '''
        params = (platform, account_id or 'default', now.isoformat(), 
                 platform, account_id or 'default', daily_reset.isoformat())
        
        self.data_manager.execute_query(query, params)
    
    def get_next_available_time(self, platform: str, account_id: str = None) -> Optional[datetime]:
        """Get when next post is allowed"""
        can_post, reason, wait_time = self.can_post(platform, account_id)
        
        if can_post:
            return datetime.now()
        elif wait_time > 0:
            return datetime.now() + timedelta(seconds=wait_time)
        else:
            # Daily limit reached, next available tomorrow
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

class UnifiedContentEngine:
    """Centralized content generation and optimization"""
    
    def __init__(self, config: UnifiedConfig, data_manager: UnifiedDataManager):
        self.config = config
        self.data_manager = data_manager
        self.hashtag_pools = config.hashtag_pools
        self.used_hashtags_today = set()
        self.last_hashtag_reset = datetime.now().date()
    
    def generate_content(self, platform: str, content_type: str, region: str, 
                        language: str = 'en', offer: Dict = None) -> str:
        """Unified content generation"""
        
        # Content templates
        templates = {
            'twitter': {
                'gpu_deals': [
                    "🚀 Incredible GPU cluster deal! {gpu_count}x {gpu_type} at ${price_per_hour}/hour in {location}. Perfect for AI/ML workloads! {hashtags}",
                    "⚡ GPU Alert: {gpu_type} cluster available for ${price_per_hour}/hour! {uptime}% uptime guaranteed. Ideal for deep learning! {hashtags}",
                    "🔥 Hot deal: {gpu_count}x {gpu_type} GPUs in {location} - only ${price_per_hour}/hour! Great for neural networks! {hashtags}"
                ]
            },
            'telegram': {
                'gpu_deals': [
                    "🚀 **GPU DEAL ALERT** 🚀\n\n💻 {gpu_count}x {gpu_type}\n💰 ${price_per_hour}/hour\n📍 {location}\n⚡ {uptime}% uptime\n\nPerfect for AI/ML projects!"
                ]
            },
            'reddit': {
                'gpu_deals': [
                    "I've been researching cost-effective GPU solutions for AI development and discovered some interesting alternatives to traditional cloud providers. Has anyone experimented with decentralized GPU networks?"
                ]
            }
        }
        
        # Get template
        platform_templates = templates.get(platform, {})
        content_templates = platform_templates.get(content_type, ["Generic content for {platform}"])
        
        import random
        template = random.choice(content_templates)
        
        # Generate hashtags for Twitter
        hashtags = ""
        if platform == 'twitter':
            hashtags = self._get_diverse_hashtags(3)
        
        # Format content
        if offer:
            try:
                content = template.format(
                    gpu_count=offer.get('gpu_count', 4),
                    gpu_type=offer.get('gpu_type', 'H100'),
                    price_per_hour=offer.get('price_per_hour', 35.99),
                    location=offer.get('location', 'Singapore'),
                    uptime=offer.get('uptime', 99.5),
                    hashtags=hashtags,
                    platform=platform
                )
            except KeyError:
                content = template.replace('{hashtags}', hashtags).replace('{platform}', platform)
        else:
            content = template.replace('{hashtags}', hashtags).replace('{platform}', platform)
        
        # Record content generation
        content_hash = str(hash(content))
        self._record_content_usage(content_hash, platform, content_type, hashtags)
        
        return content
    
    def _get_diverse_hashtags(self, count: int = 3) -> str:
        """Generate diverse hashtags avoiding repetition"""
        today = datetime.now().date()
        
        # Reset used hashtags daily
        if today != self.last_hashtag_reset:
            self.used_hashtags_today.clear()
            self.last_hashtag_reset = today
        
        # Collect available hashtags
        all_hashtags = []
        for pool in self.hashtag_pools.values():
            all_hashtags.extend(pool)
        
        # Filter out recently used
        available_hashtags = [h for h in all_hashtags if h not in self.used_hashtags_today]
        
        if len(available_hashtags) < count:
            self.used_hashtags_today.clear()
            available_hashtags = all_hashtags
        
        # Select diverse hashtags from different pools
        selected = []
        pools_used = set()
        
        import random
        for pool_name, hashtags in self.hashtag_pools.items():
            if len(selected) >= count:
                break
            
            available_from_pool = [h for h in hashtags if h not in self.used_hashtags_today]
            if available_from_pool and pool_name not in pools_used:
                hashtag = random.choice(available_from_pool)
                selected.append(hashtag)
                self.used_hashtags_today.add(hashtag)
                pools_used.add(pool_name)
        
        return ' '.join(selected)
    
    def _record_content_usage(self, content_hash: str, platform: str, 
                             content_type: str, hashtags: str):
        """Record content usage for analytics"""
        query = '''
            INSERT OR REPLACE INTO content_data 
            (content_hash, platform, content_type, hashtags, usage_count, last_used)
            VALUES (?, ?, ?, ?, 
                    COALESCE((SELECT usage_count FROM content_data WHERE content_hash = ?), 0) + 1,
                    ?)
        '''
        params = (content_hash, platform, content_type, hashtags, 
                 content_hash, datetime.now().isoformat())
        
        self.data_manager.execute_query(query, params)

class UnifiedTimezoneOptimizer:
    """Centralized timezone optimization"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.timezone_regions = config.timezone_regions
        self.region_switch_interval = config.region_switch_interval
        self.last_region_switch = datetime.now()
        self.current_region = 'EU_WEST'
    
    def get_current_optimal_region(self) -> Tuple[str, str, str]:
        """Get optimal region with stable switching"""
        now = datetime.now()
        
        # Only switch regions every 4 hours
        if (now - self.last_region_switch).total_seconds() < self.region_switch_interval:
            return self.current_region, 'en', self.timezone_regions[self.current_region]['timezone']
        
        # Determine optimal region based on current time
        current_hour = now.hour
        
        if 6 <= current_hour <= 14:  # EU morning/afternoon
            region = 'EU_WEST'
        elif 14 <= current_hour <= 22:  # US East afternoon/evening
            region = 'US_EAST'
        elif 22 <= current_hour <= 6:  # Asia Pacific evening/night
            region = 'ASIA_PACIFIC'
        else:
            region = 'US_WEST'
        
        if region != self.current_region:
            self.current_region = region
            self.last_region_switch = now
            logging.info(f"🌍 Region switched to: {region}")
        
        return region, 'en', self.timezone_regions[region]['timezone']
    
    def is_peak_time(self, region: str) -> bool:
        """Check if current time is peak for region"""
        now = datetime.now()
        current_hour = now.hour
        
        if region in self.timezone_regions:
            peak_hours = self.timezone_regions[region]['peak_hours']
            return current_hour in peak_hours
        
        return False

class BotErrorHandler:
    """Unified error handling and logging"""
    
    def __init__(self):
        self.error_log = []
        self.error_counts = {}
    
    def handle_error(self, module: str, method: str, error: Exception, 
                    context: Dict = None) -> bool:
        """Handle error with unified logging and recovery"""
        error_key = f"{module}.{method}"
        
        # Count errors
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Log error
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'module': module,
            'method': method,
            'error': str(error),
            'error_type': type(error).__name__,
            'context': context or {},
            'count': self.error_counts[error_key]
        }
        
        self.error_log.append(error_info)
        
        # Keep only last 100 errors
        self.error_log = self.error_log[-100:]
        
        # Log to file
        logging.error(f"❌ {module}.{method}: {error} (count: {self.error_counts[error_key]})")
        
        # Determine if error is recoverable
        recoverable_errors = [
            'ConnectionError', 'TimeoutError', 'HTTPError', 
            'TooManyRequests', 'TemporaryFailure'
        ]
        
        return any(err_type in str(type(error)) for err_type in recoverable_errors)
    
    def get_error_summary(self) -> Dict:
        """Get error summary for monitoring"""
        if not self.error_log:
            return {'status': 'healthy', 'total_errors': 0}
        
        recent_errors = [e for e in self.error_log 
                        if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=1)]
        
        return {
            'status': 'degraded' if len(recent_errors) > 10 else 'healthy',
            'total_errors': len(self.error_log),
            'recent_errors': len(recent_errors),
            'top_errors': sorted(self.error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }

class UnifiedBotEngine:
    """Main unified engine coordinating all components"""
    
    def __init__(self):
        self.config = UnifiedConfig()
        self.data_manager = UnifiedDataManager(self.config)
        self.rate_limiter = UnifiedRateLimiter(self.config, self.data_manager)
        self.content_engine = UnifiedContentEngine(self.config, self.data_manager)
        self.timezone_optimizer = UnifiedTimezoneOptimizer(self.config)
        self.error_handler = BotErrorHandler()
        
        logging.info("🚀 Unified Bot Engine initialized")
    
    def can_post(self, platform: str, account_id: str = None) -> Tuple[bool, str, int]:
        """Unified posting check"""
        return self.rate_limiter.can_post(platform, account_id)
    
    def generate_content(self, platform: str, content_type: str, offer: Dict = None) -> str:
        """Unified content generation"""
        region, language, timezone_name = self.timezone_optimizer.get_current_optimal_region()
        return self.content_engine.generate_content(platform, content_type, region, language, offer)
    
    def record_post(self, platform: str, content: str, success: bool, 
                   engagement: int = 0, reach: int = 0, account_id: str = None):
        """Unified post recording"""
        # Record rate limiting
        if success:
            self.rate_limiter.record_post(platform, account_id)
        
        # Record performance
        region, language, _ = self.timezone_optimizer.get_current_optimal_region()
        content_hash = str(hash(content))
        score = (engagement + reach) / 100.0 if success else 0.0
        
        self.data_manager.record_performance(
            platform, region, language, 'auto_generated', content_hash,
            success, engagement, reach, score, 'unified_engine'
        )
    
    def get_status(self) -> Dict:
        """Get unified system status"""
        region, language, timezone_name = self.timezone_optimizer.get_current_optimal_region()
        is_peak = self.timezone_optimizer.is_peak_time(region)
        error_summary = self.error_handler.get_error_summary()
        
        # Get platform status
        platform_status = {}
        for platform in ['twitter', 'telegram', 'reddit']:
            can_post, reason, wait_time = self.rate_limiter.can_post(platform)
            platform_status[platform] = {
                'can_post': can_post,
                'reason': reason,
                'wait_time': wait_time,
                'next_available': self.rate_limiter.get_next_available_time(platform)
            }
        
        return {
            'current_region': region,
            'current_language': language,
            'is_peak_time': is_peak,
            'timezone': timezone_name,
            'platform_status': platform_status,
            'error_status': error_summary,
            'engine_status': 'operational'
        }
