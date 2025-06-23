#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Autonomous Discovery Module - BOT SHA-256
Automatically discovers and joins relevant Telegram groups and Reddit communities
"""

import asyncio
import logging
import random
import time
import json
import os
from typing import List, Dict, Set
from datetime import datetime, timedelta
import requests
import praw
import telegram
from telegram.error import TelegramError

class AutonomousGroupDiscovery:
    """Automatically discovers and joins relevant groups/communities"""
    
    def __init__(self, telegram_bot=None, reddit_clients=None):
        self.telegram_bot = telegram_bot
        self.reddit_clients = reddit_clients or []
        
        # Discovery patterns for different platforms
        self.telegram_search_patterns = {
            'en': [
                'AI', 'MachineLearning', 'DeepLearning', 'GPU', 'CloudComputing',
                'DataScience', 'NeuralNetworks', 'TensorFlow', 'PyTorch', 'CUDA',
                'Blockchain', 'Crypto', 'Mining', 'Tech', 'Programming', 'Python',
                'Developers', 'Startup', 'Innovation', 'Research'
            ],
            'zh': [
                '人工智能', '机器学习', '深度学习', 'GPU', '云计算',
                '数据科学', '神经网络', '区块链', '加密货币', '挖矿',
                '技术', '编程', '开发者', '创业', '创新', '研究'
            ],
            'pt': [
                'IA', 'MachineLearning', 'DeepLearning', 'GPU', 'Computacao',
                'DataScience', 'Blockchain', 'Crypto', 'Mineracao', 'Tech',
                'Programacao', 'Desenvolvedores', 'Startup', 'Inovacao'
            ],
            'de': [
                'KI', 'MachineLearning', 'DeepLearning', 'GPU', 'CloudComputing',
                'DataScience', 'Blockchain', 'Krypto', 'Tech', 'Programmierung',
                'Entwickler', 'Startup', 'Innovation', 'Forschung'
            ]
        }
        
        self.reddit_discovery_keywords = {
            'en': [
                'MachineLearning', 'DeepLearning', 'artificial', 'GPU', 'CloudComputing',
                'DataScience', 'programming', 'Python', 'compsci', 'technology',
                'startups', 'entrepreneur', 'LocalLLaMA', 'OpenAI', 'ChatGPT',
                'StableDiffusion', 'MLOps', 'ArtificialIntelligence', 'nvidia',
                'AMD', 'computing', 'servers', 'homelab', 'selfhosted'
            ]
        }
        
        # Discovered groups storage
        self.discovered_groups = {
            'telegram': set(),
            'reddit': set()
        }
        
        # Performance tracking for discovered groups
        self.group_performance = {}
        
        # Load previous discoveries
        self._load_discoveries()
    
    def _load_discoveries(self):
        """Load previously discovered groups"""
        try:
            if os.path.exists('discovered_groups.json'):
                with open('discovered_groups.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.discovered_groups['telegram'] = set(data.get('telegram', []))
                self.discovered_groups['reddit'] = set(data.get('reddit', []))
                self.group_performance = data.get('performance', {})
                
                logging.info(f"🔍 Loaded {len(self.discovered_groups['telegram'])} Telegram groups, {len(self.discovered_groups['reddit'])} Reddit communities")
        except Exception as e:
            logging.error(f"❌ Failed to load discoveries: {e}")
    
    def _save_discoveries(self):
        """Save discovered groups"""
        try:
            data = {
                'telegram': list(self.discovered_groups['telegram']),
                'reddit': list(self.discovered_groups['reddit']),
                'performance': self.group_performance,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('discovered_groups.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logging.info("💾 Discoveries saved successfully")
        except Exception as e:
            logging.error(f"❌ Failed to save discoveries: {e}")
    
    async def discover_telegram_groups(self, language: str = 'en', max_discoveries: int = 10):
        """Autonomously discover Telegram groups"""
        if not self.telegram_bot:
            return []
        
        discovered = []
        keywords = self.telegram_search_patterns.get(language, self.telegram_search_patterns['en'])
        
        # Common group naming patterns
        patterns = [
            '{keyword}',
            '{keyword}Group',
            '{keyword}Chat',
            '{keyword}Community',
            '{keyword}Hub',
            '{keyword}Network',
            '{keyword}Official',
            '{keyword}Global',
            '{keyword}World',
            'Official{keyword}',
            'Global{keyword}',
            '{keyword}Developers',
            '{keyword}Enthusiasts'
        ]
        
        for keyword in random.sample(keywords, min(5, len(keywords))):
            if len(discovered) >= max_discoveries:
                break
                
            for pattern in random.sample(patterns, min(3, len(patterns))):
                try:
                    # Generate potential group username
                    group_name = pattern.format(keyword=keyword)
                    group_username = f"@{group_name}"
                    
                    if group_username in self.discovered_groups['telegram']:
                        continue
                    
                    # Try to access the group
                    try:
                        chat = await self.telegram_bot.get_chat(group_username)
                        
                        if chat.type in ['group', 'supergroup', 'channel']:
                            # Try to get member count
                            try:
                                member_count = await self.telegram_bot.get_chat_member_count(group_username)
                                
                                # Only consider active groups
                                if member_count > 50:
                                    self.discovered_groups['telegram'].add(group_username)
                                    discovered.append({
                                        'username': group_username,
                                        'title': chat.title,
                                        'type': chat.type,
                                        'members': member_count,
                                        'keyword': keyword
                                    })
                                    
                                    logging.info(f"🔍 DISCOVERED: {group_username} ({member_count} members) via keyword '{keyword}'")
                                    
                                    # Rate limiting
                                    await asyncio.sleep(random.uniform(1, 3))
                                    
                            except TelegramError:
                                # Can't get member count, but group exists
                                self.discovered_groups['telegram'].add(group_username)
                                discovered.append({
                                    'username': group_username,
                                    'title': chat.title,
                                    'type': chat.type,
                                    'members': 'Unknown',
                                    'keyword': keyword
                                })
                                
                                logging.info(f"🔍 DISCOVERED: {group_username} (private count) via keyword '{keyword}'")
                                
                    except TelegramError:
                        # Group doesn't exist or is private
                        continue
                        
                except Exception as e:
                    logging.debug(f"Discovery error for {group_name}: {e}")
                    continue
                
                # Small delay between attempts
                await asyncio.sleep(random.uniform(0.5, 1.5))
        
        if discovered:
            self._save_discoveries()
            
        return discovered
    
    def discover_reddit_communities(self, language: str = 'en', max_discoveries: int = 15):
        """Autonomously discover Reddit communities"""
        if not self.reddit_clients:
            return []
        
        discovered = []
        keywords = self.reddit_discovery_keywords.get(language, self.reddit_discovery_keywords['en'])
        reddit = self.reddit_clients[0]['client']  # Use first Reddit client
        
        # Search patterns for subreddit names
        patterns = [
            '{keyword}',
            '{keyword}s',
            'r{keyword}',
            '{keyword}Community',
            '{keyword}Hub',
            '{keyword}Discussion',
            '{keyword}Help',
            '{keyword}News',
            'Learn{keyword}',
            '{keyword}Beginners',
            '{keyword}Advanced',
            '{keyword}Research',
            '{keyword}Dev',
            '{keyword}Developers'
        ]
        
        for keyword in random.sample(keywords, min(8, len(keywords))):
            if len(discovered) >= max_discoveries:
                break
                
            for pattern in random.sample(patterns, min(4, len(patterns))):
                try:
                    subreddit_name = pattern.format(keyword=keyword).lower()
                    
                    if subreddit_name in self.discovered_groups['reddit']:
                        continue
                    
                    # Try to access the subreddit
                    try:
                        subreddit = reddit.subreddit(subreddit_name)
                        
                        # Check if subreddit exists and is accessible
                        subreddit_info = {
                            'name': subreddit.display_name,
                            'title': subreddit.title,
                            'subscribers': subreddit.subscribers,
                            'description': subreddit.public_description[:200] if subreddit.public_description else '',
                            'keyword': keyword,
                            'over18': subreddit.over18
                        }
                        
                        # Only consider active subreddits
                        if subreddit_info['subscribers'] > 100 and not subreddit_info['over18']:
                            self.discovered_groups['reddit'].add(subreddit_name)
                            discovered.append(subreddit_info)
                            
                            logging.info(f"🔍 DISCOVERED: r/{subreddit_name} ({subreddit_info['subscribers']} subscribers) via keyword '{keyword}'")
                            
                    except Exception as e:
                        # Subreddit doesn't exist, is private, or banned
                        continue
                        
                except Exception as e:
                    logging.debug(f"Reddit discovery error for {keyword}: {e}")
                    continue
                
                # Rate limiting
                time.sleep(random.uniform(0.5, 1.0))
        
        if discovered:
            self._save_discoveries()
            
        return discovered
    
    def get_best_groups(self, platform: str, region: str, language: str, limit: int = 5) -> List[str]:
        """Get best performing groups for a platform/region/language"""
        if platform == 'telegram':
            groups = list(self.discovered_groups['telegram'])
        elif platform == 'reddit':
            groups = list(self.discovered_groups['reddit'])
        else:
            return []
        
        # Sort by performance if available
        if self.group_performance:
            groups.sort(key=lambda g: self.group_performance.get(g, {}).get('score', 0), reverse=True)
        
        return groups[:limit]
    
    def record_group_performance(self, group_name: str, success: bool, engagement: int = 0):
        """Record performance for a group"""
        if group_name not in self.group_performance:
            self.group_performance[group_name] = {
                'posts': 0,
                'successes': 0,
                'total_engagement': 0,
                'score': 0.0,
                'last_used': datetime.now().isoformat()
            }
        
        perf = self.group_performance[group_name]
        perf['posts'] += 1
        perf['last_used'] = datetime.now().isoformat()
        
        if success:
            perf['successes'] += 1
            perf['total_engagement'] += engagement
        
        # Calculate performance score
        success_rate = perf['successes'] / perf['posts']
        avg_engagement = perf['total_engagement'] / max(perf['successes'], 1)
        perf['score'] = success_rate * 0.7 + min(avg_engagement / 100, 1.0) * 0.3
        
        self._save_discoveries()
    
    async def autonomous_discovery_cycle(self, region: str, language: str):
        """Run a complete autonomous discovery cycle"""
        logging.info(f"🤖 Starting autonomous discovery for {region}/{language}")
        
        # Discover Telegram groups
        if self.telegram_bot:
            telegram_discoveries = await self.discover_telegram_groups(language, max_discoveries=5)
            if telegram_discoveries:
                logging.info(f"🔍 Discovered {len(telegram_discoveries)} new Telegram groups")
        
        # Discover Reddit communities
        if self.reddit_clients:
            reddit_discoveries = self.discover_reddit_communities(language, max_discoveries=8)
            if reddit_discoveries:
                logging.info(f"🔍 Discovered {len(reddit_discoveries)} new Reddit communities")
        
        # Clean up old/inactive groups
        self._cleanup_inactive_groups()
        
        logging.info(f"🤖 Discovery cycle complete. Total: {len(self.discovered_groups['telegram'])} Telegram, {len(self.discovered_groups['reddit'])} Reddit")
    
    def _cleanup_inactive_groups(self):
        """Remove groups that haven't performed well"""
        cutoff_date = datetime.now() - timedelta(days=7)
        
        groups_to_remove = []
        for group_name, perf in self.group_performance.items():
            last_used = datetime.fromisoformat(perf['last_used'])
            
            # Remove if not used recently and poor performance
            if last_used < cutoff_date and perf['score'] < 0.1 and perf['posts'] > 5:
                groups_to_remove.append(group_name)
        
        for group_name in groups_to_remove:
            # Remove from discovered groups
            self.discovered_groups['telegram'].discard(group_name)
            self.discovered_groups['reddit'].discard(group_name)
            
            # Remove performance data
            del self.group_performance[group_name]
            
            logging.info(f"🧹 Cleaned up inactive group: {group_name}")
        
        if groups_to_remove:
            self._save_discoveries()

