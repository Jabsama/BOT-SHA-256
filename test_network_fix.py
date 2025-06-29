#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Network Fix Test - SHA-256 Bot
Test and apply network fixes for proxy and connection issues
"""

import os
import requests
import socket

# CRITICAL FIX: Disable proxy globally
os.environ['NO_PROXY'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

def test_network_connectivity():
    """Test network connectivity with fixes applied"""
    print("🔧 NETWORK CONNECTIVITY TEST")
    print("=" * 50)
    
    # Test 1: Basic internet connectivity
    print("\n1. Testing basic internet connectivity...")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ Internet connection: OK")
    except OSError:
        print("❌ No internet connection")
        return False
    
    # Test 2: HTTP requests without proxy
    print("\n2. Testing HTTP requests (no proxy)...")
    try:
        session = requests.Session()
        session.trust_env = False
        session.proxies = {}
        
