# 🚀 BOT SHA-256 - AI-Powered Social Media Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

> **The most advanced open-source social media automation bot with AI performance analysis, timezone optimization, and smart targeting.**

## 🌟 What is BOT SHA-256?

BOT SHA-256 is an intelligent, multi-platform social media automation bot that uses AI to optimize your content strategy across Twitter, Reddit, and Telegram. It automatically adapts to different timezones, languages, and audiences to maximize engagement and reach.

## ✨ Key Features

### 🤖 **AI Performance Analysis**
- Real-time engagement tracking and optimization
- Adaptive content strategy based on performance data
- Smart recommendations for best-performing content types

### 🌍 **Global Timezone Optimization**
- Automatic targeting of 10+ major regions (US, EU, Asia, LATAM)
- Peak hour detection for maximum engagement
- Dynamic region switching based on optimal posting times

### 📍 **Smart Platform Targeting**
- **Reddit**: Intelligent subreddit selection with automatic flair detection
- **Twitter**: Multi-account support with rate limiting
- **Telegram**: Autonomous group joining and targeted posting

### 🗣️ **Multilingual Support**
- Content generation in English, Chinese, Portuguese, and German
- Cultural adaptation for local markets
- Language-specific hashtags and templates

### 📊 **Advanced Analytics**
- SQLite database for performance tracking
- Real-time insights and recommendations
- Detailed error reporting with timing information

## 🚀 Quick Start Guide

### 1. **Clone the Repository**
```bash
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure Your Bot**
```bash
# Copy the example configuration
cp .env.example .env

# Edit the configuration file
nano .env  # or use your favorite editor
```

### 4. **Launch Your Bot**
```bash
# Test mode (recommended first)
python bot_voltage_fixed.py --test

# Production mode
python bot_voltage_fixed.py
```

## 🔧 Configuration Guide

### **Step 1: Basic Setup**

Edit your `.env` file with your API credentials:

```env
# 🐦 Twitter Configuration (Get from https://developer.twitter.com)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# 💬 Telegram Configuration (Get from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_channel

# 📍 Reddit Configuration (Get from https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password

# 💰 Your Affiliate Code
AFFILIATE_CODE=your_affiliate_code
```

### **Step 2: Platform Setup**

#### 🐦 **Twitter Setup**
1. Go to [Twitter Developer Portal](https://developer.twitter.com)
2. Create a new app and get your API keys
3. Add keys to your `.env` file

#### 💬 **Telegram Setup**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token and add to `.env`

#### 📍 **Reddit Setup**
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Create a new "script" application
3. Get your client ID and secret

### **Step 3: Launch & Monitor**

```bash
# Start with test mode to verify configuration
python bot_voltage_fixed.py --test

# If everything works, start production mode
python bot_voltage_fixed.py
```

## 📊 Dashboard Integration

Want to monitor your bot's performance? BOT SHA-256 includes a built-in dashboard API!

### **Enable Dashboard API**
```bash
# Start the dashboard server
python analytics_dashboard.py
```

### **Access Your Dashboard**
- Local: `http://localhost:5000`
- Production: Configure reverse proxy to your domain

### **API Endpoints**
```
GET /api/stats          - Get bot statistics
GET /api/performance    - Get performance analytics
GET /api/regions        - Get regional targeting data
GET /api/health         - Health check
```

## 🎯 Advanced Features

### **Multi-Account Support**
Add multiple accounts for higher posting volume:

```env
# Second Twitter Account
TWITTER_API_KEY_2=your_second_twitter_key
TWITTER_API_SECRET_2=your_second_twitter_secret
# ... add all credentials with _2 suffix

# Second Reddit Account
REDDIT_CLIENT_ID_2=your_second_reddit_id
REDDIT_CLIENT_SECRET_2=your_second_reddit_secret
# ... add all credentials with _2 suffix
```

### **Custom Content Templates**
Modify `multilingual_templates.json` to customize your content:

```json
{
  "en": {
    "twitter": {
      "gpu_deals": [
        "Your custom template here with {variables}"
      ]
    }
  }
}
```

### **Regional Targeting**
The bot automatically targets optimal regions based on time:

- **US East Coast**: 1-8 PM EST
- **US West Coast**: 10 AM - 5 PM PST  
- **Europe**: 8 AM - 8 PM CET
- **India**: 9-11 AM & 6-10 PM IST
- **China**: 8-10 AM & 7-11 PM CST
- **Brazil**: 11 AM - 10 PM BRT

## 🛠️ Troubleshooting

### **Common Issues**

#### ❌ **Twitter Rate Limiting**
```
Error: 429 Too Many Requests
Solution: Wait 1 hour or add more Twitter accounts
```

#### ❌ **Reddit Flair Errors**
```
Error: Flair required
Solution: Bot automatically handles this with smart flair detection
```

#### ❌ **Telegram Connection Issues**
```
Error: Connection timeout
Solution: Check your bot token and internet connection
```

### **Debug Mode**
```bash
# Run with verbose logging
python bot_voltage_fixed.py --test
```

## 📈 Performance Optimization

### **Best Practices**
1. **Start with test mode** to verify configuration
2. **Monitor rate limits** across all platforms
3. **Use multiple accounts** for higher volume
4. **Check regional performance** in analytics
5. **Customize content** for your audience

### **Scaling Up**
- Add more social media accounts
- Implement custom content strategies
- Use the dashboard API for monitoring
- Deploy on cloud servers for 24/7 operation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Clone the repo
git clone https://github.com/Jabsama/BOT-SHA-256.git

# Install development dependencies
pip install -r requirements.txt

# Run tests
python bot_voltage_fixed.py --test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: Check our guides in the `/docs` folder
- 🐛 **Bug Reports**: [Create an issue](https://github.com/Jabsama/BOT-SHA-256/issues)
- 💡 **Feature Requests**: [Create an issue](https://github.com/Jabsama/BOT-SHA-256/issues)
- 💬 **Community**: Join our discussions

## 🌟 Star History

If BOT SHA-256 helps you automate your social media, please give us a star! ⭐

---

**Made with ❤️ by the open source community**

*BOT SHA-256 - Intelligent Social Media Automation for Everyone*
