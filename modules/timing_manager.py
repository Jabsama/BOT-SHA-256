#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de timing intelligent pour éviter les bans et respecter les limites
"""

import time
import json
import pytz
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
import logging
from config.timing_config import TWITTER_CONFIG, REDDIT_CONFIG, TELEGRAM_CONFIG, SAFETY_INTERVALS

class TimezoneOptimizer:
    """Optimizes posting times based on target regions and timezones"""
    
    def __init__(self):
        self.timezone_mapping = {
            'US_EAST': 'America/New_York',
            'US_CENTRAL': 'America/Chicago', 
            'US_WEST': 'America/Los_Angeles',
            'INDIA': 'Asia/Kolkata',
            'CHINA': 'Asia/Shanghai',
            'BRAZIL': 'America/Sao_Paulo',
            'EU_WEST': 'Europe/London',
            'EU_CENTRAL': 'Europe/Berlin',
            'AUSTRALIA': 'Australia/Sydney',
            'JAPAN': 'Asia/Tokyo'
        }
        
        self.peak_hours = {
            'US_EAST': [13, 14, 15, 16, 17, 18, 19, 20],
            'US_CENTRAL': [12, 13, 14, 15, 16, 17, 18, 19],
            'US_WEST': [10, 11, 12, 13, 14, 15, 16, 17],
            'INDIA': [9, 10, 11, 18, 19, 20, 21, 22],
            'CHINA': [8, 9, 10, 19, 20, 21, 22, 23],
            'BRAZIL': [11, 12, 13, 18, 19, 20, 21, 22],
            'EU_WEST': [8, 9, 12, 13, 17, 18, 19, 20],
            'EU_CENTRAL': [9, 10, 13, 14, 18, 19, 20, 21],
            'AUSTRALIA': [7, 8, 9, 17, 18, 19, 20, 21],
            'JAPAN': [8, 9, 10, 19, 20, 21, 22, 23]
        }
        
        self.language_mapping = {
            'US_EAST': 'en',
            'US_CENTRAL': 'en',
            'US_WEST': 'en',
            'INDIA': 'en',
            'CHINA': 'zh',
            'BRAZIL': 'pt',
            'EU_WEST': 'en',
            'EU_CENTRAL': 'de',
            'AUSTRALIA': 'en',
            'JAPAN': 'ja'
        }
        
    def get_current_optimal_region(self) -> Tuple[str, str, str]:
        """Get the currently optimal region to target based on time"""
        utc_now = datetime.now(timezone.utc)
        
        best_region = None
        best_score = 0
        
        for region, tz_name in self.timezone_mapping.items():
            try:
                tz = pytz.timezone(tz_name)
                local_time = utc_now.astimezone(tz)
                current_hour = local_time.hour
                
                # Calculate score based on peak hours
                peak_hours = self.peak_hours.get(region, [])
                if current_hour in peak_hours:
                    # Higher score for peak hours
                    score = 10 + (len(peak_hours) - peak_hours.index(current_hour))
                else:
                    # Lower score for off-peak hours
                    score = max(0, 5 - min(abs(current_hour - h) for h in peak_hours))
                
                if score > best_score:
                    best_score = score
                    best_region = region
                    
            except Exception as e:
                logging.warning(f"Timezone calculation error for {region}: {e}")
                continue
        
        if not best_region:
            best_region = 'US_EAST'  # Fallback
            
        language = self.language_mapping.get(best_region, 'en')
        timezone_name = self.timezone_mapping.get(best_region, 'America/New_York')
        
        return best_region, language, timezone_name
        
    def is_peak_time(self, region: str) -> bool:
        """Check if current time is peak time for region"""
        try:
            tz = pytz.timezone(self.timezone_mapping[region])
            local_time = datetime.now(timezone.utc).astimezone(tz)
            return local_time.hour in self.peak_hours.get(region, [])
        except:
            return False

class TimingManager:
    """Gestionnaire intelligent du timing des posts"""
    
    def __init__(self, data_file: str = 'data/timing_data.json'):
        self.data_file = data_file
        self.timing_data = self._load_timing_data()
        
        # Compteurs par plateforme et compte
        self.daily_counters = {
            'twitter': {},  # {account_id: count}
            'reddit': {},   # {account_id: count}
            'telegram': {}  # {account_id: count}
        }
        
        # Derniers posts par plateforme
        self.last_posts = {
            'twitter': {},  # {account_id: timestamp}
            'reddit': {},   # {account_id: timestamp}
            'telegram': {}  # {account_id: timestamp}
        }
        
        # Subreddits utilisés récemment
        self.recent_subreddits = {}  # {account_id: {subreddit: timestamp}}
        
        # Groupes Telegram utilisés récemment
        self.recent_telegram_groups = {}  # {account_id: {group: timestamp}}
        
        self._load_daily_data()
    
    def _load_timing_data(self) -> Dict:
        """Charge les données de timing depuis le fichier"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'daily_counters': {},
                'last_posts': {},
                'recent_subreddits': {},
                'recent_telegram_groups': {},
                'last_reset': datetime.now().strftime('%Y-%m-%d')
            }
    
    def _save_timing_data(self):
        """Sauvegarde les données de timing"""
        try:
            import os
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {
                'daily_counters': self.daily_counters,
                'last_posts': {
                    platform: {
                        account: timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp
                        for account, timestamp in accounts.items()
                    }
                    for platform, accounts in self.last_posts.items()
                },
                'recent_subreddits': {
                    account: {
                        subreddit: timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp
                        for subreddit, timestamp in subreddits.items()
                    }
                    for account, subreddits in self.recent_subreddits.items()
                },
                'recent_telegram_groups': {
                    account: {
                        group: timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp
                        for group, timestamp in groups.items()
                    }
                    for account, groups in self.recent_telegram_groups.items()
                },
                'last_reset': datetime.now().strftime('%Y-%m-%d')
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Erreur sauvegarde timing: {e}")
    
    def _load_daily_data(self):
        """Charge les données quotidiennes et reset si nécessaire"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if self.timing_data.get('last_reset') != today:
            # Nouveau jour, reset des compteurs
            self.daily_counters = {'twitter': {}, 'reddit': {}, 'telegram': {}}
            logging.info(f"🔄 Reset quotidien des compteurs - {today}")
        else:
            # Charger les données existantes
            self.daily_counters = self.timing_data.get('daily_counters', {'twitter': {}, 'reddit': {}, 'telegram': {}})
            
            # Charger les derniers posts
            for platform, accounts in self.timing_data.get('last_posts', {}).items():
                self.last_posts[platform] = {}
                for account, timestamp_str in accounts.items():
                    try:
                        self.last_posts[platform][account] = datetime.fromisoformat(timestamp_str)
                    except:
                        self.last_posts[platform][account] = datetime.now() - timedelta(hours=24)
            
            # Charger les subreddits récents
            for account, subreddits in self.timing_data.get('recent_subreddits', {}).items():
                self.recent_subreddits[account] = {}
                for subreddit, timestamp_str in subreddits.items():
                    try:
                        self.recent_subreddits[account][subreddit] = datetime.fromisoformat(timestamp_str)
                    except:
                        continue
            
            # Charger les groupes Telegram récents
            for account, groups in self.timing_data.get('recent_telegram_groups', {}).items():
                self.recent_telegram_groups[account] = {}
                for group, timestamp_str in groups.items():
                    try:
                        self.recent_telegram_groups[account][group] = datetime.fromisoformat(timestamp_str)
                    except:
                        continue
    
    def can_post_twitter(self, account_id: str) -> tuple[bool, str, int]:
        """Vérifie si on peut poster sur Twitter"""
        # Vérifier le compteur quotidien
        daily_count = self.daily_counters['twitter'].get(account_id, 0)
        if daily_count >= TWITTER_CONFIG['max_posts_per_day']:
            return False, f"Limite quotidienne atteinte ({daily_count}/15)", 0
        
        # Vérifier l'intervalle entre posts
        last_post = self.last_posts['twitter'].get(account_id)
        if last_post:
            time_since_last = datetime.now() - last_post
            required_interval = timedelta(minutes=TWITTER_CONFIG['post_interval_minutes'])
            
            if time_since_last < required_interval:
                wait_time = int((required_interval - time_since_last).total_seconds())
                return False, f"Trop tôt (attendre {wait_time//60}min)", wait_time
        
        return True, "OK", 0
    
    def can_post_reddit(self, account_id: str, subreddit: str = None) -> tuple[bool, str, int]:
        """Vérifie si on peut poster sur Reddit"""
        # Vérifier le compteur quotidien
        daily_count = self.daily_counters['reddit'].get(account_id, 0)
        if daily_count >= REDDIT_CONFIG['max_posts_per_day']:
            return False, f"Limite quotidienne atteinte ({daily_count}/3)", 0
        
        # Vérifier l'intervalle entre posts
        last_post = self.last_posts['reddit'].get(account_id)
        if last_post:
            time_since_last = datetime.now() - last_post
            required_interval = timedelta(hours=REDDIT_CONFIG['post_interval_hours'])
            
            if time_since_last < required_interval:
                wait_time = int((required_interval - time_since_last).total_seconds())
                return False, f"Trop tôt (attendre {wait_time//3600}h)", wait_time
        
        # Vérifier si le subreddit a été utilisé récemment
        if subreddit and account_id in self.recent_subreddits:
            last_subreddit_use = self.recent_subreddits[account_id].get(subreddit)
            if last_subreddit_use:
                time_since_subreddit = datetime.now() - last_subreddit_use
                required_subreddit_interval = timedelta(hours=REDDIT_CONFIG['avoid_same_subreddit_hours'])
                
                if time_since_subreddit < required_subreddit_interval:
                    wait_time = int((required_subreddit_interval - time_since_subreddit).total_seconds())
                    return False, f"Subreddit r/{subreddit} utilisé récemment", wait_time
        
        return True, "OK", 0
    
    def can_post_telegram(self, account_id: str, group: str = None) -> tuple[bool, str, int]:
        """Vérifie si on peut poster sur Telegram"""
        # Vérifier le compteur quotidien
        daily_count = self.daily_counters['telegram'].get(account_id, 0)
        if daily_count >= TELEGRAM_CONFIG['max_posts_per_day']:
            return False, f"Limite quotidienne atteinte ({daily_count}/20)", 0
        
        # Vérifier l'intervalle entre posts
        last_post = self.last_posts['telegram'].get(account_id)
        if last_post:
            time_since_last = datetime.now() - last_post
            required_interval = timedelta(minutes=TELEGRAM_CONFIG['post_interval_minutes'])
            
            if time_since_last < required_interval:
                wait_time = int((required_interval - time_since_last).total_seconds())
                return False, f"Trop tôt (attendre {wait_time//60}min)", wait_time
        
        # Vérifier si le groupe a été utilisé récemment (éviter le spam)
        if group and account_id in self.recent_telegram_groups:
            last_group_use = self.recent_telegram_groups[account_id].get(group)
            if last_group_use:
                time_since_group = datetime.now() - last_group_use
                required_group_interval = timedelta(hours=2)  # 2h entre posts dans le même groupe
                
                if time_since_group < required_group_interval:
                    wait_time = int((required_group_interval - time_since_group).total_seconds())
                    return False, f"Groupe {group} utilisé récemment", wait_time
        
        return True, "OK", 0
    
    def record_post(self, platform: str, account_id: str, subreddit: str = None, group: str = None):
        """Enregistre un post effectué"""
        now = datetime.now()
        
        # Incrémenter le compteur quotidien
        if account_id not in self.daily_counters[platform]:
            self.daily_counters[platform][account_id] = 0
        self.daily_counters[platform][account_id] += 1
        
        # Enregistrer le timestamp du dernier post
        self.last_posts[platform][account_id] = now
        
        # Enregistrer le subreddit pour Reddit
        if platform == 'reddit' and subreddit:
            if account_id not in self.recent_subreddits:
                self.recent_subreddits[account_id] = {}
            self.recent_subreddits[account_id][subreddit] = now
        
        # Enregistrer le groupe pour Telegram
        if platform == 'telegram' and group:
            if account_id not in self.recent_telegram_groups:
                self.recent_telegram_groups[account_id] = {}
            self.recent_telegram_groups[account_id][group] = now
        
        # Sauvegarder
        self._save_timing_data()
        
        logging.info(f"📝 Post enregistré: {platform}/{account_id} (compteur: {self.daily_counters[platform][account_id]})")
    
    def get_next_twitter_account(self, twitter_accounts: List[Dict]) -> Optional[Dict]:
        """Retourne le prochain compte Twitter à utiliser (alternance)"""
        available_accounts = []
        
        for account in twitter_accounts:
            account_id = account.get('name', 'default')
            can_post, reason, wait_time = self.can_post_twitter(account_id)
            
            if can_post:
                available_accounts.append({
                    'account': account,
                    'id': account_id,
                    'posts_today': self.daily_counters['twitter'].get(account_id, 0)
                })
        
        if not available_accounts:
            return None
        
        # Choisir le compte avec le moins de posts aujourd'hui
        return min(available_accounts, key=lambda x: x['posts_today'])['account']
    
    def get_next_reddit_account(self, reddit_accounts: List[Dict], subreddit: str = None) -> Optional[Dict]:
        """Retourne le prochain compte Reddit à utiliser"""
        available_accounts = []
        
        for account in reddit_accounts:
            account_id = account.get('name', 'default')
            can_post, reason, wait_time = self.can_post_reddit(account_id, subreddit)
            
            if can_post:
                available_accounts.append({
                    'account': account,
                    'id': account_id,
                    'posts_today': self.daily_counters['reddit'].get(account_id, 0)
                })
        
        if not available_accounts:
            return None
        
        # Choisir le compte avec le moins de posts aujourd'hui
        return min(available_accounts, key=lambda x: x['posts_today'])['account']
    
    def get_available_subreddits(self, account_id: str, subreddit_list: List[str]) -> List[str]:
        """Retourne les subreddits disponibles pour un compte"""
        available = []
        
        for subreddit in subreddit_list:
            can_post, reason, wait_time = self.can_post_reddit(account_id, subreddit)
            if can_post:
                available.append(subreddit)
        
        return available
    
    def get_available_telegram_groups(self, account_id: str, group_list: List[str]) -> List[str]:
        """Retourne les groupes Telegram disponibles pour un compte"""
        available = []
        
        for group in group_list:
            can_post, reason, wait_time = self.can_post_telegram(account_id, group)
            if can_post:
                available.append(group)
        
        return available
    
    def get_status_summary(self) -> Dict:
        """Retourne un résumé du statut des comptes"""
        summary = {
            'twitter': {},
            'reddit': {},
            'telegram': {}
        }
        
        for platform in ['twitter', 'reddit', 'telegram']:
            for account_id, count in self.daily_counters[platform].items():
                max_posts = {
                    'twitter': TWITTER_CONFIG['max_posts_per_day'],
                    'reddit': REDDIT_CONFIG['max_posts_per_day'],
                    'telegram': TELEGRAM_CONFIG['max_posts_per_day']
                }[platform]
                
                last_post = self.last_posts[platform].get(account_id)
                time_since_last = "Jamais" if not last_post else str(datetime.now() - last_post).split('.')[0]
                
                summary[platform][account_id] = {
                    'posts_today': count,
                    'max_posts': max_posts,
                    'remaining': max_posts - count,
                    'last_post': time_since_last,
                    'can_post': count < max_posts
                }
        
        return summary
    
    def cleanup_old_data(self):
        """Nettoie les anciennes données (subreddits/groupes anciens)"""
        now = datetime.now()
        cutoff = now - timedelta(days=7)  # Garder 7 jours d'historique
        
        # Nettoyer les subreddits anciens
        for account_id in list(self.recent_subreddits.keys()):
            for subreddit in list(self.recent_subreddits[account_id].keys()):
                if self.recent_subreddits[account_id][subreddit] < cutoff:
                    del self.recent_subreddits[account_id][subreddit]
            
            if not self.recent_subreddits[account_id]:
                del self.recent_subreddits[account_id]
        
        # Nettoyer les groupes Telegram anciens
        for account_id in list(self.recent_telegram_groups.keys()):
            for group in list(self.recent_telegram_groups[account_id].keys()):
                if self.recent_telegram_groups[account_id][group] < cutoff:
                    del self.recent_telegram_groups[account_id][group]
            
            if not self.recent_telegram_groups[account_id]:
                del self.recent_telegram_groups[account_id]
        
        self._save_timing_data()
        logging.info("🧹 Nettoyage des anciennes données effectué")
