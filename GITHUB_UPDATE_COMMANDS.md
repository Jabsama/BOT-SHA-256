# 🚀 GitHub Update Commands

## Commands to update your repository

Run these commands in your terminal to push the cleaned project to GitHub:

```bash
# 1. Add all files (except .env which is protected by .gitignore)
git add .

# 2. Commit with descriptive message
git commit -m "🚀 Major Update: Unified Launcher + Autonomous Telegram + Multi-Reddit

- ✅ Single unified launcher (launch_bot.py) replaces all separate bots
- ✅ Autonomous Telegram with multi-channel support
- ✅ Multi-account Reddit support (2 accounts with smart rotation)
- ✅ Enhanced error handling with specific Reddit troubleshooting
- ✅ Complete English documentation for international users
- ✅ Security compliant (no API keys exposed)
- ✅ 90+ automated posts/day across all platforms
- 🗑️ Cleaned project: removed 15+ redundant files"

# 3. Push to GitHub
git push origin main
```

## Alternative if you have issues:

```bash
# Force push if needed (be careful!)
git push --force origin main
```

## Verify the update:

After pushing, check https://github.com/Jabsama/BOT-SHA-256 to confirm:
- ✅ launch_bot.py is the main file
- ✅ README.md shows the unified launcher documentation
- ✅ REDDIT_TROUBLESHOOTING.md includes the new error fix
- ✅ Old bot files are removed
- ✅ .env file is NOT visible (protected by .gitignore)

## Project is now ready for users!

Users can simply:
1. Clone the repo
2. Copy .env.example to .env
3. Fill in their API keys
4. Run: `python launch_bot.py`
