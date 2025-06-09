# 🚀 VoltageGPU Bot - 2-Minute Setup Guide

> **Transform your social media into a passive income machine!** 💰

## 🎯 What You'll Get
- **Automated posting** on Twitter, Telegram & Reddit
- **1810+ posts per month** with zero effort
- **Passive affiliate income** from VoltageGPU referrals
- **Multi-language support** (English + Chinese)
- **Smart scheduling** for maximum engagement

---

## ⚡ Quick Start (2 Minutes!)

### Step 1: Download & Setup (30 seconds)
```bash
# Clone the repository
git clone https://github.com/Jabsama/BOT-SHA-256.git
cd BOT-SHA-256

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get Your API Keys (60 seconds)

#### 🐦 Twitter (Required)
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app → Get your keys
3. Copy: `API Key`, `API Secret`, `Bearer Token`, `Access Token`, `Access Secret`

#### 📱 Telegram (Optional but Recommended)
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Type `/newbot` → Follow instructions
3. Copy your `Bot Token`
4. Create a channel → Get channel ID (e.g., `@YourChannel`)

#### ⚡ VoltageGPU (Required)
1. Sign up at [VoltageGPU](https://voltagegpu.com)
2. Get your API key from dashboard
3. Get your affiliate code (format: `SHA-256-XXXXXXXX`)

### Step 3: Configure Your Bot (30 seconds)
```bash
# Copy the example configuration
cp .env.example .env

# Edit with your favorite editor
nano .env
```

**Fill in your keys:**
```env
# ⚡ VoltageGPU API
VOLTAGE_API_KEY=your_actual_api_key_here

# 🐦 Twitter
TWITTER_ENABLED=true
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret

# 📱 Telegram (Optional)
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_channel_name

# 💰 Your Affiliate Code
AFFILIATE_CODE=SHA-256-YOUR_CODE_HERE
```

---

## 🎮 Choose Your Bot Mode

### 🧪 Test Mode (Recommended First)
```bash
# Test all platforms
python final_optimized_bot.py --test
```

### 🚀 Production Mode
```bash
# Start the optimized bot
python final_optimized_bot.py
```

### 💥 Explosive Mode (1810 posts/month)
```bash
# Maximum posting frequency
python bot_explosif.py
```

### 🧠 Intelligent Mode (AI-powered)
```bash
# Adaptive content generation
python intelligent_bot.py
```

---

## 📊 Bot Comparison

| Bot Type | Posts/Day | Platforms | Best For |
|----------|-----------|-----------|----------|
| **Optimized** | 5-7 | All | Beginners |
| **Explosive** | 59 | All | Max Revenue |
| **Intelligent** | 3-8 | All | Quality Content |
| **Timer** | 32+ | Twitter+Telegram | Real-time tracking |

---

## 🎯 Pro Tips for Maximum Revenue

### 💡 Content Strategy
- **70% GPU deals** (technical audience)
- **30% affiliate links** (conversion focus)
- **Multi-language** posts for global reach

### ⏰ Optimal Timing
- **Twitter**: 2 PM UTC (peak engagement)
- **Telegram**: 10 AM & 6 PM UTC
- **Reddit**: 3 PM UTC (every 2 days)

### 🔥 Growth Hacks
1. **Use multiple accounts** (set up `TWITTER_API_KEY_2` etc.)
2. **Enable all platforms** for maximum reach
3. **Monitor performance** with built-in analytics
4. **Adjust affiliate codes** for different campaigns

---

## 🛠️ Troubleshooting

### ❌ Common Issues

**"Twitter API Error"**
```bash
# Check your API keys in .env file
# Ensure Twitter Developer account is approved
```

**"Module not found"**
```bash
# Install missing dependencies
pip install tweepy python-telegram-bot praw requests schedule python-dotenv
```

**"No posts generated"**
```bash
# Check your .env configuration
# Run in test mode first: python final_optimized_bot.py --test
```

### 🔧 Advanced Configuration

**Multi-Account Setup:**
```env
# Add second Twitter account
TWITTER_API_KEY_2=your_second_account_key
TWITTER_API_SECRET_2=your_second_account_secret
# ... (repeat for all keys)
```

**Custom Scheduling:**
- Edit the `schedule` calls in your chosen bot file
- Modify posting frequencies in the configuration

---

## 📈 Expected Results

### 💰 Revenue Projections
- **Month 1**: $50-100 (building audience)
- **Month 3**: $150-300 (established presence)
- **Month 6**: $300-500+ (optimized conversion)

### 📊 Growth Metrics
- **1810+ posts/month** (explosive mode)
- **50-100 clicks/day** on affiliate links
- **2-5% conversion rate** (industry average)

---

## 🚀 Ready to Launch?

### Final Checklist ✅
- [ ] All API keys configured in `.env`
- [ ] Test mode successful
- [ ] Affiliate code verified
- [ ] Bot mode selected
- [ ] Monitoring setup ready

### Launch Command
```bash
# Start your money-making machine!
python final_optimized_bot.py

# Or for maximum results:
python bot_explosif.py
```

---

## 🎉 Congratulations!

Your VoltageGPU bot is now running and generating passive income! 

**What happens next:**
- Bot posts automatically according to schedule
- Affiliate links generate clicks and conversions
- Revenue grows as your audience expands
- You earn money while you sleep! 💤💰

---

## 📞 Support & Community

- **Issues**: Open a GitHub issue
- **Updates**: Watch this repository
- **Tips**: Check the strategy guides in `/docs`

**Happy earning! 🚀💰**

---

*⚠️ Disclaimer: Results may vary. Always comply with platform terms of service.*
