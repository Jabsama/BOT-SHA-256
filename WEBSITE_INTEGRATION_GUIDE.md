# 🌐 Website Integration Guide - BOT SHA-256 Dashboard

## 📋 Overview

This guide shows you how to integrate the BOT SHA-256 dashboard into your website at `https://voltagegpu.com/SHA-256`.

## 🚀 Quick Setup

### 1. **Start the Dashboard API**

```bash
# In your BOT SHA-256 directory
python dashboard_api.py
```

The API will run on `http://localhost:5000` by default.

### 2. **API Endpoints Available**

```
GET /api/health          - Health check
GET /api/stats           - Bot statistics
GET /api/performance     - Performance analytics
GET /api/regions         - Regional targeting data
GET /api/dashboard-config - Configuration for frontend
```

### 3. **Test the API**

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test stats endpoint
curl http://localhost:5000/api/stats
```

## 🎨 Frontend Integration for voltagegpu.com/SHA-256

### **HTML Structure**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOT SHA-256 Dashboard - VoltageGPU</title>
    <style>
        /* Dashboard Styles */
        .sha256-dashboard {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .dashboard-header {
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .dashboard-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e1e5e9;
        }
        
        .card-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
            display: flex;
            align-items: center;
        }
        
        .card-title::before {
            content: '';
            width: 4px;
            height: 20px;
            background: #3498db;
            margin-right: 10px;
            border-radius: 2px;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            margin: 10px 0;
        }
        
        .stat-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active { background-color: #27ae60; }
        .status-inactive { background-color: #e74c3c; }
        
        .refresh-btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        
        .refresh-btn:hover {
            background: #2980b9;
        }
        
        .loading {
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
        }
        
        .error {
            color: #e74c3c;
            background: #fdf2f2;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #e74c3c;
        }
        
        .performance-chart {
            height: 200px;
            background: #f8f9fa;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #6c757d;
        }
        
        .region-list {
            list-style: none;
            padding: 0;
        }
        
        .region-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .region-item:last-child {
            border-bottom: none;
        }
        
        .region-score {
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }
    </style>
</head>
<body>
    <div class="sha256-dashboard">
        <!-- Dashboard Header -->
        <div class="dashboard-header">
            <h1>🚀 BOT SHA-256 Dashboard</h1>
            <p>AI-Powered Social Media Automation</p>
            <button class="refresh-btn" onclick="loadDashboardData()">
                🔄 Refresh Data
            </button>
        </div>
        
        <!-- Main Dashboard Grid -->
        <div class="dashboard-grid">
            <!-- Bot Status Card -->
            <div class="dashboard-card">
                <div class="card-title">📊 Bot Status</div>
                <div id="bot-status" class="loading">Loading...</div>
            </div>
            
            <!-- Performance Stats Card -->
            <div class="dashboard-card">
                <div class="card-title">📈 Performance Stats</div>
                <div id="performance-stats" class="loading">Loading...</div>
            </div>
            
            <!-- Regional Targeting Card -->
            <div class="dashboard-card">
                <div class="card-title">🌍 Regional Targeting</div>
                <div id="regional-targeting" class="loading">Loading...</div>
            </div>
        </div>
        
        <!-- Detailed Analytics -->
        <div class="dashboard-grid">
            <!-- Posts Overview -->
            <div class="dashboard-card">
                <div class="card-title">📱 Platform Posts</div>
                <div id="platform-posts" class="loading">Loading...</div>
            </div>
            
            <!-- Performance Chart -->
            <div class="dashboard-card">
                <div class="card-title">📊 Performance Trend</div>
                <div id="performance-chart" class="performance-chart">
                    Performance chart will be displayed here
                </div>
            </div>
        </div>
    </div>

    <script>
        // Configuration
        const API_BASE_URL = 'http://localhost:5000/api'; // Change to your production URL
        const UPDATE_INTERVAL = 30000; // 30 seconds
        
        // Dashboard Data Loading
        async function loadDashboardData() {
            try {
                // Load bot statistics
                const statsResponse = await fetch(`${API_BASE_URL}/stats`);
                const stats = await statsResponse.json();
                
                if (stats.error) {
                    throw new Error(stats.error);
                }
                
                updateBotStatus(stats);
                updatePerformanceStats(stats);
                updatePlatformPosts(stats);
                
                // Load regional data
                const regionsResponse = await fetch(`${API_BASE_URL}/regions`);
                const regions = await regionsResponse.json();
                
                if (!regions.error) {
                    updateRegionalTargeting(regions);
                }
                
                // Load performance data
                const performanceResponse = await fetch(`${API_BASE_URL}/performance?days=7`);
                const performance = await performanceResponse.json();
                
                if (!performance.error) {
                    updatePerformanceChart(performance);
                }
                
            } catch (error) {
                console.error('Error loading dashboard data:', error);
                showError('Failed to load dashboard data. Please check your connection.');
            }
        }
        
        function updateBotStatus(stats) {
            const statusHtml = `
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <span class="status-indicator status-${stats.status}"></span>
                    <strong>Status: ${stats.status.toUpperCase()}</strong>
                </div>
                <p><strong>Current Target:</strong> ${stats.current_target.region} (${stats.current_target.language})</p>
                <p><strong>Average Performance:</strong> ${stats.average_performance}</p>
                <p><strong>Last Updated:</strong> ${new Date(stats.last_updated).toLocaleString()}</p>
            `;
            document.getElementById('bot-status').innerHTML = statusHtml;
        }
        
        function updatePerformanceStats(stats) {
            const total24h = stats.posts_24h.twitter + stats.posts_24h.telegram + stats.posts_24h.reddit;
            const totalAll = stats.total_posts.twitter + stats.total_posts.telegram + stats.total_posts.reddit;
            
            const statsHtml = `
                <div style="text-align: center;">
                    <div class="stat-number">${total24h}</div>
                    <div class="stat-label">Posts in Last 24h</div>
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <div class="stat-number" style="font-size: 1.5em;">${totalAll}</div>
                    <div class="stat-label">Total Posts</div>
                </div>
            `;
            document.getElementById('performance-stats').innerHTML = statsHtml;
        }
        
        function updatePlatformPosts(stats) {
            const platformsHtml = `
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; text-align: center;">
                    <div>
                        <div class="stat-number" style="font-size: 1.8em; color: #1da1f2;">${stats.total_posts.twitter}</div>
                        <div class="stat-label">Twitter</div>
                        <div style="font-size: 0.8em; color: #95a5a6;">${stats.posts_24h.twitter} today</div>
                    </div>
                    <div>
                        <div class="stat-number" style="font-size: 1.8em; color: #0088cc;">${stats.total_posts.telegram}</div>
                        <div class="stat-label">Telegram</div>
                        <div style="font-size: 0.8em; color: #95a5a6;">${stats.posts_24h.telegram} today</div>
                    </div>
                    <div>
                        <div class="stat-number" style="font-size: 1.8em; color: #ff4500;">${stats.total_posts.reddit}</div>
                        <div class="stat-label">Reddit</div>
                        <div style="font-size: 0.8em; color: #95a5a6;">${stats.posts_24h.reddit} today</div>
                    </div>
                </div>
            `;
            document.getElementById('platform-posts').innerHTML = platformsHtml;
        }
        
        function updateRegionalTargeting(regions) {
            let regionHtml = `
                <div style="margin-bottom: 20px;">
                    <strong>Current Optimal:</strong> 
                    <span style="background: #3498db; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.9em;">
                        ${regions.current_optimal}
                    </span>
                </div>
                <ul class="region-list">
            `;
            
            regions.regional_performance.slice(0, 5).forEach(region => {
                regionHtml += `
                    <li class="region-item">
                        <span>${region.region} (${region.language})</span>
                        <span class="region-score">${region.avg_score}</span>
                    </li>
                `;
            });
            
            regionHtml += '</ul>';
            document.getElementById('regional-targeting').innerHTML = regionHtml;
        }
        
        function updatePerformanceChart(performance) {
            // Simple performance display - you can integrate Chart.js here for real charts
            const chartHtml = `
                <div style="text-align: center;">
                    <h4>Last 7 Days Performance</h4>
                    <p>Top Content Types:</p>
                    <ul style="list-style: none; padding: 0;">
                        ${performance.top_content_types.slice(0, 3).map(content => 
                            `<li style="margin: 5px 0;">${content.content_type} (${content.platform}): ${content.avg_score}</li>`
                        ).join('')}
                    </ul>
                </div>
            `;
            document.getElementById('performance-chart').innerHTML = chartHtml;
        }
        
        function showError(message) {
            const errorHtml = `<div class="error">${message}</div>`;
            document.getElementById('bot-status').innerHTML = errorHtml;
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardData();
            
            // Auto-refresh every 30 seconds
            setInterval(loadDashboardData, UPDATE_INTERVAL);
        });
    </script>
</body>
</html>
```

