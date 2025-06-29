#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Autonomous Group Discovery Module - BOT SHA-256
Intelligent discovery and management of social media groups
"""

import asyncio
import json
import logging
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sqlite3
import os

class AutonomousGroupDiscovery:
    """Autonomous discovery and management of social media groups"""
    
    def __init__(self, telegram_bot=None, reddit_clients=None):
        self.telegram_bot = telegram_bot
        self.reddit_clients = reddit_clients or []
        
        # Initialize discovered groups storage
        self.discovered_groups = {
            'telegram': [],
            'reddit': []
        }
        
        # Performance tracking
        self.group_performance = {}
        
        # Discovery parameters
        self.discovery_keywords = {
            'gpu': ['gpu', 'graphics', 'nvidia', 'amd', 'mining', 'ai', 'ml'],
            'crypto': ['crypto', 'bitcoin', 'ethereum', 'mining', 'blockchain'],
            'tech': ['tech', 'technology', 'programming', 'coding', 'development'],
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'deep learning']
        }
        
        # Load existing discoveries
        self._load_discoveries()
        
        logging.info("🔍 Autonomous Group Discovery initialized")
    
    async def autonomous_discovery_cycle(self, region: str, language: str):
        """Run autonomous discovery cycle for a specific region/language"""
        try:
            # Discover Telegram groups
            if self.telegram_bot:
                await self._discover_telegram_groups(region, language)
            
            # Discover Reddit communities
            if self.reddit_clients:
                await self._discover_reddit_communities(region, language)
            
            # Clean up inactive groups
            self._cleanup_inactive_groups()
            
            # Save discoveries
            self._save_discoveries()
            
            logging.info(f"🔍 Discovery cycle completed for {region}/{language}")
            
        except Exception as e:
            logging.error(f"❌ Discovery cycle failed: {e}")
    
    async def _discover_telegram_groups(self, region: str, language: str):
        """Discover relevant Telegram groups"""
        try:
            # For now, use predefined groups based on region/language
            # In a real implementation, this would use Telegram's search API
            
            regional_groups = self._get_regional_telegram_groups(region, language)
            
            for group_info in regional_groups:
                if group_info not in self.discovered_groups['telegram']:
                    # Test group accessibility
                    try:
                        # Try to get chat info (this would work for public groups)
                        # For demo purposes, we'll simulate this
                        self.discovered_groups['telegram'].append(group_info)
                        logging.info(f"🔍 Discovered Telegram group: {group_info['name']}")
                        
                        # Initialize performance tracking
                        self.group_performance[group_info['id']] = {
                            'platform': 'telegram',
                            'success_rate': 0.0,
                            'total_posts': 0,
                            'successful_posts': 0,
                            'last_post': None,
                            'discovered_at': datetime.now().isoformat()
                        }
                        
                    except Exception as e:
                        logging.warning(f"⚠️ Cannot access Telegram group {group_info['name']}: {e}")
                        continue
                        
        except Exception as e:
            logging.error(f"❌ Telegram discovery failed: {e}")
    
    async def _discover_reddit_communities(self, region: str, language: str):
        """Discover relevant Reddit communities"""
        try:
            if not self.reddit_clients:
                return
                
            reddit_client = self.reddit_clients[0]['client']
            
            # Search for relevant subreddits
            keywords = self._get_discovery_keywords(region, language)
            
            for keyword in keywords[:3]:  # Limit to avoid rate limits
                try:
                    # Search subreddits
                    subreddits = reddit_client.subreddits.search(keyword, limit=5)
                    
                    for subreddit in subreddits:
                        subreddit_info = {
                            'name': subreddit.display_name,
                            'id': subreddit.display_name,
                            'subscribers': subreddit.subscribers,
                            'description': subreddit.public_description[:200] if subreddit.public_description else '',
                            'region': region,
                            'language': language,
                            'keyword': keyword
                        }
                        
                        # Check if already discovered
                        if not any(g['name'] == subreddit_info['name'] for g in self.discovered_groups['reddit']):
                            # Validate subreddit (check if we can post)
                            if self._validate_reddit_community(reddit_client, subreddit):
                                self.discovered_groups['reddit'].append(subreddit_info)
                                logging.info(f"🔍 Discovered Reddit community: r/{subreddit_info['name']}")
                                
                                # Initialize performance tracking
                                self.group_performance[subreddit_info['name']] = {
                                    'platform': 'reddit',
                                    'success_rate': 0.0,
                                    'total_posts': 0,
                                    'successful_posts': 0,
                                    'last_post': None,
                                    'discovered_at': datetime.now().isoformat()
                                }
                    
                    # Rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logging.warning(f"⚠️ Reddit search for '{keyword}' failed: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"❌ Reddit discovery failed: {e}")
    
    def _get_regional_telegram_groups(self, region: str, language: str) -> List[Dict]:
        """Get predefined Telegram groups for region/language"""
        # This would be expanded with real group discovery
        regional_groups = {
            'US_EAST': {
                'en': [
                    {'id': '@TechDeals', 'name': 'Tech Deals', 'type': 'public'},
                    {'id': '@GPUMining', 'name': 'GPU Mining', 'type': 'public'},
                    {'id': '@CryptoTech', 'name': 'Crypto Tech', 'type': 'public'}
                ]
            },
            'EU_WEST': {
                'en': [
                    {'id': '@EuroTech', 'name': 'Euro Tech', 'type': 'public'},
                    {'id': '@EUMining', 'name': 'EU Mining', 'type': 'public'}
                ]
            },
            'ASIA_PACIFIC': {
                'en': [
                    {'id': '@AsiaTech', 'name': 'Asia Tech', 'type': 'public'},
                    {'id': '@APACMining', 'name': 'APAC Mining', 'type': 'public'}
                ]
            }
        }
        
        return regional_groups.get(region, {}).get(language, [])
    
    def _get_discovery_keywords(self, region: str, language: str) -> List[str]:
        """Get discovery keywords based on region and language"""
        base_keywords = []
        
        # Add all keyword categories
        for category, keywords in self.discovery_keywords.items():
            base_keywords.extend(keywords)
        
        # Add regional variations
        if region == 'US_EAST':
            base_keywords.extend(['usa', 'america', 'us'])
        elif region == 'EU_WEST':
            base_keywords.extend(['europe', 'eu', 'european'])
        elif region == 'ASIA_PACIFIC':
            base_keywords.extend(['asia', 'apac', 'pacific'])
        
        return base_keywords
    
    def _validate_reddit_community(self, reddit_client, subreddit) -> bool:
        """Validate if we can post to a Reddit community"""
        try:
            # Check basic requirements
            if subreddit.subscribers < 1000:  # Too small
                return False
            
            if subreddit.subscribers > 1000000:  # Too large (likely strict moderation)
                return False
            
            # Check if subreddit allows text posts
            if not subreddit.submission_type in ['any', 'self']:
                return False
            
            # Check if we're banned (this would require more complex logic)
            # For now, assume we're not banned
            
            return True
            
        except Exception as e:
            logging.warning(f"⚠️ Validation failed for r/{subreddit.display_name}: {e}")
            return False
    
    def record_group_performance(self, group_id: str, success: bool, engagement: int = 0):
        """Record performance for a group"""
        if group_id not in self.group_performance:
            self.group_performance[group_id] = {
                'platform': 'unknown',
                'success_rate': 0.0,
                'total_posts': 0,
                'successful_posts': 0,
                'last_post': None,
                'discovered_at': datetime.now().isoformat()
            }
        
        perf = self.group_performance[group_id]
        perf['total_posts'] += 1
        perf['last_post'] = datetime.now().isoformat()
        
        if success:
            perf['successful_posts'] += 1
        
        # Update success rate
        perf['success_rate'] = perf['successful_posts'] / perf['total_posts']
        
        # Store engagement data
        if 'engagement_history' not in perf:
            perf['engagement_history'] = []
        
        perf['engagement_history'].append({
            'timestamp': datetime.now().isoformat(),
            'engagement': engagement,
            'success': success
        })
        
        # Keep only last 10 engagement records
        perf['engagement_history'] = perf['engagement_history'][-10:]
    
    def get_best_groups(self, platform: str, limit: int = 5) -> List[Dict]:
        """Get best performing groups for a platform"""
        platform_groups = []
        
        for group_id, perf in self.group_performance.items():
            if perf['platform'] == platform and perf['total_posts'] > 0:
                # Find group info
                group_info = None
                for group in self.discovered_groups[platform]:
                    if group['id'] == group_id or group['name'] == group_id:
                        group_info = group
                        break
                
                if group_info:
                    platform_groups.append({
                        'group': group_info,
                        'performance': perf
                    })
        
        # Sort by success rate and total posts
        platform_groups.sort(
            key=lambda x: (x['performance']['success_rate'], x['performance']['total_posts']),
            reverse=True
        )
        
        return platform_groups[:limit]
    
    def _cleanup_inactive_groups(self):
        """Remove groups that haven't been used or are performing poorly"""
        cutoff_date = datetime.now() - timedelta(days=30)
        
        groups_to_remove = []
        
        for group_id, perf in self.group_performance.items():
            # Remove if no posts in 30 days
            if perf['last_post']:
                last_post = datetime.fromisoformat(perf['last_post'])
                if last_post < cutoff_date:
                    groups_to_remove.append(group_id)
            
            # Remove if success rate is very low after many attempts
            elif perf['total_posts'] > 10 and perf['success_rate'] < 0.1:
                groups_to_remove.append(group_id)
        
        # Remove from performance tracking
        for group_id in groups_to_remove:
            del self.group_performance[group_id]
            logging.info(f"🧹 Removed inactive group: {group_id}")
        
        # Remove from discovered groups
        for platform in self.discovered_groups:
            self.discovered_groups[platform] = [
                group for group in self.discovered_groups[platform]
                if group['id'] not in groups_to_remove and group.get('name') not in groups_to_remove
            ]
    
    def _save_discoveries(self):
        """Save discoveries to file"""
        try:
            data = {
                'discovered_groups': self.discovered_groups,
                'group_performance': self.group_performance,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('autonomous_discoveries.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logging.info(f"💾 Saved discoveries: {len(self.discovered_groups['telegram'])} Telegram, {len(self.discovered_groups['reddit'])} Reddit")
            
        except Exception as e:
            logging.error(f"❌ Failed to save discoveries: {e}")
    
    def _load_discoveries(self):
        """Load discoveries from file"""
        try:
            if os.path.exists('autonomous_discoveries.json'):
                with open('autonomous_discoveries.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.discovered_groups = data.get('discovered_groups', {'telegram': [], 'reddit': []})
                self.group_performance = data.get('group_performance', {})
                
                total_groups = len(self.discovered_groups['telegram']) + len(self.discovered_groups['reddit'])
                logging.info(f"📂 Loaded {total_groups} discovered groups")
                
        except Exception as e:
            logging.error(f"❌ Failed to load discoveries: {e}")
    
    def get_discovery_stats(self) -> Dict:
        """Get discovery statistics"""
        stats = {
            'total_groups': len(self.discovered_groups['telegram']) + len(self.discovered_groups['reddit']),
            'telegram_groups': len(self.discovered_groups['telegram']),
            'reddit_groups': len(self.discovered_groups['reddit']),
            'active_groups': 0,
            'avg_success_rate': 0.0
        }
        
        if self.group_performance:
            active_groups = [p for p in self.group_performance.values() if p['total_posts'] > 0]
            stats['active_groups'] = len(active_groups)
            
            if active_groups:
                stats['avg_success_rate'] = sum(p['success_rate'] for p in active_groups) / len(active_groups)
        
        return stats
