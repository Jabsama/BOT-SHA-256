#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 BOT SHA-256 Dashboard API
Web API for monitoring and controlling the bot from your website
Compatible with https://voltagegpu.com/SHA-256
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for website integration

# Configuration
DB_PATH = os.getenv('DATABASE_PATH', 'performance_analytics.db')
API_PORT = int(os.getenv('DASHBOARD_PORT', 5000))
API_HOST = os.getenv('DASHBOARD_HOST', '0.0.0.0')

class DashboardAPI:
    """Dashboard API for BOT SHA-256"""
    
    def __init__(self):
        self.db_path = DB_PATH
        
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            return None
    
    def get_bot_stats(self):
        """Get overall bot statistics"""
        conn = self.get_connection()
        if not conn:
            return {"error": "Database connection failed"}
        
        try:
            cursor = conn.cursor()
            
            # Get total posts by platform
            cursor.execute('''
                SELECT platform, COUNT(*) as total_posts
                FROM post_performance 
                GROUP BY platform
            ''')
            platform_stats = dict(cursor.fetchall())
            
            # Get posts in last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            cursor.execute('''
                SELECT platform, COUNT(*) as posts_24h
                FROM post_performance 
                WHERE post_time > ?
                GROUP BY platform
            ''', (yesterday,))
            recent_stats = dict(cursor.fetchall())
            
            # Get average performance score
            cursor.execute('''
                SELECT AVG(performance_score) as avg_score
                FROM post_performance 
                WHERE performance_score > 0
            ''')
            avg_score = cursor.fetchone()[0] or 0
            
            # Get current region targeting
            cursor.execute('''
                SELECT region, language, COUNT(*) as posts
                FROM post_performance 
                WHERE post_time > ?
                GROUP BY region, language
                ORDER BY posts DESC
                LIMIT 1
            ''', (yesterday,))
            current_target = cursor.fetchone()
            
            conn.close()
            
            return {
                "status": "active",
                "total_posts": {
                    "twitter": platform_stats.get("twitter", 0),
                    "telegram": platform_stats.get("telegram", 0),
                    "reddit": platform_stats.get("reddit", 0)
                },
                "posts_24h": {
                    "twitter": recent_stats.get("twitter", 0),
                    "telegram": recent_stats.get("telegram", 0),
                    "reddit": recent_stats.get("reddit", 0)
                },
                "average_performance": round(avg_score, 3),
                "current_target": {
                    "region": current_target[0] if current_target else "US_EAST",
                    "language": current_target[1] if current_target else "en"
                },
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting bot stats: {e}")
            conn.close()
            return {"error": str(e)}
    
    def get_performance_data(self, days=7):
        """Get performance analytics for the last N days"""
        conn = self.get_connection()
        if not conn:
            return {"error": "Database connection failed"}
        
        try:
            cursor = conn.cursor()
            start_date = datetime.now() - timedelta(days=days)
            
            # Get daily performance
            cursor.execute('''
                SELECT 
                    DATE(post_time) as date,
                    platform,
                    COUNT(*) as posts,
                    AVG(performance_score) as avg_score,
                    SUM(engagement_count) as total_engagement,
                    SUM(click_count) as total_clicks
                FROM post_performance 
                WHERE post_time > ?
                GROUP BY DATE(post_time), platform
                ORDER BY date DESC
            ''', (start_date,))
            
            daily_data = {}
            for row in cursor.fetchall():
                date = row[0]
                if date not in daily_data:
                    daily_data[date] = {}
                
                daily_data[date][row[1]] = {
                    "posts": row[2],
                    "avg_score": round(row[3] or 0, 3),
                    "engagement": row[4] or 0,
                    "clicks": row[5] or 0
                }
            
            # Get top performing content types
            cursor.execute('''
                SELECT 
                    content_type,
                    platform,
                    COUNT(*) as posts,
                    AVG(performance_score) as avg_score
                FROM post_performance 
                WHERE post_time > ? AND performance_score > 0
                GROUP BY content_type, platform
                ORDER BY avg_score DESC
                LIMIT 10
            ''', (start_date,))
            
            top_content = []
            for row in cursor.fetchall():
                top_content.append({
                    "content_type": row[0],
                    "platform": row[1],
                    "posts": row[2],
                    "avg_score": round(row[3], 3)
                })
            
            conn.close()
            
            return {
                "daily_performance": daily_data,
                "top_content_types": top_content,
                "period_days": days,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting performance data: {e}")
            conn.close()
            return {"error": str(e)}
    
    def get_regional_data(self):
        """Get regional targeting performance"""
        conn = self.get_connection()
        if not conn:
            return {"error": "Database connection failed"}
        
        try:
            cursor = conn.cursor()
            
            # Get performance by region
            cursor.execute('''
                SELECT 
                    region,
                    language,
                    COUNT(*) as posts,
                    AVG(performance_score) as avg_score,
                    SUM(engagement_count) as total_engagement
                FROM post_performance 
                WHERE performance_score > 0
                GROUP BY region, language
                ORDER BY avg_score DESC
            ''')
            
            regional_data = []
            for row in cursor.fetchall():
                regional_data.append({
                    "region": row[0],
                    "language": row[1],
                    "posts": row[2],
                    "avg_score": round(row[3], 3),
                    "total_engagement": row[4] or 0
                })
            
            # Get current optimal region
            from datetime import timezone as tz
            utc_now = datetime.now(tz.utc)
            current_hour = utc_now.hour
            
            # Simple peak time detection
            peak_regions = {
                "US_EAST": [13, 14, 15, 16, 17, 18, 19, 20],
                "EU_WEST": [8, 9, 12, 13, 17, 18, 19, 20],
                "INDIA": [9, 10, 11, 18, 19, 20, 21, 22],
                "CHINA": [8, 9, 10, 19, 20, 21, 22, 23]
            }
            
            optimal_region = "US_EAST"  # Default
            for region, hours in peak_regions.items():
                if current_hour in hours:
                    optimal_region = region
                    break
            
            conn.close()
            
            return {
                "regional_performance": regional_data,
                "current_optimal": optimal_region,
                "current_hour_utc": current_hour,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting regional data: {e}")
            conn.close()
            return {"error": str(e)}

# Initialize API
api = DashboardAPI()

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "BOT SHA-256 Dashboard API",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get bot statistics"""
    return jsonify(api.get_bot_stats())

@app.route('/api/performance', methods=['GET'])
def get_performance():
    """Get performance analytics"""
    days = request.args.get('days', 7, type=int)
    return jsonify(api.get_performance_data(days))

@app.route('/api/regions', methods=['GET'])
def get_regions():
    """Get regional targeting data"""
    return jsonify(api.get_regional_data())

@app.route('/api/dashboard-config', methods=['GET'])
def get_dashboard_config():
    """Get dashboard configuration for website integration"""
    return jsonify({
        "api_endpoints": {
            "stats": "/api/stats",
            "performance": "/api/performance?days=7",
            "regions": "/api/regions",
            "health": "/api/health"
        },
        "update_interval": 30,  # seconds
        "features": {
            "real_time_stats": True,
            "performance_charts": True,
            "regional_targeting": True,
            "ai_insights": True
        },
        "branding": {
            "name": "BOT SHA-256",
            "version": "2.0",
            "description": "AI-Powered Social Media Automation"
        }
    })

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Simple dashboard for testing"""
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BOT SHA-256 Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .stat-item { text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; color: #007bff; }
            .stat-label { color: #666; margin-top: 5px; }
            .status-active { color: #28a745; }
            .status-inactive { color: #dc3545; }
            h1 { color: #333; text-align: center; }
            h2 { color: #555; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
            .refresh-btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
            .refresh-btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 BOT SHA-256 Dashboard</h1>
            
            <div class="card">
                <h2>📊 Bot Status</h2>
                <div id="bot-status">Loading...</div>
                <button class="refresh-btn" onclick="loadData()">Refresh Data</button>
            </div>
            
            <div class="card">
                <h2>📈 Performance Stats</h2>
                <div class="stats-grid" id="stats-grid">Loading...</div>
            </div>
            
            <div class="card">
                <h2>🌍 Regional Targeting</h2>
                <div id="regional-data">Loading...</div>
            </div>
        </div>
        
        <script>
            async function loadData() {
                try {
                    // Load bot stats
                    const statsResponse = await fetch('/api/stats');
                    const stats = await statsResponse.json();
                    
                    document.getElementById('bot-status').innerHTML = `
                        <p>Status: <span class="status-${stats.status === 'active' ? 'active' : 'inactive'}">${stats.status}</span></p>
                        <p>Current Target: ${stats.current_target.region} (${stats.current_target.language})</p>
                        <p>Average Performance: ${stats.average_performance}</p>
                        <p>Last Updated: ${new Date(stats.last_updated).toLocaleString()}</p>
                    `;
                    
                    document.getElementById('stats-grid').innerHTML = `
                        <div class="stat-item">
                            <div class="stat-number">${stats.total_posts.twitter}</div>
                            <div class="stat-label">Twitter Posts</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${stats.total_posts.telegram}</div>
                            <div class="stat-label">Telegram Posts</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${stats.total_posts.reddit}</div>
                            <div class="stat-label">Reddit Posts</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${stats.posts_24h.twitter + stats.posts_24h.telegram + stats.posts_24h.reddit}</div>
                            <div class="stat-label">Posts (24h)</div>
                        </div>
                    `;
                    
                    // Load regional data
                    const regionsResponse = await fetch('/api/regions');
                    const regions = await regionsResponse.json();
                    
                    let regionalHtml = `<p>Current Optimal: <strong>${regions.current_optimal}</strong></p>`;
                    regionalHtml += '<h3>Regional Performance:</h3><ul>';
                    
                    regions.regional_performance.forEach(region => {
                        regionalHtml += `<li>${region.region} (${region.language}): ${region.posts} posts, Score: ${region.avg_score}</li>`;
                    });
                    
                    regionalHtml += '</ul>';
                    document.getElementById('regional-data').innerHTML = regionalHtml;
                    
                } catch (error) {
                    console.error('Error loading data:', error);
                    document.getElementById('bot-status').innerHTML = '<p style="color: red;">Error loading data</p>';
                }
            }
            
            // Load data on page load
            loadData();
            
            // Auto-refresh every 30 seconds
            setInterval(loadData, 30000);
        </script>
    </body>
    </html>
    """
    return dashboard_html

if __name__ == '__main__':
    logger.info(f"🚀 Starting BOT SHA-256 Dashboard API on {API_HOST}:{API_PORT}")
    logger.info(f"📊 Dashboard URL: http://localhost:{API_PORT}/dashboard")
    logger.info(f"🔗 API Base URL: http://localhost:{API_PORT}/api")
    
    app.run(
        host=API_HOST,
        port=API_PORT,
        debug=os.getenv('ENVIRONMENT', 'development') == 'development'
    )
