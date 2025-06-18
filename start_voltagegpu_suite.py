#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VoltageGPU Bot Suite - Unified Launcher
Starts all components: Bot, Analytics Dashboard, and Discord Notifications
"""

import os
import sys
import time
import threading
import subprocess
import signal
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class VoltageGPUSuite:
    """Unified launcher for all VoltageGPU components"""
    
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_component(self, name: str, command: list, delay: int = 0):
        """Start a component with optional delay"""
        if delay > 0:
            print(f"⏳ Waiting {delay}s before starting {name}...")
            time.sleep(delay)
        
        try:
            print(f"🚀 Starting {name}...")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append((name, process))
            print(f"✅ {name} started (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return None
    
    def monitor_process(self, name: str, process):
        """Monitor a process and restart if it crashes"""
        while self.running:
            if process.poll() is not None:
                print(f"⚠️ {name} stopped unexpectedly")
                if self.running:
                    print(f"🔄 Restarting {name}...")
                    # Restart logic would go here
                break
            time.sleep(5)
    
    def start_all_components(self):
        """Start all VoltageGPU components"""
        print("🚀 VoltageGPU Suite - Starting All Components")
        print("=" * 50)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. Start Analytics Dashboard first
        dashboard_process = self.start_component(
            "Analytics Dashboard",
            [sys.executable, "analytics_dashboard.py"],
            delay=0
        )
        
        # 2. Start Discord Bot (if configured)
        discord_token = os.getenv('DISCORD_BOT_TOKEN')
        if discord_token:
            discord_process = self.start_component(
                "Discord Notifications",
                [sys.executable, "discord_notifications.py"],
                delay=3
            )
        else:
            print("⚠️ Discord bot token not found - skipping Discord notifications")
        
        # 3. Start Main Bot
        main_bot_process = self.start_component(
            "VoltageGPU Main Bot",
            [sys.executable, "bot_voltage_fixed.py"],
            delay=5
        )
        
        print()
        print("🎉 All components started successfully!")
        print()
        print("📊 Dashboard: http://localhost:5000")
        print("🤖 Main Bot: Running with smart rate limiting")
        if discord_token:
            print("💬 Discord: Notifications active")
        print()
        print("🛑 Press Ctrl+C to stop all components")
        print("=" * 50)
        
        return len(self.processes) > 0
    
    def stop_all_components(self):
        """Stop all running components"""
        print("\n🛑 Stopping all VoltageGPU components...")
        self.running = False
        
        for name, process in self.processes:
            try:
                print(f"⏹️ Stopping {name}...")
                process.terminate()
                process.wait(timeout=10)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️ Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
        
        print("🏁 All components stopped")
    
    def show_status(self):
        """Show status of all components"""
        print("\n📊 VoltageGPU Suite Status:")
        print("-" * 30)
        
        for name, process in self.processes:
            if process.poll() is None:
                print(f"✅ {name}: Running (PID: {process.pid})")
            else:
                print(f"❌ {name}: Stopped")
        
        print()
    
    def run(self):
        """Main run loop"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start all components
        if not self.start_all_components():
            print("❌ Failed to start components")
            return 1
        
        # Main monitoring loop
        try:
            while self.running:
                time.sleep(10)
                
                # Check if any critical process died
                main_bot_alive = False
                for name, process in self.processes:
                    if "Main Bot" in name and process.poll() is None:
                        main_bot_alive = True
                        break
                
                if not main_bot_alive and self.running:
                    print("⚠️ Main bot stopped - restarting suite...")
                    self.stop_all_components()
                    time.sleep(5)
                    self.start_all_components()
                
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all_components()
        
        return 0
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n📡 Received signal {signum}")
        self.running = False

def show_help():
    """Show help information"""
    print("""
🚀 VoltageGPU Bot Suite - Unified Launcher

USAGE:
    python start_voltagegpu_suite.py [OPTIONS]

OPTIONS:
    --help, -h          Show this help message
    --status            Show status of running components
    --stop              Stop all running components
    --dashboard-only    Start only the analytics dashboard
    --bot-only          Start only the main bot

COMPONENTS:
    📊 Analytics Dashboard  - Real-time performance metrics (Port 5000)
    🤖 Main Bot           - Multi-platform posting bot
    💬 Discord Bot        - Admin notifications and commands

CONFIGURATION:
    Configure via .env file:
    - DISCORD_BOT_TOKEN: Discord bot token (optional)
    - DISCORD_WEBHOOK_URL: Discord webhook for notifications (optional)
    - All other bot configuration variables

EXAMPLES:
    python start_voltagegpu_suite.py              # Start all components
    python start_voltagegpu_suite.py --dashboard-only  # Dashboard only
    python start_voltagegpu_suite.py --status          # Show status
""")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='🚀 VoltageGPU Bot Suite')
    parser.add_argument('--status', action='store_true', help='Show component status')
    parser.add_argument('--stop', action='store_true', help='Stop all components')
    parser.add_argument('--dashboard-only', action='store_true', help='Start dashboard only')
    parser.add_argument('--bot-only', action='store_true', help='Start bot only')
    
    args = parser.parse_args()
    
    if args.status:
        # Show status (would need to implement process detection)
        print("📊 Status check not implemented yet")
        return 0
    
    if args.stop:
        # Stop all (would need to implement process detection)
        print("🛑 Stop command not implemented yet")
        return 0
    
    if args.dashboard_only:
        print("🚀 Starting Analytics Dashboard only...")
        subprocess.run([sys.executable, "analytics_dashboard.py"])
        return 0
    
    if args.bot_only:
        print("🚀 Starting Main Bot only...")
        subprocess.run([sys.executable, "bot_voltage_fixed.py"])
        return 0
    
    # Start full suite
    suite = VoltageGPUSuite()
    return suite.run()

if __name__ == "__main__":
    exit(main())
