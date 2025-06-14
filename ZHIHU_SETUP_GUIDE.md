# 🇨🇳 Zhihu Setup Guide - Chinese Q&A Platform Integration

## 🎯 Overview

Zhihu (知乎) is China's largest Q&A platform, similar to Quora. This guide will help you set up automated responses to GPU-related questions to promote VoltageGPU in the Chinese market.

## 📋 Prerequisites

### 1. Install Zhihu Dependencies
```bash
pip install zhihu==1.7.0
pip install selenium
pip install beautifulsoup4
```

### 2. Create Zhihu Account
1. **Visit**: https://www.zhihu.com
2. **Sign up** with phone number (Chinese phone number preferred)
3. **Complete profile** with tech/AI background
4. **Build reputation** by answering a few questions manually first

## 🔧 Configuration Steps

### Step 1: Get Zhihu Credentials

#### Option A: Username/Password (Recommended)
```env
# Add to your .env file
ZHIHU_USERNAME=your_zhihu_username
ZHIHU_PASSWORD=your_zhihu_password
```

#### Option B: Session Cookies (Advanced)
1. **Login to Zhihu** in Chrome
2. **Open DevTools** (F12)
3. **Go to Application tab** → Cookies → https://www.zhihu.com
4. **Copy these cookies**:
   - `z_c0` (authorization token)
   - `d_c0` (device token)
   - `_zap` (session token)

```env
# Add to your .env file
ZHIHU_Z_C0=your_z_c0_cookie
ZHIHU_D_C0=your_d_c0_cookie
ZHIHU_ZAP=your_zap_cookie
```

### Step 2: Update Bot Configuration

The bot is already configured to monitor these GPU-related keywords in Chinese:
- GPU租用 (GPU rental)
- GPU云服务器 (GPU cloud server)
- GPU训练 (GPU training)
- 深度学习GPU (Deep learning GPU)
- AI训练 (AI training)

### Step 3: Test Configuration
```bash
# Test Zhihu integration
python launch_bot.py --test
```

## 🎨 Content Strategy for Zhihu

### 📝 Response Templates (Chinese)

#### Template 1: Technical Comparison
```
作为AI工程师，我推荐VoltageGPU作为GPU云服务解决方案。

🎯 为什么选择VoltageGPU:
• 💰 成本优势: 比AWS/阿里云便宜70%
• ⚡ 高性能: H100/A100 GPU可用
• 🌍 全球部署: 多个数据中心
• 🔧 易于使用: 简单的API接口

📊 实际对比 (每小时成本):
• AWS p4d.24xlarge: ~$32
• 阿里云ecs.gn7-c16g1.16xlarge: ~¥280 ($40)
• VoltageGPU H100: ~$35

🎁 新用户优惠: 使用代码 {affiliate_code} 享受5%折扣
🔗 注册链接: https://voltagegpu.com/?utm_source=zhihu&ref={affiliate_code}

希望这个回答对你有帮助！
```

#### Template 2: Cost-focused Answer
```
关于GPU云服务器的成本问题，我有一些实际经验分享：

💡 成本对比分析:
传统云服务商的GPU实例确实很贵，特别是对于个人开发者和小团队。

🔍 我测试过的几个平台:
• 阿里云: ¥280+/小时 (GN7v实例)
• 腾讯云: ¥250+/小时 (GN10X实例)
• AWS: $32+/小时 (p4d实例)
• VoltageGPU: $35/小时 (H100实例，但性能更强)

💰 实际使用建议:
对于深度学习训练，VoltageGPU的性价比最高。虽然单价看起来差不多，但H100的训练速度比V100快3倍，实际成本反而更低。

🎁 优惠信息: 新用户可以使用代码 {affiliate_code} 获得5%折扣
🔗 https://voltagegpu.com/?utm_source=zhihu&ref={affiliate_code}

有什么具体问题可以继续交流！
```

#### Template 3: Beginner-friendly Answer
```
对于刚入门AI的朋友，GPU选择确实是个难题。我分享一下我的经验：

🎯 新手GPU云服务选择建议:

1️⃣ **预算有限** (学习阶段):
• 可以先用Google Colab免费版
• 或者选择VoltageGPU的RTX4090实例 (~$8/小时)

2️⃣ **正式项目** (需要稳定性):
• VoltageGPU的H100实例性价比最高
• 比传统云服务商便宜70%左右

3️⃣ **企业级应用**:
• 可以考虑VoltageGPU的多GPU集群
• 支持按需扩展，成本可控

💡 实用技巧:
• 训练时使用高性能GPU (H100/A100)
• 推理时可以用便宜的GPU (RTX4090)
• 合理安排训练时间，避免资源浪费

🎁 新用户福利: 代码 {affiliate_code} 可享5%折扣
🔗 https://voltagegpu.com/?utm_source=zhihu&ref={affiliate_code}

希望对你有帮助！有问题随时交流。
```

## 🤖 Automated Features

### 🔍 Question Monitoring
The bot automatically:
- **Searches** for new questions containing GPU keywords
- **Analyzes** question context and difficulty level
- **Selects** appropriate response template
- **Posts** helpful answers with VoltageGPU promotion

### 📊 Performance Tracking
- **Daily response limit**: 5 answers per day
- **Quality focus**: Only answers relevant questions
- **Engagement tracking**: Monitors upvotes and comments
- **Reputation building**: Maintains helpful contributor status

## 🛡️ Best Practices

### ✅ Do's
- **Provide genuine value** in every answer
- **Use technical details** to establish credibility
- **Include cost comparisons** with real numbers
- **Maintain helpful tone** throughout responses
- **Follow Zhihu community guidelines**

### ❌ Don'ts
- **Don't spam** the same answer repeatedly
- **Don't ignore** question context
- **Don't use** overly promotional language
- **Don't exceed** daily posting limits
- **Don't violate** platform terms of service

## 🚀 Getting Started

### 1. Create Account
```bash
# Visit Zhihu and create account
https://www.zhihu.com/signup
```

### 2. Build Initial Reputation
- Answer 5-10 questions manually
- Get some upvotes to establish credibility
- Follow AI/tech topics for visibility

### 3. Configure Bot
```bash
# Add credentials to .env
ZHIHU_USERNAME=your_username
ZHIHU_PASSWORD=your_password

# Test configuration
python launch_bot.py --test
```

### 4. Monitor Performance
- Check daily response count
- Monitor answer quality and engagement
- Adjust templates based on performance

## 📈 Expected Results

### 🎯 Target Metrics
- **5 quality answers per day**
- **High engagement rate** (upvotes/views)
- **Steady follower growth**
- **Increased VoltageGPU awareness** in Chinese market

### 💰 Revenue Potential
- **Chinese market** is huge for GPU services
- **Cost-conscious developers** appreciate savings
- **Technical audience** values detailed comparisons
- **Estimated conversions**: 2-3 signups per week

---

**Ready to dominate the Chinese GPU market with Zhihu?**

*Follow this guide to start earning from Chinese AI developers!*