## 🔧 Production Setup

### **1. Deploy the API**

```bash
# Install dependencies
pip install flask flask-cors python-dotenv

# Set production environment
export ENVIRONMENT=production
export DASHBOARD_HOST=0.0.0.0
export DASHBOARD_PORT=5000

# Run the API
python dashboard_api.py
```

### **2. Configure Reverse Proxy (Nginx)**

```nginx
# /etc/nginx/sites-available/voltagegpu.com
server {
    listen 80;
    server_name voltagegpu.com;
    
    # BOT SHA-256 Dashboard
    location /SHA-256 {
        # Serve your HTML file
        try_files $uri $uri/ /SHA-256.html;
    }
    
    # API Proxy
    location /api/sha256/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type, Authorization";
    }
}
```

### **3. Update API Base URL**

In your HTML file, change:

```javascript
const API_BASE_URL = 'https://voltagegpu.com/api/sha256';
```

## 🚀 Advanced Features

### **Real-time Updates with WebSockets**

```javascript
// Add to your HTML
const socket = new WebSocket('ws://localhost:5000/ws');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'stats_update') {
        updateBotStatus(data.stats);
    }
};
```

### **Chart Integration with Chart.js**

```html
<!-- Add Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
function createPerformanceChart(data) {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(data.daily_performance),
            datasets: [{
                label: 'Posts per Day',
                data: Object.values(data.daily_performance).map(day => 
                    (day.twitter?.posts || 0) + (day.telegram?.posts || 0) + (day.reddit?.posts || 0)
                ),
                borderColor: '#3498db',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
</script>
```

