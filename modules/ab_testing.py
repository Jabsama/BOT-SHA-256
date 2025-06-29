#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 A/B Testing Module - BOT SHA-256
Automatic A/B testing with 5 variants and performance optimization
"""

import json
import logging
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import statistics

class ABTestingEngine:
    """Advanced A/B testing with automatic variant selection"""
    
    def __init__(self):
        self.test_data = {}
        self.variant_performance = defaultdict(lambda: defaultdict(list))
        self.active_tests = {}
        self.confidence_threshold = 0.95
        self.min_samples = 10  # Minimum samples before making decisions
        
        # Load historical test data
        self._load_test_data()
        
    def _load_test_data(self):
        """Load historical A/B test data"""
        try:
            with open('data/ab_test_data.json', 'r') as f:
                data = json.load(f)
                self.test_data = data.get('tests', {})
                self.active_tests = data.get('active_tests', {})
                
                # Reconstruct variant performance
                for test_id, test_info in self.test_data.items():
                    for variant_id, results in test_info.get('results', {}).items():
                        self.variant_performance[test_id][variant_id] = results
                        
        except FileNotFoundError:
            logging.info("🧪 Initializing new A/B testing data")
            self.test_data = {}
            self.active_tests = {}
    
    def _save_test_data(self):
        """Save A/B test data"""
        try:
            import os
            os.makedirs('data', exist_ok=True)
            
            data = {
                'tests': self.test_data,
                'active_tests': self.active_tests,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('data/ab_test_data.json', 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logging.error(f"❌ Failed to save A/B test data: {e}")
    
    def create_content_variants(self, base_content: str, content_type: str, platform: str) -> List[Dict]:
        """Create 5 variants of content for A/B testing"""
        
        variants = []
        
        # Variant A: Original (Control)
        variants.append({
            'id': 'A',
            'name': 'Original',
            'content': base_content,
            'changes': 'Control group - no changes'
        })
        
        # Variant B: Urgency Enhanced
        urgency_content = self._add_urgency(base_content)
        variants.append({
            'id': 'B',
            'name': 'Urgency Enhanced',
            'content': urgency_content,
            'changes': 'Added urgency markers and time pressure'
        })
        
        # Variant C: Social Proof
        social_content = self._add_social_proof(base_content)
        variants.append({
            'id': 'C',
            'name': 'Social Proof',
            'content': social_content,
            'changes': 'Added social proof and testimonials'
        })
        
        # Variant D: Benefit Focused
        benefit_content = self._enhance_benefits(base_content)
        variants.append({
            'id': 'D',
            'name': 'Benefit Focused',
            'content': benefit_content,
            'changes': 'Enhanced benefits and value proposition'
        })
        
        # Variant E: Emotional Appeal
        emotional_content = self._add_emotional_appeal(base_content)
        variants.append({
            'id': 'E',
            'name': 'Emotional Appeal',
            'content': emotional_content,
            'changes': 'Added emotional triggers and storytelling'
        })
        
        return variants
    
    def _add_urgency(self, content: str) -> str:
        """Add urgency elements to content"""
        urgency_prefixes = [
            "⏰ LIMITED TIME:",
            "🚨 URGENT:",
            "⚡ ENDING SOON:",
            "🔥 LAST CHANCE:",
            "⏳ HURRY:"
        ]
        
        urgency_suffixes = [
            "\n\n⏰ Don't miss out - act now!",
            "\n\n🚨 Limited spots available!",
            "\n\n⚡ Offer expires soon!",
            "\n\n🔥 While supplies last!",
            "\n\n⏳ Time is running out!"
        ]
        
        # Add urgency prefix if not already present
        if not any(prefix.split()[1].lower() in content.lower() for prefix in urgency_prefixes):
            prefix = random.choice(urgency_prefixes)
            content = f"{prefix} {content}"
        
        # Add urgency suffix
        suffix = random.choice(urgency_suffixes)
        if len(content + suffix) <= 280:  # Twitter limit
            content += suffix
        
        return content
    
    def _add_social_proof(self, content: str) -> str:
        """Add social proof elements to content"""
        social_proof_elements = [
            "✅ 10,000+ developers already switched",
            "🌟 Trusted by Fortune 500 companies",
            "👥 Join 50,000+ satisfied users",
            "🏆 #1 rated GPU service",
            "💯 99.9% customer satisfaction",
            "🚀 Used by top AI startups",
            "⭐ 4.9/5 stars from 5000+ reviews"
        ]
        
        # Insert social proof near the beginning
        lines = content.split('\n')
        if len(lines) > 1:
            social_element = random.choice(social_proof_elements)
            lines.insert(1, social_element)
            content = '\n'.join(lines)
        
        return content
    
    def _enhance_benefits(self, content: str) -> str:
        """Enhance benefits and value proposition"""
        benefit_enhancements = {
            'save': 'SAVE MASSIVE AMOUNTS',
            'cheap': 'INCREDIBLY AFFORDABLE',
            'fast': 'LIGHTNING FAST',
            'easy': 'EFFORTLESSLY SIMPLE',
            'free': 'COMPLETELY FREE',
            'best': 'INDUSTRY LEADING',
            'good': 'EXCEPTIONAL'
        }
        
        enhanced_content = content
        for original, enhanced in benefit_enhancements.items():
            enhanced_content = enhanced_content.replace(original, enhanced)
        
        # Add specific benefit callouts
        benefit_callouts = [
            "💰 SAVE: Up to 70% vs competitors",
            "⚡ SPEED: 10x faster deployment",
            "🛡️ SECURITY: Enterprise-grade protection",
            "📈 GROWTH: Scale without limits",
            "🎯 RESULTS: Guaranteed performance"
        ]
        
        # Try to add a benefit callout
        callout = random.choice(benefit_callouts)
        if len(enhanced_content + f"\n{callout}") <= 280:
            enhanced_content += f"\n{callout}"
        
        return enhanced_content
    
    def _add_emotional_appeal(self, content: str) -> str:
        """Add emotional triggers and storytelling"""
        emotional_starters = [
            "💔 Tired of overpaying for cloud services?",
            "😤 Frustrated with slow GPU performance?",
            "🤯 Can't believe how much you're spending?",
            "😱 Shocked by your AWS bill?",
            "🎉 Ready to celebrate massive savings?"
        ]
        
        emotional_endings = [
            "\n\n💪 Take control of your costs today!",
            "\n\n🌟 Your future self will thank you!",
            "\n\n🚀 Join the smart developers revolution!",
            "\n\n💎 You deserve better - get it now!",
            "\n\n🔥 Don't let others get ahead - act now!"
        ]
        
        # Add emotional starter
        starter = random.choice(emotional_starters)
        content = f"{starter}\n\n{content}"
        
        # Add emotional ending if space allows
        ending = random.choice(emotional_endings)
        if len(content + ending) <= 280:
            content += ending
        
        return content
    
    def start_ab_test(self, content_type: str, platform: str, region: str, base_content: str) -> Dict:
        """Start a new A/B test"""
        
        # Create test ID
        test_id = hashlib.md5(f"{content_type}_{platform}_{region}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        # Create variants
        variants = self.create_content_variants(base_content, content_type, platform)
        
        # Initialize test
        test_info = {
            'id': test_id,
            'content_type': content_type,
            'platform': platform,
            'region': region,
            'variants': variants,
            'start_time': datetime.now().isoformat(),
            'status': 'active',
            'results': {variant['id']: [] for variant in variants}
        }
        
        self.test_data[test_id] = test_info
        self.active_tests[f"{content_type}_{platform}_{region}"] = test_id
        
        self._save_test_data()
        
        logging.info(f"🧪 Started A/B test {test_id} for {content_type}/{platform}/{region}")
        
        return test_info
    
    def get_variant_for_test(self, content_type: str, platform: str, region: str) -> Optional[Dict]:
        """Get the best variant for current context"""
        
        test_key = f"{content_type}_{platform}_{region}"
        
        # Check if there's an active test
        if test_key in self.active_tests:
            test_id = self.active_tests[test_key]
            test_info = self.test_data.get(test_id)
            
            if test_info and test_info['status'] == 'active':
                # Check if we have enough data to determine winner
                winner = self._check_for_winner(test_id)
                
                if winner:
                    # We have a winner, use it
                    winning_variant = next(v for v in test_info['variants'] if v['id'] == winner)
                    logging.info(f"🏆 Using winning variant {winner} for test {test_id}")
                    return winning_variant
                else:
                    # Still testing, use weighted random selection
                    variant = self._select_variant_weighted(test_id)
                    return variant
        
        return None
    
    def _select_variant_weighted(self, test_id: str) -> Dict:
        """Select variant using weighted random based on performance"""
        
        test_info = self.test_data[test_id]
        variants = test_info['variants']
        
        # Calculate weights based on performance
        weights = []
        for variant in variants:
            variant_id = variant['id']
            results = self.variant_performance[test_id][variant_id]
            
            if len(results) < 3:
                # Not enough data, equal weight
                weights.append(1.0)
            else:
                # Calculate success rate
                success_rate = sum(1 for r in results if r.get('success', False)) / len(results)
                avg_engagement = sum(r.get('engagement', 0) for r in results) / len(results)
                
                # Combined score (success rate weighted more heavily)
                score = success_rate * 0.7 + min(avg_engagement / 100, 1.0) * 0.3
                weights.append(max(score, 0.1))  # Minimum weight to ensure all variants get some traffic
        
        # Weighted random selection
        total_weight = sum(weights)
        r = random.uniform(0, total_weight)
        
        cumulative_weight = 0
        for i, weight in enumerate(weights):
            cumulative_weight += weight
            if r <= cumulative_weight:
                return variants[i]
        
        # Fallback to first variant
        return variants[0]
    
    def record_variant_result(self, test_id: str, variant_id: str, success: bool, 
                            engagement: int = 0, conversion: bool = False):
        """Record result for a variant"""
        
        if test_id not in self.test_data:
            return
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'engagement': engagement,
            'conversion': conversion,
            'score': self._calculate_score(success, engagement, conversion)
        }
        
        self.variant_performance[test_id][variant_id].append(result)
        self.test_data[test_id]['results'][variant_id].append(result)
        
        self._save_test_data()
        
        # Check if we can determine a winner
        self._check_for_winner(test_id)
    
    def _calculate_score(self, success: bool, engagement: int, conversion: bool) -> float:
        """Calculate overall score for a result"""
        score = 0.0
        
        if success:
            score += 0.4
        
        # Normalize engagement (assuming max 1000)
        score += min(engagement / 1000, 0.4)
        
        if conversion:
            score += 0.2
        
        return score
    
    def _check_for_winner(self, test_id: str) -> Optional[str]:
        """Check if we can determine a statistical winner"""
        
        test_info = self.test_data[test_id]
        
        if test_info['status'] != 'active':
            return test_info.get('winner')
        
        # Check if we have enough samples
        variant_scores = {}
        for variant_id, results in self.variant_performance[test_id].items():
            if len(results) >= self.min_samples:
                scores = [r['score'] for r in results]
                variant_scores[variant_id] = {
                    'mean': statistics.mean(scores),
                    'stdev': statistics.stdev(scores) if len(scores) > 1 else 0,
                    'count': len(scores)
                }
        
        if len(variant_scores) < 2:
            return None  # Not enough data
        
        # Find the best performing variant
        best_variant = max(variant_scores.items(), key=lambda x: x[1]['mean'])
        best_id, best_stats = best_variant
        
        # Check if the difference is statistically significant
        for variant_id, stats in variant_scores.items():
            if variant_id == best_id:
                continue
            
            # Simple significance test (in production, use proper statistical tests)
            difference = best_stats['mean'] - stats['mean']
            combined_stdev = (best_stats['stdev'] + stats['stdev']) / 2
            
            if combined_stdev > 0:
                significance = difference / combined_stdev
                if significance < 1.5:  # Not significant enough
                    return None
        
        # We have a winner!
        test_info['status'] = 'completed'
        test_info['winner'] = best_id
        test_info['end_time'] = datetime.now().isoformat()
        
        # Remove from active tests
        test_key = f"{test_info['content_type']}_{test_info['platform']}_{test_info['region']}"
        if test_key in self.active_tests:
            del self.active_tests[test_key]
        
        self._save_test_data()
        
        logging.info(f"🏆 A/B Test {test_id} completed! Winner: Variant {best_id}")
        
        return best_id
    
    def get_test_summary(self, test_id: str) -> Dict:
        """Get summary of A/B test results"""
        
        if test_id not in self.test_data:
            return {}
        
        test_info = self.test_data[test_id]
        summary = {
            'test_id': test_id,
            'status': test_info['status'],
            'content_type': test_info['content_type'],
            'platform': test_info['platform'],
            'region': test_info['region'],
            'start_time': test_info['start_time'],
            'variants': []
        }
        
        for variant in test_info['variants']:
            variant_id = variant['id']
            results = self.variant_performance[test_id][variant_id]
            
            if results:
                scores = [r['score'] for r in results]
                success_rate = sum(1 for r in results if r['success']) / len(results)
                avg_engagement = sum(r['engagement'] for r in results) / len(results)
                
                variant_summary = {
                    'id': variant_id,
                    'name': variant['name'],
                    'samples': len(results),
                    'success_rate': success_rate,
                    'avg_score': statistics.mean(scores),
                    'avg_engagement': avg_engagement,
                    'is_winner': test_info.get('winner') == variant_id
                }
            else:
                variant_summary = {
                    'id': variant_id,
                    'name': variant['name'],
                    'samples': 0,
                    'success_rate': 0,
                    'avg_score': 0,
                    'avg_engagement': 0,
                    'is_winner': False
                }
            
            summary['variants'].append(variant_summary)
        
        return summary
    
    def get_active_tests(self) -> List[Dict]:
        """Get all active A/B tests"""
        active = []
        
        for test_key, test_id in self.active_tests.items():
            if test_id in self.test_data:
                test_info = self.test_data[test_id]
                if test_info['status'] == 'active':
                    active.append(self.get_test_summary(test_id))
        
        return active
    
    def get_optimization_insights(self) -> List[str]:
        """Get insights from completed A/B tests"""
        insights = []
        
        completed_tests = [t for t in self.test_data.values() if t['status'] == 'completed']
        
        if not completed_tests:
            return ["No completed A/B tests yet - gathering data..."]
        
        # Analyze winning patterns
        winner_patterns = defaultdict(int)
        for test in completed_tests:
            winner_id = test.get('winner')
            if winner_id:
                winner_variant = next(v for v in test['variants'] if v['id'] == winner_id)
                winner_patterns[winner_variant['name']] += 1
        
        if winner_patterns:
            best_pattern = max(winner_patterns.items(), key=lambda x: x[1])
            insights.append(f"🏆 Best performing variant type: {best_pattern[0]} ({best_pattern[1]} wins)")
        
        # Platform-specific insights
        platform_winners = defaultdict(lambda: defaultdict(int))
        for test in completed_tests:
            platform = test['platform']
            winner_id = test.get('winner')
            if winner_id:
                winner_variant = next(v for v in test['variants'] if v['id'] == winner_id)
                platform_winners[platform][winner_variant['name']] += 1
        
        for platform, winners in platform_winners.items():
            if winners:
                best = max(winners.items(), key=lambda x: x[1])
                insights.append(f"📱 {platform.title()}: {best[0]} performs best")
        
        return insights[:5]  # Top 5 insights
