#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VoltageGPU Bot - Discord Notifications
Real-time notifications for admins about bot performance and conversions
"""

import discord
import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

class VoltageGPUDiscordBot:
    """Discord bot for VoltageGPU notifications"""
    
    def __init__(self):
        self.token = os.getenv('DISCORD_BOT_TOKEN')
        self.admin_channel_id = int(os.getenv('DISCORD_ADMIN_CHANNEL', '0'))
        self.alerts_channel_id = int(os.getenv('DISCORD_ALERTS_CHANNEL', '0'))
        
        # Discord client setup
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        
        # Setup event handlers
        self.setup_events()
        
    def setup_events(self):
        """Setup Discord event handlers"""
        
        @self.client.event
        async def on_ready():
            print(f'🤖 Discord bot logged in as {self.client.user}')
            
            # Send startup notification
            await self.send_startup_notification()
            
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
                
            # Admin commands
            if message.content.startswith('!voltage'):
                await self.handle_admin_command(message)
    
    async def send_startup_notification(self):
        """Send bot startup notification"""
        embed = discord.Embed(
            title="🚀 VoltageGPU Bot Started",
            description="Bot is now online and monitoring affiliate performance",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Status", 
            value="✅ All systems operational", 
            inline=True
        )
        
        embed.add_field(
            name="Monitoring", 
            value="Twitter, Telegram, Reddit", 
            inline=True
        )
        
        embed.set_footer(text="VoltageGPU Bot v2.0")
        
        if self.admin_channel_id:
            channel = self.client.get_channel(self.admin_channel_id)
            if channel:
                await channel.send(embed=embed)
    
    async def send_conversion_alert(self, platform: str, amount: float, gpu_type: str = None):
        """Send conversion notification"""
        embed = discord.Embed(
            title="💰 New Conversion!",
            description=f"Affiliate conversion detected from {platform}",
            color=0xffd700,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Platform", value=platform, inline=True)
        embed.add_field(name="Amount", value=f"${amount:.2f}", inline=True)
        
        if gpu_type:
            embed.add_field(name="GPU Type", value=gpu_type, inline=True)
        
        embed.set_footer(text="VoltageGPU Affiliate System")
        
        if self.alerts_channel_id:
            channel = self.client.get_channel(self.alerts_channel_id)
            if channel:
                await channel.send(embed=embed)
    
    async def send_error_alert(self, platform: str, error_message: str, severity: str = "warning"):
        """Send error notification"""
        colors = {
            "info": 0x3498db,
            "warning": 0xff9800,
            "error": 0xff0000,
            "critical": 0x8b0000
        }
        
        embed = discord.Embed(
            title=f"⚠️ {severity.upper()}: {platform}",
            description=error_message,
            color=colors.get(severity, 0xff9800),
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Platform", value=platform, inline=True)
        embed.add_field(name="Severity", value=severity.upper(), inline=True)
        
        embed.set_footer(text="VoltageGPU Error Monitor")
        
        if self.alerts_channel_id:
            channel = self.client.get_channel(self.alerts_channel_id)
            if channel:
                await channel.send(embed=embed)
    
    async def send_daily_report(self, stats: dict):
        """Send daily performance report"""
        embed = discord.Embed(
            title="📊 Daily Performance Report",
            description="VoltageGPU Bot 24h Summary",
            color=0x3498db,
            timestamp=datetime.now()
        )
        
        # Add stats fields
        embed.add_field(
            name="📱 Posts", 
            value=f"Twitter: {stats.get('twitter_posts', 0)}\nTelegram: {stats.get('telegram_posts', 0)}\nReddit: {stats.get('reddit_posts', 0)}", 
            inline=True
        )
        
        embed.add_field(
            name="📈 Performance", 
            value=f"Success Rate: {stats.get('success_rate', 0):.1f}%\nErrors: {stats.get('errors', 0)}\nUptime: {stats.get('uptime', '0h')}", 
            inline=True
        )
        
        embed.add_field(
            name="💰 Revenue", 
            value=f"Conversions: {stats.get('conversions', 0)}\nRevenue: ${stats.get('revenue', 0):.2f}\nCTR: {stats.get('ctr', 0):.2f}%", 
            inline=True
        )
        
        embed.set_footer(text="VoltageGPU Analytics")
        
        if self.admin_channel_id:
            channel = self.client.get_channel(self.admin_channel_id)
            if channel:
                await channel.send(embed=embed)
    
    async def handle_admin_command(self, message):
        """Handle admin commands"""
        command = message.content.lower()
        
        if command == '!voltage status':
            await self.send_status_report(message.channel)
        elif command == '!voltage stats':
            await self.send_stats_report(message.channel)
        elif command == '!voltage help':
            await self.send_help(message.channel)
    
    async def send_status_report(self, channel):
        """Send current bot status"""
        try:
            # Get status from analytics API (if running)
            response = requests.get('http://localhost:5000/api/realtime', timeout=5)
            data = response.json() if response.status_code == 200 else {}
        except:
            data = {}
        
        embed = discord.Embed(
            title="🤖 Bot Status",
            description="Current VoltageGPU Bot Status",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🔗 Platforms", 
            value="✅ Twitter\n✅ Telegram\n✅ Reddit", 
            inline=True
        )
        
        embed.add_field(
            name="📊 Recent Activity", 
            value=f"Posts (1h): {sum(data.get('recent_posts', {}).values())}\nConversions (24h): {len(data.get('recent_conversions', []))}", 
            inline=True
        )
        
        await channel.send(embed=embed)
    
    async def send_stats_report(self, channel):
        """Send detailed statistics"""
        try:
            response = requests.get('http://localhost:5000/api/stats', timeout=5)
            data = response.json() if response.status_code == 200 else {}
            summary = data.get('summary', {})
        except:
            summary = {}
        
        embed = discord.Embed(
            title="📈 Performance Statistics",
            description="VoltageGPU Bot Analytics",
            color=0x3498db,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="📱 Posts", 
            value=f"Total: {summary.get('total_posts', 0)}\nSuccess Rate: {summary.get('success_rate', 0):.1f}%", 
            inline=True
        )
        
        embed.add_field(
            name="💰 Revenue", 
            value=f"Total: ${summary.get('total_revenue', 0):.2f}\nConversions: {summary.get('total_conversions', 0)}", 
            inline=True
        )
        
        embed.add_field(
            name="📊 Conversion Rate", 
            value=f"{summary.get('conversion_rate', 0):.2f}%", 
            inline=True
        )
        
        await channel.send(embed=embed)
    
    async def send_help(self, channel):
        """Send help message"""
        embed = discord.Embed(
            title="🤖 VoltageGPU Bot Commands",
            description="Available admin commands",
            color=0x3498db
        )
        
        commands = [
            ("!voltage status", "Show current bot status"),
            ("!voltage stats", "Show performance statistics"),
            ("!voltage help", "Show this help message")
        ]
        
        for cmd, desc in commands:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        await channel.send(embed=embed)
    
    def run(self):
        """Start the Discord bot"""
        if self.token:
            self.client.run(self.token)
        else:
            print("❌ Discord bot token not found in .env file")

# Notification helper functions for integration with main bot
class DiscordNotifier:
    """Helper class for sending Discord notifications from main bot"""
    
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    def send_webhook_notification(self, title: str, description: str, color: int = 0x3498db):
        """Send notification via webhook (simpler than bot)"""
        if not self.webhook_url:
            return
        
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.now().isoformat(),
            "footer": {"text": "VoltageGPU Bot"}
        }
        
        data = {"embeds": [embed]}
        
        try:
            requests.post(self.webhook_url, json=data, timeout=10)
        except Exception as e:
            print(f"Failed to send Discord notification: {e}")
    
    def notify_conversion(self, platform: str, amount: float):
        """Quick conversion notification"""
        self.send_webhook_notification(
            f"💰 New Conversion: ${amount:.2f}",
            f"Affiliate conversion from {platform}",
            0xffd700
        )
    
    def notify_error(self, platform: str, error: str):
        """Quick error notification"""
        self.send_webhook_notification(
            f"⚠️ Error on {platform}",
            error,
            0xff0000
        )
    
    def notify_milestone(self, milestone: str, value: str):
        """Milestone notification"""
        self.send_webhook_notification(
            f"🎉 Milestone Reached!",
            f"{milestone}: {value}",
            0x00ff00
        )

if __name__ == "__main__":
    # Run Discord bot
    bot = VoltageGPUDiscordBot()
    print("🚀 Starting VoltageGPU Discord Bot...")
    bot.run()
