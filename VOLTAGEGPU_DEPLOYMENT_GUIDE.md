# 🚀 VoltageGPU SHA-256 Bot Dashboard - Complete Deployment Guide

## 📋 Overview

This guide provides complete instructions for deploying the SHA-256 Bot Dashboard on your VoltageGPU website. The dashboard will work as a standalone service that can be embedded into your site.

## 🎯 Affiliate Code

**Primary Affiliate Code:** Set in environment variables (see .env configuration)

## 🚀 Quick Start

### 1. Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# 4. Start the dashboard API
python dashboard_api.py
```

### 2. Dashboard Endpoints

- **Full Dashboard:** `http://localhost:5000/`
- **Embeddable Widget:** `http://localhost:5000/widget`
- **API Status:** `http://localhost:5000/api/widget/status`

## 🔧 Integration Options for VoltageGPU.com

### Option 1: Embedded Widget (Recommended)

Add this HTML code to your `/SHA-256` page:

```html
<!-- SHA-256 Bot Widget for VoltageGPU -->
<div id="sha256-widget-container">
    <iframe 
        src="http://your-server:5000/widget" 
        width="400" 
        height="600" 
        frameborder="0"
        style="border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
    </iframe>
</div>

<!-- Optional: Add custom styling -->
<style>
#sha256-widget-container {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}

@media (max-width: 768px) {
    #sha256-widget-container iframe {
        width: 100%;
        max-width: 400px;
    }
}
</style>
```

### Option 2: AJAX Integration

For more control, use JavaScript to fetch data:

```html
<div id="sha256-status">
    <div class="bot-status">
        <h3>SHA-256 Bot Status</h3>
        <div id="status-indicator">Loading...</div>
        <div id="posts-today">-</div>
        <div id="success-rate">-</div>
        <div id="affiliate-code">SHA-256-76360B81D39F</div>
    </div>
</div>

<script>
async function loadBotStatus() {
    try {
        const response = await fetch('http://your-server:5000/api/widget/status');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('status-indicator').textContent = 
                data.data.running ? 'ACTIVE' : 'STOPPED';
            document.getElementById('posts-today').textContent = 
                `Posts Today: ${data.data.posts_today}`;
            document.getElementById('success-rate').textContent = 
                `Success Rate: ${(data.data.success_rate * 100).toFixed(1)}%`;
        }
    } catch (error) {
        console.error('Error loading bot status:', error);
        document.getElementById('status-indicator').textContent = 'ERROR';
    }
}

// Load status on page load
loadBotStatus();

// Refresh every 30 seconds
setInterval(loadBotStatus, 30000);
</script>
```

## 🖥️ Server Deployment

### Production Deployment with Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 dashboard_api:app

# Or with WebSocket support
gunicorn -w 1 -b 0.0.0.0:5000 --worker-class eventlet dashboard_api:app
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "dashboard_api.py"]
```

```bash
# Build and run Docker container
docker build -t sha256-dashboard .
docker run -p 5000:5000 sha256-dashboard
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /sha256-dashboard/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 🔒 Security Configuration

### Environment Variables (.env)

```env
# Bot Configuration
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Dashboard Security
DASHBOARD_SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=https://voltagegpu.com,http://localhost:3000

# Database
DATABASE_URL=sqlite:///bot_data.db

# Affiliate Configuration
AFFILIATE_CODE=SHA-256-76360B81D39F
BASE_URL=https://voltagegpu.com
```

### CORS Configuration

The dashboard is pre-configured to allow requests from `voltagegpu.com`. Update the CORS settings in `dashboard_api.py` if needed:

```python
CORS(app, origins=[
    "https://voltagegpu.com", 
    "https://www.voltagegpu.com",
    "http://localhost:*"
])
```

## 📊 Dashboard Features

### Real-time Monitoring
- Live bot status updates
- Performance metrics
- Platform-specific statistics
- System resource monitoring

### Interactive Controls
- Start/Stop/Restart bot
- Configuration management
- Real-time log streaming
- Alert notifications

### Security Features
- Encrypted credential storage
- Authentication logging
- Rate limiting
- Input validation

### Anti-Shadow-Ban Protection
- Content risk analysis
- Platform-specific limits
- Human behavior simulation
- Intelligent timing optimization

## 🔧 API Endpoints

### Widget API
```
GET /api/widget/status
Response: {
    "success": true,
    "data": {
        "running": true,
        "posts_today": 15,
        "success_rate": 0.95,
        "uptime": 3600,
        "affiliate_code": "SHA-256-76360B81D39F"
    }
}
```

### Bot Control API
```
POST /api/bot/start
POST /api/bot/stop
POST /api/bot/restart
```

### Monitoring API
```
GET /api/status
GET /api/metrics?hours=24
GET /api/alerts?hours=24
GET /api/logs?lines=100
```

## 🚨 Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'textblob'**
   ```bash
   pip install textblob
   python -m textblob.download_corpora
   ```

2. **CORS Error**
   - Check ALLOWED_ORIGINS in .env
   - Verify domain in CORS configuration

3. **Database Connection Error**
   - Ensure write permissions in project directory
   - Check DATABASE_URL in .env

4. **WebSocket Connection Failed**
   - Use eventlet worker with Gunicorn
   - Check firewall settings

### Installation Commands

```bash
# Install all dependencies
pip install -r requirements.txt

# Install additional NLP data for TextBlob
python -m textblob.download_corpora

# Test the installation
python -c "import flask, textblob, cryptography; print('All dependencies installed successfully')"
```

## 📱 Mobile Responsiveness

The dashboard and widget are fully responsive and work on:
- Desktop browsers
- Mobile devices
- Tablets
- Embedded iframes

## 🔄 Auto-Updates

The dashboard automatically:
- Refreshes data every 30 seconds
- Reconnects on connection loss
- Updates charts in real-time
- Handles visibility changes

## 📈 Performance Optimization

### Recommended Settings
- Use Redis for session storage (optional)
- Enable gzip compression
- Set up CDN for static assets
- Use database connection pooling

### Monitoring
- CPU and memory usage tracking
- Database performance metrics
- API response time monitoring
- Error rate tracking

## 🎯 Integration with VoltageGPU

The dashboard is specifically designed for VoltageGPU with:
- Custom branding and colors
- Affiliate code integration
- GPU-focused messaging
- Performance optimization for crypto/mining audience

## 📞 Support

For technical support or customization requests:
- GitHub Issues: https://github.com/Jabsama/BOT-SHA-256/issues
- Documentation: Check the repository README
- Community: Join our Discord/Telegram channels

## 🔐 License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Ready for production deployment on voltagegpu.com!** 🚀
