#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration du timing pour les réseaux sociaux
Respecte les limites de chaque plateforme
"""

from datetime import timedelta

# Configuration Twitter - 2 comptes alternés
TWITTER_CONFIG = {
    'max_posts_per_day': 12,  # Maximum par compte (réduit pour respecter 120min)
    'accounts_count': 2,      # Nombre de comptes
    'post_interval_minutes': 240,  # 240 minutes (4h) entre posts par compte
    'alternating_interval_minutes': 120,  # 120 minutes (2h) en alternant les comptes
    'daily_reset_hour': 0,    # Remise à zéro à minuit
}

# Configuration Reddit - Plus conservateur
REDDIT_CONFIG = {
    'max_posts_per_day': 3,   # Maximum par compte pour éviter les bans
    'post_interval_hours': 8,  # 8 heures entre posts
    'avoid_same_subreddit_hours': 24,  # Éviter le même subreddit pendant 24h
    'educational_content_ratio': 0.7,  # 70% de contenu éducatif
}

# Configuration Telegram - Plus flexible
TELEGRAM_CONFIG = {
    'max_posts_per_day': 20,  # Plus permissif
    'post_interval_minutes': 60,  # 1 heure entre posts
    'group_rotation': True,   # Rotation entre groupes
    'avoid_spam_detection': True,
}

# Intervalles de sécurité
SAFETY_INTERVALS = {
    'between_platforms': 30,  # 30 secondes entre plateformes
    'after_error': 300,       # 5 minutes après une erreur
    'rate_limit_backoff': 900, # 15 minutes si rate limit
}
