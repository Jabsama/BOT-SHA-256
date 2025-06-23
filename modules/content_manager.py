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
                        "🚨 GPU DEAL ALERT! 🚨\n\n💻 {gpu_count}x {gpu_type} @ ${price}/hr\n⚡ {savings}% cheaper than AWS\n🌍 {location} | {uptime}% uptime\n\n💰 Code {affiliate_code} = 5% OFF!\n🔗 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}",
                        "🔥 INSANE GPU PRICING! 🔥\n\n🖥️ {gpu_count}x {gpu_type} for ${price}/hour\n💸 Save {savings}% vs traditional cloud\n📍 {location} datacenter | {uptime}% SLA\n\n🎁 Exclusive: {affiliate_code} for 5% discount\n🚀 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'affiliate': [
                        "💰 PASSIVE INCOME ALERT! 💰\n\n🤑 GPU referrals = steady cash flow\n📈 5% commission per rental\n🔥 Code {affiliate_code} works globally\n⚡ 70% cheaper than AWS = easy sells\n\n💸 Start earning: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ]
                }
            },
            'zh': {
                'twitter': {
                    'gpu_deals': [
                        "🚨 GPU优惠警报！🚨\n\n💻 {gpu_count}x {gpu_type} @ ${price}/小时\n⚡ 比AWS便宜{savings}%\n🌍 {location} | {uptime}%正常运行时间\n\n💰 代码 {affiliate_code} = 5%折扣！\n🔗 https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
                    ],
                    'affiliate': [
                        "💰 被动收入警报！💰\n\n🤑 GPU推荐 = 稳定现金流\n📈 每次租赁5%佣金\n🔥 代码 {affiliate_code} 全球有效\n⚡ 比AWS便宜70% = 容易销售\n\n💸 开始赚钱: https://voltagegpu.com/?ref={affiliate_code}\n\n#{hashtag1} #{hashtag2}"
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
                self.multilingual_templates[lang]['telegram'] = {
                    'gpu_deals': self.multilingual_templates[lang]['twitter']['gpu_deals'],
                    'affiliate': self.multilingual_templates[lang]['twitter']['affiliate']
                }
        
        self.hashtag_pools = {
            'en': {
                'gpu': ['GPUDeals', 'GPURental', 'CloudGPU', 'AICompute', 'GPUCloud'],
                'ai': ['AI', 'MachineLearning', 'DeepLearning', 'AITraining', 'NeuralNetworks']
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
                
                # Add unique timestamp for Twitter
                if platform == 'twitter':
                    unique_suffix = f"\n\n⏰ {datetime.now().strftime('%H:%M')}"
                    if len(content + unique_suffix) <= 280:
                        content += unique_suffix
                
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
        """Generate variables for content templates"""
        variables = {
            'affiliate_code': os.getenv('AFFILIATE_CODE', 'SHA-256-DEMO'),
        }
        
        # Get hashtags for language
        hashtag_pool = self.hashtag_pools.get(language, self.hashtag_pools['en'])
        variables['hashtag1'] = random.choice(hashtag_pool['gpu'])
        variables['hashtag2'] = random.choice(hashtag_pool['ai'])
        
        if offer:
            variables.update({
                'gpu_count': offer.get('gpu_count', random.randint(4, 16)),
                'gpu_type': offer.get('gpu_type', random.choice(['H100', 'A100', 'RTX4090'])),
                'price': f"{offer.get('price_per_hour', random.uniform(25, 45)):.2f}",
                'location': offer.get('location', random.choice(['Singapore', 'Mumbai', 'Frankfurt'])),
                'uptime': f"{offer.get('uptime', random.uniform(98, 99.9)):.1f}",
                'savings': random.randint(60, 75)
            })
        else:
            variables.update({
                'gpu_count': random.randint(4, 16),
                'gpu_type': random.choice(['H100', 'A100', 'RTX4090']),
                'price': f"{random.uniform(25, 45):.2f}",
                'location': random.choice(['Singapore', 'Mumbai', 'Frankfurt']),
                'uptime': f"{random.uniform(98, 99.9):.1f}",
                'savings': random.randint(60, 75)
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