class AutonomousContentOptimizer:
    """Automatically optimizes content based on performance"""
    
    def __init__(self):
        self.content_performance = {}
        self.optimization_rules = {}
        self._load_optimization_data()
    
    def _load_optimization_data(self):
        """Load content optimization data"""
        try:
            if os.path.exists('content_optimization.json'):
                with open('content_optimization.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.content_performance = data.get('performance', {})
                self.optimization_rules = data.get('rules', {})
                
                logging.info(f"🎯 Loaded optimization data for {len(self.content_performance)} content patterns")
        except Exception as e:
            logging.error(f"❌ Failed to load optimization data: {e}")
    
    def _save_optimization_data(self):
        """Save content optimization data"""
        try:
            data = {
                'performance': self.content_performance,
                'rules': self.optimization_rules,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('content_optimization.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logging.info("🎯 Content optimization data saved")
        except Exception as e:
            logging.error(f"❌ Failed to save optimization data: {e}")
    
    def analyze_content_pattern(self, content: str) -> Dict:
        """Analyze content to extract patterns"""
        patterns = {
            'has_emojis': len([c for c in content if ord(c) > 127]) > 0,
            'has_urgency': any(word in content.lower() for word in ['alert', 'urgent', 'limited', 'now', 'today']),
            'has_numbers': any(c.isdigit() for c in content),
            'has_percentage': '%' in content,
            'has_price': '$' in content,
            'has_hashtags': '#' in content,
            'length': len(content),
            'word_count': len(content.split()),
            'has_call_to_action': any(word in content.lower() for word in ['get', 'start', 'join', 'try', 'click', 'visit']),
            'has_social_proof': any(word in content.lower() for word in ['users', 'customers', 'people', 'community'])
        }
        
        return patterns
    
    def record_content_performance(self, content: str, platform: str, engagement: int, success: bool):
        """Record how content performed"""
        patterns = self.analyze_content_pattern(content)
        content_hash = str(hash(content))
        
        if content_hash not in self.content_performance:
            self.content_performance[content_hash] = {
                'patterns': patterns,
                'platform': platform,
                'performances': []
            }
        
        self.content_performance[content_hash]['performances'].append({
            'engagement': engagement,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update optimization rules
        self._update_optimization_rules()
        self._save_optimization_data()
    
    def _update_optimization_rules(self):
        """Update optimization rules based on performance data"""
        pattern_scores = {}
        
        for content_hash, data in self.content_performance.items():
            patterns = data['patterns']
            performances = data['performances']
            
            if not performances:
                continue
            
            # Calculate average performance
            avg_engagement = sum(p['engagement'] for p in performances) / len(performances)
            success_rate = sum(1 for p in performances if p['success']) / len(performances)
            score = success_rate * 0.7 + min(avg_engagement / 100, 1.0) * 0.3
            
            # Update pattern scores
            for pattern, value in patterns.items():
                if pattern not in pattern_scores:
                    pattern_scores[pattern] = {'true': [], 'false': []}
                
                pattern_scores[pattern][str(value).lower()].append(score)
        
        # Generate optimization rules
        for pattern, scores in pattern_scores.items():
            if len(scores['true']) > 2 and len(scores['false']) > 2:
                avg_true = sum(scores['true']) / len(scores['true'])
                avg_false = sum(scores['false']) / len(scores['false'])
                
                if abs(avg_true - avg_false) > 0.1:
                    self.optimization_rules[pattern] = {
                        'recommended': avg_true > avg_false,
                        'impact': abs(avg_true - avg_false),
                        'confidence': min(len(scores['true']), len(scores['false']))
                    }
    
    def get_content_recommendations(self, platform: str) -> List[str]:
        """Get content optimization recommendations"""
        recommendations = []
        
        for pattern, rule in self.optimization_rules.items():
            if rule['confidence'] >= 3 and rule['impact'] > 0.15:
                if rule['recommended']:
                    recommendations.append(f"✅ Include {pattern.replace('_', ' ')}")
                else:
                    recommendations.append(f"❌ Avoid {pattern.replace('_', ' ')}")
        
        return recommendations[:5]  # Top 5 recommendations
    
    def optimize_content(self, content: str, platform: str) -> str:
        """Automatically optimize content based on learned patterns"""
        optimized = content
        
        # Apply optimization rules
        for pattern, rule in self.optimization_rules.items():
            if rule['confidence'] >= 3:
                if pattern == 'has_urgency' and rule['recommended'] and 'urgent' not in optimized.lower():
                    optimized = f"🚨 URGENT: {optimized}"
                elif pattern == 'has_call_to_action' and rule['recommended'] and not any(word in optimized.lower() for word in ['get', 'start', 'join']):
                    optimized += "\n\n🚀 Get started now!"
        
        return optimized
