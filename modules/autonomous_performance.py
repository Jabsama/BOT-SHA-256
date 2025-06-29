#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Autonomous Performance Module - BOT SHA-256
Self-improving performance analysis and optimization
"""

import json
import logging
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import numpy as np
from collections import defaultdict

class AutonomousPerformanceEngine:
    """Self-improving performance analysis engine"""
    
    def __init__(self, db_path: str = 'autonomous_performance.db'):
        self.db_path = db_path
        self.performance_weights = {
            'success_rate': 0.4,
            'engagement_rate': 0.3,
            'reach_growth': 0.2,
            'conversion_rate': 0.1
        }
        
        # Learning parameters
        self.learning_rate = 0.1
        self.min_samples_for_learning = 5
        
        # Performance thresholds
        self.thresholds = {
            'excellent': 0.8,
            'good': 0.6,
            'average': 0.4,
            'poor': 0.2
        }
        
        self.init_database()
        self.performance_insights = {}
        self.optimization_strategies = {}
        self._load_insights()
    
    def init_database(self):
        """Initialize autonomous performance database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced performance tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autonomous_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                platform TEXT NOT NULL,
                region TEXT NOT NULL,
                language TEXT NOT NULL,
                content_type TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                
                -- Performance metrics
                success BOOLEAN NOT NULL,
                engagement_count INTEGER DEFAULT 0,
                reach_count INTEGER DEFAULT 0,
                click_count INTEGER DEFAULT 0,
                conversion_count INTEGER DEFAULT 0,
                
                -- Context data
                hour_of_day INTEGER,
                day_of_week INTEGER,
                timezone TEXT,
                group_name TEXT,
                
                -- Content analysis
                content_length INTEGER,
                has_emojis BOOLEAN,
                has_urgency BOOLEAN,
                has_numbers BOOLEAN,
                has_hashtags BOOLEAN,
                has_call_to_action BOOLEAN,
                
                -- Performance score (calculated)
                performance_score REAL DEFAULT 0.0
            )
        ''')
        
        # Learning insights storage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT NOT NULL,
                platform TEXT NOT NULL,
                region TEXT,
                language TEXT,
                insight_data TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Optimization strategies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_name TEXT NOT NULL,
                platform TEXT NOT NULL,
                region TEXT,
                language TEXT,
                strategy_data TEXT NOT NULL,
                effectiveness_score REAL DEFAULT 0.0,
                times_applied INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_performance(self, platform: str, region: str, language: str, 
                          content_type: str, content: str, success: bool,
                          engagement: int = 0, reach: int = 0, clicks: int = 0, 
                          conversions: int = 0, group_name: str = None):
        """Record performance data for autonomous learning"""
        
        # Analyze content
        content_analysis = self._analyze_content(content)
        content_hash = str(hash(content))
        
        # Calculate performance score
        performance_score = self._calculate_performance_score(
            success, engagement, reach, clicks, conversions
        )
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        cursor.execute('''
            INSERT INTO autonomous_performance (
                platform, region, language, content_type, content_hash,
                success, engagement_count, reach_count, click_count, conversion_count,
                hour_of_day, day_of_week, group_name,
                content_length, has_emojis, has_urgency, has_numbers, 
                has_hashtags, has_call_to_action, performance_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            platform, region, language, content_type, content_hash,
            success, engagement, reach, clicks, conversions,
            now.hour, now.weekday(), group_name,
            content_analysis['length'], content_analysis['has_emojis'],
            content_analysis['has_urgency'], content_analysis['has_numbers'],
            content_analysis['has_hashtags'], content_analysis['has_call_to_action'],
            performance_score
        ))
        
        conn.commit()
        conn.close()
        
        # Trigger autonomous learning
        self._autonomous_learning_cycle()
        
        logging.info(f"📊 Performance recorded: {platform}/{region}/{language} - Score: {performance_score:.3f}")
    
    def _analyze_content(self, content: str) -> Dict:
        """Analyze content characteristics"""
        return {
            'length': len(content),
            'has_emojis': any(ord(c) > 127 for c in content),
            'has_urgency': any(word in content.lower() for word in ['urgent', 'alert', 'limited', 'now', 'today']),
            'has_numbers': any(c.isdigit() for c in content),
            'has_hashtags': '#' in content,
            'has_call_to_action': any(word in content.lower() for word in ['get', 'start', 'join', 'try', 'click'])
        }
    
    def _calculate_performance_score(self, success: bool, engagement: int, 
                                   reach: int, clicks: int, conversions: int) -> float:
        """Calculate weighted performance score"""
        if not success:
            return 0.0
        
        # Normalize metrics
        success_rate = 1.0 if success else 0.0
        engagement_rate = min(engagement / max(reach, 1), 1.0)
        reach_growth = min(reach / 1000, 1.0)  # Normalize to 1000 reach
        conversion_rate = min(conversions / max(clicks, 1), 1.0)
        
        # Calculate weighted score
        score = (
            success_rate * self.performance_weights['success_rate'] +
            engagement_rate * self.performance_weights['engagement_rate'] +
            reach_growth * self.performance_weights['reach_growth'] +
            conversion_rate * self.performance_weights['conversion_rate']
        )
        
        return min(score, 1.0)
    
    def _autonomous_learning_cycle(self):
        """Autonomous learning cycle - discovers patterns and optimizations"""
        
        # Learn optimal timing patterns
        self._learn_timing_patterns()
        
        # Learn content optimization patterns
        self._learn_content_patterns()
        
        # Learn platform-specific strategies
        self._learn_platform_strategies()
        
        # Learn regional preferences
        self._learn_regional_patterns()
        
        # Update optimization strategies
        self._update_optimization_strategies()
    
    def _learn_timing_patterns(self):
        """Learn optimal posting times autonomously"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analyze performance by hour and day
        cursor.execute('''
            SELECT platform, region, language, hour_of_day, day_of_week,
                   AVG(performance_score) as avg_score, COUNT(*) as sample_count
            FROM autonomous_performance 
            WHERE timestamp > datetime('now', '-30 days')
            GROUP BY platform, region, language, hour_of_day, day_of_week
            HAVING sample_count >= ?
            ORDER BY avg_score DESC
        ''', (self.min_samples_for_learning,))
        
        timing_insights = cursor.fetchall()
        
        for insight in timing_insights:
            platform, region, language, hour, day, score, count = insight
            
            insight_key = f"timing_{platform}_{region}_{language}"
            if insight_key not in self.performance_insights:
                self.performance_insights[insight_key] = []
            
            self.performance_insights[insight_key].append({
                'type': 'optimal_timing',
                'hour': hour,
                'day': day,
                'score': score,
                'confidence': min(count / 20, 1.0),  # Higher confidence with more samples
                'recommendation': f"Post at {hour}:00 on {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][day]}"
            })
        
        conn.close()
    
    def _learn_content_patterns(self):
        """Learn what content characteristics work best"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analyze content characteristics impact
        content_factors = [
            'has_emojis', 'has_urgency', 'has_numbers', 
            'has_hashtags', 'has_call_to_action'
        ]
        
        for factor in content_factors:
            cursor.execute(f'''
                SELECT platform, region, language, {factor},
                       AVG(performance_score) as avg_score, COUNT(*) as sample_count
                FROM autonomous_performance 
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY platform, region, language, {factor}
                HAVING sample_count >= ?
            ''', (self.min_samples_for_learning,))
            
            results = cursor.fetchall()
            
            # Analyze impact of this factor
            for platform, region, language, factor_value, score, count in results:
                insight_key = f"content_{platform}_{region}_{language}"
                if insight_key not in self.performance_insights:
                    self.performance_insights[insight_key] = []
                
                self.performance_insights[insight_key].append({
                    'type': 'content_optimization',
                    'factor': factor,
                    'value': bool(factor_value),
                    'score': score,
                    'confidence': min(count / 15, 1.0),
                    'recommendation': f"{'Include' if factor_value else 'Avoid'} {factor.replace('_', ' ')}"
                })
        
        conn.close()
    
    def _learn_platform_strategies(self):
        """Learn platform-specific optimization strategies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analyze what works best on each platform
        cursor.execute('''
            SELECT platform, content_type, AVG(performance_score) as avg_score, 
                   COUNT(*) as sample_count
            FROM autonomous_performance 
            WHERE timestamp > datetime('now', '-30 days')
            GROUP BY platform, content_type
            HAVING sample_count >= ?
            ORDER BY platform, avg_score DESC
        ''', (self.min_samples_for_learning,))
        
        platform_insights = cursor.fetchall()
        
        for platform, content_type, score, count in platform_insights:
            insight_key = f"platform_{platform}"
            if insight_key not in self.performance_insights:
                self.performance_insights[insight_key] = []
            
            self.performance_insights[insight_key].append({
                'type': 'platform_strategy',
                'content_type': content_type,
                'score': score,
                'confidence': min(count / 10, 1.0),
                'recommendation': f"Focus on {content_type} content for {platform}"
            })
        
        conn.close()
    
    def _learn_regional_patterns(self):
        """Learn regional preferences and patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analyze regional performance patterns
        cursor.execute('''
            SELECT region, language, platform, AVG(performance_score) as avg_score,
                   COUNT(*) as sample_count
            FROM autonomous_performance 
            WHERE timestamp > datetime('now', '-30 days')
            GROUP BY region, language, platform
            HAVING sample_count >= ?
            ORDER BY avg_score DESC
        ''', (self.min_samples_for_learning,))
        
        regional_insights = cursor.fetchall()
        
        for region, language, platform, score, count in regional_insights:
            insight_key = f"regional_{region}_{language}"
            if insight_key not in self.performance_insights:
                self.performance_insights[insight_key] = []
            
            self.performance_insights[insight_key].append({
                'type': 'regional_preference',
                'platform': platform,
                'score': score,
                'confidence': min(count / 8, 1.0),
                'recommendation': f"Prioritize {platform} for {region}/{language}"
            })
        
        conn.close()
    
    def _update_optimization_strategies(self):
        """Update and create new optimization strategies"""
        
        # Generate strategies from insights
        for insight_key, insights in self.performance_insights.items():
            high_confidence_insights = [i for i in insights if i['confidence'] > 0.6]
            
            if len(high_confidence_insights) >= 3:
                strategy = self._create_optimization_strategy(insight_key, high_confidence_insights)
                if strategy:
                    self.optimization_strategies[insight_key] = strategy
        
        # Save insights and strategies
        self._save_insights()
    
    def _create_optimization_strategy(self, key: str, insights: List[Dict]) -> Optional[Dict]:
        """Create optimization strategy from insights"""
        
        # Sort insights by score and confidence
        insights.sort(key=lambda x: x['score'] * x['confidence'], reverse=True)
        
        strategy = {
            'name': f"Auto-optimized strategy for {key}",
            'insights': insights[:5],  # Top 5 insights
            'effectiveness_score': sum(i['score'] * i['confidence'] for i in insights[:5]) / 5,
            'recommendations': [i['recommendation'] for i in insights[:5]],
            'created_at': datetime.now().isoformat()
        }
        
        return strategy
    
    def get_autonomous_recommendations(self, platform: str, region: str, language: str) -> List[str]:
        """Get autonomous recommendations for optimization"""
        recommendations = []
        
        # Get relevant insights
        keys_to_check = [
            f"timing_{platform}_{region}_{language}",
            f"content_{platform}_{region}_{language}",
            f"platform_{platform}",
            f"regional_{region}_{language}"
        ]
        
        for key in keys_to_check:
            if key in self.performance_insights:
                insights = self.performance_insights[key]
                high_confidence = [i for i in insights if i['confidence'] > 0.5]
                high_confidence.sort(key=lambda x: x['score'] * x['confidence'], reverse=True)
                
                for insight in high_confidence[:2]:  # Top 2 per category
                    recommendations.append(f"🤖 {insight['recommendation']} (confidence: {insight['confidence']:.1%})")
        
        return recommendations[:8]  # Max 8 recommendations
    
    def get_performance_summary(self, days: int = 7) -> Dict:
        """Get autonomous performance summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Overall performance metrics
        cursor.execute('''
            SELECT 
                COUNT(*) as total_posts,
                AVG(performance_score) as avg_score,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_posts,
                SUM(engagement_count) as total_engagement,
                SUM(reach_count) as total_reach
            FROM autonomous_performance 
            WHERE timestamp > datetime('now', '-{} days')
        '''.format(days))
        
        overall = cursor.fetchone()
        
        # Platform breakdown
        cursor.execute('''
            SELECT platform, AVG(performance_score) as avg_score, COUNT(*) as posts
            FROM autonomous_performance 
            WHERE timestamp > datetime('now', '-{} days')
            GROUP BY platform
            ORDER BY avg_score DESC
        '''.format(days))
        
        platform_breakdown = cursor.fetchall()
        
        # Performance trend
        cursor.execute('''
            SELECT DATE(timestamp) as date, AVG(performance_score) as daily_score
            FROM autonomous_performance 
            WHERE timestamp > datetime('now', '-{} days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        '''.format(days))
        
        trend_data = cursor.fetchall()
        
        conn.close()
        
        if overall[0] == 0:  # No data
            return {'status': 'no_data'}
        
        total_posts, avg_score, successful_posts, total_engagement, total_reach = overall
        success_rate = successful_posts / total_posts if total_posts > 0 else 0
        
        # Determine performance level
        if avg_score >= self.thresholds['excellent']:
            performance_level = "🚀 EXCELLENT"
        elif avg_score >= self.thresholds['good']:
            performance_level = "✅ GOOD"
        elif avg_score >= self.thresholds['average']:
            performance_level = "⚠️ AVERAGE"
        else:
            performance_level = "❌ NEEDS IMPROVEMENT"
        
        return {
            'status': 'active',
            'performance_level': performance_level,
            'avg_score': avg_score,
            'success_rate': success_rate,
            'total_posts': total_posts,
            'total_engagement': total_engagement,
            'total_reach': total_reach,
            'platform_breakdown': [
                {'platform': p[0], 'score': p[1], 'posts': p[2]} 
                for p in platform_breakdown
            ],
            'trend': [
                {'date': t[0], 'score': t[1]} 
                for t in trend_data
            ],
            'insights_count': len(self.performance_insights),
            'strategies_count': len(self.optimization_strategies)
        }
    
    def _save_insights(self):
        """Save insights to file for persistence"""
        try:
            data = {
                'insights': self.performance_insights,
                'strategies': self.optimization_strategies,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('autonomous_insights.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logging.info(f"🧠 Saved {len(self.performance_insights)} insights and {len(self.optimization_strategies)} strategies")
        except Exception as e:
            logging.error(f"❌ Failed to save insights: {e}")
    
    def _load_insights(self):
        """Load insights from file"""
        try:
            if os.path.exists('autonomous_insights.json'):
                with open('autonomous_insights.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.performance_insights = data.get('insights', {})
                self.optimization_strategies = data.get('strategies', {})
                
                logging.info(f"🧠 Loaded {len(self.performance_insights)} insights and {len(self.optimization_strategies)} strategies")
        except Exception as e:
            logging.error(f"❌ Failed to load insights: {e}")
    
    def should_post_now(self, platform: str, region: str, language: str) -> Tuple[bool, str]:
        """Autonomous decision on whether to post now"""
        now = datetime.now()
        current_hour = now.hour
        current_day = now.weekday()
        
        # Check timing insights
        timing_key = f"timing_{platform}_{region}_{language}"
        if timing_key in self.performance_insights:
            timing_insights = self.performance_insights[timing_key]
            
            # Find insights for current time
            current_time_insights = [
                i for i in timing_insights 
                if i.get('hour') == current_hour and i.get('day') == current_day
                and i.get('confidence', 0) > 0.5
            ]
            
            if current_time_insights:
                best_insight = max(current_time_insights, key=lambda x: x['score'])
                if best_insight['score'] > self.thresholds['good']:
                    return True, f"🎯 Optimal time detected (score: {best_insight['score']:.2f})"
                elif best_insight['score'] < self.thresholds['poor']:
                    return False, f"⏰ Poor timing detected (score: {best_insight['score']:.2f})"
        
        # Default: allow posting but with neutral recommendation
        return True, "⚡ No specific timing insights, proceeding"
    
    def optimize_content_autonomously(self, content: str, platform: str, region: str, language: str) -> str:
        """Autonomously optimize content based on learned patterns"""
        optimized = content
        
        # Get content optimization insights
        content_key = f"content_{platform}_{region}_{language}"
        if content_key in self.performance_insights:
            content_insights = self.performance_insights[content_key]
            
            high_confidence_insights = [
                i for i in content_insights 
                if i.get('confidence', 0) > 0.6 and i.get('type') == 'content_optimization'
            ]
            
            for insight in high_confidence_insights:
                factor = insight.get('factor', '')
                should_include = insight.get('value', False)
                
                if factor == 'has_urgency' and should_include and 'urgent' not in optimized.lower():
                    optimized = f"🚨 URGENT: {optimized}"
                elif factor == 'has_call_to_action' and should_include:
                    if not any(word in optimized.lower() for word in ['get', 'start', 'join']):
                        optimized += "\n\n🚀 Get started now!"
                elif factor == 'has_emojis' and should_include:
                    if not any(ord(c) > 127 for c in optimized):
                        optimized = f"⚡ {optimized}"
        
        return optimized
