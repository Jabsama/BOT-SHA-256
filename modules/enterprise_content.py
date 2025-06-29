#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💼 Enterprise Content Module - BOT SHA-256
B2B content generation for Fortune 500, startups, and universities
"""

import random
import os
from datetime import datetime
from typing import Dict, List, Optional

class EnterpriseContentGenerator:
    """Generate high-value B2B enterprise content"""
    
    def __init__(self):
        self.enterprise_templates = {
            'fortune500': {
                'twitter': [
                    "🏢 ENTERPRISE ALERT: Fortune 500 companies are switching to VoltageGPU\n\n💰 Average savings: ${savings}/month vs AWS\n🎯 {gpu_count}x {gpu_type} clusters starting at ${price}/hr\n⚡ 99.9% uptime SLA guaranteed\n\n📊 Enterprise demo: https://voltagegpu.com/enterprise?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                    
                    "📈 CFOs LOVE THIS: {company_type} reduced cloud costs by {savings}%\n\n💻 VoltageGPU Enterprise:\n• {gpu_count}x {gpu_type} @ ${price}/hr\n• AWS equivalent: ${aws_price}/hr\n• Annual savings: ${yearly_savings}\n\n🎯 Enterprise consultation: https://voltagegpu.com/enterprise?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                    
                    "🚨 ENTERPRISE BREAKTHROUGH: Major {industry} company saves ${monthly_savings}/month\n\n⚡ VoltageGPU Enterprise Features:\n• Dedicated GPU clusters\n• 24/7 enterprise support\n• Custom SLA agreements\n• Volume discounts available\n\n📞 Book demo: https://voltagegpu.com/enterprise?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                ],
                'linkedin': [
                    "Enterprise GPU Infrastructure Revolution 🏢\n\nAfter analyzing 500+ enterprise cloud bills, the pattern is clear: companies are overpaying for GPU compute by 60-80%.\n\nVoltageGPU Enterprise offers:\n✅ {gpu_count}x {gpu_type} clusters at ${price}/hr\n✅ 99.9% uptime SLA\n✅ Dedicated account management\n✅ Custom enterprise agreements\n\nCompare this to AWS at ${aws_price}/hr - the ROI is immediate.\n\nInterested in reducing your cloud costs? Let's connect.\n\n#Enterprise #CloudCosts #GPU #AI #MachineLearning",
                    
                    "CFO Perspective: Cloud Cost Optimization 📊\n\nJust reviewed a Fortune 500 company's cloud spend:\n• Current AWS GPU costs: ${aws_price}/hr\n• VoltageGPU equivalent: ${price}/hr\n• Potential annual savings: ${yearly_savings}\n\nFor enterprises running AI/ML workloads, this represents a significant OPEX reduction without compromising performance.\n\nKey enterprise features:\n• Dedicated infrastructure\n• Enterprise SLA\n• Volume pricing\n• 24/7 support\n\nWorth exploring for any organization with substantial GPU compute needs.\n\n#CFO #CloudOptimization #EnterpriseAI #CostReduction"
                ]
            },
            'startups': {
                'twitter': [
                    "🚀 STARTUP FOUNDERS: Stop burning cash on AWS GPU costs!\n\n💸 Typical startup waste:\n• AWS: ${aws_price}/hr for {gpu_type}\n• VoltageGPU: ${price}/hr (same GPU!)\n• Monthly savings: ${monthly_savings}\n\n🎯 Use saved money for hiring, not cloud bills\n\n💰 Startup discount: {affiliate_code}\n🔗 https://voltagegpu.com/startups?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                    
                    "📈 Y COMBINATOR STARTUPS are switching to VoltageGPU\n\n🧮 The math is simple:\n• Runway extension: +{runway_months} months\n• Cost reduction: {savings}%\n• Performance: Identical to AWS\n\n🚀 More runway = more time to find PMF\n\n🎁 YC discount code: {affiliate_code}\n💻 https://voltagegpu.com/yc?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                    
                    "💡 STARTUP HACK: Train your AI models for 70% less\n\n🎯 Perfect for:\n• AI/ML startups\n• Computer vision companies\n• LLM fine-tuning\n• Research projects\n\n💰 {gpu_count}x {gpu_type} @ ${price}/hr\n⚡ Same performance as AWS at ${aws_price}/hr\n\n🚀 Startup program: https://voltagegpu.com/startups?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                ],
                'reddit': [
                    "Startup founders: How we cut our GPU costs by 70% and extended runway by 8 months\n\nAs a technical co-founder, I was spending $15K/month on AWS GPU instances for our AI training. After switching to VoltageGPU, we're now spending $4.5K/month for the same performance.\n\nThe savings allowed us to:\n• Hire 2 additional engineers\n• Extend runway by 8 months\n• Invest more in customer acquisition\n\nFor any startup doing AI/ML work, this is a no-brainer. The performance is identical, setup is straightforward, and the cost savings are massive.\n\nHappy to share more details if anyone's interested.",
                    
                    "YC startup here - VoltageGPU saved our company\n\nWe were burning through our seed funding with AWS GPU costs. $20K/month for training our computer vision models.\n\nSwitched to VoltageGPU and now paying $6K/month for the same infrastructure. That $14K/month savings literally saved our company.\n\nFor any AI startups struggling with cloud costs, seriously consider alternatives to the big cloud providers. The savings can be company-changing."
                ]
            },
            'universities': {
                'twitter': [
                    "🎓 UNIVERSITIES: Maximize your research budget with VoltageGPU\n\n📚 Perfect for:\n• PhD research projects\n• Computer science departments\n• AI/ML coursework\n• Student competitions\n\n💰 Academic pricing: {gpu_count}x {gpu_type} @ ${price}/hr\n📊 vs University AWS rates: ${aws_price}/hr\n\n🎓 Academic program: https://voltagegpu.com/academic?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                    
                    "📖 PROFESSORS: Stretch your research grants further\n\n🔬 Research-grade GPU clusters:\n• {gpu_count}x {gpu_type} available\n• ${price}/hr vs AWS ${aws_price}/hr\n• Perfect for deep learning research\n\n🎓 Academic discounts available\n📝 Grant-friendly billing\n\n📧 Academic inquiry: https://voltagegpu.com/research?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                ]
            }
        }
        
        self.enterprise_hashtags = {
            'fortune500': ['Enterprise', 'Fortune500', 'B2B', 'CloudCosts', 'CFO', 'ROI', 'EnterpriseAI'],
            'startups': ['Startup', 'YCombinator', 'Founders', 'Runway', 'StartupLife', 'TechStartup', 'AI'],
            'universities': ['Academic', 'Research', 'University', 'PhD', 'Education', 'Science', 'Students']
        }
        
        self.company_types = [
            'Fortune 500 tech company', 'Major financial institution', 'Healthcare corporation',
            'Automotive manufacturer', 'Pharmaceutical company', 'Retail giant', 'Media conglomerate'
        ]
        
        self.industries = [
            'fintech', 'healthcare', 'automotive', 'retail', 'manufacturing', 'media', 'energy'
        ]
    
    def generate_enterprise_content(self, target: str, platform: str, offer: Optional[Dict] = None) -> str:
        """Generate enterprise-focused content"""
        
        if target not in self.enterprise_templates:
            target = 'startups'  # Default fallback
            
        if platform not in self.enterprise_templates[target]:
            platform = 'twitter'  # Default fallback
            
        templates = self.enterprise_templates[target][platform]
        template = random.choice(templates)
        
        # Generate enterprise variables
        variables = self._generate_enterprise_variables(target, offer)
        
        # Format content
        content = template.format(**variables)
        
        return content
    
    def _generate_enterprise_variables(self, target: str, offer: Optional[Dict] = None) -> Dict:
        """Generate variables for enterprise content"""
        
        # Base GPU configuration
        if offer:
            gpu_count = offer.get('gpu_count', random.randint(8, 32))
            gpu_type = offer.get('gpu_type', random.choice(['H100', 'A100']))
            voltage_price = offer.get('price_per_hour', random.uniform(30, 50))
        else:
            gpu_count = random.randint(8, 32)
            gpu_type = random.choice(['H100', 'A100', 'RTX4090'])
            voltage_price = random.uniform(30, 50)
        
        # Enterprise AWS pricing (higher than consumer)
        aws_enterprise_prices = {
            'H100': 120.0,  # Enterprise rates are higher
            'A100': 45.0,
            'RTX4090': 35.0
        }
        
        aws_price_per_gpu = aws_enterprise_prices.get(gpu_type, 40.0)
        aws_total_price = aws_price_per_gpu * gpu_count
        voltage_total_price = voltage_price
        
        # Calculate enterprise savings
        savings_amount = aws_total_price - voltage_total_price
        savings_percentage = int((savings_amount / aws_total_price) * 100)
        monthly_savings = savings_amount * 24 * 30  # 24/7 usage
        yearly_savings = monthly_savings * 12
        
        # Enterprise-specific calculations
        runway_extension = int(monthly_savings / 10000)  # Months of runway per $10K saved
        combo_value = monthly_savings + random.randint(5000, 15000)  # Additional enterprise value
        
        variables = {
            'affiliate_code': os.getenv('AFFILIATE_CODE', 'SHA-256-ENTERPRISE'),
            'gpu_count': gpu_count,
            'gpu_type': gpu_type,
            'price': f"{voltage_total_price:.2f}",
            'aws_price': f"{aws_total_price:.2f}",
            'savings_amount': f"{savings_amount:.2f}",
            'monthly_savings': f"${monthly_savings:,.0f}",
            'yearly_savings': f"${yearly_savings:,.0f}",
            'savings': savings_percentage,
            'runway_months': max(runway_extension, 3),
            'combo_value': f"{combo_value:,.0f}",
            'company_type': random.choice(self.company_types),
            'industry': random.choice(self.industries)
        }
        
        # Add target-specific hashtags
        hashtags = self.enterprise_hashtags.get(target, self.enterprise_hashtags['startups'])
        variables['hashtag1'] = random.choice(hashtags)
        variables['hashtag2'] = random.choice([h for h in hashtags if h != variables['hashtag1']])
        
        return variables
    
    def get_enterprise_targets(self) -> List[str]:
        """Get available enterprise targets"""
        return list(self.enterprise_templates.keys())
    
    def get_enterprise_platforms(self, target: str) -> List[str]:
        """Get available platforms for enterprise target"""
        return list(self.enterprise_templates.get(target, {}).keys())
    
    def is_enterprise_content(self, content: str) -> bool:
        """Check if content is enterprise-focused"""
        enterprise_keywords = [
            'enterprise', 'fortune', 'cfo', 'startup', 'university', 'academic',
            'b2b', 'corporate', 'business', 'professional', 'organization'
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in enterprise_keywords)
    
    def get_enterprise_recommendations(self, target: str, time_of_day: int) -> List[str]:
        """Get enterprise content recommendations"""
        
        recommendations = []
        
        if target == 'fortune500':
            if 9 <= time_of_day <= 17:  # Business hours
                recommendations.extend([
                    "Focus on ROI and cost savings",
                    "Mention enterprise SLA and support",
                    "Use professional tone",
                    "Include specific dollar amounts"
                ])
            else:
                recommendations.extend([
                    "Share case studies and success stories",
                    "Focus on competitive advantages"
                ])
                
        elif target == 'startups':
            recommendations.extend([
                "Emphasize runway extension",
                "Mention Y Combinator and startup programs",
                "Focus on growth and scaling",
                "Use founder-friendly language"
            ])
            
        elif target == 'universities':
            recommendations.extend([
                "Highlight academic pricing",
                "Mention research applications",
                "Focus on educational value",
                "Include grant-friendly options"
            ])
        
        return recommendations[:3]  # Top 3 recommendations
