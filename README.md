# 🚀 SHA-256 Bot - Autonomous Social Media Marketing Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/Jabsama/BOT-SHA-256)

> 🤖 **The smartest autonomous social media bot that learns, adapts, and grows your audience across Twitter, Telegram, and Reddit!**

## ✨ What Makes This Bot Special?

🧠 **AI-Powered Intelligence** - Learns from every post and optimizes automatically  
⚡ **Multi-Platform Magic** - Manages Twitter, Telegram, and Reddit simultaneously  
🛡️ **Ban-Proof Design** - Smart rate limiting keeps your accounts safe  
🌍 **Global Reach** - Automatically targets optimal timezones worldwide  
📈 **Growth Automation** - Intelligent follow/unfollow and community building  

---

## 🎯 Quick Setup Guide

### Choose Your Operating System:
- 🪟 [**Windows Setup**](#-step-1-windows-setup)
- 🐧 [**Linux Setup**](#-step-1-linux-setup)  
- 🍎 [**macOS Setup**](#-step-1-macos-setup)

---

## 🪟 Windows Setup

### 📦 Step 1: Install Requirements

#### 1.1 Install Python
```powershell
# Download Python 3.8+ from python.org
# ✅ Make sure to check "Add Python to PATH" during installation
python --version
```

#### 1.2 Install Git
```powershell
# Download Git from git-scm.com
# ✅ Use default settings during installation
git --version
```

#### 1.3 Clone the Repository
```powershell
# Open PowerShell or Command Prompt
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256
```

### ⚙️ Step 2: Configure Environment

#### 2.1 Install Dependencies
```powershell
# Install required Python packages
pip install -r requirements.txt
```

#### 2.2 Create Configuration File
```powershell
# Copy the example configuration
copy .env.example .env
# Open .env with Notepad
notepad .env
```

#### 2.3 Add Your API Keys
```env
# Edit .env file with your credentials:
AFFILIATE_CODE=your-affiliate-code
TWITTER_API_KEY=your-twitter-key
TELEGRAM_BOT_TOKEN=your-telegram-token
REDDIT_CLIENT_ID=your-reddit-id
```

### 🚀 Step 3: Launch the Bot

#### 3.1 Test Configuration
```powershell
# Run in test mode first
python SHA-256BOT.py --test
```

#### 3.2 Start Live Mode
```powershell
# Launch the autonomous bot
python SHA-256BOT.py
```

#### 3.3 Monitor Performance
```powershell
# The bot will display real-time stats
# Press Ctrl+C to stop safely
```

---

## 🐧 Linux Setup

### 📦 Step 1: Install Requirements

#### 1.1 Update System & Install Python
```bash
# Update package manager
sudo apt update && sudo apt upgrade -y
# Install Python 3.8+
sudo apt install python3 python3-pip git -y
python3 --version
```

#### 1.2 Install Virtual Environment
```bash
# Install venv for isolated environment
sudo apt install python3-venv -y
# Create virtual environment
python3 -m venv sha256-bot-env
```

#### 1.3 Clone Repository
```bash
# Clone and enter directory
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256
```

### ⚙️ Step 2: Configure Environment

#### 2.1 Activate Environment & Install Dependencies
```bash
# Activate virtual environment
source sha256-bot-env/bin/activate
# Install requirements
pip install -r requirements.txt
```

#### 2.2 Create Configuration File
```bash
# Copy example configuration
cp .env.example .env
# Edit with your preferred editor
nano .env  # or vim .env
```

#### 2.3 Set Permissions & Add API Keys
```bash
# Set proper permissions
chmod 600 .env
# Add your API credentials to .env file
```

### 🚀 Step 3: Launch the Bot

#### 3.1 Test Configuration
```bash
# Ensure virtual environment is active
source sha256-bot-env/bin/activate
# Test the bot
python SHA-256BOT.py --test
```

#### 3.2 Run as Service (Optional)
```bash
# Create systemd service for auto-start
sudo nano /etc/systemd/system/sha256bot.service
# Enable and start service
sudo systemctl enable sha256bot
sudo systemctl start sha256bot
```

#### 3.3 Monitor Logs
```bash
# View real-time logs
tail -f logs/sha256bot_autonomous.log
# Or check service status
sudo systemctl status sha256bot
```

---

## 🍎 macOS Setup

### 📦 Step 1: Install Requirements

#### 1.1 Install Homebrew & Python
```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Install Python 3.8+
brew install python git
python3 --version
```

#### 1.2 Install Xcode Command Line Tools
```bash
# Install development tools
xcode-select --install
# Verify installation
gcc --version
```

#### 1.3 Clone Repository
```bash
# Clone to your preferred directory
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256
```

### ⚙️ Step 2: Configure Environment

#### 2.1 Create Virtual Environment
```bash
# Create isolated Python environment
python3 -m venv sha256-bot-env
# Activate environment
source sha256-bot-env/bin/activate
# Install dependencies
pip install -r requirements.txt
```

#### 2.2 Configure Environment File
```bash
# Copy configuration template
cp .env.example .env
# Edit with TextEdit or preferred editor
open -e .env
```

#### 2.3 Secure Configuration
```bash
# Set secure permissions on config file
chmod 600 .env
# Verify permissions
ls -la .env
```

### 🚀 Step 3: Launch the Bot

#### 3.1 Test Setup
```bash
# Activate environment
source sha256-bot-env/bin/activate
# Run test mode
python SHA-256BOT.py --test
```

#### 3.2 Create Launch Script
```bash
# Create convenient launch script
cat > start_bot.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source sha256-bot-env/bin/activate
python SHA-256BOT.py
EOF
chmod +x start_bot.sh
```

#### 3.3 Run the Bot
```bash
# Launch using script
./start_bot.sh
# Or manually
source sha256-bot-env/bin/activate && python SHA-256BOT.py
```

---

## 🔑 API Keys Setup Guide

### 🐦 Twitter API (Optional but Recommended)
1. **Visit:** [developer.twitter.com](https://developer.twitter.com)
2. **Apply:** For developer account (free)
3. **Create:** New app and get your keys
4. **Add to .env:**
```env
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

### 💬 Telegram Bot (Optional)
1. **Message:** [@BotFather](https://t.me/botfather) on Telegram
2. **Create:** New bot with `/newbot` command
3. **Get:** Your bot token
4. **Add to .env:**
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_name
```

### 📱 Reddit API (Optional)
1. **Visit:** [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
2. **Create:** New application (script type)
3. **Note:** Client ID and secret
4. **Add to .env:**
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

---

## 🎮 Bot Features & Commands

### 🤖 Autonomous Features
- **Smart Posting:** Automatically creates and posts content
- **Audience Growth:** Intelligent follow/unfollow strategies  
- **Community Building:** Finds and joins relevant groups
- **Performance Learning:** Adapts based on engagement data

### 📊 Real-Time Monitoring
```bash
# The bot displays live stats:
🤖 SHA-256 BOT - FULLY AUTONOMOUS AI
💰 AFFILIATE CODE: your-code
⏰ 10:30:45 | Uptime: 3600s
🌍 Current Target: EU_WEST (en) 🔥 PEAK TIME

🔗 PLATFORM STATUS:
   🐦 Twitter: 🟢 READY (5 posts)
   💬 Telegram: 🟢 READY (3 posts, 12 invites)
   📍 Reddit: ⏰ Next post in 45m (2 posts)
```

### ⚙️ Advanced Configuration
```env
# Optional advanced settings
VOLTAGE_API_KEY=your_gpu_api_key        # For GPU deal content
AFFILIATE_CODE=your_affiliate_code      # Your referral code
```

---

## 🛡️ Safety & Best Practices

### ✅ Built-in Protection
- **Conservative Rate Limits:** Well below platform maximums
- **Smart Timing:** Posts during optimal hours for each region
- **Content Variation:** Avoids repetitive patterns
- **Error Recovery:** Handles temporary failures gracefully

### 🚨 Important Guidelines
- **Start with Test Mode:** Always run `--test` first
- **Monitor Initially:** Watch the bot for the first few hours
- **Respect ToS:** Ensure compliance with platform terms
- **Use Real Content:** Provide genuine value to your audience

---

## 🆘 Troubleshooting

### Common Issues & Solutions

#### ❌ "Module not found" Error
```bash
# Solution: Activate virtual environment
source sha256-bot-env/bin/activate  # Linux/Mac
# or
sha256-bot-env\Scripts\activate     # Windows
```

#### ❌ "API Authentication Failed"
```bash
# Solution: Check your .env file
cat .env  # Verify API keys are correct
```

#### ❌ "Permission Denied"
```bash
# Solution: Fix file permissions
chmod +x SHA-256BOT.py              # Linux/Mac
# or run as administrator on Windows
```

### 📞 Get Help
- **Issues:** [GitHub Issues](https://github.com/Jabsama/BOT-SHA-256/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Jabsama/BOT-SHA-256/discussions)

---

## 🤝 Contributing

We love contributions! Here's how to help:

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch (`git checkout -b amazing-feature`)
3. **💾 Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **📤 Push** to the branch (`git push origin amazing-feature`)
5. **🔄 Open** a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is for **educational and legitimate marketing purposes only**. Users are responsible for:
- ✅ Complying with platform Terms of Service
- ✅ Respecting rate limits and community guidelines  
- ✅ Using appropriate content and targeting
- ✅ Following applicable laws and regulations

---

## 🌟 Star This Project!

If you find this bot useful, please ⭐ **star this repository** to show your support!

**Made with ❤️ for the open source community**

---

*Ready to grow your social media presence? Let's get started! 🚀*
