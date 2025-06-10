# 🚨 Reddit Troubleshooting Guide

## Common Reddit Errors & Solutions

### ❌ Error: unauthorized_client (Only script apps may use password auth)

**What it means:** Your Reddit app is configured as "web app" instead of "script app".

**Solution:**
1. Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
2. Find your "VoltageGPU-Bot" app
3. Click "edit"
4. Change app type from "web app" to "script"
5. Save changes
6. Restart the bot

### ❌ Error 403 Forbidden

**What it means:** Your Reddit account is banned from posting to that subreddit or has insufficient permissions.

**Solutions:**
1. **Create a new Reddit account**
   - Use different email/username
   - Build karma slowly (comment, upvote)
   - Wait 1-2 weeks before posting

2. **Build account reputation**
   - Comment on posts in target subreddits
   - Get upvotes to build karma
   - Follow subreddit rules strictly

3. **Check subreddit rules**
   - Some require minimum karma (50-100+)
   - Some require account age (30+ days)
   - Some ban promotional content

### ❌ Rate Limiting (429 Error)

**What it means:** You're posting too frequently.

**Solutions:**
1. **Increase posting intervals**
   - Change from 30min to 2+ hours
   - Reduce daily post limits
   - Use multiple accounts

2. **Bot automatically handles this**
   - Waits 2 hours when rate limited
   - Logs helpful messages
   - Continues with other platforms

### ❌ Low Karma Issues

**What it means:** Your account doesn't have enough karma to post.

**Solutions:**
1. **Build karma organically**
   ```
   Target: 100+ comment karma, 50+ post karma
   Method: Comment helpful answers in tech subreddits
   Time: 1-2 weeks of regular activity
   ```

2. **Focus on comment karma first**
   - Easier to get than post karma
   - Comment in r/AskReddit, r/explainlikeimfive
   - Give helpful tech advice

### ❌ Account Too New

**What it means:** Subreddit requires older accounts.

**Solutions:**
1. **Wait it out**
   - Most subreddits: 7-30 days minimum
   - High-value subreddits: 90+ days
   - Be patient, build reputation

2. **Use older accounts**
   - Buy aged accounts (risky)
   - Use personal accounts (careful)
   - Create accounts in advance

## 🛠️ Bot Improvements Made

### ✅ Better Error Detection
```python
# Now detects specific error types:
- 403 Forbidden (banned/insufficient permissions)
- 429 Rate Limited (posting too fast)
- Karma issues (account too new/low karma)
- Account issues (shadowbanned, etc.)
```

### ✅ Smart Recovery
```python
# Automatic responses:
- Bans: Skip subreddit, try others
- Rate limits: Wait 2 hours
- Karma issues: Helpful suggestions
- Unknown errors: Wait 1 hour, retry
```

### ✅ Helpful Logging
```
❌ BANNED from r/MachineLearning - RoleCold4185 (403 Forbidden)
💡 Solution: Create new Reddit account or wait 24h before retry

❌ RATE LIMITED on Reddit - RoleCold4185
💡 Solution: Waiting 2 hours before next attempt

❌ ACCOUNT ISSUE r/LocalLLaMA - RoleCold4185: insufficient karma
💡 Solution: Build karma by commenting/upvoting before posting
```

## 🎯 Best Practices

### 1. Account Management
- **Use multiple accounts** (2-3 max)
- **Age accounts slowly** (1-2 months)
- **Build karma organically** (comment, upvote)
- **Follow subreddit rules** strictly

### 2. Posting Strategy
- **Start with easy subreddits** (r/GPURental, r/vastai)
- **Avoid high-moderation subs** initially
- **Quality over quantity** (better content = less bans)
- **Vary posting times** (don't be predictable)

### 3. Content Guidelines
- **No direct promotion** in title
- **Provide value first** (analysis, comparison)
- **Use affiliate links sparingly** (in comments better)
- **Engage authentically** (respond to comments)

## 🚀 Recommended Subreddit Progression

### Phase 1: Easy Targets (Week 1-2)
```
✅ r/GPURental (12k members) - Direct promo OK
✅ r/vastai (42k members) - Competitor comparisons welcome
✅ r/CloudComputing (small, tech-focused)
```

### Phase 2: Medium Targets (Week 3-4)
```
✅ r/LocalLLaMA (400k members) - Technical focus
✅ r/developersIndia (200k members) - Cost-conscious
✅ r/programacao (80k members) - Portuguese
```

### Phase 3: High-Value Targets (Month 2+)
```
✅ r/MachineLearning (3.6M members) - High moderation
✅ r/DeepLearning (1.1M members) - Academic focus
✅ r/artificial (1.8M members) - General AI
```

## 🔧 Quick Fixes

### If Bot Keeps Getting Banned:
1. **Reduce posting frequency**
   ```python
   # In launch_bot.py, change:
   self.reddit_next_post = now + timedelta(hours=2)  # Instead of 30min
   ```

2. **Focus on fewer subreddits**
   ```python
   # Remove high-moderation subreddits temporarily
   # Keep only: GPURental, vastai, LocalLLaMA
   ```

3. **Improve content quality**
   - Add more technical details
   - Include real benchmarks
   - Provide genuine value

### If No Posts Going Through:
1. **Check account status**
   - Log into Reddit manually
   - Verify not shadowbanned
   - Check karma levels

2. **Test with safe content**
   - Post without affiliate links
   - Use general tech discussion
   - Build reputation first

## 📞 Support

If you continue having issues:
1. **Check logs** for specific error messages
2. **Try manual posting** to test account status
3. **Create new accounts** if needed
4. **Focus on Twitter/Telegram** while fixing Reddit

Remember: **Reddit is the hardest platform** but also the most valuable for tech audiences. Be patient and build reputation slowly!
