#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple HTTP Server for SHA-256 BOT Dashboard
Serves the dashboard web interface with proper CORS headers
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time

class DashboardHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS support"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom logging
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def start_dashboard_server(port=8080):
    """Start the dashboard HTTP server"""
    
    # Change to the current directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create server
    with socketserver.TCPServer(("", port), DashboardHTTPRequestHandler) as httpd:
        print(f"🚀 SHA-256 BOT Dashboard Server")
        print(f"📊 Serving at: http://localhost:{port}")
        print(f"🌐 Dashboard URL: http://localhost:{port}/dashboard_web.html")
        print("-" * 60)
        
        # Open browser automatically after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{port}/dashboard_web.html')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️ Dashboard server stopped")

if __name__ == "__main__":
    start_dashboard_server()
