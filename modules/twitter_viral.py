#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Twitter Viral Optimization Module - Maximum Engagement & Anti-Shadow-Ban
Optimizes hashtags, timing, content for viral potential while avoiding bans
"""

import re
import json
import time
import random
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import tweepy

@dataclass
class ViralPattern:
    """Pattern viral identifié"""
    hashtags: List[str]
    content_type: str
    engagement_rate: float
    reach: int
    time_of_day: int
    day_of_week: int
    sentiment: str
    media_type: str
    last_used: datetime

@dataclass
class AccountHealth:
    """Santé d'un compte Twitter"""
    username: str
    shadow_ban_risk: int
    engagement_rate: float
    follower_growth: float
    last_viral_post: Optional[datetime]
    posting_frequency: float
    content_diversity_score: float
    interaction_ratio: float

class TwitterViralOptimizer:
    """Optimiseur viral pour Twitter avec protection anti-shadow-ban"""
    
    def __init__(self, data_file: str = 'data/twitter_viral.json'):
        self.data_file = data_file
        self.viral_patterns = []
        self.trending_hashtags = {}
        self.account_health = {}
        self.shadow_ban_indicators = {}
        self.successful_content = []
        self.failed_content = []
        
        # Hashtags de base par catégorie
        self.base_hashtags = {
            'gpu_tech': ['#GPU', '#AI', '#MachineLearning', '#DeepLearning', '#CUDA', '#TensorFlow', '#PyTorch'],
            'cloud_computing': ['#CloudComputing', '#AWS', '#Azure', '#GCP', '#DevOps', '#Infrastructure'],
            'crypto_mining': ['#CryptoMining', '#Bitcoin', '#Ethereum', '#Mining', '#Blockchain'],
            'gaming': ['#Gaming', '#PCGaming', '#RTX', '#GameDev', '#Streaming'],
            'tech_deals': ['#TechDeals', '#Savings', '#TechNews', '#Innovation', '#Startup'],
            'ai_research': ['#AIResearch', '#NeuralNetworks', '#DataScience', '#BigData', '#Analytics']
        }
        
        # Patterns de contenu viral
        self.viral_content_patterns = {
            'comparison': "🔥 {service1} vs {service2}: {comparison_point}",
            'savings': "💰 Save {percentage}% on {service}: {benefit}",
            'breaking_news': "🚨 BREAKING: {news_item}",
            'tutorial': "🧵 Thread: How to {action} in {timeframe}",
            'question': "🤔 Quick question: {question}",
            'achievement': "🎉 Just {achievement}! {details}",
            'tip': "💡 Pro tip: {tip_content}",
            'warning': "⚠️ PSA: {warning_content}"
        }
        
        # Indicateurs de shadow ban
        self.shadow_ban_signals = [
            'sudden_engagement_drop',
            'hashtag_invisibility',
            'reduced_reach',
            'notification_delays',
            'search_invisibility'
        ]
        
        self._load_viral_data()
    
    def _load_viral_data(self):
        """Charge les données virales depuis le fichier"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Charger les patterns viraux
            for pattern_data in data.get('viral_patterns', []):
                self.viral_patterns.append(ViralPattern(
                    hashtags=pattern_data['hashtags'],
                    content_type=pattern_data['content_type'],
                    engagement_rate=pattern_data['engagement_rate'],
                    reach=pattern_data['reach'],
                    time_of_day=pattern_data['time_of_day'],
                    day_of_week=pattern_data['day_of_week'],
                    sentiment=pattern_data['sentiment'],
                    media_type=pattern_data['media_type'],
                    last_used=datetime.fromisoformat(pattern_data['last_used'])
                ))
            
            # Charger la santé des comptes
            for username, health_data in data.get('account_health', {}).items():
                self.account_health[username] = AccountHealth(
                    username=health_data['username'],
                    shadow_ban_risk=health_data['shadow_ban_risk'],
                    engagement_rate=health_data['engagement_rate'],
                    follower_growth=health_data['follower_growth'],
                    last_viral_post=datetime.fromisoformat(health_data['last_viral_post']) if health_data['last_viral_post'] else None,
                    posting_frequency=health_data['posting_frequency'],
                    content_diversity_score=health_data['content_diversity_score'],
                    interaction_ratio=health_data['interaction_ratio']
                )
            
            self.trending_hashtags = data.get('trending_hashtags', {})
            self.shadow_ban_indicators = data.get('shadow_ban_indicators', {})
            self.successful_content = data.get('successful_content', [])
            self.failed_content = data.get('failed_content', [])
            
        except (FileNotFoundError, json.JSONDecodeError):
            logging.info("🚀 Initializing new Twitter viral optimization database")
            self._initialize_default_data()
    
    def _save_viral_data(self):
        """Sauvegarde les données virales"""
        try:
            import os
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Convertir les patterns en dictionnaire
            viral_patterns_dict = []
            for pattern in self.viral_patterns:
                viral_patterns_dict.append({
                    'hashtags': pattern.hashtags,
                    'content_type': pattern.content_type,
                    'engagement_rate': pattern.engagement_rate,
                    'reach': pattern.reach,
                    'time_of_day': pattern.time_of_day,
                    'day_of_week': pattern.day_of_week,
                    'sentiment': pattern.sentiment,
                    'media_type': pattern.media_type,
                    'last_used': pattern.last_used.isoformat()
                })
            
            # Convertir la santé des comptes
            account_health_dict = {}
            for username, health in self.account_health.items():
                account_health_dict[username] = {
                    'username': health.username,
                    'shadow_ban_risk': health.shadow_ban_risk,
                    'engagement_rate': health.engagement_rate,
                    'follower_growth': health.follower_growth,
                    'last_viral_post': health.last_viral_post.isoformat() if health.last_viral_post else None,
                    'posting_frequency': health.posting_frequency,
                    'content_diversity_score': health.content_diversity_score,
                    'interaction_ratio': health.interaction_ratio
                }
            
            data = {
                'viral_patterns': viral_patterns_dict,
                'account_health': account_health_dict,
                'trending_hashtags': self.trending_hashtags,
                'shadow_ban_indicators': self.shadow_ban_indicators,
                'successful_content': self.successful_content,
                'failed_content': self.failed_content
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"❌ Erreur sauvegarde données virales Twitter: {e}")
    
    def _initialize_default_data(self):
        """Initialise les données par défaut"""
        # Patterns viraux de base
        default_patterns = [
            ViralPattern(
                hashtags=['#AI', '#GPU', '#MachineLearning'],
                content_type='tech_comparison',
                engagement_rate=0.15,
                reach=5000,
                time_of_day=14,
                day_of_week=2,
                sentiment='positive',
                media_type='text',
                last_used=datetime.now() - timedelta(days=7)
            ),
            ViralPattern(
                hashtags=['#CloudComputing', '#AWS', '#Savings'],
                content_type='cost_savings',
                engagement_rate=0.12,
                reach=3000,
                time_of_day=10,
                day_of_week=1,
                sentiment='informative',
                media_type='text',
                last_used=datetime.now() - timedelta(days=5)
            )
        ]
        
        self.viral_patterns.extend(default_patterns)
        self._save_viral_data()
    
    def fetch_trending_hashtags(self, twitter_client) -> List[str]:
        """Récupère les hashtags tendance en temps réel"""
        try:
            # Récupérer les tendances pour différentes locations
            locations = [1, 23424977, 23424975]  # Worldwide, USA, UK
            trending_hashtags = set()
            
            for location in locations:
                try:
                    trends = twitter_client.get_place_trends(location)
                    for trend_list in trends:
                        for trend in trend_list['trends']:
                            name = trend['name']
                            if name.startswith('#') and len(name) > 2:
                                trending_hashtags.add(name)
                except Exception as e:
                    logging.warning(f"⚠️ Erreur récupération tendances pour {location}: {e}")
                    continue
            
            # Filtrer les hashtags pertinents
            relevant_hashtags = []
            tech_keywords = ['ai', 'gpu', 'tech', 'cloud', 'data', 'crypto', 'gaming', 'dev', 'code', 'ml']
            
            for hashtag in trending_hashtags:
                hashtag_lower = hashtag.lower()
                if any(keyword in hashtag_lower for keyword in tech_keywords):
                    relevant_hashtags.append(hashtag)
            
            # Mettre à jour le cache
            self.trending_hashtags = {
                'hashtags': relevant_hashtags[:20],  # Top 20
                'last_updated': datetime.now().isoformat()
            }
            
            logging.info(f"🔥 {len(relevant_hashtags)} hashtags tendance tech récupérés")
            return relevant_hashtags
            
        except Exception as e:
            logging.error(f"❌ Erreur récupération hashtags tendance: {e}")
            # Retourner des hashtags par défaut
            return ['#AI', '#GPU', '#TechNews', '#Innovation', '#CloudComputing']
    
    def optimize_hashtags(self, content: str, content_type: str, current_time: datetime) -> List[str]:
        """Optimise les hashtags pour un maximum de viralité"""
        # Analyser le contenu pour déterminer la catégorie
        content_lower = content.lower()
        
        # Déterminer les catégories pertinentes
        relevant_categories = []
        if any(word in content_lower for word in ['gpu', 'graphics', 'nvidia', 'amd']):
            relevant_categories.append('gpu_tech')
        if any(word in content_lower for word in ['cloud', 'aws', 'azure', 'server']):
            relevant_categories.append('cloud_computing')
        if any(word in content_lower for word in ['mining', 'crypto', 'bitcoin', 'ethereum']):
            relevant_categories.append('crypto_mining')
        if any(word in content_lower for word in ['game', 'gaming', 'stream']):
            relevant_categories.append('gaming')
        if any(word in content_lower for word in ['ai', 'machine learning', 'neural', 'deep learning']):
            relevant_categories.append('ai_research')
        
        if not relevant_categories:
            relevant_categories = ['tech_deals']
        
        # Combiner hashtags de base et tendance
        optimized_hashtags = []
        
        # Ajouter des hashtags de base (2-3)
        for category in relevant_categories[:2]:
            base_hashtags = self.base_hashtags.get(category, [])
            optimized_hashtags.extend(random.sample(base_hashtags, min(2, len(base_hashtags))))
        
        # Ajouter des hashtags tendance (1-2)
        trending = self.trending_hashtags.get('hashtags', [])
        if trending:
            optimized_hashtags.extend(random.sample(trending, min(2, len(trending))))
        
        # Ajouter des hashtags basés sur les patterns viraux
        current_hour = current_time.hour
        current_day = current_time.weekday()
        
        for pattern in self.viral_patterns:
            if (abs(pattern.time_of_day - current_hour) <= 2 and 
                pattern.day_of_week == current_day and
                pattern.content_type == content_type):
                optimized_hashtags.extend(pattern.hashtags[:2])
                break
        
        # Supprimer les doublons et limiter à 5 hashtags max
        unique_hashtags = list(dict.fromkeys(optimized_hashtags))[:5]
        
        logging.info(f"🎯 Hashtags optimisés: {unique_hashtags}")
        return unique_hashtags
    
    def generate_viral_content(self, base_content: str, content_type: str, offer_data: Dict = None) -> str:
        """Génère du contenu optimisé pour la viralité"""
        # Choisir un pattern viral approprié
        if content_type in self.viral_content_patterns:
            pattern = self.viral_content_patterns[content_type]
        else:
            pattern = random.choice(list(self.viral_content_patterns.values()))
        
        # Adapter le contenu selon le type
        if content_type == 'comparison' and offer_data:
            viral_content = pattern.format(
                service1="VoltageGPU",
                service2="AWS/Azure",
                comparison_point=f"Save {random.randint(60, 80)}% on GPU costs"
            )
        elif content_type == 'savings' and offer_data:
            percentage = random.randint(60, 80)
            viral_content = pattern.format(
                percentage=percentage,
                service="GPU rentals",
                benefit=f"Perfect for AI/ML workloads"
            )
        elif content_type == 'breaking_news':
            viral_content = pattern.format(
                news_item="New GPU rental platform offers 70% savings vs traditional cloud"
            )
        elif content_type == 'question':
            viral_content = pattern.format(
                question="What's your biggest challenge with GPU costs for AI/ML?"
            )
        elif content_type == 'tip':
            viral_content = pattern.format(
                tip_content="Use decentralized GPU networks to cut AI training costs by 70%"
            )
        else:
            # Utiliser le contenu de base avec des améliorations
            viral_content = base_content
        
        # Ajouter des éléments viraux
        viral_elements = ['🔥', '💰', '🚀', '⚡', '🎯', '💡', '🧵', '👇']
        if not any(element in viral_content for element in viral_elements):
            viral_content = f"{random.choice(viral_elements)} {viral_content}"
        
        return viral_content
    
    def check_shadow_ban_risk(self, username: str) -> Tuple[int, List[str]]:
        """Vérifie le risque de shadow ban pour un compte"""
        if username not in self.account_health:
            self.account_health[username] = AccountHealth(
                username=username,
                shadow_ban_risk=0,
                engagement_rate=0.05,
                follower_growth=0.0,
                last_viral_post=None,
                posting_frequency=0.0,
                content_diversity_score=1.0,
                interaction_ratio=0.1
            )
        
        health = self.account_health[username]
        risk_factors = []
        
        # Analyser les facteurs de risque
        if health.posting_frequency > 10:  # Plus de 10 posts par jour
            risk_factors.append("High posting frequency")
            health.shadow_ban_risk += 2
        
        if health.engagement_rate < 0.01:  # Moins de 1% d'engagement
            risk_factors.append("Low engagement rate")
            health.shadow_ban_risk += 1
        
        if health.content_diversity_score < 0.3:  # Contenu trop répétitif
            risk_factors.append("Low content diversity")
            health.shadow_ban_risk += 1
        
        if health.interaction_ratio < 0.05:  # Peu d'interactions avec d'autres
            risk_factors.append("Low interaction ratio")
            health.shadow_ban_risk += 1
        
        # Réduire le risque si le compte performe bien
        if health.engagement_rate > 0.1:
            health.shadow_ban_risk = max(0, health.shadow_ban_risk - 1)
        
        if health.follower_growth > 0.05:
            health.shadow_ban_risk = max(0, health.shadow_ban_risk - 1)
        
        # Limiter le score de risque
        health.shadow_ban_risk = min(10, max(0, health.shadow_ban_risk))
        
        return health.shadow_ban_risk, risk_factors
    
    def get_optimal_posting_time(self, content_type: str, timezone: str = 'UTC') -> datetime:
        """Détermine le meilleur moment pour poster"""
        # Analyser les patterns viraux pour ce type de contenu
        relevant_patterns = [p for p in self.viral_patterns if p.content_type == content_type]
        
        if relevant_patterns:
            # Utiliser les patterns existants
            best_pattern = max(relevant_patterns, key=lambda p: p.engagement_rate)
            optimal_hour = best_pattern.time_of_day
            optimal_day = best_pattern.day_of_week
        else:
            # Utiliser des heures optimales par défaut
            optimal_hours = {
                'tech_comparison': [9, 14, 18],
                'cost_savings': [10, 15, 19],
                'breaking_news': [8, 12, 17],
                'question': [11, 16, 20],
                'tip': [13, 17, 21]
            }
            
            hours = optimal_hours.get(content_type, [9, 14, 18])
            optimal_hour = random.choice(hours)
            optimal_day = random.choice([1, 2, 3])  # Lundi, Mardi, Mercredi
        
        # Calculer la prochaine occurrence
        now = datetime.now()
        days_ahead = optimal_day - now.weekday()
        if days_ahead <= 0:  # Le jour cible est passé cette semaine
            days_ahead += 7
        
        optimal_time = now + timedelta(days=days_ahead)
        optimal_time = optimal_time.replace(hour=optimal_hour, minute=random.randint(0, 59), second=0, microsecond=0)
        
        return optimal_time
    
    def record_post_performance(self, username: str, content: str, hashtags: List[str], 
                              engagement: int, reach: int, content_type: str):
        """Enregistre les performances d'un post pour l'apprentissage"""
        if username not in self.account_health:
            self.account_health[username] = AccountHealth(
                username=username,
                shadow_ban_risk=0,
                engagement_rate=0.05,
                follower_growth=0.0,
                last_viral_post=None,
                posting_frequency=0.0,
                content_diversity_score=1.0,
                interaction_ratio=0.1
            )
        
        health = self.account_health[username]
        
        # Calculer le taux d'engagement
        engagement_rate = engagement / max(reach, 1)
        
        # Mettre à jour la santé du compte
        health.engagement_rate = (health.engagement_rate * 0.8) + (engagement_rate * 0.2)
        
        # Enregistrer comme pattern viral si performance élevée
        if engagement_rate > 0.1 or engagement > 50:  # Seuil de viralité
            viral_pattern = ViralPattern(
                hashtags=hashtags,
                content_type=content_type,
                engagement_rate=engagement_rate,
                reach=reach,
                time_of_day=datetime.now().hour,
                day_of_week=datetime.now().weekday(),
                sentiment=self._analyze_sentiment(content),
                media_type='text',
                last_used=datetime.now()
            )
            
            self.viral_patterns.append(viral_pattern)
            health.last_viral_post = datetime.now()
            
            # Garder seulement les 50 meilleurs patterns
            self.viral_patterns.sort(key=lambda p: p.engagement_rate, reverse=True)
            self.viral_patterns = self.viral_patterns[:50]
            
            logging.info(f"🚀 Pattern viral enregistré: {engagement_rate:.2%} engagement, {reach} reach")
        
        # Enregistrer le contenu
        post_data = {
            'content': content,
            'hashtags': hashtags,
            'engagement': engagement,
            'reach': reach,
            'engagement_rate': engagement_rate,
            'timestamp': datetime.now().isoformat(),
            'username': username
        }
        
        if engagement_rate > 0.05:
            self.successful_content.append(post_data)
            # Garder seulement les 100 meilleurs
            self.successful_content.sort(key=lambda p: p['engagement_rate'], reverse=True)
            self.successful_content = self.successful_content[:100]
        else:
            self.failed_content.append(post_data)
            # Garder seulement les 50 derniers échecs
            self.failed_content = self.failed_content[-50:]
        
        self._save_viral_data()
    
    def _analyze_sentiment(self, content: str) -> str:
        """Analyse le sentiment du contenu"""
        positive_words = ['amazing', 'great', 'awesome', 'fantastic', 'excellent', 'love', 'best', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def get_content_suggestions(self, content_type: str) -> List[str]:
        """Retourne des suggestions de contenu basées sur les patterns viraux"""
        # Analyser les contenus qui ont bien performé
        successful_by_type = [
            post for post in self.successful_content 
            if content_type in post.get('content', '').lower()
        ]
        
        if not successful_by_type:
            # Suggestions par défaut
            suggestions = {
                'gpu_deals': [
                    "🔥 GPU rental costs got you down? Here's how I cut mine by 70%...",
                    "💰 Thread: Why I switched from AWS to decentralized GPU networks",
                    "🚀 PSA: You're probably overpaying for GPU compute. Here's why..."
                ],
                'ai_research': [
                    "🧵 The hidden costs of AI training that nobody talks about",
                    "💡 Pro tip: How to train large models without breaking the bank",
                    "🔥 This GPU rental hack saved my startup $10k/month"
                ]
            }
            return suggestions.get(content_type, suggestions['gpu_deals'])
        
        # Extraire des patterns des contenus réussis
        suggestions = []
        for post in successful_by_type[:5]:
            # Simplifier et généraliser le contenu
            content = post['content']
            if len(content) > 100:
                content = content[:100] + "..."
            suggestions.append(content)
        
        return suggestions
    
    def get_viral_summary(self) -> Dict:
        """Retourne un résumé des performances virales"""
        total_patterns = len(self.viral_patterns)
        total_accounts = len(self.account_health)
        
        # Calculer les moyennes
        avg_engagement = sum(p.engagement_rate for p in self.viral_patterns) / max(total_patterns, 1)
        avg_reach = sum(p.reach for p in self.viral_patterns) / max(total_patterns, 1)
        
        # Compter les posts viraux récents (7 derniers jours)
        recent_viral = len([
            p for p in self.viral_patterns 
            if p.last_used > datetime.now() - timedelta(days=7)
        ])
        
        return {
            'total_viral_patterns': total_patterns,
            'accounts_tracked': total_accounts,
            'average_engagement_rate': avg_engagement,
            'average_reach': avg_reach,
            'recent_viral_posts': recent_viral,
            'successful_posts': len(self.successful_content),
            'failed_posts': len(self.failed_content),
            'trending_hashtags_count': len(self.trending_hashtags.get('hashtags', []))
        }