## 🔒 Security Considerations

### **API Authentication**

```python
# Add to dashboard_api.py
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != f"Bearer {os.getenv('API_SECRET_KEY')}":
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/stats', methods=['GET'])
@require_auth
def get_stats():
    return jsonify(api.get_bot_stats())
```

### **Rate Limiting**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/stats', methods=['GET'])
@limiter.limit("10 per minute")
def get_stats():
    return jsonify(api.get_bot_stats())
```

## 📱 Mobile Responsive Design

The provided CSS is already mobile-responsive, but you can enhance it:

```css
@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .dashboard-header {
        padding: 20px;
    }
    
    .stat-number {
        font-size: 2em;
    }
}
```

## 🎯 Integration Checklist

- [ ] API running on production server
- [ ] Reverse proxy configured
- [ ] CORS headers set correctly
- [ ] SSL certificate installed
- [ ] Dashboard HTML integrated into website
- [ ] API endpoints tested
- [ ] Auto-refresh working
- [ ] Mobile responsiveness verified
- [ ] Error handling implemented
- [ ] Security measures in place

## 🆘 Troubleshooting

### **Common Issues**

1. **CORS Errors**: Ensure CORS is enabled in Flask and Nginx
2. **API Connection Failed**: Check firewall and port settings
3. **Data Not Loading**: Verify database path and permissions
4. **Slow Performance**: Implement caching and optimize queries

### **Debug Mode**

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python dashboard_api.py
```

This integration will give you a professional, real-time dashboard for BOT SHA-256 on your website!
