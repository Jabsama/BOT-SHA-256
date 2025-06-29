#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 Improved Content Manager Module - BOT SHA-256
Professional content generator with better quality and engagement
"""

import os
import random
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class ContentGenerator:
    """Professional content generator with improved quality"""
    
    def __init__(self):
        self.used_content_hashes = set()
        self.professional_templates = {
            'en': {
                'twitter': {
                    'gpu_deals': [
                        "💡 Cost comparison: {gpu_count}x {gpu_type} GPU cluster\n• VoltageGPU: ${price}/hour\n• AWS equivalent: ${aws_price}/hour\n• Savings: {savings}% for AI training workloads\nPerfect for researchers on a budget! #AI #MachineLearning",
                        
                        "🧠 GPU Economics 101: Why decentralized computing matters\nTraditional cloud: ${aws_price}/hour for {gpu_type}s\nDecentralized networks: ${price}/hour\nThe math is simple for AI researchers and startups.\nWhat's your experience with GPU costs? #AI #CloudComputing",
                        
                        "📊 Real-world GPU pricing analysis:\n{gpu_count}x {gpu_type} configuration\n🔹 AWS: ${aws_price}/hr\n🔹 VoltageGPU: ${price}/hr\n🔹 Monthly savings: ${monthly_savings}\nGreat for ML experimentation! #MachineLearning #GPU",
                        
                        "🚀 Found an interesting GPU deal for AI training:\n{gpu_count}x {gpu_type} at ${price}/hour in {location}\nUptime: {uptime}% | Significant cost savings vs traditional cloud\nAnyone else exploring decentralized GPU networks? #AI #DeepLearning",
                        
                        "💰 Budget-friendly AI infrastructure:\n{gpu_count}x {gpu_type} clusters starting at ${price}/hour\nCompare that to ${aws_price}/hour on traditional platforms\nPerfect for startups and researchers! #AI #Startup #MachineLearning"
                    ],
                    'educational': [
                        "🧠 Understanding GPU rental economics:\nWhy are decentralized networks 60-80% cheaper?\n• No enterprise markup\n• Direct peer-to-peer access\n• Efficient resource utilization\nThoughts on this trend? #AI #CloudComputing",
                        
                        "📚 AI Training Cost Optimization 101:\n1. Compare hourly rates across providers\n2. Consider uptime and reliability\n3. Factor in data transfer costs\n4. Test with small workloads first\nWhat's your optimization strategy? #MachineLearning #AI",
                        
                        "🔍 GPU architecture comparison for AI workloads:\nH100: Best for large language models\nA100: Versatile for most ML tasks\nRTX4090: Cost-effective for experimentation\nWhich do you prefer for your projects? #AI #GPU",
                        
                        "💡 Pro tip: GPU rental cost calculation\nHourly rate × Training time × Number of experiments\nExample: ${price}/hr × 10hrs × 5 experiments = ${total_cost}\nAlways budget for multiple iterations! #MachineLearning #AI"
                    ],
                    'community': [
                        "🤔 Question for the AI community:\nWhat's your biggest challenge with GPU costs for training?\nI've been exploring alternatives to traditional cloud providers.\nShare your experiences! #AI #MachineLearning #Community",
                        
                        "📈 Interesting trend: More researchers switching to decentralized GPU networks\nReasons I'm hearing:\n• 60-80% cost savings\n• Better availability\n• More flexible pricing\nWhat's driving your infrastructure decisions? #AI #Research",
                        
                        "🎯 Poll: What's your monthly GPU budget for AI projects?\nA) Under $500\nB) $500-2000\nC) $2000-5000\nD) Over $5000\nCurious about the community's spending patterns! #AI #MachineLearning #Poll",
                        
                        "💬 Discussion: Future of AI infrastructure\nWith GPU demand skyrocketing, what solutions are you exploring?\n• Traditional cloud (AWS, GCP, Azure)\n• Decentralized networks\n• On-premise hardware\nLet's discuss! #AI #Infrastructure"
                    ]
                },
                'telegram': {
                    'gpu_deals': [
                        "🔥 GPU Deal Alert!\n\n💻 {gpu_count}x {gpu_type} available\n💰 Price: ${price}/hour\n📍 Location: {location}\n⚡ Uptime: {uptime}%\n\nCompare to AWS: ${aws_price}/hour\nSavings: {savings}%\n\nGreat for AI training and research!\nCode: {affiliate_code}\n🔗 https://voltagegpu.com/?ref={affiliate_code}",
                        
                        "💡 Cost-Effective AI Infrastructure\n\nFound: {gpu_count}x {gpu_type} cluster\n💵 ${price}/hour vs ${aws_price}/hour (AWS)\n📊 Monthly savings: ${monthly_savings}\n🌍 {location} datacenter\n\nPerfect for:\n• Machine learning training\n• AI research projects\n• Model fine-tuning\n\nUse code: {affiliate_code}\n🚀 https://voltagegpu.com/?ref={affiliate_code}",
                        
                        "🧠 AI Researchers, Check This Out!\n\n{gpu_count}x {gpu_type} GPUs available\n⚡ ${price}/hour (vs ${aws_price}/hour traditional cloud)\n📈 {savings}% savings for your projects\n🌐 {location} | {uptime}% uptime\n\nIdeal for deep learning workloads\nAffiliate code: {affiliate_code}\n💻 https://voltagegpu.com/?ref={affiliate_code}"
                    ],
                    'educational': [
                        "📚 GPU Rental Guide for AI Developers\n\n🔍 What to look for:\n• Competitive hourly rates\n• High uptime (>99%)\n• Fast interconnects\n• Flexible billing\n\n💡 Pro tip: Always test with small workloads first\n\nCurrent deal: {gpu_count}x {gpu_type} @ ${price}/hr\nCode: {affiliate_code}\n🔗 https://voltagegpu.com/?ref={affiliate_code}",
                        
                        "🧠 Understanding GPU Economics\n\nWhy decentralized networks cost less:\n• No enterprise markup\n• Direct peer-to-peer access\n• Efficient resource sharing\n• Lower operational overhead\n\nExample: {gpu_type} cluster\n• Traditional: ${aws_price}/hr\n• Decentralized: ${price}/hr\n• Your savings: {savings}%\n\nTry it: {affiliate_code}\n🚀 https://voltagegpu.com/?ref={affiliate_code}"
                    ]
                }
            }
        }
        
        self.hashtag_pools = {
            'en': {
                'ai': ['AI', 'MachineLearning', 'DeepLearning', 'AIResearch', 'NeuralNetworks', 'DataScience'],
                'gpu': ['GPU', 'CloudComputing', 'AIInfrastructure', 'HPC', 'Computing'],
                'business': ['Startup', 'Research', 'Innovation', 'Technology', 'CostOptimization'],
                'community': ['Community', 'Discussion', 'Poll', 'Question', 'Experience']
            }
        }
        
    def generate_unique_content(self, platform: str, content_type: str, language: str = 'en', 
                              offer: Optional[Dict] = None) -> str:
        """Generate professional, engaging content"""
        max_attempts = 10
        
        # Map old content types to new professional ones
        content_type_mapping = {
            'gpu_deals': 'gpu_deals',
            'free_vpn': 'educational',
            'promo_earnings': 'community',
            'combo_deals': 'gpu_deals'
        }
        
        mapped_type = content_type_mapping.get(content_type, 'gpu_deals')
        
        # Fallback to English if language not supported
        if language not in self.professional_templates:
            language = 'en'
            
        for attempt in range(max_attempts):
            try:
                templates = self.professional_templates[language][platform][mapped_type]
                template = random.choice(templates)
                
                variables = self._generate_variables(language, offer, mapped_type)
                content = template.format(**variables)
                
                # Check uniqueness
                content_hash = hashlib.md5(content.encode()).hexdigest()
                if content_hash not in self.used_content_hashes:
                    self.used_content_hashes.add(content_hash)
                    return content
                    
            except Exception as e:
                continue
                
        # Fallback
        return self._generate_fallback_content(platform, content_type, language, offer)
        
    def _generate_variables(self, language: str, offer: Optional[Dict] = None, content_type: str = 'gpu_deals') -> Dict:
        """Generate variables for professional content templates"""
        variables = {
            'affiliate_code': os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO'),
        }
        
        if offer:
            gpu_count = offer.get('gpu_count', random.randint(4, 16))
            gpu_type = offer.get('gpu_type', random.choice(['H100', 'A100', 'RTX4090']))
            voltage_price = offer.get('price_per_hour', random.uniform(25, 45))
        else:
            gpu_count = random.randint(4, 16)
            gpu_type = random.choice(['H100', 'A100', 'RTX4090'])
            voltage_price = random.uniform(25, 45)
        
        # Calculate realistic AWS pricing for comparison
        aws_prices = {
            'H100': 98.32,  # AWS p5.48xlarge per hour
            'A100': 32.77,  # AWS p4d.24xlarge per hour  
            'RTX4090': 24.48  # AWS g5.48xlarge per hour
        }
        
        aws_price_per_gpu = aws_prices.get(gpu_type, 30.0)
        aws_total_price = aws_price_per_gpu * gpu_count
        voltage_total_price = voltage_price
        
        savings_amount = aws_total_price - voltage_total_price
        savings_percentage = int((savings_amount / aws_total_price) * 100)
        monthly_savings = savings_amount * 24 * 30  # 24h/day * 30 days
        total_cost = voltage_price * 10 * 5  # Example calculation for educational content
        
        variables.update({
            'gpu_count': gpu_count,
            'gpu_type': gpu_type,
            'price': f"{voltage_total_price:.2f}",
            'aws_price': f"{aws_total_price:.2f}",
            'savings_amount': f"{savings_amount:.2f}",
            'monthly_savings': f"${monthly_savings:,.0f}",
            'savings': savings_percentage,
            'total_cost': f"${total_cost:.0f}",
            'location': offer.get('location', random.choice(['Singapore', 'Mumbai', 'Frankfurt'])) if offer else random.choice(['Singapore', 'Mumbai', 'Frankfurt']),
            'uptime': f"{offer.get('uptime', random.uniform(98, 99.9)):.1f}" if offer else f"{random.uniform(98, 99.9):.1f}"
        })
            
        return variables
        
    def _generate_fallback_content(self, platform: str, content_type: str, language: str, 
                                 offer: Optional[Dict] = None) -> str:
        """Generate professional fallback content"""
        unique_id = str(uuid.uuid4())[:8]
        
        fallback_messages = {
            'en': f"💡 Exploring cost-effective GPU solutions for AI training. VoltageGPU offers competitive rates vs traditional cloud providers. Code {os.getenv('AFFILIATE_CODE', 'DEMO')} for additional savings. https://voltagegpu.com #AI #MachineLearning",
        }
        
        return fallback_messages.get(language, fallback_messages['en'])
