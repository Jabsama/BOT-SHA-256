# 🚀 VoltageGPU Bot - Unified Launcher

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/Platforms-Twitter%20%7C%20Telegram%20%7C%20Reddit-orange.svg)](#platforms)

> **Automated marketing bot for VoltageGPU with unified launcher - Twitter + Telegram + Reddit**

One simple script to launch all bots! Automatically promotes VoltageGPU's 70% cheaper GPU rentals across multiple platforms while earning you affiliate commissions.

## ⚡ Quick Start (2 Minutes Setup)

1. **Clone & Install**
```bash
git clone https://github.com/your-username/voltagegpu-bot.git
cd voltagegpu-bot
pip install -r requirements.txt
```

2. **Configure .env**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Launch**
```bash
# Test mode (no real posts)
python launch_bot.py --test

# Production mode (real posts)
python launch_bot.py
```

## 📊 Performance

- **🐦 Twitter**: 40 posts/day (2 accounts × 20 posts)
- **💬 Telegram**: 30 posts/day
- **📍 Reddit**: 20+ posts/day (9 targeted subreddits)
- **📈 Total**: 90+ automated posts/day

## 🔧 Configuration

### 1. VoltageGPU API (Required)
```env
VOLTAGE_API_KEY=your_api_key
AFFILIATE_CODE=your_affiliate_code
```

### 2. Twitter (Optional - 2 accounts max)
```env
# Account 1
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# Account 2 (optional)
TWITTER_API_KEY_2=your_api_key_2
TWITTER_API_SECRET_2=your_api_secret_2
TWITTER_BEARER_TOKEN_2=your_bearer_token_2
TWITTER_ACCESS_TOKEN_2=your_access_token_2
TWITTER_ACCESS_SECRET_2=your_access_secret_2
```

### 3. Telegram (Optional but Recommended)
```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@your_public_channel
```

**⚠️ Important:** Create a **PUBLIC channel** with subscribers, not a private group! 
- Public channels can be found by anyone
- Share your channel link to build audience
- Example: @VoltageGPUDeals, @CheapGPURentals, @AITrainingDeals

**🤖 Autonomous Telegram Strategies:**
1. **Join existing tech groups** and share your bot's content manually
2. **Create themed channel** (@YourNameGPUDeals) and promote it
3. **Cross-promote** on Twitter/Reddit to build Telegram audience
4. **Partner with influencers** to share your channel
5. **Use bot for personal messaging** to friends/colleagues interested in GPU deals

### 4. Reddit (Optional - 2 accounts max)
```env
# Account 1
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password

# Account 2 (optional)
REDDIT_CLIENT_ID_2=your_client_id_2
REDDIT_CLIENT_SECRET_2=your_client_secret_2
REDDIT_USERNAME_2=your_username_2
REDDIT_PASSWORD_2=your_password_2
```

## 🎯 Targeted Subreddits

| Subreddit | Posts/day | Audience | Priority |
|-----------|-----------|----------|----------|
| r/GPURental | 8 | 12k | 🔥 Max |
| r/MachineLearning | 2 | 3.6M | 🔥 High |
| r/DeepLearning | 2 | 1.1M | 🔥 High |
| r/LocalLLaMA | 2 | 400k | 🔥 High |
| r/artificial | 2 | 1.8M | 🔥 High |
| r/developersIndia | 2 | 200k | 🔥 High |
| r/indiandevs | 2 | 50k | 🔥 Med |
| r/programacao | 2 | 80k | 🔥 High |
| r/vastai | 2 | 42k | 🔥 Med |

## 📱 Real-Time Dashboard

```
🚀 VOLTAGEGPU BOT - UNIFIED LAUNCHER
⏰ 14:32:15 | Uptime: 2:15:30

📊 POSTS TODAY:
   🐦 Twitter: 25
   💬 Telegram: 18
   📍 Reddit: 12
   📈 TOTAL: 55

⏰ NEXT POSTS:
   🐦 Twitter1: 15min (12/20)
   🐦 Twitter2: 45min (13/20)
   💬 Telegram: 23min (18/30)
   📍 Reddit: 08min

📍 TOP SUBREDDITS:
   r/GPURental: 4 posts
   r/MachineLearning: 2 posts
   r/LocalLLaMA: 2 posts

💰 CODE: SHA-256-76360B81D39F
🛑 Ctrl+C to stop
```

## 🔑 Getting API Keys

### Twitter
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Create an app
3. Generate API keys

### Telegram
1. Message [@BotFather](https://t.me/botfather)
2. Create bot with `/newbot`
3. Get the token

### Reddit
1. Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
2. Create "script" app
3. Note client_id and client_secret

### VoltageGPU
1. Sign up at [voltagegpu.com](https://voltagegpu.com)
2. Get API key from settings
3. Generate affiliate code

## 🛠️ Features

### ✅ Automatic Timer
- **Twitter**: Posts every 90 minutes per account
- **Telegram**: Posts every hour
- **Reddit**: Posts every 30 minutes

### ✅ Multi-Account Support
- Automatic support for 2 Twitter accounts
- Automatic support for 2 Reddit accounts
- Intelligent post distribution

### ✅ Built-in Templates
- GPU deals and affiliate templates
- Platform-adapted content
- Automatic variables (price, GPU, etc.)

### ✅ VoltageGPU API Integration
- Automatic offer retrieval
- Fallback to mock offers
- Affiliate code in every post

### ✅ Smart Management
- Reddit ban detection
- Daily limits respected
- Automatic midnight reset
- Detailed logging

## 📋 Commands

```bash
# Test without posting
python launch_bot.py --test

# Normal launch
python launch_bot.py

# View logs
tail -f voltagegpu_bot.log
```

## 🚨 Safety Limits

- **Twitter**: 20 posts/day per account (API limit)
- **Telegram**: 30 posts/day (bot limit)
- **Reddit**: 2-8 posts/day per subreddit (community guidelines)

## 🎨 Content Examples

### Twitter
```
🚨 INSANE GPU DEAL! 🚨

💻 8x H200 for $42.08/hour
⚡ 70% cheaper than AWS
🌍 Raleigh | 97.8% uptime

💰 Code SHA-256-76360B81D39F = 5% OFF!
🔗 https://voltagegpu.com/?ref=SHA-256-76360B81D39F

#GPUDeals #AI
```

### Telegram
```
💰 EASY MONEY WITH GPU REFERRALS! 💰

🚀 70% cheaper than AWS
💎 Your code = Your ATM
📱 Share once, earn forever!

✅ 5% commission
✅ 5% discount for users

🔗 https://voltagegpu.com/?ref=SHA-256-76360B81D39F

💬 What's your biggest AI challenge?
```

### Reddit
```
🔬 **VoltageGPU vs AWS: Real Cost Analysis**

**Config:** 8x H200
**Price:** $42.08/hour vs $120+/hour AWS
**Savings:** 70%+ cost reduction
**Location:** Raleigh | **Uptime:** 97.8%

**Bonus:** Code `SHA-256-76360B81D39F` for 5% off
**Link:** https://voltagegpu.com/?ref=SHA-256-76360B81D39F

Anyone else tired of AWS pricing?
```

## 🔧 Advanced Features

### 🧠 Smart Rotation
- **Reddit**: Automatically rotates between 9 optimized subreddits
- **Content**: Platform-specific strategies
- **Timing**: Optimal posting schedules

### 📊 Built-in Analytics
- Real-time post tracking
- Error logging and monitoring
- Performance metrics

### 🛡️ Safety Features
- Rate limiting to avoid restrictions
- Fallback data when API unavailable
- Automatic error recovery
- Ban detection and avoidance

## 💡 Pro Tips

### 🎯 Maximize Earnings
1. **Start with all platforms** for maximum reach
2. **Share your affiliate code** in relevant communities
3. **Monitor dashboard** to optimize performance
4. **Let it run 24/7** for consistent results

### 🔧 Troubleshooting
- **Twitter 403 errors**: Check app permissions
- **Telegram not posting**: Verify bot is channel admin
- **Reddit issues**: Ensure account has enough karma
- **API errors**: Check your VoltageGPU API key

### 📈 Scaling Up
- **Multiple instances**: Run on different servers
- **More accounts**: Add more Twitter/Reddit accounts
- **Custom content**: Modify templates as needed

## 📁 Project Structure

```
voltagegpu-bot/
├── launch_bot.py                # 🚀 Main unified launcher
├── multilingual_templates.json  # Content templates
├── requirements.txt             # Python dependencies
├── .env.example                # Configuration template
├── .gitignore                  # Security
└── README.md                   # This guide
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

- Use responsibly and follow platform terms of service
- Monitor your bot's activity regularly
- Respect community guidelines on all platforms

## 🎉 Success Stories

> "Made $200+ in my first month just by running this bot!" - Anonymous User

> "The unified launcher makes it so easy - one command and everything works!" - Developer

---

**🚀 Ready to automate your VoltageGPU promotion?**

**⭐ Star this repo if it helps you!**

**💬 Questions? Open an issue!**
