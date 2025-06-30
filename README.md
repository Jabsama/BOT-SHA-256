# 🚀 SHA-256 Bot - Autonomous Social Media Marketing Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

An advanced, fully autonomous social media marketing bot with AI-powered content generation, intelligent rate limiting, and multi-platform support for Twitter, Telegram, and Reddit.

## ✨ Features

### 🤖 **Autonomous Operation**
- **Self-Learning AI**: Adapts posting strategies based on performance data
- **Intelligent Rate Limiting**: Respects platform limits to avoid bans
- **Multi-Platform Support**: Twitter, Telegram, Reddit with unified management
- **Regional Targeting**: Automatic timezone optimization for global reach

### 🧠 **AI-Powered Content**
- **Dynamic Content Generation**: Creates unique posts for each platform
- **Hashtag Optimization**: Intelligent hashtag rotation and diversification
- **A/B Testing**: Automatic content variant testing and optimization
- **Performance Tracking**: Real-time analytics and learning from engagement

### 🔧 **Advanced Features**
- **Twitter Follow/Unfollow**: Intelligent audience growth management
- **Telegram Invitations**: Automated group invitation system
- **Reddit Intelligence**: Rule-compliant posting with subreddit analysis
- **Enterprise Content**: Professional content for business targeting

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- API keys for desired platforms (Twitter, Telegram, Reddit)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/SHA-256-Bot.git
cd SHA-256-Bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. **Run the bot**
```bash
python SHA-256BOT.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```env
# Affiliate Configuration
AFFILIATE_CODE=your-affiliate-code

# Twitter API (Optional)
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret
TWITTER_BEARER_TOKEN=your-bearer-token

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHANNEL_ID=@your-channel

# Reddit API (Optional)
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
REDDIT_USERNAME=your-reddit-username
REDDIT_PASSWORD=your-reddit-password

# VoltageGPU API (Optional)
VOLTAGE_API_KEY=your-voltage-api-key
```

### Rate Limiting Configuration

The bot includes intelligent rate limiting to prevent API violations:

- **Twitter**: 3 posts/hour, 20 posts/day, 20-minute intervals
- **Telegram**: 2 posts/hour, 15 posts/day, 30-minute intervals
- **Reddit**: 1 post/hour, 5 posts/day, 60-minute intervals

## 🏗️ Architecture

### Core Components

- **`SHA-256BOT.py`**: Main bot orchestrator
- **`modules/unified_engine.py`**: Centralized engine with unified configuration
- **`modules/autonomous_performance.py`**: AI performance tracking and optimization
- **`modules/twitter_follow_manager.py`**: Twitter audience growth management
- **`modules/reddit_intelligence.py`**: Reddit rule compliance and optimization

### Module Structure

```
modules/
├── unified_engine.py          # Centralized bot engine
├── autonomous_performance.py  # Performance tracking & AI learning
├── autonomous_discovery.py    # Group/community discovery
├── twitter_follow_manager.py  # Twitter growth automation
├── reddit_intelligence.py     # Reddit compliance system
├── telegram_autonomous.py     # Telegram automation
├── predictive_ai.py          # AI predictions and optimization
├── ab_testing.py             # A/B testing framework
└── enterprise_content.py     # Business content generation
```

## 🎯 Usage Examples

### Basic Usage
```bash
# Run in normal mode
python SHA-256BOT.py

# Run in test mode (no actual posting)
python SHA-256BOT.py --test
```

### Advanced Configuration

The bot automatically:
- Switches between global regions every 4 hours
- Generates diverse hashtags to avoid repetition
- Learns from post performance and adapts strategy
- Manages Twitter follows/unfollows for organic growth
- Invites relevant users to Telegram groups

## 📊 Performance Monitoring

The bot includes comprehensive analytics:

- **Real-time Performance**: Success rates, engagement metrics
- **AI Learning**: Autonomous strategy optimization
- **Platform Health**: Rate limit status, error tracking
- **Content Analytics**: Hashtag performance, A/B test results

## 🛡️ Safety Features

### Anti-Ban Protection
- **Conservative Rate Limits**: Well below platform maximums
- **Intelligent Timing**: Respects platform-specific optimal posting times
- **Content Variation**: Avoids repetitive patterns that trigger spam detection
- **Error Recovery**: Automatic handling of temporary failures

### Privacy & Security
- **No Data Collection**: All data stored locally
- **Secure API Handling**: Encrypted credential storage
- **Open Source**: Full transparency of operations

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run in test mode
python SHA-256BOT.py --test
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is for educational and legitimate marketing purposes only. Users are responsible for:
- Complying with platform Terms of Service
- Respecting rate limits and community guidelines
- Using appropriate content and targeting
- Following applicable laws and regulations

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/SHA-256-Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/SHA-256-Bot/discussions)
- **Documentation**: This README and inline code comments

## 🔄 Updates

The bot includes automatic optimization and learning capabilities. Regular updates include:
- Performance improvements
- New platform integrations
- Enhanced AI algorithms
- Security updates

---

**Made with ❤️ for the open source community**

*Star ⭐ this repository if you find it useful!*
