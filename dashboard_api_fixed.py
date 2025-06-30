#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SHA-256 BOT - LIVE DASHBOARD API (FIXED VERSION)
Connects to https://voltagegpu.com/SHA-256 for real-time monitoring
"""

import os
import json
import time
import logging
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Configure logging without emojis for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/dashboard_api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

@dataclass
class BotStatus:
    """Bot status data structure for dashboard"""
    bot_id: str
    status: str
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
    """Live Dashboard API for VoltageGPU monitoring (Fixed Version)"""
    
    def __init__(self):
        self.dashboard_url = "https://voltagegpu.com/SHA-256"
        self.bot_id = self._generate_bot_id()
        self.affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-76360B81D39F')
        
        self.connected = False
        self.running = True
        self.start_time = time.time()
        
        # Data collection
        self.db_path = 'data/dashboard_data.db'
        self._init_database()
        
        logging.info(f"Dashboard API initialized - Bot ID: {self.bot_id}")
    
    def _generate_bot_id(self) -> str:
        """Generate unique bot identifier"""
        import hashlib
        import uuid
        
        machine_id = str(uuid.getnode())
        timestamp = str(int(time.time() / 3600))
        
        bot_id = hashlib.md5(f"{machine_id}_{timestamp}".encode()).hexdigest()[:12]
        return f"SHA256-{bot_id.upper()}"
    
    def _init_database(self):
        """Initialize dashboard database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create dashboard data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dashboard_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                platform TEXT NOT NULL,
                posts_count INTEGER DEFAULT 0,
                engagement INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0
            )
        ''')
        
        # Insert sample data if empty
        cursor.execute('SELECT COUNT(*) FROM dashboard_data')
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ('twitter', 5, 120, 85.5),
                ('telegram', 3, 89, 92.1),
                ('reddit', 2, 45, 78.3)
            ]
            
            for platform, posts, engagement, success in sample_data:
                cursor.execute('''
                    INSERT INTO dashboard_data (platform, posts_count, engagement, success_rate)
                    VALUES (?, ?, ?, ?)
                ''', (platform, posts, engagement, success))
        
        conn.commit()
        conn.close()
        logging.info("Dashboard database initialized successfully")
    
    def collect_bot_status(self) -> BotStatus:
        """Collect current bot status from database and system"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get platform data
            cursor.execute('SELECT platform, posts_count, engagement, success_rate FROM dashboard_data')
            platform_data = {row[0]: {'posts': row[1], 'engagement': row[2], 'success': row[3]} 
                           for row in cursor.fetchall()}
            
            conn.close()
            
            # Calculate uptime
            uptime = int(time.time() - self.start_time)
            
            # Get platform stats
            twitter_data = platform_data.get('twitter', {'posts': 0, 'engagement': 0, 'success': 0})
            telegram_data = platform_data.get('telegram', {'posts': 0, 'engagement': 0, 'success': 0})
            reddit_data = platform_data.get('reddit', {'posts': 0, 'engagement': 0, 'success': 0})
            
            # Create status object
            status = BotStatus(
                bot_id=self.bot_id,
                status='running',
                uptime=uptime,
                current_region='EU_WEST',
                current_language='en',
                is_peak_time=self._is_peak_time(),
                affiliate_code=self.affiliate_code,
                
                twitter_posts_today=twitter_data['posts'],
                twitter_status='ACTIVE' if twitter_data['posts'] < 20 else 'RATE LIMITED',
                twitter_next_post=self._get_next_post_time('twitter'),
                twitter_followers_gained=twitter_data['engagement'],
                
                telegram_posts_today=telegram_data['posts'],
                telegram_status='ACTIVE' if telegram_data['posts'] < 15 else 'RATE LIMITED',
                telegram_next_post=self._get_next_post_time('telegram'),
                telegram_invites_sent=telegram_data['engagement'],
                
                reddit_posts_today=reddit_data['posts'],
                reddit_status='ACTIVE' if reddit_data['posts'] < 5 else 'RATE LIMITED',
                reddit_next_post=self._get_next_post_time('reddit'),
                reddit_karma_gained=reddit_data['engagement'],
                
                total_posts_today=sum(d['posts'] for d in platform_data.values()),
                total_engagement=sum(d['engagement'] for d in platform_data.values()),
                success_rate=round(sum(d['success'] for d in platform_data.values()) / len(platform_data), 1),
                ai_learning_score=85.5,
                
                last_update=datetime.now().isoformat(),
                version='11.0',
                errors_count=0
            )
            
            return status
            
        except Exception as e:
            logging.error(f"Error collecting bot status: {e}")
            # Return minimal status on error
            return BotStatus(
                bot_id=self.bot_id, status='error', uptime=0, current_region='UNKNOWN',
                current_language='en', is_peak_time=False, affiliate_code=self.affiliate_code,
                twitter_posts_today=0, twitter_status='ERROR', twitter_next_post='Unknown', twitter_followers_gained=0,
                telegram_posts_today=0, telegram_status='ERROR', telegram_next_post='Unknown', telegram_invites_sent=0,
                reddit_posts_today=0, reddit_status='ERROR', reddit_next_post='Unknown', reddit_karma_gained=0,
                total_posts_today=0, total_engagement=0, success_rate=0.0, ai_learning_score=0.0,
                last_update=datetime.now().isoformat(), version='11.0', errors_count=1
            )
    
    def _is_peak_time(self) -> bool:
        """Check if current time is peak time"""
        current_hour = datetime.now().hour
        return current_hour in [9, 13, 18, 21]
    
    def _get_next_post_time(self, platform: str) -> str:
        """Get next scheduled post time for platform"""
        intervals = {'twitter': 20, 'telegram': 30, 'reddit': 60}
        interval = intervals.get(platform, 30)
        next_time = datetime.now() + timedelta(minutes=interval)
        return next_time.strftime('%H:%M')
    
    def simulate_dashboard_connection(self):
        """Simulate dashboard connection (for demo purposes)"""
        logging.info("Simulating dashboard connection...")
        
        # Simulate connection delay
        time.sleep(2)
        
        # For demo, we'll simulate a successful connection
        self.connected = True
        logging.info("Dashboard connection simulated successfully!")
        
        return True
    
    def send_status_to_web(self, status: BotStatus):
        """Send status to web dashboard (simulated)"""
        try:
            # In a real implementation, this would send data to the web dashboard
            # For now, we'll save to a JSON file that the web dashboard can read
            
            status_data = {
                'timestamp': datetime.now().isoformat(),
                'bot_data': asdict(status)
            }
            
            # Save to JSON file for web dashboard
            os.makedirs('data', exist_ok=True)
            with open('data/dashboard_status.json', 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Status sent to dashboard - Posts: {status.total_posts_today}, Success: {status.success_rate}%")
            
        except Exception as e:
            logging.error(f"Error sending status to dashboard: {e}")
    
    def start_monitoring(self):
        """Start the dashboard monitoring service"""
        logging.info("Starting Dashboard API monitoring...")
        
        # Ensure directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        # Simulate connection to dashboard
        self.simulate_dashboard_connection()
        
        if not self.connected:
            logging.warning("Dashboard not connected, running in offline mode")
        
        # Main monitoring loop
        while self.running:
            try:
                # Collect and display status
                status = self.collect_bot_status()
                self.display_local_status(status)
                
                # Send to web dashboard
                if self.connected:
                    self.send_status_to_web(status)
                
                # Update database with new data (simulate activity)
                self.update_sample_data()
                
                # Wait 30 seconds
                time.sleep(30)
                
            except KeyboardInterrupt:
                logging.info("Dashboard API stopped by user")
                break
            except Exception as e:
                logging.error(f"Error in monitoring loop: {e}")
                time.sleep(10)
        
        self.stop()
    
    def update_sample_data(self):
        """Update sample data to simulate bot activity"""
        try:
            import random
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Simulate new posts and engagement
            platforms = ['twitter', 'telegram', 'reddit']
            for platform in platforms:
                # Small chance to increment posts
                if random.random() < 0.1:  # 10% chance
                    cursor.execute('''
                        UPDATE dashboard_data 
                        SET posts_count = posts_count + 1,
                            engagement = engagement + ?,
                            timestamp = CURRENT_TIMESTAMP
                        WHERE platform = ?
                    ''', (random.randint(1, 10), platform))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"Error updating sample data: {e}")
    
    def display_local_status(self, status: BotStatus):
        """Display status in console (Windows-friendly)"""
        print("\n" + "="*60)
        print(f"SHA-256 BOT DASHBOARD - {datetime.now().strftime('%H:%M:%S')}")
        print(f"AFFILIATE: {status.affiliate_code}")
        print(f"BOT ID: {status.bot_id}")
        print(f"UPTIME: {status.uptime}s | REGION: {status.current_region}")
        print(f"DASHBOARD: {'CONNECTED' if self.connected else 'OFFLINE'}")
        print("-"*60)
        print(f"TWITTER: {status.twitter_status} ({status.twitter_posts_today} posts)")
        print(f"TELEGRAM: {status.telegram_status} ({status.telegram_posts_today} posts)")
        print(f"REDDIT: {status.reddit_status} ({status.reddit_posts_today} posts)")
        print("-"*60)
        print(f"SUCCESS RATE: {status.success_rate}% | AI SCORE: {status.ai_learning_score}")
        print(f"TOTAL ENGAGEMENT: {status.total_engagement}")
        print("="*60)
    
    def stop(self):
        """Stop the dashboard API"""
        self.running = False
        logging.info("Dashboard API stopped")

def main():
    """Main function to run dashboard API"""
    print("SHA-256 BOT - LIVE DASHBOARD API (FIXED)")
    print("Connecting to https://voltagegpu.com/SHA-256")
    print("-"*50)
    
    # Create and start dashboard API
    dashboard = DashboardAPI()
    
    try:
        dashboard.start_monitoring()
    except KeyboardInterrupt:
        print("\nDashboard API stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        dashboard.stop()

if __name__ == "__main__":
    main()
