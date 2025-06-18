#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VoltageGPU Bot - Analytics Dashboard
Real-time dashboard for tracking affiliate performance and bot metrics
"""

import sqlite3
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
import threading
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class VoltageGPUAnalytics:
    """Analytics system for VoltageGPU affiliate tracking"""
    
    def __init__(self):
        self.db_path = 'data/voltagegpu_analytics.db'
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for analytics"""
        os.makedirs('data', exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                content_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN NOT NULL,
                engagement_score INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0
            )
        ''')
        
        # Conversions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                affiliate_code TEXT NOT NULL,
                platform_source TEXT,
                conversion_value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_country TEXT,
                gpu_type TEXT
            )
        ''')
        
        # Performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                platform TEXT NOT NULL,
                posts_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0,
                engagement_rate REAL DEFAULT 0,
                conversion_rate REAL DEFAULT 0,
                revenue REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_post(self, platform: str, content_type: str, success: bool):
        """Log a post attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (platform, content_type, success)
            VALUES (?, ?, ?)
        ''', (platform, content_type, success))
        
        conn.commit()
        conn.close()
        
    def log_conversion(self, affiliate_code: str, platform_source: str, value: float, 
                      user_country: str = None, gpu_type: str = None):
        """Log an affiliate conversion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversions (affiliate_code, platform_source, conversion_value, user_country, gpu_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (affiliate_code, platform_source, value, user_country, gpu_type))
        
        conn.commit()
        conn.close()
        
    def get_daily_stats(self, days: int = 7):
        """Get daily statistics for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                DATE(timestamp) as date,
                platform,
                COUNT(*) as posts,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_posts,
                AVG(engagement_score) as avg_engagement
            FROM posts 
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY DATE(timestamp), platform
            ORDER BY date DESC
        '''.format(days))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'date': row[0],
                'platform': row[1],
                'posts': row[2],
                'successful_posts': row[3],
                'success_rate': (row[3] / row[2] * 100) if row[2] > 0 else 0,
                'avg_engagement': row[4] or 0
            }
            for row in results
        ]
        
    def get_conversion_stats(self, days: int = 30):
        """Get conversion statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                platform_source,
                COUNT(*) as conversions,
                SUM(conversion_value) as total_revenue,
                AVG(conversion_value) as avg_value
            FROM conversions 
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY platform_source
        '''.format(days))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'platform': row[0],
                'conversions': row[1],
                'total_revenue': row[2] or 0,
                'avg_value': row[3] or 0
            }
            for row in results
        ]

# Flask Dashboard App
app = Flask(__name__)
analytics = VoltageGPUAnalytics()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    daily_stats = analytics.get_daily_stats(7)
    conversion_stats = analytics.get_conversion_stats(30)
    
    # Calculate totals
    total_posts = sum(stat['posts'] for stat in daily_stats)
    total_successful = sum(stat['successful_posts'] for stat in daily_stats)
    total_revenue = sum(stat['total_revenue'] for stat in conversion_stats)
    total_conversions = sum(stat['conversions'] for stat in conversion_stats)
    
    return jsonify({
        'summary': {
            'total_posts': total_posts,
            'success_rate': (total_successful / total_posts * 100) if total_posts > 0 else 0,
            'total_revenue': total_revenue,
            'total_conversions': total_conversions,
            'conversion_rate': (total_conversions / total_posts * 100) if total_posts > 0 else 0
        },
        'daily_stats': daily_stats,
        'conversion_stats': conversion_stats
    })

@app.route('/api/realtime')
def api_realtime():
    """Real-time metrics for live dashboard"""
    conn = sqlite3.connect(analytics.db_path)
    cursor = conn.cursor()
    
    # Posts in last hour
    cursor.execute('''
        SELECT platform, COUNT(*) 
        FROM posts 
        WHERE timestamp >= datetime('now', '-1 hour')
        GROUP BY platform
    ''')
    recent_posts = dict(cursor.fetchall())
    
    # Recent conversions
    cursor.execute('''
        SELECT * FROM conversions 
        WHERE timestamp >= datetime('now', '-24 hours')
        ORDER BY timestamp DESC
        LIMIT 10
    ''')
    recent_conversions = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'recent_posts': recent_posts,
        'recent_conversions': [
            {
                'platform': conv[2],
                'value': conv[3],
                'timestamp': conv[4],
                'country': conv[5],
                'gpu_type': conv[6]
            }
            for conv in recent_conversions
        ]
    })

def create_dashboard_template():
    """Create HTML template for dashboard"""
    os.makedirs('templates', exist_ok=True)
    
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoltageGPU Bot Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            opacity: 0.8;
            font-size: 0.9em;
        }
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .chart-container {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .recent-activity {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .activity-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .status-success { background: #4CAF50; }
        .status-error { background: #f44336; }
        .status-warning { background: #ff9800; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 VoltageGPU Bot Dashboard</h1>
            <p>Real-time affiliate marketing performance</p>
        </div>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be loaded here -->
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <h3>Posts by Platform</h3>
                <canvas id="postsChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>Revenue by Platform</h3>
                <canvas id="revenueChart"></canvas>
            </div>
        </div>
        
        <div class="recent-activity">
            <h3>Recent Activity</h3>
            <div id="recentActivity">
                <!-- Recent activity will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        // Load dashboard data
        async function loadDashboard() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                // Update stats cards
                updateStatsCards(data.summary);
                
                // Update charts
                updateCharts(data);
                
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        function updateStatsCards(summary) {
            const statsGrid = document.getElementById('statsGrid');
            statsGrid.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${summary.total_posts}</div>
                    <div class="stat-label">Total Posts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${summary.success_rate.toFixed(1)}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">$${summary.total_revenue.toFixed(2)}</div>
                    <div class="stat-label">Total Revenue</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${summary.total_conversions}</div>
                    <div class="stat-label">Conversions</div>
                </div>
            `;
        }
        
        function updateCharts(data) {
            // Posts by platform chart
            const postsCtx = document.getElementById('postsChart').getContext('2d');
            const platformData = {};
            
            data.daily_stats.forEach(stat => {
                if (!platformData[stat.platform]) {
                    platformData[stat.platform] = 0;
                }
                platformData[stat.platform] += stat.posts;
            });
            
            new Chart(postsCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(platformData),
                    datasets: [{
                        data: Object.values(platformData),
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: 'white' }
                        }
                    }
                }
            });
            
            // Revenue by platform chart
            const revenueCtx = document.getElementById('revenueChart').getContext('2d');
            const revenueData = {};
            
            data.conversion_stats.forEach(stat => {
                revenueData[stat.platform] = stat.total_revenue;
            });
            
            new Chart(revenueCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(revenueData),
                    datasets: [{
                        label: 'Revenue ($)',
                        data: Object.values(revenueData),
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: 'white' }
                        },
                        x: {
                            ticks: { color: 'white' }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: { color: 'white' }
                        }
                    }
                }
            });
        }
        
        // Load dashboard on page load
        loadDashboard();
        
        // Refresh every 30 seconds
        setInterval(loadDashboard, 30000);
    </script>
</body>
</html>
    '''
    
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def run_dashboard(port=5000):
    """Run the Flask dashboard"""
    create_dashboard_template()
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    # Create dashboard template
    create_dashboard_template()
    
    # Run dashboard
    print("🚀 Starting VoltageGPU Analytics Dashboard...")
    print(f"📊 Dashboard available at: http://localhost:5000")
    run_dashboard()
