#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SHA-256 BOT - LIVE DASHBOARD API
Connects to https://voltagegpu.com/SHA-256 for real-time monitoring
"""

import os
import json
import time
import asyncio
import logging
import requests
import websocket
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/dashboard_api.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class BotStatus:
    """Bot status data structure for dashboard"""
    bot_id: str
    status: str  # 'running', 'stopped', 'error'
    uptime: int
    current_region: str
    current_language: str
    is_peak_time: bool
    affiliate_code: str
    
    # Platform statistics
    twitter_posts_today: int
    twitter_status: str
    twitter_next_post: str
    twitter_followers_gained: int
    
    telegram_posts_today: int
    telegram_status: str
    telegram_next_post: str
    telegram_invites_sent: int
    
    reddit_posts_today: int
    reddit_status: str
    reddit_next_post: str
    reddit_karma_gained: int
    
    # Performance metrics
    total_posts_today: int
    total_engagement: int
    success_rate: float
    ai_learning_score: float
    
    # System info
    last_update: str
    version: str
    errors_count: int

class DashboardAPI:
    """Live Dashboard API for VoltageGPU monitoring"""
    
    def __init__(self):
        self.dashboard_url = "https://voltagegpu.com/SHA-256"
        self.api_endpoint = "wss://api.voltagegpu.com/dashboard/sha256"
        self.bot_id = self._generate_bot_id()
        self.affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-76360B81D39F')
        
        self.ws = None
        self.connected = False
        self.running = True
        self.last_heartbeat = time.time()
        
        # Data collection
        self.db_path = 'data/unified_bot_data.db'
        self.status_cache = {}
        
        logging.info(f"🚀 Dashboard API initialized - Bot ID: {self.bot_id}")
    
    def _generate_bot_id(self) -> str:
        """Generate unique bot identifier"""
        import hashlib
        import uuid
        
        # Use machine-specific info for consistent ID
        machine_id = str(uuid.getnode())
        timestamp = str(int(time.time() / 3600))  # Changes every hour
        
        bot_id = hashlib.md5(f"{machine_id}_{timestamp}".encode()).hexdigest()[:12]
        return f"SHA256-{bot_id.upper()}"
    
    def collect_bot_status(self) -> BotStatus:
        """Collect current bot status from database and system"""
        try:
            # Get database stats
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get today's performance data
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Twitter stats
            cursor.execute('''
                SELECT COUNT(*), AVG(engagement_count), AVG(performance_score)
                FROM performance_data 
                WHERE platform = 'twitter' AND date(timestamp) = ?
            ''', (today,))
            twitter_data = cursor.fetchone()
            twitter_posts = twitter_data[0] if twitter_data[0] else 0
            twitter_engagement = int(twitter_data[1]) if twitter_data[1] else 0
            
            # Telegram stats
            cursor.execute('''
                SELECT COUNT(*), AVG(engagement_count)
                FROM performance_data 
                WHERE platform = 'telegram' AND date(timestamp) = ?
            ''', (today,))
            telegram_data = cursor.fetchone()
            telegram_posts = telegram_data[0] if telegram_data[0] else 0
            telegram_engagement = int(telegram_data[1]) if telegram_data[1] else 0
            
            # Reddit stats
            cursor.execute('''
                SELECT COUNT(*), AVG(engagement_count)
                FROM performance_data 
                WHERE platform = 'reddit' AND date(timestamp) = ?
            ''', (today,))
            reddit_data = cursor.fetchone()
            reddit_posts = reddit_data[0] if reddit_data[0] else 0
            reddit_engagement = int(reddit_data[1]) if reddit_data[1] else 0
            
            # Overall success rate
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
                FROM performance_data 
                WHERE date(timestamp) = ?
            ''', (today,))
            success_data = cursor.fetchone()
            total_posts = success_data[0] if success_data[0] else 0
            successful_posts = success_data[1] if success_data[1] else 0
            success_rate = (successful_posts / total_posts * 100) if total_posts > 0 else 0
            
            conn.close()
            
            # Calculate uptime (assuming bot started when first record was created)
            uptime = int(time.time() - (time.time() - 3600))  # Placeholder
            
            # Create status object
            status = BotStatus(
                bot_id=self.bot_id,
                status='running',
                uptime=uptime,
                current_region='EU_WEST',  # This should come from timezone optimizer
                current_language='en',
                is_peak_time=self._is_peak_time(),
                affiliate_code=self.affiliate_code,
                
                twitter_posts_today=twitter_posts,
                twitter_status='🟢 ACTIVE' if twitter_posts < 20 else '⏰ RATE LIMITED',
                twitter_next_post=self._get_next_post_time('twitter'),
                twitter_followers_gained=twitter_engagement,
                
                telegram_posts_today=telegram_posts,
                telegram_status='🟢 ACTIVE' if telegram_posts < 15 else '⏰ RATE LIMITED',
                telegram_next_post=self._get_next_post_time('telegram'),
                telegram_invites_sent=telegram_engagement,
                
                reddit_posts_today=reddit_posts,
                reddit_status='🟢 ACTIVE' if reddit_posts < 5 else '⏰ RATE LIMITED',
                reddit_next_post=self._get_next_post_time('reddit'),
                reddit_karma_gained=reddit_engagement,
                
                total_posts_today=total_posts,
                total_engagement=twitter_engagement + telegram_engagement + reddit_engagement,
                success_rate=round(success_rate, 1),
                ai_learning_score=85.5,  # This should come from AI module
                
                last_update=datetime.now().isoformat(),
                version='10.0',
                errors_count=0
            )
            
            return status
            
        except Exception as e:
            logging.error(f"❌ Error collecting bot status: {e}")
            # Return minimal status on error
            return BotStatus(
                bot_id=self.bot_id,
                status='error',
                uptime=0,
                current_region='UNKNOWN',
                current_language='en',
                is_peak_time=False,
                affiliate_code=self.affiliate_code,
                twitter_posts_today=0, twitter_status='❌ ERROR', twitter_next_post='Unknown', twitter_followers_gained=0,
                telegram_posts_today=0, telegram_status='❌ ERROR', telegram_next_post='Unknown', telegram_invites_sent=0,
                reddit_posts_today=0, reddit_status='❌ ERROR', reddit_next_post='Unknown', reddit_karma_gained=0,
                total_posts_today=0, total_engagement=0, success_rate=0.0, ai_learning_score=0.0,
                last_update=datetime.now().isoformat(), version='10.0', errors_count=1
            )
    
    def _is_peak_time(self) -> bool:
        """Check if current time is peak time"""
        current_hour = datetime.now().hour
        # EU peak hours: 9, 13, 18, 21
        return current_hour in [9, 13, 18, 21]
    
    def _get_next_post_time(self, platform: str) -> str:
        """Get next scheduled post time for platform"""
        intervals = {
            'twitter': 20,  # 20 minutes
            'telegram': 30,  # 30 minutes
            'reddit': 60    # 60 minutes
        }
        
        interval = intervals.get(platform, 30)
        next_time = datetime.now() + timedelta(minutes=interval)
        return next_time.strftime('%H:%M')
    
    def connect_to_dashboard(self):
        """Connect to VoltageGPU dashboard via WebSocket"""
        try:
            logging.info(f"🔌 Connecting to dashboard: {self.api_endpoint}")
            
            def on_open(ws):
                logging.info("✅ Dashboard connected successfully!")
                self.connected = True
                
                # Send initial registration
                registration = {
                    'type': 'register',
                    'bot_id': self.bot_id,
                    'affiliate_code': self.affiliate_code,
                    'version': '10.0',
                    'timestamp': datetime.now().isoformat()
                }
                ws.send(json.dumps(registration))
            
            def on_message(ws, message):
                try:
                    data = json.loads(message)
                    if data.get('type') == 'ping':
                        # Respond to ping with pong
                        pong = {'type': 'pong', 'bot_id': self.bot_id}
                        ws.send(json.dumps(pong))
                        self.last_heartbeat = time.time()
                except Exception as e:
                    logging.error(f"❌ Error handling message: {e}")
            
            def on_error(ws, error):
                logging.error(f"❌ Dashboard connection error: {error}")
                self.connected = False
            
            def on_close(ws, close_status_code, close_msg):
                logging.warning("⚠️ Dashboard connection closed")
                self.connected = False
            
            # Create WebSocket connection
            self.ws = websocket.WebSocketApp(
                self.api_endpoint,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # Run WebSocket in separate thread
            ws_thread = threading.Thread(target=self.ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
        except Exception as e:
            logging.error(f"❌ Failed to connect to dashboard: {e}")
            self.connected = False
    
    def send_status_update(self):
        """Send bot status update to dashboard"""
        if not self.connected or not self.ws:
            return
        
        try:
            status = self.collect_bot_status()
            
            # Convert to dictionary for JSON serialization
            status_data = {
                'type': 'status_update',
                'data': asdict(status)
            }
            
            self.ws.send(json.dumps(status_data))
            logging.info(f"📊 Status update sent - Posts: {status.total_posts_today}, Success: {status.success_rate}%")
            
        except Exception as e:
            logging.error(f"❌ Error sending status update: {e}")
    
    def start_monitoring(self):
        """Start the dashboard monitoring service"""
        logging.info("🚀 Starting Dashboard API monitoring...")
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        # Connect to dashboard
        self.connect_to_dashboard()
        
        # Wait for connection
        time.sleep(2)
        
        if not self.connected:
            logging.warning("⚠️ Dashboard not connected, running in offline mode")
        
        # Main monitoring loop
        while self.running:
            try:
                # Send status update every 30 seconds
                if self.connected:
                    self.send_status_update()
                else:
                    # Try to reconnect
                    logging.info("🔄 Attempting to reconnect to dashboard...")
                    self.connect_to_dashboard()
                
                # Display local status
                status = self.collect_bot_status()
                self.display_local_status(status)
                
                # Wait 30 seconds
                time.sleep(30)
                
            except KeyboardInterrupt:
                logging.info("⏹️ Dashboard API stopped by user")
                break
            except Exception as e:
                logging.error(f"❌ Error in monitoring loop: {e}")
                time.sleep(10)
        
        self.stop()
    
    def display_local_status(self, status: BotStatus):
        """Display status in console"""
        print("\n" + "="*60)
        print(f"🤖 SHA-256 BOT DASHBOARD - {datetime.now().strftime('%H:%M:%S')}")
        print(f"💰 AFFILIATE: {status.affiliate_code}")
        print(f"🆔 BOT ID: {status.bot_id}")
        print(f"⏰ UPTIME: {status.uptime}s | 🌍 REGION: {status.current_region}")
        print(f"🔗 DASHBOARD: {'🟢 CONNECTED' if self.connected else '🔴 OFFLINE'}")
        print("-"*60)
        print(f"🐦 TWITTER: {status.twitter_status} ({status.twitter_posts_today} posts)")
        print(f"💬 TELEGRAM: {status.telegram_status} ({status.telegram_posts_today} posts)")
        print(f"📍 REDDIT: {status.reddit_status} ({status.reddit_posts_today} posts)")
        print("-"*60)
        print(f"📊 SUCCESS RATE: {status.success_rate}% | 🧠 AI SCORE: {status.ai_learning_score}")
        print(f"📈 TOTAL ENGAGEMENT: {status.total_engagement}")
        print("="*60)
    
    def stop(self):
        """Stop the dashboard API"""
        self.running = False
        if self.ws:
            self.ws.close()
        logging.info("⏹️ Dashboard API stopped")

def main():
    """Main function to run dashboard API"""
    print("🚀 SHA-256 BOT - LIVE DASHBOARD API")
    print("📊 Connecting to https://voltagegpu.com/SHA-256")
    print("-"*50)
    
    # Create and start dashboard API
    dashboard = DashboardAPI()
    
    try:
        dashboard.start_monitoring()
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard API stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        dashboard.stop()

if __name__ == "__main__":
    main()
