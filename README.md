# 🤖 VoltageGPU Bot - Automated Multi-Platform Marketing

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/Jabsama/BOT-SHA-256/workflows/CI/badge.svg)](https://github.com/Jabsama/BOT-SHA-256/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![Platforms](https://img.shields.io/badge/Platforms-Twitter%20%7C%20Telegram%20%7C%20Reddit-orange.svg)](#platforms)
[![Stars](https://img.shields.io/github/stars/Jabsama/BOT-SHA-256.svg)](https://github.com/Jabsama/BOT-SHA-256/stargazers)
[![Forks](https://img.shields.io/github/forks/Jabsama/BOT-SHA-256.svg)](https://github.com/Jabsama/BOT-SHA-256/network)

> **Automated marketing bot for VoltageGPU affiliate program with SHA-256 referral codes**

Transform your social media presence into a passive income stream! This intelligent bot automatically promotes VoltageGPU's 70% cheaper GPU rentals across multiple platforms while earning you affiliate commissions.

## 🚀 Quick Start (5 Minutes Setup)

### 1. Clone & Install
```bash
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256
pip install -r requirements.txt
```

### 2. Configure Your Bot
```bash
cp .env.example .env
# Edit .env with your API keys (see setup guide below)
```

### 3. Test & Launch
```bash
# Test your configuration
python final_optimized_bot.py --test

# Launch in production
python final_optimized_bot.py
```

## 💰 What This Bot Does

### 📊 **Daily Performance**
- **43-59 posts per day** across all platforms (MAXIMUM MODE)
- **1290-1810 posts per month** with intelligent scheduling
- **500+ affiliate clicks monthly** potential

### 🎯 **Smart Content Strategy**
- **Twitter**: Alternates GPU deals ↔ Affiliate promotions
- **Telegram**: 80% affiliate focus (mobile users love easy money)
- **Reddit**: 90% technical analysis (developers want details)

### 🌍 **Multi-Language Support**
- **70% English** (primary market)
- **30% Chinese** (high-value Asian market)
- Culturally adapted content for each audience

## 🛠️ Platform Setup Guides

### 🐦 Twitter Setup (Required)

1. **Create Twitter Developer Account**
   - Go to [developer.twitter.com](https://developer.twitter.com)
   - Apply for developer access
   - Create a new app

2. **Get Your API Keys**
   ```
   API Key: your_api_key_here
   API Secret: your_api_secret_here
   Bearer Token: your_bearer_token_here
   Access Token: your_access_token_here
   Access Token Secret: your_access_token_secret_here
   ```

3. **Configure App Permissions**
   - Set to "Read and Write"
   - App type: "Web App, Automated App or Bot"

### 📱 Telegram Setup (Optional but Recommended)

1. **Create Telegram Bot**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot`
   - Choose name: "YourName VoltageGPU Bot"
   - Get your bot token

2. **Create Public Channel**
   - Create a public channel for your posts
   - Add your bot as administrator
   - Get channel username (e.g., @your_channel)

### 🔴 Reddit Setup (Optional)

1. **Create Reddit App**
   - Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
   - Create "script" application
   - Get client ID and secret

2. **Use Your Reddit Account**
   - Username and password of your Reddit account
   - Bot will post using your account

## ⚙️ Configuration (.env file)

Create your `.env` file with these settings:

```bash
# VoltageGPU API (Required)
VOLTAGE_API_KEY=your_voltagegpu_api_key

# Twitter (Required)
TWITTER_ENABLED=true
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret

# Telegram (Optional - High ROI)
TELEGRAM_ENABLED=false
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_channel_name

# Reddit (Optional - Tech Audience)
REDDIT_ENABLED=false
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password

# Your Affiliate Code (Required)
AFFILIATE_CODE=SHA-256-YOUR_UNIQUE_CODE
```

## 📅 Posting Schedule

### ⏰ **MAXIMUM Posting Schedule**
- **Twitter**: 16 posts/day (every 90 minutes)
- **Telegram**: 24 posts/day (every hour)
- **Reddit**: 3 posts/day (8h, 14h, 20h UTC)

### 🎯 **Content Strategy**
```
📊 DAILY BREAKDOWN (MAXIMUM MODE):
├── Twitter: 16 posts (alternating GPU deals/affiliate)
├── Telegram: 24 posts (80% affiliate, 20% GPU deals)
└── Reddit: 3 posts (rotating 6 subreddits)

🎯 DAILY TOTAL: 43 posts/day = 1290 posts/month
🚀 EXPLOSIVE MODE: 59 posts/day = 1810 posts/month
```

## 🎨 Content Examples

### Twitter
```
🚀 4x B200 @ $45.50/h – 70% cheaper than AWS!
Available in Raleigh 🌍
Perfect for AI training & development
🔗 https://voltagegpu.com/?ref=SHA-256-YOUR_CODE
#AI #CloudGPU #MachineLearning
```

### Telegram
```
💰 EASY MONEY WITH GPU REFERRALS! 💰

🚀 VoltageGPU = 70% cheaper than AWS
💎 Your SHA-256 code = Your ATM machine
📱 Share once, earn forever!

✅ 5% commission on EVERY rental
🔗 Start earning: https://voltagegpu.com/?ref=SHA-256-YOUR_CODE
```

### Reddit
```
**VoltageGPU vs AWS: Real Cost Analysis**

Configuration: 4x B200
VoltageGPU: $45.50/hour
AWS P5 equivalent: ~$120+/hour
Your savings: 70%+ cost reduction

Bonus: Use code SHA-256-YOUR_CODE for additional 5% off
Link: https://voltagegpu.com/?ref=SHA-256-YOUR_CODE

Anyone else tired of AWS pricing?
```

## 🔧 Advanced Features

### 🧠 **Intelligent Rotation**
- **Reddit**: Automatically rotates between 6 optimized subreddits
- **Languages**: Smart distribution (70% EN, 30% ZH)
- **Content Types**: Platform-specific strategies

### 📊 **Built-in Analytics**
- Post tracking and statistics
- Error logging and monitoring
- Performance metrics

### 🛡️ **Safety Features**
- Rate limiting to avoid platform restrictions
- Fallback data when API is unavailable
- Automatic error recovery

## 🚀 Running Your Bot

### 🧪 **Test Mode**
```bash
python final_optimized_bot.py --test
```
This shows you what content will be posted without actually posting.

### 🔴 **Production Mode**
```bash
python final_optimized_bot.py
```
Starts the bot with scheduled posting.

### 📊 **Monitor Performance**
```bash
tail -f logs.txt
```
Watch your bot's activity in real-time.

## 💡 Pro Tips

### 🎯 **Maximize Earnings**
1. **Start with Twitter + Telegram** (highest ROI)
2. **Share your affiliate code** in relevant communities
3. **Monitor logs** to optimize posting times
4. **Add Reddit** once comfortable with the bot

### 🔧 **Troubleshooting**
- **Twitter 403 errors**: Check app permissions in Developer Portal
- **Telegram not posting**: Verify bot is admin of your channel
- **Reddit issues**: Ensure account has enough karma

### 📈 **Scaling Up**
- **Multiple accounts**: Run separate instances
- **More platforms**: Easy to add Discord, LinkedIn
- **Custom content**: Modify templates in `multilingual_templates.json`

## 📁 Project Structure

```
BOT-SHA-256/
├── final_optimized_bot.py      # Main bot (recommended)
├── multilingual_templates.json # Content templates
├── mock_data.json             # Fallback GPU data
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
├── .gitignore               # Security (hides sensitive files)
└── README.md               # This guide
```

## 🤝 Contributing

Found a bug or want to add a feature? 

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

- Use responsibly and follow platform terms of service
- This bot is for educational and legitimate affiliate marketing
- Monitor your bot's activity regularly
- Respect community guidelines on all platforms

## 🎉 Success Stories

> "Made $200+ in my first month just by running this bot and sharing my affiliate code with colleagues!" - Anonymous User

> "The Reddit integration is genius - posts look completely natural and get great engagement." - Tech Entrepreneur

---

**🚀 Ready to turn your social media into a money-making machine?**

**⭐ Star this repo if it helps you earn passive income!**

**💬 Questions? Open an issue or join our community discussions.**
