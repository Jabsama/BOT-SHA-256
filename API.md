# 🔌 VoltageGPU API Integration

## 🎯 Overview

VoltageGPU Bot integrates directly with the **VoltageGPU API** to fetch real-time GPU offers and pricing, ensuring your promotional content is always accurate and up-to-date.

## 🚀 API Features

### 📊 Real-time Data
- **Live GPU Offers** - Current available GPUs with pricing
- **Dynamic Pricing** - Real-time hourly rates
- **Availability Status** - Live inventory updates
- **Performance Metrics** - Uptime and location data

### 🔗 Affiliate Integration
- **SHA-256 Code Tracking** - Automatic affiliate code insertion
- **UTM Parameters** - Conversion tracking for analytics
- **Commission Tracking** - Real-time earnings monitoring
- **Withdrawal Integration** - Stripe-powered payouts

## 🔧 API Configuration

### 1. Get Your API Key
```bash
# Visit voltagegpu.com and create an account
# Navigate to API section in your dashboard
# Generate your API key
```

### 2. Configure Environment
```bash
# Add to your .env file
VOLTAGE_API_KEY=your_api_key_here
AFFILIATE_CODE=your_sha256_code_here
```

### 3. Test Connection
```bash
python launch_bot.py --test
```

## 📡 API Endpoints Used

### 🖥️ GPU Offers Endpoint
```
GET https://voltagegpu.com/api/pods
Authorization: Bearer YOUR_API_KEY
```

**Response Example:**
```json
{
  "pods": [
    {
      "gpu_count": 8,
      "gpu_type": "H100",
      "price_per_hour": 35.50,
      "location": "Mumbai",
      "uptime": 99.2,
      "availability": "available"
    }
  ]
}
```

### 💰 Affiliate Tracking
```
GET https://voltagegpu.com/api/affiliate/stats
Authorization: Bearer YOUR_API_KEY
```

**Response Example:**
```json
{
  "total_earnings": 1250.75,
  "pending_withdrawal": 45.20,
  "clicks_today": 23,
  "conversions_today": 3
}
```

## 🎨 Content Generation

### 📝 Dynamic Templates
The bot uses real API data to generate compelling content:

```python
# Example: Twitter post generation
content = f"""🚨 INSANE GPU DEAL! 🚨

💻 {gpu_count}x {gpu_type} for ${price}/hour
⚡ 70% cheaper than AWS
🌍 {location} | {uptime}% uptime

💰 Code {affiliate_code} = 5% OFF!
🔗 https://voltagegpu.com/?ref={affiliate_code}

#GPUDeals #AI"""
```

### 🌍 Multi-language Support
- **English** - Global markets (Twitter, Reddit, LinkedIn)
- **Chinese** - WeChat, Bilibili, Zhihu, Weibo
- **Portuguese** - Brazilian market

## 📊 Performance Tracking

### 🎯 UTM Parameters
All generated links include tracking parameters:
```
https://voltagegpu.com/?utm_source=twitter&utm_campaign=gpu_deals&ref=YOUR_CODE
```

### 📈 Analytics Integration
- **Click Tracking** - Monitor link performance
- **Conversion Tracking** - Track successful signups
- **Revenue Attribution** - Connect posts to earnings
- **Platform Performance** - Compare platform effectiveness

## 🛡️ Security & Rate Limits

### 🔒 Authentication
- **Bearer Token** authentication for all requests
- **API Key Rotation** supported for security
- **Request Signing** for sensitive operations

### ⚡ Rate Limits
- **100 requests/minute** for offer data
- **10 requests/minute** for affiliate stats
- **Automatic retry** with exponential backoff
- **Graceful degradation** to mock data if needed

## 🔄 Fallback System

### 📦 Mock Data
If API is unavailable, the bot uses realistic mock data:
```python
mock_offers = [{
    'gpu_count': random.choice([4, 8, 16]),
    'gpu_type': random.choice(['B200', 'H200', 'RTX4090']),
    'price_per_hour': round(random.uniform(35, 55), 2),
    'location': random.choice(['Mumbai', 'Raleigh', 'Singapore']),
    'uptime': round(random.uniform(97, 99.5), 1)
}]
```

### 🔄 Automatic Recovery
- **Health Checks** every 5 minutes
- **Automatic Reconnection** when API is restored
- **Seamless Transition** between real and mock data
- **Error Logging** for debugging

## 💰 Affiliate Program Details

### 🎯 Commission Structure
- **5% Commission** on all deposits made with your code
- **5% Discount** for customers using your code
- **No Minimum** deposit requirement
- **Instant Tracking** of referrals

### 💳 Withdrawal System
- **$20 Minimum** withdrawal amount
- **Stripe Integration** for secure payouts
- **Multiple Currencies** supported
- **Weekly Payouts** available

### 📊 Earnings Dashboard
Track your performance in real-time:
- **Total Earnings** - Lifetime commission earned
- **Pending Withdrawals** - Available for payout
- **Click Analytics** - Link performance metrics
- **Conversion Rates** - Signup success rates

## 🚀 Getting Started

### 1. Create VoltageGPU Account
```bash
# Visit https://voltagegpu.com
# Sign up in 10 seconds
# Get your unique SHA-256 affiliate code
```

### 2. Generate API Key
```bash
# Go to API section in dashboard
# Click "Generate New Key"
# Copy your API key securely
```

### 3. Configure Bot
```bash
# Add credentials to .env file
VOLTAGE_API_KEY=your_api_key
AFFILIATE_CODE=your_sha256_code
```

### 4. Start Earning
```bash
# Launch the bot
python launch_bot.py

# Watch real-time earnings in dashboard
# Withdraw profits via Stripe
```

---

**Ready to start earning with VoltageGPU affiliate marketing?**

*Get your API key and start promoting today!*
