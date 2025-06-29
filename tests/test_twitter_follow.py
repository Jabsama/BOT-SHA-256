#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐦 Twitter Follow Manager Test - See exactly what the bot will do
"""

import os
import sys
from dotenv import load_dotenv
import tweepy

# Add modules to path
sys.path.append('.')
from modules.twitter_follow_manager import TwitterFollowManager

def test_twitter_follow_manager():
    """Test Twitter Follow Manager functionality"""
    print("🐦 TWITTER FOLLOW MANAGER TEST")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check if Twitter credentials exist
    if not os.getenv('TWITTER_API_KEY'):
        print("❌ No Twitter API credentials found in .env file")
        print("📝 Please add your Twitter API credentials to test follow functionality")
        return
    
    try:
        # Initialize Twitter client
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_SECRET'),
            wait_on_rate_limit=False
        )
        
        print("✅ Twitter client initialized")
        
        # Initialize Follow Manager
        follow_manager = TwitterFollowManager(client)
        print("✅ Twitter Follow Manager initialized")
        
        # Get current stats
        stats = follow_manager.get_follow_stats()
        print(f"\n📊 CURRENT STATS:")
        print(f"   Today's follows: {stats['today']['follows']}")
        print(f"   Today's unfollows: {stats['today']['unfollows']}")
        print(f"   Total following: {stats['total_following']}")
        print(f"   Follow backs: {stats['follow_backs']}")
        print(f"   Follow back rate: {stats['follow_back_rate']:.1f}%")
        print(f"   Follows remaining today: {stats['daily_limits']['follow_remaining']}")
        print(f"   Unfollows remaining today: {stats['daily_limits']['unfollow_remaining']}")
        
        # Test user discovery
        print(f"\n🔍 TESTING USER DISCOVERY:")
        search_terms = ['AI developer', 'GPU computing', 'machine learning']
        
        try:
            relevant_users = follow_manager.find_relevant_users(search_terms, limit=5)
            print(f"✅ Found {len(relevant_users)} relevant users")
            
            for i, user in enumerate(relevant_users[:3]):
                print(f"   {i+1}. @{user.username} - {user.display_name}")
                print(f"      Followers: {user.followers_count:,} | Following: {user.following_count:,}")
                print(f"      Relevance: {user.relevance_score:.2f} | Bio: {user.bio[:50]}...")
                
        except Exception as e:
            print(f"⚠️ User discovery failed: {e}")
            print("💡 This might be due to rate limits or API restrictions")
        
        # Test follow cycle (dry run)
        print(f"\n🧪 TESTING FOLLOW CYCLE (DRY RUN):")
        try:
            # Get unfollow candidates
            unfollow_candidates = follow_manager.get_unfollow_candidates()
            print(f"   Unfollow candidates: {len(unfollow_candidates)}")
            
            if stats['daily_limits']['follow_remaining'] > 0:
                print(f"   ✅ Can follow {stats['daily_limits']['follow_remaining']} more users today")
            else:
                print(f"   ⚠️ Daily follow limit reached")
                
            if stats['daily_limits']['unfollow_remaining'] > 0:
                print(f"   ✅ Can unfollow {stats['daily_limits']['unfollow_remaining']} more users today")
            else:
                print(f"   ⚠️ Daily unfollow limit reached")
                
        except Exception as e:
            print(f"❌ Follow cycle test failed: {e}")
        
        # Show what content the bot would post
        print(f"\n📝 EXAMPLE TWITTER CONTENT:")
        
        # Mock GPU offer
        mock_offer = {
            'gpu_count': 8,
            'gpu_type': 'H100',
            'price_per_hour': 32.50,
            'location': 'Singapore',
            'uptime': 99.2
        }
        
        # Example tweets the bot would generate
        example_tweets = [
            f"🚀 Just discovered an incredible GPU deal: {mock_offer['gpu_count']}x {mock_offer['gpu_type']} at ${mock_offer['price_per_hour']}/hour in {mock_offer['location']}! Perfect for AI training. Anyone else using decentralized GPU networks? #AI #MachineLearning #GPU",
            
            f"💡 Cost comparison: Traditional cloud vs decentralized GPU networks. The savings are massive! {mock_offer['gpu_count']}x {mock_offer['gpu_type']} configurations starting at ${mock_offer['price_per_hour']}/hour. Game changer for ML researchers! #CloudComputing #AI",
            
            f"🔥 Hot deal alert! {mock_offer['gpu_count']}x {mock_offer['gpu_type']} available in {mock_offer['location']} with {mock_offer['uptime']}% uptime. Perfect for training large models without breaking the bank! #GPU #DeepLearning #AI",
            
            f"📊 Economics of AI training: Why I switched to decentralized GPU networks. {mock_offer['gpu_count']}x {mock_offer['gpu_type']} at ${mock_offer['price_per_hour']}/hour vs $80+/hour on traditional clouds. The math is simple! #AI #MachineLearning",
            
            f"🎯 For AI researchers on a budget: Found {mock_offer['gpu_count']}x {mock_offer['gpu_type']} clusters at ${mock_offer['price_per_hour']}/hour. Location: {mock_offer['location']}, Uptime: {mock_offer['uptime']}%. Perfect for experimentation! #AI #Research #GPU"
        ]
        
        for i, tweet in enumerate(example_tweets, 1):
            print(f"   Tweet {i}: {tweet}")
            print(f"   Length: {len(tweet)} characters")
            print()
        
        print(f"🎯 TARGETING STRATEGY:")
        print(f"   Target audience: AI/ML developers, GPU enthusiasts, crypto miners")
        print(f"   Keywords: {', '.join(follow_manager.target_keywords[:10])}...")
        print(f"   Daily limits: 150 follows, 175 unfollows")
        print(f"   Grace period: 72 hours before unfollowing")
        print(f"   Quality filters: 10-100K followers, good ratios")
        
        print(f"\n✅ Twitter Follow Manager test completed!")
        print(f"💡 The bot will automatically follow relevant users and post engaging content")
        print(f"🔄 Run the main bot to see it in action: python SHA-256BOT.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print(f"💡 Make sure your Twitter API credentials are correct in .env file")

if __name__ == "__main__":
    test_twitter_follow_manager()
