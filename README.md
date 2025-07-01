# 🚀 BOT SHA-256 - Autonomous AI-Powered Social Media Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/Jabsama/BOT-SHA-256.svg)](https://github.com/Jabsama/BOT-SHA-256/stargazers)

An advanced, fully autonomous AI-powered social media automation bot designed for VoltageGPU affiliate marketing. Features intelligent content generation, multi-platform posting, and advanced performance optimization.

## ✨ Features

### 🤖 Autonomous AI Engine
- **Self-Learning AI**: Adapts content based on performance metrics
- **Predictive Analytics**: Optimizes posting times and content types
- **A/B Testing**: Automatically tests different content variants
- **Performance Tracking**: Real-time analytics and optimization

### 📱 Multi-Platform Support
- **Twitter**: Dual account support with intelligent rate limiting
- **Telegram**: Channel and group posting with discovery
- **Reddit**: AI-powered rule compliance and subreddit targeting
- **Follow Management**: Automated Twitter growth strategies

### 🎯 Intelligent Content Generation
- **Ultimate Viral Content**: 25+ optimized templates for maximum engagement
- **Dynamic Variables**: Real-time GPU pricing and market data
- **Hashtag Optimization**: AI-powered hashtag selection
- **Platform Adaptation**: Content optimized for each platform

### 🌍 Global Targeting
- **Timezone Optimization**: Posts at optimal times for different regions
- **Multi-Language Support**: Content generation in multiple languages
- **Regional Adaptation**: Tailored content for different markets

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- API keys for your chosen platforms (Twitter, Telegram, Reddit)
- VoltageGPU affiliate account

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and affiliate code
```

4. **Run the bot**

**Option 1: Interactive Launcher (Recommended)**
```bash
python start_bot.py
```

**Option 2: Direct Bot Execution**
```bash
# Test mode (no actual posting)
python SHA-256BOT.py --test

# Production mode
python SHA-256BOT.py
```

## ⚙️ Configuration

### Essential Configuration

Edit your `.env` file with the following required settings:

```env
# Your VoltageGPU affiliate code
AFFILIATE_CODE=your_affiliate_code_here

# VoltageGPU API key
VOLTAGE_API_KEY=your_api_key_here

# Twitter API credentials
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

### Platform Setup

#### Twitter
1. Create a Twitter Developer account
2. Create a new app and generate API keys
3. Add keys to your `.env` file
4. Optional: Configure second account for higher volume

#### Telegram
1. Create a bot via @BotFather
2. Get your bot token
3. Create a channel and add the bot as admin
4. Add configuration to `.env`

#### Reddit
1. Create a Reddit app at reddit.com/prefs/apps
2. Get client ID and secret
3. Add credentials to `.env`

## 🎯 Usage

### Basic Usage

```bash
# Run in test mode (no actual posting)
python SHA-256BOT.py --test

# Run in production mode
python SHA-256BOT.py
```

### Advanced Usage

```bash
# Start with the interactive launcher
python start_bot.py
```

The interactive launcher provides options for:
- Test mode
- Configuration validation
- Performance monitoring
- Dashboard access

## 📊 Features Overview

### Content Generation
- **Viral Templates**: 25+ proven high-engagement templates
- **Dynamic Pricing**: Real-time GPU market data integration
- **Affiliate Integration**: Seamless affiliate link and code insertion
- **Platform Optimization**: Content adapted for each platform's requirements

### AI Optimization
- **Performance Learning**: Analyzes engagement metrics to improve content
- **Timing Optimization**: Posts at optimal times for maximum reach
- **Hashtag Intelligence**: AI-powered hashtag selection and optimization
- **A/B Testing**: Automatic testing of content variations

### Safety Features
- **Rate Limiting**: Intelligent rate limiting to avoid platform restrictions
- **Account Protection**: Advanced anti-ban measures
- **Error Recovery**: Automatic error handling and recovery
- **Compliance**: Platform rule compliance checking

## 🔧 Advanced Configuration

### Rate Limiting
```env
TWITTER_MAX_POSTS_PER_HOUR=15
TELEGRAM_MAX_POSTS_PER_HOUR=30
REDDIT_MAX_POSTS_PER_HOUR=10
```

### Regional Targeting
```env
DEFAULT_REGION=US_EAST
DEFAULT_LANGUAGE=en
```

### Performance Tracking
```env
TRACK_CONVERSIONS=true
TRACK_CLICKS=true
TRACK_ENGAGEMENT=true
```

## 📈 Performance Monitoring

The bot includes comprehensive analytics:
- **Engagement Metrics**: Likes, shares, comments, clicks
- **Conversion Tracking**: Affiliate link performance
- **Platform Analytics**: Performance by platform
- **Time-based Analysis**: Optimal posting times
- **Content Performance**: Best performing content types

## 🛡️ Security & Privacy

- **API Key Protection**: Secure storage of sensitive credentials
- **Rate Limit Compliance**: Respects platform rate limits
- **Error Handling**: Graceful handling of API errors
- **Logging**: Comprehensive logging for debugging
- **Data Privacy**: No personal data collection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is designed for legitimate affiliate marketing purposes. Users are responsible for:
- Complying with platform terms of service
- Following applicable laws and regulations
- Using the bot ethically and responsibly
- Respecting rate limits and platform guidelines

## 🆘 Support

- **Issues**: Report bugs via [GitHub Issues](https://github.com/Jabsama/BOT-SHA-256/issues)
- **Documentation**: Check the wiki for detailed guides
- **Community**: Join discussions in the repository

## 🔗 Links

- **VoltageGPU**: [https://voltagegpu.com](https://voltagegpu.com)
- **Repository**: [https://github.com/Jabsama/BOT-SHA-256](https://github.com/Jabsama/BOT-SHA-256)
- **License**: [MIT License](LICENSE)

---

**Made with ❤️ for the AI community**

*Automate your affiliate marketing with intelligence and efficiency*
