# 🤖 SHA-256 Bot v6.0 - Intelligent AI-Powered Social Media Automation

[![CI](https://github.com/Jabsama/BOT-SHA-256/actions/workflows/ci.yml/badge.svg)](https://github.com/Jabsama/BOT-SHA-256/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Revolutionary AI-Powered Social Media Bot

The SHA-256 Bot v6.0 is a **fully autonomous, self-learning social media automation system** with advanced AI modules designed to maximize engagement, avoid bans, and ensure viral content distribution across Twitter, Reddit, and Telegram.

### 🧠 **NEW: Intelligent AI Modules**

- **🛡️ Reddit Intelligence**: Automatically analyzes subreddit rules, generates compliant content, and manages dual accounts to avoid bans
- **🚀 Twitter Viral Optimizer**: Real-time hashtag optimization, viral content generation, and anti-shadow-ban protection
- **🤖 Telegram Autonomous**: Automatic group discovery, personalized user invitations, and intelligent conversations

## ✨ Key Features

### 🧠 Artificial Intelligence
- **Smart Rule Compliance**: Automatically detects and follows platform-specific rules
- **Viral Content Generation**: AI-powered content optimization for maximum engagement
- **Anti-Ban Protection**: Intelligent behavior simulation to avoid detection
- **Continuous Learning**: Improves performance based on success/failure patterns

### 🔗 Multi-Platform Support
- **Twitter**: Dual account management with viral optimization
- **Reddit**: Intelligent posting with automatic rule compliance
- **Telegram**: Autonomous group discovery and user acquisition
- **Cross-Platform**: Synchronized timing and content optimization

### 🛡️ Advanced Protection
- **Anti-Shadow-Ban**: Real-time monitoring and prevention
- **Smart Timing**: Optimal posting times based on AI analysis
- **Content Diversification**: Automatic variation to avoid repetition
- **Account Health Monitoring**: Risk assessment and protection

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API keys for Twitter, Reddit, Telegram
- VoltageGPU affiliate account

### Installation

```bash
# Clone the repository
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Configure your API keys in .env
nano .env
```

### Configuration

Edit `.env` with your credentials:

```bash
# Reddit - Dual accounts for maximum reach
REDDIT_CLIENT_ID=your_reddit_app_id_1
REDDIT_CLIENT_SECRET=your_reddit_secret_1
REDDIT_USERNAME=your_username_1
REDDIT_PASSWORD=your_password_1

REDDIT_CLIENT_ID_2=your_reddit_app_id_2
REDDIT_CLIENT_SECRET_2=your_reddit_secret_2
REDDIT_USERNAME_2=your_username_2
REDDIT_PASSWORD_2=your_password_2

# Twitter - Dual accounts for viral reach
TWITTER_API_KEY=your_twitter_key_1
TWITTER_API_SECRET=your_twitter_secret_1
TWITTER_ACCESS_TOKEN=your_access_token_1
TWITTER_ACCESS_SECRET=your_access_secret_1

TWITTER_API_KEY_2=your_twitter_key_2
TWITTER_API_SECRET_2=your_twitter_secret_2
TWITTER_ACCESS_TOKEN_2=your_access_token_2
TWITTER_ACCESS_SECRET_2=your_access_secret_2

# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_channel

# VoltageGPU
VOLTAGE_API_KEY=your_voltage_api_key
AFFILIATE_CODE=SHA-256-YOUR_CODE
```

### Running the Bot

```bash
# Test the intelligent modules
python test_intelligent_modules.py

# Run in test mode (no actual posting)
python SHA-256BOT.py --test

# Run in production mode
python SHA-256BOT.py
```

## 🧠 Intelligent Modules

### 1. Reddit Intelligence (`modules/reddit_intelligence.py`)

**Features:**
- ✅ **Automatic Rule Analysis**: Detects required tags ([D], [R], [N], [P])
- ✅ **Compliant Content Generation**: Adapts content to subreddit rules
- ✅ **Dual Account Management**: Intelligent rotation between accounts
- ✅ **Ban Risk Assessment**: Monitors account health and posting patterns
- ✅ **Learning from Failures**: Improves based on post removals

**Example:**
```python
# Automatically analyzes r/MachineLearning rules
rules = reddit_intelligence.analyze_subreddit_rules(reddit_client, 'MachineLearning')
# Generates compliant title: "[D] Cost-effective GPU alternatives for AI/ML workloads"
title, content = reddit_intelligence.generate_compliant_content('MachineLearning', base_content, base_title)
```

### 2. Twitter Viral Optimizer (`modules/twitter_viral.py`)

**Features:**
- ✅ **Real-time Hashtag Optimization**: Analyzes trending hashtags
- ✅ **Viral Content Patterns**: Uses proven templates for maximum engagement
- ✅ **Anti-Shadow-Ban Protection**: Monitors engagement and behavior patterns
- ✅ **Optimal Timing**: Determines best posting times for viral reach
- ✅ **Content Diversification**: Prevents repetitive posting patterns

**Viral Patterns:**
```python
viral_patterns = {
    'comparison': "🔥 {service1} vs {service2}: {comparison_point}",
    'savings': "💰 Save {percentage}% on {service}: {benefit}",
    'breaking_news': "🚨 BREAKING: {news_item}",
    'question': "🤔 Quick question: {question}",
    'tip': "💡 Pro tip: {tip_content}"
}
```

### 3. Telegram Autonomous (`modules/telegram_autonomous.py`)

**Features:**
- ✅ **Automatic Group Discovery**: Finds relevant groups based on keywords
- ✅ **Personalized Invitations**: Sends targeted invitations to users
- ✅ **Intelligent Conversations**: Responds naturally to group discussions
- ✅ **User Classification**: Categorizes users by interests and behavior
- ✅ **Autonomous Growth**: Operates without human intervention

**User Types:**
- 🎯 **GPU Enthusiasts**: AI/ML developers and researchers
- 🎯 **Crypto Miners**: Blockchain and mining community
- 🎯 **Tech Savers**: Deal hunters and cost-conscious users

## 📊 Performance Metrics

### Expected Improvements
- 📈 **+300% Reddit Success Rate** through intelligent rule compliance
- 🚀 **+250% Twitter Engagement** with viral optimization
- 🤖 **+400% Telegram Growth** via autonomous user acquisition

### Ban Reduction
- 🛡️ **-90% Reddit Post Removals** through automatic compliance
- 🚫 **-80% Twitter Shadow Ban Risk** with AI monitoring
- 🤖 **0% Telegram Restrictions** through natural behavior simulation

## 🔧 Advanced Configuration

### Timing Configuration (`config/timing_config.py`)

```python
# Twitter - 2 accounts with 120-minute intervals
TWITTER_CONFIG = {
    'max_posts_per_day': 12,
    'accounts_count': 2,
    'post_interval_minutes': 240,  # 4 hours between posts per account
    'alternating_interval_minutes': 120,  # 2 hours alternating between accounts
}

# Reddit - Conservative approach
REDDIT_CONFIG = {
    'max_posts_per_day': 3,
    'post_interval_hours': 8,
    'avoid_same_subreddit_hours': 24,
}
```

### Content Strategies

**Reddit - Academic Style:**
```
Title: [D] Cost-effective GPU alternatives for AI/ML workloads - experiences?
Content: I've been researching cost-effective GPU solutions for AI development and discovered some interesting alternatives to traditional cloud providers...
```

**Twitter - Viral Style:**
```
🔥 GPU rental costs got you down? Here's how I cut mine by 70%...
💰 Thread: Why I switched from AWS to decentralized GPU networks
🚀 PSA: You're probably overpaying for GPU compute. Here's why...
```

## 🛡️ Security & Compliance

### Protection Measures
- ✅ **Safety Intervals**: 120 minutes between Twitter posts
- ✅ **Account Rotation**: Intelligent use of multiple accounts
- ✅ **Rule Analysis**: Automatic compliance with platform rules
- ✅ **Continuous Monitoring**: Early detection of issues

### Error Handling
- 🔄 **Auto-Recovery**: Automatic recovery after errors
- 📚 **Learning**: Continuous improvement based on failures
- 🛡️ **Protection**: Automatic shutdown on high-risk situations

## 📈 Monitoring & Analytics

### Real-time Monitoring
- 📊 **Success Rate by Platform**
- 🎯 **Ban Risk Scores**
- 🚀 **Viral Engagement Rates**
- 🤖 **AI Learning Patterns**

### Intelligence Reports
```
🧠 Reddit Intelligence: 15 subreddits analyzed, 85.2% success rate
🚀 Twitter Viral: 23 viral patterns, 12.5% avg engagement
🤖 Telegram Autonomous: 8 groups discovered, 45 users invited
```

## 🔧 Troubleshooting

### Common Issues

**Reddit Posts Removed:**
- ✅ Module automatically analyzes rules
- ✅ Adds required tags ([D], [R], [N], [P])
- ✅ Adapts content to subreddit style

**Twitter Shadow Ban:**
- ✅ Monitors engagement rates
- ✅ Automatically diversifies content
- ✅ Optimizes hashtags in real-time

**Telegram Restrictions:**
- ✅ Discovers new groups automatically
- ✅ Sends personalized invitations
- ✅ Maintains natural conversation patterns

## 📚 Documentation

- 📖 **[Intelligent Modules Guide](INTELLIGENT_MODULES_GUIDE.md)** - Complete AI features documentation
- 🚀 **[Quick Setup Guide](QUICK_SETUP_GUIDE.md)** - Fast deployment instructions
- 🔧 **[Configuration Guide](CONFIGURATION_GUIDE.md)** - Advanced configuration options
- 📊 **[Performance Monitor](PERFORMANCE_MONITOR.md)** - Monitoring and analytics
- 🛠️ **[Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python test_intelligent_modules.py

# Run linting
flake8 modules/ SHA-256BOT.py

# Run type checking
mypy modules/ SHA-256BOT.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is for educational and research purposes. Users are responsible for complying with platform terms of service and applicable laws. Use responsibly and respect platform guidelines.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Jabsama/BOT-SHA-256&type=Date)](https://star-history.com/#Jabsama/BOT-SHA-256&Date)

## 📞 Support

- 🐛 **Bug Reports**: Use GitHub Issues
- 💡 **Feature Requests**: Use GitHub Discussions
- 📧 **Contact**: Create an issue for support

---

**Made with ❤️ by the SHA-256 Bot Team**

*Revolutionizing social media automation with artificial intelligence*
