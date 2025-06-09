#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Post Réel - Faire poster tous les comptes maintenant
"""

import os
import json
import random
import logging
import requests
import tweepy
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_post_reel():
    """Test avec posts réels sur tous les comptes"""
    print("🚀 TEST POST RÉEL - TOUS LES COMPTES")
    print("=" * 60)
    
    load_dotenv()
    affiliate_code = 'SHA-256-76360B81D39F'
    
    # Charger templates
    with open('multilingual_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    # Mock offer
    offer = {
        'gpu_count': 8,
        'gpu_type': 'H200',
        'price_per_hour': 39.10,
        'location': 'Mumbai',
        'uptime': 99.2
    }
    
    # Configuration Twitter
    twitter_configs = [
        {
            'name': '@GpuVoltage',
            'api_key': '5WUZlylBsGPI8iFaDQlZ9SLh8',
            'api_secret': 'HZTkcKB1WgcccrtoBJ2JT3TTEaf6Li4MvlnDHjd6FGzyMA0Vfk',
            'bearer_token': 'AAAAAAAAAAAAAAAAAAAAADZ32QEAAAAA4r0K%2ByFAHO7ltMH%2BSAvJ1bHXt%2BA%3DrE1uyMPYWyN3Z9Sy6Ox1ke2DxbuWYtXGt08g70Y9sz4F4s39pQ',
            'access_token': '1932098674869297152-E0F0bLGuaTUrUVSPgxeDSbTTGFzMJT',
            'access_secret': '7YLXMOVfHA5jafrNlMwLkF3agJwskEWNqMhoUpxJ3Gss0'
        },
        {
            'name': '@CRYPT0_BRY',
            'api_key': '1oLnaxobDbHfZXFJsWkOMmKRo',
            'api_secret': 'WVtcrADZyweiFkGm9RMHslh3vW3d4t64lYJNOFORJUM6dxqjlB',
            'bearer_token': 'AAAAAAAAAAAAAAAAAAAAAOF62QEAAAAA2lYfQXBZsTQHy%2B9baELdTQObLmI%3D3KOcmPWyNeDtmKnCxiGl1VYcl6yvuCOstyMNcLrqFUQQqcpFYk',
            'access_token': '1789442105602879488-Dyucdr4wBLkutsN31qEfzVkAwHbOTh',
            'access_secret': 'mgzjYomxmZl3WNpFgQ8QEkWKBRmyrihhY73MDjpcRwijc'
        }
    ]
    
    # Test Twitter
    print("🐦 TEST TWITTER RÉEL:")
    print("-" * 30)
    
    for i, config in enumerate(twitter_configs):
        try:
            client = tweepy.Client(
                bearer_token=config['bearer_token'],
                consumer_key=config['api_key'],
                consumer_secret=config['api_secret'],
                access_token=config['access_token'],
                access_token_secret=config['access_secret'],
                wait_on_rate_limit=True
            )
            
            # Générer contenu
            content_type = 'gpu_deals' if i == 0 else 'affiliate'
            template = templates['twitter']['en'][content_type][0]
            
            if content_type == 'gpu_deals':
                content = template.format(
                    gpu_count=offer['gpu_count'],
                    gpu_type=offer['gpu_type'],
                    price=f"${offer['price_per_hour']:.2f}",
                    location=offer['location'],
                    uptime=f"{offer['uptime']:.1f}%",
                    affiliate_code=affiliate_code
                )
            else:
                content = template.format(affiliate_code=affiliate_code)
            
            # Raccourcir si nécessaire
            if len(content) > 280:
                content = content[:277] + "..."
            
            print(f"📱 {config['name']} - {content_type.upper()}:")
            print(f"📄 ({len(content)} caractères)")
            print(content)
            print()
            
            # POSTER RÉELLEMENT
            response = client.create_tweet(text=content)
            tweet_id = response.data['id']
            
            print(f"✅ TWEET POSTÉ AVEC SUCCÈS !")
            print(f"🔗 ID: {tweet_id}")
            print(f"🌐 URL: https://twitter.com/i/status/{tweet_id}")
            print()
            
        except Exception as e:
            print(f"❌ Erreur {config['name']}: {e}")
            print()
    
    # Test Telegram
    print("💬 TEST TELEGRAM RÉEL:")
    print("-" * 30)
    
    try:
        import telegram
        bot = telegram.Bot(token='8106770803:AAEWKzXzpcNkpHHm7gEh_nVa8mty0G8HZr0')
        
        # Générer contenu Telegram
        template = templates['telegram']['en']['affiliate'][0]
        content = template.format(affiliate_code=affiliate_code)
        
        # Ajouter question engageante
        content += "\n\n🚀 Who's ready to save 70% on GPU costs?"
        
        print(f"📄 ({len(content)} caractères)")
        print(content)
        print()
        
        # POSTER RÉELLEMENT
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            message = loop.run_until_complete(
                bot.send_message(
                    chat_id='@VoltageGPU',
                    text=content
                )
            )
            
            print(f"✅ MESSAGE TELEGRAM POSTÉ AVEC SUCCÈS !")
            print(f"🔗 ID: {message.message_id}")
            print(f"🌐 Canal: @VoltageGPU")
            print()
            
        finally:
            loop.close()
            
    except Exception as e:
        print(f"❌ Erreur Telegram: {e}")
        print()
    
    print("🎉 TEST POST RÉEL TERMINÉ !")
    print("=" * 60)
    print("✅ Vérifiez vos comptes Twitter et Telegram")
    print("✅ Les posts devraient être visibles maintenant")
    print("✅ Code SHA-256-76360B81D39F inclus dans chaque post")
    print("💰 Vos revenus passifs commencent maintenant !")

if __name__ == "__main__":
    test_post_reel()
