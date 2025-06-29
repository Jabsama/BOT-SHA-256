#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐦 Twitter Follow Manager - Intelligent Follow/Unfollow Automation
Safely manages Twitter follows and unfollows to grow audience while avoiding bans
"""

import json
import time
import random
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import tweepy

@dataclass
class TwitterUser:
    """Information about a Twitter user"""
    id: int
    username: str
    display_name: str
    followers_count: int
    following_count: int
    tweet_count: int
    verified: bool
    created_at: datetime
    bio: str
    location: str
    interests: List[str]
    relevance_score: float
    followed_at: Optional[datetime] = None
    unfollowed_at: Optional[datetime] = None
    follows_back: bool = False
    last_checked: Optional[datetime] = None

class TwitterFollowManager:
    """
    🐦 TWITTER FOLLOW/UNFOLLOW MANAGER
    
    ⚠️ TWITTER LIMITS (2024):
    - Follow: 400/day for new accounts, 1000/day for established accounts
    - Unfollow: No official limit, but 1000/day is safe
    - Follow/Following ratio: Must stay under 1.1 (110 following per 100 followers)
    - Rate limits: 15 follows per 15-minute window
    
    🛡️ SAFE STRATEGY:
    - 150 follows/day (well under limits)
    - 175 unfollows/day (maintain good ratio)
    - 48-72h follow-back grace period
    - Smart targeting based on interests
    """
    
    def __init__(self, twitter_client: tweepy.Client, db_path: str = 'data/twitter_follows.db'):
        self.client = twitter_client
        self.db_path = db_path
        
        # Safe daily limits (conservative approach)
        self.daily_follow_limit = 150      # Conservative: 150/day instead of 400
        self.daily_unfollow_limit = 175    # Slightly higher to maintain ratio
        self.follow_back_grace_hours = 72  # 3 days grace period
        self.min_interval_seconds = 60     # 1 minute between actions
        self.max_interval_seconds = 180    # 3 minutes between actions
        
        # Targeting keywords for relevant users
        self.target_keywords = [
            # AI/ML Keywords
            'artificial intelligence', 'machine learning', 'deep learning', 'neural networks',
            'data science', 'AI researcher', 'ML engineer', 'computer vision', 'NLP',
            
            # GPU/Computing Keywords
            'GPU computing', 'CUDA', 'parallel computing', 'high performance computing',
            'cloud computing', 'distributed computing', 'NVIDIA', 'AMD',
            
            # Crypto/Mining Keywords
            'cryptocurrency', 'crypto mining', 'blockchain', 'bitcoin mining', 'ethereum',
            'mining rig', 'crypto trader', 'DeFi', 'Web3',
            
            # Tech/Developer Keywords
            'software engineer', 'developer', 'programmer', 'tech entrepreneur',
            'startup founder', 'CTO', 'tech lead', 'DevOps', 'cloud architect',
            
            # Cost-Conscious Keywords
            'cost optimization', 'budget tech', 'affordable solutions', 'save money',
            'deal hunter', 'frugal', 'efficiency'
        ]
        
        # Initialize database
        self._init_database()
        
        # Load existing data
        self.followed_users = self._load_followed_users()
        self.daily_stats = self._load_daily_stats()
        
        logging.info("🐦 Twitter Follow Manager initialized with safe limits")
    
    def _init_database(self):
        """Initialize SQLite database for follow tracking"""
        try:
            import os
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    display_name TEXT,
                    followers_count INTEGER,
                    following_count INTEGER,
                    tweet_count INTEGER,
                    verified BOOLEAN,
                    created_at TEXT,
                    bio TEXT,
                    location TEXT,
                    interests TEXT,
                    relevance_score REAL,
                    followed_at TEXT,
                    unfollowed_at TEXT,
                    follows_back BOOLEAN DEFAULT FALSE,
                    last_checked TEXT
                )
            ''')
            
            # Daily stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    follows_count INTEGER DEFAULT 0,
                    unfollows_count INTEGER DEFAULT 0,
                    follow_backs_count INTEGER DEFAULT 0
                )
            ''')
            
            # Follow actions log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS follow_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    timestamp TEXT,
                    reason TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"❌ Database initialization failed: {e}")
    
    def _load_followed_users(self) -> Dict[int, TwitterUser]:
        """Load followed users from database"""
        users = {}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE followed_at IS NOT NULL AND unfollowed_at IS NULL')
            rows = cursor.fetchall()
            
            for row in rows:
                user = TwitterUser(
                    id=row[0],
                    username=row[1],
                    display_name=row[2],
                    followers_count=row[3],
                    following_count=row[4],
                    tweet_count=row[5],
                    verified=bool(row[6]),
                    created_at=datetime.fromisoformat(row[7]),
                    bio=row[8] or '',
                    location=row[9] or '',
                    interests=json.loads(row[10]) if row[10] else [],
                    relevance_score=row[11],
                    followed_at=datetime.fromisoformat(row[12]) if row[12] else None,
                    unfollowed_at=datetime.fromisoformat(row[13]) if row[13] else None,
                    follows_back=bool(row[14]),
                    last_checked=datetime.fromisoformat(row[15]) if row[15] else None
                )
                users[user.id] = user
            
            conn.close()
            logging.info(f"📊 Loaded {len(users)} followed users from database")
            
        except Exception as e:
            logging.error(f"❌ Failed to load followed users: {e}")
        
        return users
    
    def _load_daily_stats(self) -> Dict[str, Dict]:
        """Load daily statistics"""
        stats = {}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get last 7 days
            cursor.execute('''
                SELECT * FROM daily_stats 
                WHERE date >= date('now', '-7 days')
                ORDER BY date DESC
            ''')
            rows = cursor.fetchall()
            
            for row in rows:
                stats[row[0]] = {
                    'follows': row[1],
                    'unfollows': row[2],
                    'follow_backs': row[3]
                }
            
            conn.close()
            
        except Exception as e:
            logging.error(f"❌ Failed to load daily stats: {e}")
        
        return stats
    
    def _save_user(self, user: TwitterUser):
        """Save user to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user.id, user.username, user.display_name, user.followers_count,
                user.following_count, user.tweet_count, user.verified,
                user.created_at.isoformat(), user.bio, user.location,
                json.dumps(user.interests), user.relevance_score,
                user.followed_at.isoformat() if user.followed_at else None,
                user.unfollowed_at.isoformat() if user.unfollowed_at else None,
                user.follows_back,
                user.last_checked.isoformat() if user.last_checked else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"❌ Failed to save user {user.username}: {e}")
    
    def _log_action(self, user_id: int, action: str, reason: str):
        """Log follow/unfollow action"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO follow_actions (user_id, action, timestamp, reason)
                VALUES (?, ?, ?, ?)
            ''', (user_id, action, datetime.now().isoformat(), reason))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"❌ Failed to log action: {e}")
    
    def _update_daily_stats(self, action: str):
        """Update daily statistics"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get or create today's stats
            cursor.execute('SELECT * FROM daily_stats WHERE date = ?', (today,))
            row = cursor.fetchone()
            
            if row:
                follows = row[1]
                unfollows = row[2]
                follow_backs = row[3]
            else:
                follows = unfollows = follow_backs = 0
            
            # Update based on action
            if action == 'follow':
                follows += 1
            elif action == 'unfollow':
                unfollows += 1
            elif action == 'follow_back':
                follow_backs += 1
            
            cursor.execute('''
                INSERT OR REPLACE INTO daily_stats (date, follows_count, unfollows_count, follow_backs_count)
                VALUES (?, ?, ?, ?)
            ''', (today, follows, unfollows, follow_backs))
            
            conn.commit()
            conn.close()
            
            # Update in-memory stats
            self.daily_stats[today] = {
                'follows': follows,
                'unfollows': unfollows,
                'follow_backs': follow_backs
            }
            
        except Exception as e:
            logging.error(f"❌ Failed to update daily stats: {e}")
    
    def _calculate_relevance_score(self, user_data: dict) -> float:
        """Calculate relevance score for a user (0.0 to 1.0)"""
        score = 0.0
        
        # Bio analysis (40% weight)
        bio = (user_data.get('description') or '').lower()
        bio_score = 0.0
        for keyword in self.target_keywords:
            if keyword.lower() in bio:
                bio_score += 0.1
        score += min(bio_score, 0.4)
        
        # Follower quality (20% weight)
        followers = user_data.get('public_metrics', {}).get('followers_count', 0)
        following = user_data.get('public_metrics', {}).get('following_count', 0)
        
        if followers > 0 and following > 0:
            ratio = followers / following
            if 0.1 <= ratio <= 10:  # Good ratio
                score += 0.2
            elif ratio > 10:  # Very good ratio
                score += 0.15
        
        # Account age (15% weight)
        created_at = user_data.get('created_at')
        if created_at:
            try:
                account_age = (datetime.now() - datetime.fromisoformat(created_at.replace('Z', '+00:00'))).days
                if account_age > 365:  # Older than 1 year
                    score += 0.15
                elif account_age > 90:  # Older than 3 months
                    score += 0.1
            except:
                pass
        
        # Activity level (15% weight)
        tweets = user_data.get('public_metrics', {}).get('tweet_count', 0)
        if tweets > 1000:
            score += 0.15
        elif tweets > 100:
            score += 0.1
        elif tweets > 10:
            score += 0.05
        
        # Verification (10% weight)
        if user_data.get('verified'):
            score += 0.1
        
        return min(score, 1.0)
    
    def _get_today_stats(self) -> Dict[str, int]:
        """Get today's follow/unfollow stats"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.daily_stats.get(today, {'follows': 0, 'unfollows': 0, 'follow_backs': 0})
    
    def _can_follow_today(self) -> bool:
        """Check if we can follow more users today"""
        stats = self._get_today_stats()
        return stats['follows'] < self.daily_follow_limit
    
    def _can_unfollow_today(self) -> bool:
        """Check if we can unfollow more users today"""
        stats = self._get_today_stats()
        return stats['unfollows'] < self.daily_unfollow_limit
    
    def find_relevant_users(self, search_terms: List[str], limit: int = 50) -> List[TwitterUser]:
        """Find relevant users to follow based on search terms"""
        relevant_users = []
        
        try:
            for term in search_terms[:3]:  # Limit to 3 terms to avoid rate limits
                try:
                    # Search for users
                    users = self.client.search_recent_tweets(
                        query=f'"{term}" -is:retweet lang:en',
                        max_results=20,
                        expansions=['author_id'],
                        user_fields=['public_metrics', 'description', 'verified', 'created_at', 'location']
                    )
                    
                    if users.includes and 'users' in users.includes:
                        for user_data in users.includes['users']:
                            # Skip if already following
                            if user_data.id in self.followed_users:
                                continue
                            
                            # Calculate relevance
                            relevance = self._calculate_relevance_score(user_data)
                            
                            # Only consider users with good relevance
                            if relevance >= 0.3:
                                user = TwitterUser(
                                    id=user_data.id,
                                    username=user_data.username,
                                    display_name=user_data.name,
                                    followers_count=user_data.public_metrics['followers_count'],
                                    following_count=user_data.public_metrics['following_count'],
                                    tweet_count=user_data.public_metrics['tweet_count'],
                                    verified=user_data.verified or False,
                                    created_at=datetime.fromisoformat(user_data.created_at.replace('Z', '+00:00')),
                                    bio=user_data.description or '',
                                    location=user_data.location or '',
                                    interests=[term],
                                    relevance_score=relevance
                                )
                                relevant_users.append(user)
                    
                    # Rate limit protection
                    time.sleep(2)
                    
                except Exception as e:
                    logging.warning(f"⚠️ Search failed for term '{term}': {e}")
                    continue
            
            # Sort by relevance and return top results
            relevant_users.sort(key=lambda u: u.relevance_score, reverse=True)
            return relevant_users[:limit]
            
        except Exception as e:
            logging.error(f"❌ Failed to find relevant users: {e}")
            return []
    
    def follow_user(self, user: TwitterUser, reason: str = "Relevant content") -> bool:
        """Follow a user safely"""
        try:
            # Check daily limits
            if not self._can_follow_today():
                logging.info("📊 Daily follow limit reached")
                return False
            
            # Follow the user
            self.client.follow_user(user.id)
            
            # Update user data
            user.followed_at = datetime.now()
            self.followed_users[user.id] = user
            
            # Save to database
            self._save_user(user)
            self._log_action(user.id, 'follow', reason)
            self._update_daily_stats('follow')
            
            logging.info(f"✅ Followed @{user.username} (relevance: {user.relevance_score:.2f})")
            
            # Random delay to appear natural
            delay = random.randint(self.min_interval_seconds, self.max_interval_seconds)
            time.sleep(delay)
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to follow @{user.username}: {e}")
            return False
    
    def unfollow_user(self, user: TwitterUser, reason: str) -> bool:
        """Unfollow a user safely"""
        try:
            # Check daily limits
            if not self._can_unfollow_today():
                logging.info("📊 Daily unfollow limit reached")
                return False
            
            # Unfollow the user
            self.client.unfollow_user(user.id)
            
            # Update user data
            user.unfollowed_at = datetime.now()
            if user.id in self.followed_users:
                del self.followed_users[user.id]
            
            # Save to database
            self._save_user(user)
            self._log_action(user.id, 'unfollow', reason)
            self._update_daily_stats('unfollow')
            
            logging.info(f"❌ Unfollowed @{user.username} - {reason}")
            
            # Random delay to appear natural
            delay = random.randint(self.min_interval_seconds, self.max_interval_seconds)
            time.sleep(delay)
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to unfollow @{user.username}: {e}")
            return False
    
    def check_follow_backs(self) -> int:
        """Check which followed users have followed back"""
        follow_backs = 0
        
        try:
            # Get our current followers
            me = self.client.get_me(user_fields=['public_metrics'])
            my_followers = set()
            
            # Get followers (limited to avoid rate limits)
            followers = self.client.get_users_followers(
                me.data.id,
                max_results=1000,
                user_fields=['public_metrics']
            )
            
            if followers.data:
                my_followers = {user.id for user in followers.data}
            
            # Check each followed user
            for user_id, user in self.followed_users.items():
                if user_id in my_followers and not user.follows_back:
                    user.follows_back = True
                    user.last_checked = datetime.now()
                    self._save_user(user)
                    self._update_daily_stats('follow_back')
                    follow_backs += 1
                    logging.info(f"🎉 @{user.username} followed back!")
                elif user_id not in my_followers:
                    user.follows_back = False
                    user.last_checked = datetime.now()
                    self._save_user(user)
            
        except Exception as e:
            logging.error(f"❌ Failed to check follow backs: {e}")
        
        return follow_backs
    
    def get_unfollow_candidates(self) -> List[TwitterUser]:
        """Get users to unfollow (prioritize non-followers)"""
        candidates = []
        now = datetime.now()
        grace_period = timedelta(hours=self.follow_back_grace_hours)
        
        for user in self.followed_users.values():
            # Skip if within grace period
            if user.followed_at and (now - user.followed_at) < grace_period:
                continue
            
            # Priority 1: Users who don't follow back
            if not user.follows_back:
                candidates.append((user, "No follow back after grace period"))
            
            # Priority 2: Users followed more than 7 days ago
            elif user.followed_at and (now - user.followed_at) > timedelta(days=7):
                candidates.append((user, "Followed over 7 days ago"))
        
        # Sort by priority (non-followers first, then by follow date)
        candidates.sort(key=lambda x: (x[0].follows_back, x[0].followed_at or now))
        
        return candidates
    
    def auto_follow_cycle(self, max_follows: int = 10) -> Dict[str, int]:
        """Automated follow cycle"""
        results = {'followed': 0, 'skipped': 0, 'errors': 0}
        
        if not self._can_follow_today():
            logging.info("📊 Daily follow limit reached")
            return results
        
        # Search terms for relevant users
        search_terms = [
            'AI developer', 'machine learning engineer', 'GPU computing',
            'crypto mining', 'blockchain developer', 'cloud computing',
            'data scientist', 'tech entrepreneur', 'startup founder'
        ]
        
        # Find relevant users
        relevant_users = self.find_relevant_users(search_terms, limit=max_follows * 2)
        
        followed_count = 0
        for user in relevant_users:
            if followed_count >= max_follows or not self._can_follow_today():
                break
            
            # Additional filters
            if user.followers_count < 10 or user.followers_count > 100000:
                results['skipped'] += 1
                continue
            
            if user.following_count > user.followers_count * 5:  # Bad ratio
                results['skipped'] += 1
                continue
            
            # Follow the user
            if self.follow_user(user, f"Auto-follow: {user.relevance_score:.2f} relevance"):
                results['followed'] += 1
                followed_count += 1
            else:
                results['errors'] += 1
        
        return results
    
    def auto_unfollow_cycle(self, max_unfollows: int = 15) -> Dict[str, int]:
        """Automated unfollow cycle"""
        results = {'unfollowed': 0, 'skipped': 0, 'errors': 0}
        
        if not self._can_unfollow_today():
            logging.info("📊 Daily unfollow limit reached")
            return results
        
        # Get unfollow candidates
        candidates = self.get_unfollow_candidates()
        
        unfollowed_count = 0
        for user, reason in candidates:
            if unfollowed_count >= max_unfollows or not self._can_unfollow_today():
                break
            
            if self.unfollow_user(user, reason):
                results['unfollowed'] += 1
                unfollowed_count += 1
            else:
                results['errors'] += 1
        
        return results
    
    def get_follow_stats(self) -> Dict:
        """Get comprehensive follow statistics"""
        today_stats = self._get_today_stats()
        
        # Calculate ratios and health metrics
        total_followed = len(self.followed_users)
        follow_backs = sum(1 for user in self.followed_users.values() if user.follows_back)
        follow_back_rate = (follow_backs / total_followed * 100) if total_followed > 0 else 0
        
        return {
            'today': today_stats,
            'total_following': total_followed,
            'follow_backs': follow_backs,
            'follow_back_rate': follow_back_rate,
            'daily_limits': {
                'follow_limit': self.daily_follow_limit,
                'unfollow_limit': self.daily_unfollow_limit,
                'follow_remaining': self.daily_follow_limit - today_stats['follows'],
                'unfollow_remaining': self.daily_unfollow_limit - today_stats['unfollows']
            },
            'grace_period_hours': self.follow_back_grace_hours
        }
    
    def run_daily_cycle(self) -> Dict:
        """Run complete daily follow/unfollow cycle"""
        logging.info("🐦 Starting daily Twitter follow/unfollow cycle")
        
        # Check follow backs first
        follow_backs = self.check_follow_backs()
        
        # Auto follow cycle (conservative)
        follow_results = self.auto_follow_cycle(max_follows=8)
        
        # Wait between cycles
        time.sleep(random.randint(300, 600))  # 5-10 minutes
        
        # Auto unfollow cycle
        unfollow_results = self.auto_unfollow_cycle(max_unfollows=10)
        
        # Get final stats
        stats = self.get_follow_stats()
        
        results = {
            'follow_backs_detected': follow_backs,
            'follows': follow_results,
            'unfollows': unfollow_results,
            'final_stats': stats
        }
        
        logging.info(f"🐦 Daily cycle complete: {follow_results['followed']} follows, {unfollow_results['unfollowed']} unfollows")
        
        return results
