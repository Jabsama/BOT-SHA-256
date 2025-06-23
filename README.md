# 🤖 SHA-256 Bot - Fully Autonomous AI-Powered Social Media Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Autonomous AI](https://img.shields.io/badge/AI-Autonomous-green.svg)](https://github.com/Jabsama/BOT-SHA-256)
[![Multi-Platform](https://img.shields.io/badge/Platform-Twitter%20%7C%20Telegram%20%7C%20Reddit-orange.svg)](https://github.com/Jabsama/BOT-SHA-256)

> 🚀 **The world's first fully autonomous, self-learning affiliate marketing bot with AI-powered content optimization and automatic group discovery!**

## 🌟 What Makes This Bot Special?

This isn't just another social media bot - it's a **fully autonomous AI system** that:

- 🧠 **Learns from its own performance** and gets better over time
- 🔍 **Automatically discovers** new Telegram groups and Reddit communities
- 🌍 **Targets optimal regions** based on timezone analysis
- ⚡ **Optimizes content** in real-time based on engagement data
- 🎯 **Self-improves** without any manual intervention

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256
pip install -r requirements.txt
```

### 2. Configure Your Credentials
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Test Run (Recommended First!)
```bash
python SHA-256BOT.py --test
```

### 4. Go Live! 🎉
```bash
python SHA-256BOT.py
```

## 🤖 Autonomous Features

### 🧠 **AI-Powered Self-Learning**
- **Performance Analysis**: Tracks success rates, engagement, and conversions
- **Pattern Recognition**: Identifies what content works best for each platform
- **Automatic Optimization**: Adjusts posting strategy based on learned patterns
- **Continuous Improvement**: Gets smarter with every post

### 🔍 **Automatic Group Discovery**
- **Telegram Groups**: Finds relevant tech/AI/GPU groups automatically
- **Reddit Communities**: Discovers active subreddits in your niche
- **Smart Filtering**: Only targets groups with good engagement potential
- **Performance Tracking**: Remembers which groups perform best

### 🌍 **Global Timezone Optimization**
- **Peak Time Detection**: Posts when your target audience is most active
- **Multi-Region Support**: US, Europe, Asia, Australia, Brazil, India
- **Language Adaptation**: Automatically switches between English, Chinese, Portuguese, German
- **Smart Scheduling**: Maximizes reach by timing posts perfectly

### ⚡ **Real-Time Content Optimization**
- **A/B Testing**: Automatically tests different content styles
- **Engagement Analysis**: Learns what emojis, hashtags, and formats work best
- **Dynamic Adaptation**: Adjusts content based on platform-specific performance
- **Viral Optimization**: Focuses on content patterns that generate the most engagement

## 📁 Modular Architecture

The bot is built with a clean, modular architecture for easy maintenance and expansion:

```
SHA-256BOT/
├── SHA-256BOT.py                    # 🤖 Main autonomous bot
├── modules/
│   ├── autonomous_discovery.py      # 🔍 Auto group discovery
│   ├── autonomous_performance.py    # 📊 AI performance engine
│   ├── timing_manager.py           # ⏰ Timezone optimization
│   ├── content_manager.py          # 📝 Content generation
│   └── platform_manager.py         # 🔗 Connection management
├── config/
│   └── timing_config.py            # ⚙️ Timing configurations
└── logs/                           # 📋 Performance logs
```

## 🎯 Supported Platforms

### 🐦 **Twitter/X**
- ✅ Multiple account support
- ✅ Smart rate limiting
- ✅ Engagement tracking
- ✅ Hashtag optimization

### 💬 **Telegram**
- ✅ Auto group discovery
- ✅ Channel broadcasting
- ✅ Group performance analysis
- ✅ Anti-spam protection

### 📍 **Reddit**
- ✅ Subreddit discovery
- ✅ Community targeting
- ✅ Karma-based posting
- ✅ Engagement optimization

## 🌍 Global Reach

### 🗺️ **Supported Regions**
- 🇺🇸 **United States** (East, Central, West)
- 🇪🇺 **Europe** (UK, Germany, France)
- 🇨🇳 **China** (Beijing, Shanghai)
- 🇮🇳 **India** (Mumbai, Delhi)
- 🇧🇷 **Brazil** (São Paulo, Rio)
- 🇦🇺 **Australia** (Sydney, Melbourne)
- 🇯🇵 **Japan** (Tokyo, Osaka)

### 🌐 **Languages**
- 🇺🇸 **English** - Primary language
- 🇨🇳 **Chinese** - For Asian markets
- 🇧🇷 **Portuguese** - For Brazilian market
- 🇩🇪 **German** - For European market

## 📊 Performance Dashboard

The bot includes a real-time performance dashboard showing:

- 📈 **Success Rates** by platform and region
- 🎯 **Engagement Metrics** and conversion tracking
- 🧠 **AI Insights** and learned patterns
- 🔍 **Discovery Stats** for new groups/communities
- ⚡ **Optimization Recommendations**

## ⚙️ Configuration

### 🔑 **Required API Keys**

Create a `.env` file with your credentials:

```env
# Affiliate Configuration
AFFILIATE_CODE=your-sha-256-code

# Twitter/X API (v2)
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret
TWITTER_BEARER_TOKEN=your-bearer-token

# Optional: Second Twitter Account
TWITTER_API_KEY_2=your-second-twitter-key
# ... (same pattern for second account)

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHANNEL_ID=@your-channel

# Reddit API
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-secret
REDDIT_USERNAME=your-reddit-username
REDDIT_PASSWORD=your-reddit-password

# Optional: Second Reddit Account
REDDIT_CLIENT_ID_2=your-second-reddit-id
# ... (same pattern for second account)

# VoltageGPU API (Optional)
VOLTAGE_API_KEY=your-voltage-api-key
```

### 🎛️ **Advanced Settings**

The bot automatically optimizes these settings, but you can customize:

- **Discovery Intervals**: How often to search for new groups
- **Performance Thresholds**: When to consider content successful
- **Rate Limits**: Platform-specific posting limits
- **Content Templates**: Multilingual message templates

## 🚀 Advanced Usage

### 🧪 **Testing Mode**
Always test first to see how the bot performs:
```bash
python SHA-256BOT.py --test
```

### 📊 **Performance Analysis**
View detailed analytics:
```bash
python analytics_dashboard.py
```

### 🔧 **Custom Configuration**
Modify `config/timing_config.py` for custom timing rules.

## 🛡️ Safety Features

### 🔒 **Anti-Ban Protection**
- **Smart Rate Limiting**: Respects platform limits
- **Human-like Behavior**: Randomized timing and content
- **Error Recovery**: Automatic retry with backoff
- **Account Rotation**: Distributes load across multiple accounts

### 🎯 **Quality Control**
- **Content Uniqueness**: Never posts duplicate content
- **Engagement Filtering**: Only targets active communities
- **Performance Monitoring**: Stops posting to low-performing groups
- **Spam Prevention**: Built-in anti-spam mechanisms

## 📈 Performance Metrics

### 🎯 **What the Bot Tracks**
- **Success Rate**: Percentage of successful posts
- **Engagement Rate**: Likes, comments, shares per post
- **Reach Growth**: Audience expansion over time
- **Conversion Rate**: Click-through to affiliate links
- **Discovery Rate**: New groups/communities found

### 🧠 **AI Learning Indicators**
- **Pattern Recognition**: Content patterns that work best
- **Timing Optimization**: Optimal posting times per region
- **Platform Preferences**: Which platforms perform best
- **Audience Insights**: What resonates with your audience

## 🔧 Troubleshooting

### ❓ **Common Issues**

**Bot not posting?**
- ✅ Check API credentials in `.env`
- ✅ Verify rate limits haven't been exceeded
- ✅ Run in test mode first: `python SHA-256BOT.py --test`

**Low engagement?**
- ✅ Let the AI learn (give it 24-48 hours)
- ✅ Check if targeting the right regions
- ✅ Review discovered groups quality

**Discovery not working?**
- ✅ Ensure Telegram bot has proper permissions
- ✅ Check Reddit account karma and age
- ✅ Verify API rate limits

### 📋 **Logs and Debugging**
- Check `logs/sha256bot_autonomous.log` for detailed logs
- Use `--test` mode to debug without posting
- Monitor `autonomous_performance.db` for AI learning data

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch
3. ✨ **Add** your improvements
4. 🧪 **Test** thoroughly
5. 📤 **Submit** a pull request

### 🎯 **Areas for Contribution**
- 🌐 **New Platforms**: Discord, LinkedIn, TikTok
- 🗣️ **Languages**: Add more language support
- 🧠 **AI Features**: Enhanced learning algorithms
- 📊 **Analytics**: Better performance tracking
- 🎨 **UI/UX**: Web dashboard improvements

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is for educational and legitimate affiliate marketing purposes only. Users are responsible for:

- ✅ Complying with platform terms of service
- ✅ Following local laws and regulations
- ✅ Using ethical marketing practices
- ✅ Respecting community guidelines

## 🌟 Star History

If this bot helps you succeed with affiliate marketing, please give it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=Jabsama/BOT-SHA-256&type=Date)](https://star-history.com/#Jabsama/BOT-SHA-256&Date)

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/Jabsama/BOT-SHA-256/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/Jabsama/BOT-SHA-256/discussions)
- 📧 **Contact**: Create an issue for support

---

<div align="center">

**🚀 Ready to revolutionize your affiliate marketing with AI? Let's go!**

[⭐ Star this repo](https://github.com/Jabsama/BOT-SHA-256) • [🍴 Fork it](https://github.com/Jabsama/BOT-SHA-256/fork) • [📢 Share it](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20autonomous%20AI%20bot%20for%20affiliate%20marketing!&url=https://github.com/Jabsama/BOT-SHA-256)

</div>
