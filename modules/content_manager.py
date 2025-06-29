#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 Content Manager Module - BOT SHA-256
Enhanced content generator with multilingual support
"""

import os
import random
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class ContentGenerator:
    """Enhanced content generator with multilingual support"""
    
    def __init__(self):
        self.used_content_hashes = set()
        self.multilingual_templates = {
            'en': {
                'twitter': {
                    'gpu_deals': [
                        "🚨 BREAKING: AWS JUST GOT DESTROYED! 🚨\n\n💥 {gpu_count}x {gpu_type} @ ${price}/hr\n🔥 AWS charges ${aws_price}/hr (INSANE!)\n💰 YOU SAVE ${savings_amount}/hr = ${monthly_savings}/month!\n\n🎯 Code {affiliate_code} = EXTRA 5% OFF\n⚡ https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🤯 NVIDIA H100 FOR PENNIES?! 🤯\n\n💻 {gpu_count}x {gpu_type} @ ${price}/hr\n🚫 AWS: ${aws_price}/hr (ROBBERY!)\n✅ VoltageGPU: ${price}/hr (GENIUS!)\n💸 Save ${yearly_savings}/YEAR!\n\n🔥 {affiliate_code} = 5% OFF\n🚀 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🚨 GPU RENTAL HACK EXPOSED! 🚨\n\n🤫 Secret: VoltageGPU vs AWS\n💰 AWS: ${aws_price}/hr (SCAM)\n⚡ VoltageGPU: ${price}/hr (STEAL)\n🎯 {savings}% CHEAPER!\n\n🔥 Use {affiliate_code} for 5% OFF\n💎 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🔥 MILLIONAIRE AI DEVS HATE THIS TRICK! 🔥\n\n💻 {gpu_count}x {gpu_type} @ ${price}/hr\n🚫 Big Tech wants you to pay ${aws_price}/hr\n✅ Smart devs pay ${price}/hr\n💰 Save ${monthly_savings}/month!\n\n🎁 {affiliate_code} = EXTRA 5%\n🚀 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🚨 AWS CUSTOMERS ARE FURIOUS! 🚨\n\n😡 AWS: ${aws_price}/hr for {gpu_type}\n😎 VoltageGPU: ${price}/hr for SAME GPU\n💸 Difference: ${savings_amount}/hr\n🤑 Monthly savings: ${monthly_savings}\n\n🔥 Code {affiliate_code} = 5% OFF\n⚡ https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'free_vpn': [
                        "🚨 FREE VPN ALERT! 🚨\n\n🔒 100% FREE VPN included with GPU rental\n🌍 Global servers, unlimited bandwidth\n⚡ No logs, military-grade encryption\n💰 Save $10/month vs ExpressVPN\n\n🎁 Code {affiliate_code} = 5% OFF GPU\n🚀 https://voltagegpu.com/vpn?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🤯 THEY'RE GIVING AWAY FREE VPN! 🤯\n\n🔥 VoltageGPU = GPU + FREE VPN\n💸 ExpressVPN: $12.95/month\n✅ VoltageGPU VPN: $0/month\n🌍 Same features, ZERO cost!\n\n🎯 {affiliate_code} = Extra 5% OFF\n⚡ https://voltagegpu.com/vpn?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🚨 VPN COMPANIES HATE THIS TRICK! 🚨\n\n🤫 Secret: Free premium VPN\n🔒 Military encryption + no logs\n🌍 50+ countries available\n💰 $0 vs $15/month competitors\n\n🔥 Code {affiliate_code} works\n💎 https://voltagegpu.com/vpn?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'promo_earnings': [
                        "💰 I MADE $2,847 THIS MONTH! 💰\n\n🤑 VoltageGPU affiliate program\n📈 5% commission on ALL referrals\n🔥 My code: {affiliate_code}\n⚡ People save 70% vs AWS = easy sells\n\n💸 Start earning: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🚨 PASSIVE INCOME HACK EXPOSED! 🚨\n\n💻 Share GPU deals = get paid\n📊 $500-3000/month possible\n🎯 Code {affiliate_code} = your money maker\n⚡ 70% savings = customers love it\n\n🤑 Join now: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🔥 QUIT MY JOB THANKS TO THIS! 🔥\n\n💰 VoltageGPU referrals = freedom\n📈 $4,200 last month from code {affiliate_code}\n🚀 AI boom = massive demand\n⚡ 70% cheaper = instant sales\n\n💸 Your turn: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'combo_deals': [
                        "🚨 INSANE COMBO DEAL! 🚨\n\n💻 {gpu_count}x {gpu_type} @ ${price}/hr\n🔒 + FREE Premium VPN ($15/month value)\n💰 + 5% commission on referrals\n⚡ Total value: ${combo_value}/month\n\n🎁 Code {affiliate_code} = Extra 5% OFF\n🚀 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🤯 3-IN-1 DEAL NOBODY KNOWS! 🤯\n\n🖥️ Cheap GPU rental\n🔒 Free premium VPN\n💰 Earn money sharing your code\n⚡ AWS users switching daily!\n\n🔥 {affiliate_code} = Your starter code\n💎 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ]
                }
            },
            'zh': {
                'twitter': {
                    'gpu_deals': [
                        "🚨 GPU优惠警报！🚨\n\n💻 {gpu_count}x {gpu_type} @ ${price}/小时\n⚡ 比AWS便宜{savings}%\n🌍 {location} | {uptime}%正常运行时间\n\n💰 代码 {affiliate_code} = 5%折扣！\n🔗 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'free_vpn': [
                        "🚨 免费VPN警报！🚨\n\n🔒 GPU租赁包含100%免费VPN\n🌍 全球服务器，无限带宽\n⚡ 无日志，军用级加密\n💰 比ExpressVPN节省$10/月\n\n🎁 代码 {affiliate_code} = GPU额外5%折扣\n🚀 https://voltagegpu.com/vpn?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'promo_earnings': [
                        "💰 我这个月赚了$2,847！💰\n\n🤑 VoltageGPU联盟计划\n📈 所有推荐5%佣金\n🔥 我的代码：{affiliate_code}\n⚡ 比AWS便宜70% = 容易销售\n\n💸 开始赚钱: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'combo_deals': [
                        "🚨 疯狂组合优惠！🚨\n\n💻 {gpu_count}x {gpu_type} @ ${price}/小时\n🔒 + 免费高级VPN（价值$15/月）\n💰 + 推荐5%佣金\n⚡ 总价值：${combo_value}/月\n\n🎁 代码 {affiliate_code} = 额外5%折扣\n🚀 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ]
                }
            },
            'pt': {
                'twitter': {
                    'gpu_deals': [
                        "🚨 ALERTA DE OFERTA GPU! 🚨\n\n💻 {gpu_count}x {gpu_type} @ ${price}/hora\n⚡ {savings}% mais barato que AWS\n🌍 {location} | {uptime}% uptime\n\n💰 Código {affiliate_code} = 5% OFF!\n🔗 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'affiliate': [
                        "💰 ALERTA DE RENDA PASSIVA! 💰\n\n🤑 Referências GPU = fluxo de caixa constante\n📈 5% comissão por aluguel\n🔥 Código {affiliate_code} funciona globalmente\n⚡ 70% mais barato que AWS = vendas fáceis\n\n💸 Comece a ganhar: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ]
                }
            },
            'de': {
                'twitter': {
                    'gpu_deals': [
                        "🚨 GPU ANGEBOT ALARM! 🚨\n\n💻 {gpu_count}x {gpu_type} @ ${price}/Stunde\n⚡ {savings}% günstiger als AWS\n🌍 {location} | {uptime}% Verfügbarkeit\n\n💰 Code {affiliate_code} = 5% RABATT!\n🔗 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'affiliate': [
                        "💰 PASSIVES EINKOMMEN ALARM! 💰\n\n🤑 GPU Empfehlungen = stetiger Cashflow\n📈 5% Provision pro Miete\n🔥 Code {affiliate_code} funktioniert global\n⚡ 70% günstiger als AWS = einfache Verkäufe\n\n💸 Verdienen starten: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ]
                }
            }
        }
        
        # Add telegram templates for each language
        for lang in self.multilingual_templates:
            if 'telegram' not in self.multilingual_templates[lang]:
                self.multilingual_templates[lang]['telegram'] = {}
            
            # Copy all Twitter templates to Telegram
            for content_type, templates in self.multilingual_templates[lang]['twitter'].items():
                self.multilingual_templates[lang]['telegram'][content_type] = templates
        
        self.hashtag_pools = {
            'en': {
                'gpu': ['GPUDeals', 'GPURental', 'CloudGPU', 'AICompute', 'GPUCloud', 'CheapGPU', 'GPUHack', 'CloudSavings'],
                'ai': ['AI', 'MachineLearning', 'DeepLearning', 'AITraining', 'NeuralNetworks', 'ChatGPT', 'OpenAI', 'AIStartup'],
                'viral': ['ViralDeal', 'Exposed', 'Hack', 'Secret', 'Insane', 'Breaking', 'Urgent', 'Alert'],
                'money': ['PassiveIncome', 'SideHustle', 'MakeMoneyOnline', 'AffiliateMarketing', 'Entrepreneur', 'BusinessHack'],
                'vpn': ['FreeVPN', 'VPNDeal', 'Privacy', 'Security', 'Anonymous', 'VPNHack']
            },
            'zh': {
                'gpu': ['GPU交易', 'GPU租赁', '云GPU', 'AI计算', 'GPU云'],
                'ai': ['人工智能', '机器学习', '深度学习', 'AI训练', '神经网络']
            },
            'pt': {
                'gpu': ['GPUOfertas', 'GPUAluguel', 'GPUNuvem', 'ComputacaoAI', 'NuvemGPU'],
                'ai': ['IA', 'AprendizadoMaquina', 'AprendizadoProfundo', 'TreinamentoIA', 'RedesNeurais']
            },
            'de': {
                'gpu': ['GPUAngebote', 'GPUMiete', 'CloudGPU', 'AICompute', 'GPUCloud'],
                'ai': ['KI', 'MachineLearning', 'DeepLearning', 'AITraining', 'NeuralNetworks']
            }
        }
        
    def generate_unique_content(self, platform: str, content_type: str, language: str = 'en', 
                              offer: Optional[Dict] = None) -> str:
        """Generate unique multilingual content"""
        max_attempts = 10
        
        # Fallback to English if language not supported
        if language not in self.multilingual_templates:
            language = 'en'
            
        for attempt in range(max_attempts):
            try:
                templates = self.multilingual_templates[language][platform][content_type]
                template = random.choice(templates)
                
                variables = self._generate_variables(language, offer)
                content = template.format(**variables)
                
                # No timestamp suffix - removed as requested
                pass
                
                # Check uniqueness
                content_hash = hashlib.md5(content.encode()).hexdigest()
                if content_hash not in self.used_content_hashes:
                    self.used_content_hashes.add(content_hash)
                    return content
                    
            except Exception as e:
                continue
                
        # Fallback
        return self._generate_fallback_content(platform, content_type, language, offer)
        
    def _generate_variables(self, language: str, offer: Optional[Dict] = None) -> Dict:
        """Generate variables for content templates with viral pricing comparisons"""
        variables = {
            'affiliate_code': os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO'),
        }
        
        # Get hashtags for language with smart selection based on content type
        hashtag_pool = self.hashtag_pools.get(language, self.hashtag_pools['en'])
        
        # Smart hashtag selection based on content type
        if 'free_vpn' in str(variables.get('content_type', '')):
            variables['hashtag1'] = random.choice(hashtag_pool.get('vpn', hashtag_pool['gpu']))
            variables['hashtag2'] = random.choice(hashtag_pool.get('viral', hashtag_pool['ai']))
        elif 'promo_earnings' in str(variables.get('content_type', '')):
            variables['hashtag1'] = random.choice(hashtag_pool.get('money', hashtag_pool['gpu']))
            variables['hashtag2'] = random.choice(hashtag_pool.get('viral', hashtag_pool['ai']))
        else:
            variables['hashtag1'] = random.choice(hashtag_pool['gpu'])
            variables['hashtag2'] = random.choice(hashtag_pool.get('viral', hashtag_pool['ai']))
        
        if offer:
            gpu_count = offer.get('gpu_count', random.randint(4, 16))
            gpu_type = offer.get('gpu_type', random.choice(['H100', 'A100', 'RTX4090']))
            voltage_price = offer.get('price_per_hour', random.uniform(25, 45))
        else:
            gpu_count = random.randint(4, 16)
            gpu_type = random.choice(['H100', 'A100', 'RTX4090'])
            voltage_price = random.uniform(25, 45)
        
        # Calculate AWS pricing for viral comparison
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
        yearly_savings = monthly_savings * 12
        
        variables.update({
            'gpu_count': gpu_count,
            'gpu_type': gpu_type,
            'price': f"{voltage_total_price:.2f}",
            'aws_price': f"{aws_total_price:.2f}",
            'savings_amount': f"{savings_amount:.2f}",
            'monthly_savings': f"${monthly_savings:,.0f}",
            'yearly_savings': f"${yearly_savings:,.0f}",
            'savings': savings_percentage,
            'location': offer.get('location', random.choice(['Singapore', 'Mumbai', 'Frankfurt'])) if offer else random.choice(['Singapore', 'Mumbai', 'Frankfurt']),
            'uptime': f"{offer.get('uptime', random.uniform(98, 99.9)):.1f}" if offer else f"{random.uniform(98, 99.9):.1f}"
        })
            
        return variables
        
    def _generate_fallback_content(self, platform: str, content_type: str, language: str, 
                                 offer: Optional[Dict] = None) -> str:
        """Generate fallback content"""
        unique_id = str(uuid.uuid4())[:8]
        
        fallback_messages = {
            'en': f"🚀 VoltageGPU - 70% cheaper GPU rentals! Code {os.getenv('AFFILIATE_CODE', 'DEMO')} saves 5% | https://voltagegpu.com | #{unique_id}",
            'zh': f"🚀 VoltageGPU - GPU租赁便宜70%！代码 {os.getenv('AFFILIATE_CODE', 'DEMO')} 节省5% | https://voltagegpu.com | #{unique_id}",
            'pt': f"🚀 VoltageGPU - Aluguel de GPU 70% mais barato! Código {os.getenv('AFFILIATE_CODE', 'DEMO')} economiza 5% | https://voltagegpu.com | #{unique_id}",
            'de': f"🚀 VoltageGPU - 70% günstigere GPU-Miete! Code {os.getenv('AFFILIATE_CODE', 'DEMO')} spart 5% | https://voltagegpu.com | #{unique_id}"
        }
        
        return fallback_messages.get(language, fallback_messages['en'])
