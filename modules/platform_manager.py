#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 Platform Manager Module - BOT SHA-256
Advanced rate limiting and connection management
"""

import os
import threading
from datetime import datetime, timedelta
from typing import Dict
import telegram
from telegram.request import HTTPXRequest

class AdvancedRateLimitManager:
    """Advanced rate limiting with timezone awareness"""
    
    def __init__(self):
        self.limits = {
            'twitter': {'requests': 0, 'reset_time': datetime.now(), 'max_per_hour': 15, 'failures': 0},
            'telegram': {'requests': 0, 'reset_time': datetime.now(), 'max_per_hour': 30, 'failures': 0},
            'reddit': {'requests': 0, 'reset_time': datetime.now(), 'max_per_hour': 10, 'failures': 0}
        }
        
    def can_post(self, platform: str) -> bool:
        """Check if we can post to platform"""
        now = datetime.now()
        limit_info = self.limits[platform]
        
        if now >= limit_info['reset_time']:
            limit_info['requests'] = 0
            limit_info['reset_time'] = now + timedelta(hours=1)
            
        return limit_info['requests'] < limit_info['max_per_hour']
    
    def record_request(self, platform: str):
        """Record a request for rate limiting"""
        self.limits[platform]['requests'] += 1
        
    def get_wait_time(self, platform: str) -> int:
        """Get wait time until next request allowed"""
        now = datetime.now()
        reset_time = self.limits[platform]['reset_time']
        if now < reset_time:
            return int((reset_time - now).total_seconds())
        return 0

class ConnectionPoolManager:
    """Manages connection pools to prevent timeout issues"""
    
    def __init__(self):
        self.telegram_session = None
        self.session_lock = threading.Lock()
        
    def get_telegram_session(self):
        """Get or create Telegram session with proper connection pooling"""
        with self.session_lock:
            if self.telegram_session is None:
                # Create session with connection pooling
                request = HTTPXRequest(
                    connection_pool_size=20,
                    pool_timeout=60,
                    read_timeout=60,
                    write_timeout=60,
                    connect_timeout=30
                )
                
                self.telegram_session = telegram.Bot(
                    token=os.getenv('TELEGRAM_BOT_TOKEN'),
                    request=request
                )
                
            return self.telegram_session
    
    def close_connections(self):
        """Close all connections"""
        with self.session_lock:
            if self.telegram_session:
                try:
                    pass  # Telegram bot doesn't need explicit closing
                except:
                    pass
                self.telegram_session = None
