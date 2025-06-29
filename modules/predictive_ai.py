#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Predictive AI Module - BOT SHA-256
Advanced AI for trend prediction, hashtag optimization, and tone adaptation
"""

import json
import logging
import random
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import re
from collections import Counter

class PredictiveAI:
    """Advanced AI for performance prediction and optimization"""
    
    def __init__(self):
        self.trending_keywords = []
        self.hashtag_performance = {}
        self.tone_performance = {}
        self.trend_cache = {}
        self.last_trend_update = None
        
        # Load historical data
        self._load_performance_data()
        
    def _load_performance_data(self):
        """Load historical performance data"""
        try:
            with open('data/predictive_performance.json', 'r') as f:
                data = json.load(f)
                self.hashtag_performance = data.get('hashtags', {})
                self.tone_performance = data.get('tones', {})
                self.trend_cache = data.get('trends', {})
        except FileNotFoundError:
            logging.info("🤖 Initializing new predictive AI data")
            self.hashtag_performance = {}
            self.tone_performance = {}
            self.trend_cache = {}
    
    def _save_performance_data(self):
        """Save performance data"""
        try:
            import os
            os.makedirs('data', exist_ok=True)
            
            data = {
                'hashtags': self.hashtag_performance,
                'tones': self.tone_performance,
                'trends': self.trend_cache,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('data/predictive_performance.json', 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logging.error(f"❌ Failed to save predictive data: {e}")
    
    def predict_trending_keywords(self) -> List[str]:
        """Predict trending keywords based on tech news and patterns"""
        # Check if we need to update trends (every 6 hours)
        if (self.last_trend_update is None or 
            datetime.now() - self.last_trend_update > timedelta(hours=6)):
            
            self._update_trending_keywords()
            self.last_trend_update = datetime.now()
        
        return self.trending_keywords[:10]  # Top 10 trending
    
    def _update_trending_keywords(self):
        """Update trending keywords from various sources"""
        trending = []
        
        # Tech trends (simulated - in production would use real APIs)
        tech_trends = [
            'ChatGPT', 'OpenAI', 'Claude', 'Anthropic', 'LLaMA', 'Mistral',
            'NVIDIA', 'H100', 'A100', 'RTX4090', 'RTX5090', 'Blackwell',
            'Kubernetes', 'Docker', 'AWS', 'Azure', 'GCP', 'Terraform',
            'React', 'NextJS', 'Python', 'Rust', 'Go', 'TypeScript',
            'Bitcoin', 'Ethereum', 'Solana', 'DeFi', 'Web3', 'Blockchain',
            'Startup', 'YCombinator', 'TechCrunch', 'ProductHunt', 'GitHub'
        ]
        
        # Add seasonal/time-based trends
        current_month = datetime.now().month
        if current_month in [1, 2]:  # Q1
            tech_trends.extend(['NewYear', 'Q1Goals', 'TechResolutions'])
        elif current_month in [3, 4, 5]:  # Q2
            tech_trends.extend(['SpringTech', 'Conferences', 'LaunchSeason'])
        elif current_month in [6, 7, 8]:  # Q3
            tech_trends.extend(['SummerHack', 'Internships', 'TechSummer'])
        elif current_month in [9, 10, 11, 12]:  # Q4
            tech_trends.extend(['BackToSchool', 'TechFall', 'YearEnd'])
        
        # Simulate trend scoring (in production would use real data)
        scored_trends = []
        for trend in tech_trends:
            score = random.uniform(0.1, 1.0)  # Simulate trend score
            scored_trends.append((trend, score))
        
        # Sort by score and take top trends
        scored_trends.sort(key=lambda x: x[1], reverse=True)
        self.trending_keywords = [trend[0] for trend in scored_trends[:20]]
        
        logging.info(f"🔮 Updated trending keywords: {self.trending_keywords[:5]}...")
    
    def optimize_hashtags(self, content: str, platform: str, current_hashtags: List[str]) -> List[str]:
        """Optimize hashtags based on performance data and trends"""
        optimized = []
        
        # Get trending keywords
        trending = self.predict_trending_keywords()
        
        # Analyze content for relevant keywords
        content_lower = content.lower()
        relevant_trends = [t for t in trending if t.lower() in content_lower]
        
        # Platform-specific hashtag pools
        platform_hashtags = {
            'twitter': {
                'viral': ['Viral', 'Trending', 'Breaking', 'Urgent', 'Alert', 'Exposed'],
                'tech': ['Tech', 'AI', 'GPU', 'Cloud', 'DevOps', 'Startup'],
                'money': ['Money', 'Savings', 'Deal', 'Discount', 'Cheap', 'Free'],
                'crypto': ['Crypto', 'Bitcoin', 'Mining', 'Blockchain', 'DeFi']
            },
            'telegram': {
                'community': ['Community', 'Group', 'Chat', 'Discussion'],
                'tech': ['TechNews', 'Innovation', 'Development', 'Programming'],
                'business': ['Business', 'Entrepreneur', 'Startup', 'Growth']
            }
        }
        
        # Get platform-specific hashtags
        platform_pool = platform_hashtags.get(platform, platform_hashtags['twitter'])
        
        # Add high-performing hashtags from history
        for hashtag, perf in self.hashtag_performance.items():
            if perf.get('success_rate', 0) > 0.7 and len(optimized) < 3:
                optimized.append(hashtag)
        
        # Add trending hashtags
        for trend in relevant_trends[:2]:
            if len(optimized) < 5:
                optimized.append(trend)
        
        # Add platform-specific hashtags
        for category, hashtags in platform_pool.items():
            if any(keyword in content_lower for keyword in ['gpu', 'cloud', 'aws']) and category == 'tech':
                optimized.extend(random.sample(hashtags, min(2, len(hashtags))))
            elif any(keyword in content_lower for keyword in ['save', 'cheap', 'discount']) and category == 'money':
                optimized.extend(random.sample(hashtags, min(2, len(hashtags))))
        
        # Remove duplicates and limit to 5
        optimized = list(dict.fromkeys(optimized))[:5]
        
        # If still not enough, add from current hashtags
        for hashtag in current_hashtags:
            if len(optimized) < 5 and hashtag not in optimized:
                optimized.append(hashtag)
        
        return optimized[:5]
    
    def adapt_tone(self, content: str, platform: str, region: str, time_of_day: int) -> str:
        """Adapt content tone based on performance data and context"""
        
        # Analyze current tone
        current_tone = self._analyze_tone(content)
        
        # Get optimal tone for context
        optimal_tone = self._get_optimal_tone(platform, region, time_of_day)
        
        # If current tone is already optimal, return as-is
        if current_tone == optimal_tone:
            return content
        
        # Adapt content to optimal tone
        adapted_content = self._apply_tone_adaptation(content, current_tone, optimal_tone)
        
        return adapted_content
    
    def _analyze_tone(self, content: str) -> str:
        """Analyze the current tone of content"""
        content_lower = content.lower()
        
        # Tone indicators
        urgent_words = ['urgent', 'breaking', 'alert', 'now', 'limited', 'hurry']
        excited_words = ['amazing', 'incredible', 'insane', 'wow', 'fantastic']
        professional_words = ['enterprise', 'solution', 'optimize', 'efficiency']
        casual_words = ['hey', 'guys', 'check', 'cool', 'awesome']
        
        # Count tone indicators
        urgent_score = sum(1 for word in urgent_words if word in content_lower)
        excited_score = sum(1 for word in excited_words if word in content_lower)
        professional_score = sum(1 for word in professional_words if word in content_lower)
        casual_score = sum(1 for word in casual_words if word in content_lower)
        
        # Determine dominant tone
        scores = {
            'urgent': urgent_score,
            'excited': excited_score,
            'professional': professional_score,
            'casual': casual_score
        }
        
        return max(scores, key=scores.get)
    
    def _get_optimal_tone(self, platform: str, region: str, time_of_day: int) -> str:
        """Get optimal tone based on context"""
        
        # Platform preferences
        platform_tones = {
            'twitter': 'excited',  # Twitter loves excitement
            'telegram': 'casual',  # Telegram is more casual
            'reddit': 'professional'  # Reddit prefers professional tone
        }
        
        # Regional preferences
        regional_tones = {
            'US_EAST': 'excited',
            'US_WEST': 'casual',
            'EU_WEST': 'professional',
            'ASIA': 'professional'
        }
        
        # Time-based preferences
        if 9 <= time_of_day <= 17:  # Business hours
            time_tone = 'professional'
        elif 18 <= time_of_day <= 22:  # Evening
            time_tone = 'excited'
        else:  # Night/early morning
            time_tone = 'casual'
        
        # Combine preferences (platform has highest weight)
        platform_tone = platform_tones.get(platform, 'excited')
        
        # Check historical performance
        context_key = f"{platform}_{region}_{time_of_day//6}"  # 6-hour blocks
        if context_key in self.tone_performance:
            best_tone = max(self.tone_performance[context_key], 
                          key=lambda x: self.tone_performance[context_key][x].get('success_rate', 0))
            return best_tone
        
        return platform_tone
    
    def _apply_tone_adaptation(self, content: str, current_tone: str, target_tone: str) -> str:
        """Apply tone adaptation to content"""
        
        if current_tone == target_tone:
            return content
        
        adapted = content
        
        # Tone transformation rules
        if target_tone == 'urgent':
            if not any(word in content.lower() for word in ['urgent', 'breaking', 'alert']):
                adapted = f"🚨 URGENT: {adapted}"
            
        elif target_tone == 'excited':
            # Add excitement markers
            adapted = re.sub(r'!', '! 🔥', adapted, count=1)
            if '🤯' not in adapted and '🚨' not in adapted:
                adapted = f"🤯 {adapted}"
                
        elif target_tone == 'professional':
            # Remove excessive emojis and caps
            adapted = re.sub(r'🚨|🔥|🤯|💥', '', adapted)
            adapted = re.sub(r'[A-Z]{3,}', lambda m: m.group().title(), adapted)
            
        elif target_tone == 'casual':
            # Make more conversational
            if not adapted.startswith(('Hey', 'Hi', 'Check')):
                adapted = f"Hey! {adapted}"
        
        return adapted
    
    def record_performance(self, hashtags: List[str], tone: str, platform: str, 
                          region: str, time_of_day: int, success: bool, engagement: int = 0):
        """Record performance data for learning"""
        
        # Record hashtag performance
        for hashtag in hashtags:
            if hashtag not in self.hashtag_performance:
                self.hashtag_performance[hashtag] = {
                    'uses': 0,
                    'successes': 0,
                    'total_engagement': 0,
                    'success_rate': 0.0
                }
            
            perf = self.hashtag_performance[hashtag]
            perf['uses'] += 1
            if success:
                perf['successes'] += 1
                perf['total_engagement'] += engagement
            
            perf['success_rate'] = perf['successes'] / perf['uses']
        
        # Record tone performance
        context_key = f"{platform}_{region}_{time_of_day//6}"
        if context_key not in self.tone_performance:
            self.tone_performance[context_key] = {}
        
        if tone not in self.tone_performance[context_key]:
            self.tone_performance[context_key][tone] = {
                'uses': 0,
                'successes': 0,
                'success_rate': 0.0
            }
        
        tone_perf = self.tone_performance[context_key][tone]
        tone_perf['uses'] += 1
        if success:
            tone_perf['successes'] += 1
        
        tone_perf['success_rate'] = tone_perf['successes'] / tone_perf['uses']
        
        # Save data
        self._save_performance_data()
    
    def get_predictions(self, platform: str, region: str) -> Dict:
        """Get AI predictions for optimal posting"""
        
        current_hour = datetime.now().hour
        trending = self.predict_trending_keywords()
        optimal_tone = self._get_optimal_tone(platform, region, current_hour)
        
        # Predict best hashtags
        top_hashtags = sorted(
            self.hashtag_performance.items(),
            key=lambda x: x[1].get('success_rate', 0),
            reverse=True
        )[:5]
        
        return {
            'trending_keywords': trending[:5],
            'optimal_tone': optimal_tone,
            'best_hashtags': [h[0] for h in top_hashtags],
            'confidence': min(len(self.hashtag_performance) / 50, 1.0),  # Confidence based on data
            'recommendations': [
                f"Use trending keyword: {trending[0]}" if trending else "Gather more trend data",
                f"Optimal tone: {optimal_tone}",
                f"Best performing hashtag: {top_hashtags[0][0]}" if top_hashtags else "Collect hashtag data"
            ]
        }
