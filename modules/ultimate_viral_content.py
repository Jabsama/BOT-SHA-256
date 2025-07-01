#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ULTIMATE VIRAL CONTENT GENERATOR - BOT SHA-256
UN SEUL MODULE POUR TOUS LES TWEETS ULTRA-VIRAUX
"""

import os
import random
import hashlib
from typing import Dict, List, Optional

class UltimateViralContentGenerator:
    """LE module ultime pour générer des tweets ultra-viraux"""
    
    def __init__(self):
        self.viral_templates = [
            # 🤯 PASSIVE INCOME HACKS (COURTS)
            "🤯 Made €847 last month sharing my GPU code!\n\n✅ 2-click setup\n✅ Personal code\n✅ 5% earnings\n✅ €20+ withdrawals\n✅ FREE bot\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#PassiveIncome #AI #GPU #FinTech",
            
            "💰 VoltageGPU gives EVERYONE a referral code!\n\n• 5% discount for users\n• 5% profit for code owners\n• €20 min withdrawal\n• Stripe transfers\n• FREE viral bot\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Referral #AI #GPU #FinTech",
            
            "🤖 VIRAL BOT INCLUDED: They give you an open-source bot that auto-shares your code where GPU demand is highest!\n\nSetup in 5 minutes ⚡\nAuto-targets AI communities 🎯\nMaximizes code exposure 📈\n100% legal & ethical ✅\n\nThis changes EVERYTHING!\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#ViralMarketing #OpenSource #Bot #AI #GPU #Automation #Marketing #Growth #Tech #Innovation",
            
            # 🔥 GPU DEALS ULTRA-VIRAL
            "🔥 MIND BLOWN: Just found GPU rentals for ${price}/hour while AWS charges ${aws_price}/hour for the same specs!\n\n💻 VoltageGPU features:\n✅ Account setup: 2 clicks\n✅ Personal promo code\n✅ 5% earnings on referrals\n✅ €20 min withdrawal\n✅ FREE VPN included\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#AI #GPU #CloudComputing #MachineLearning #DeepLearning #Savings #Tech #Innovation #Crypto #FinTech",
            
            "🚀 STARTUP FOUNDERS: Stop burning cash on AWS GPU costs!\n\n💸 The math:\n• AWS: ${aws_price}/hour for {gpu_type}\n• VoltageGPU: ${price}/hour (same GPU!)\n• Monthly savings: ${monthly_savings}\n• Setup time: 2 clicks\n• Personal referral code: Instant\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Startup #AI #GPU #CloudComputing #CostSaving #Founders #YCombinator #TechStartup #MachineLearning #Innovation",
            
            "💡 GENIUS HACK: Train your AI models for 80% less + earn passive income!\n\n🎯 VoltageGPU system:\n• Create account (2 clicks)\n• Get personal promo code\n• Share code = 5% earnings\n• Withdraw €20+ via Stripe\n• FREE viral bot included\n• FREE VPN bonus\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#AI #MachineLearning #GPU #PassiveIncome #Hack #Innovation #Tech #Startup #FinTech #Viral",
            
            # 🔐 VPN + SYSTEM COMBO
            "🔥 TRIPLE BONUS: VoltageGPU includes FREE open-source VPN + referral system!\n\n✅ Cheap GPU rentals\n✅ Unlimited VPN bandwidth\n✅ No logs policy\n✅ Personal promo code\n✅ 5% earnings on referrals\n✅ €20 min withdrawal\n✅ Viral bot included\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#VPN #Privacy #AI #GPU #FreeTech #Security #OpenSource #PassiveIncome #Innovation #Tech",
            
            "🤯 COMPLETE PACKAGE: GPU + VPN + Affiliate system = Money machine!\n\n💰 What you get:\n• Cheap GPU rentals (2-click setup)\n• FREE open-source VPN\n• Personal referral code\n• 5% earnings on deposits\n• Viral marketing bot\n• €20+ withdrawals via Stripe\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Complete #AI #GPU #VPN #PassiveIncome #System #Innovation #Tech #FinTech #Viral",
            
            # 💳 EASY MONEY SYSTEM
            "💳 EASIEST MONEY EVER: Hit €20, click withdraw, money in your bank via Stripe!\n\n🚫 No complex crypto wallets\n🚫 No waiting weeks\n🚫 No hidden fees\n✅ Just instant bank transfer\n✅ 2-click account setup\n✅ Personal promo code\n\nAlready withdrew €540 this month! 💰\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#EasyMoney #Stripe #BankTransfer #AI #GPU #MoneyMaking #Withdrawal #Finance #Profit #FinTech",
            
            "📊 INCOME COMPARISON:\n\nTraditional job: €15/hour ⏰\nVoltageGPU referrals: €50+/hour 💰\n\nI shared my code in 3 AI Discord servers yesterday. Already earned €187 while sleeping! 😴\n\nThe viral bot does the work! 🤖\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#IncomeComparison #PassiveIncome #AI #GPU #SideHustle #MoneyMaking #Automation #Profit #Success #FinTech",
            
            # 🧠 AI COMMUNITY FOCUSED
            "🧠 AI DEVELOPERS: Stop paying full price for GPU rentals!\n\n🎯 VoltageGPU benefits:\n• 2-click account setup\n• 5% discount with my code\n• I earn 5% when you deposit\n• You save money, I make money\n• FREE VPN included\n• Viral bot for max exposure\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#AI #MachineLearning #GPU #DeepLearning #CloudComputing #Developers #Savings #Community #Tech #Innovation",
            
            "🚀 AI COMMUNITY: VoltageGPU's viral bot finds communities and shares your code automatically!\n\n✅ Reddit AI subreddits\n✅ Discord ML servers\n✅ Twitter AI hashtags\n✅ Telegram GPU groups\n✅ 2-click setup\n✅ 5% earnings\n\nSet it and forget it! 🤖💰\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#AIcommunity #ViralMarketing #AI #GPU #OpenSource #Automation #Marketing #Growth #Bot #Tech",
            
            # 💸 SUCCESS STORIES
            "💸 SUCCESS STORY: Started with VoltageGPU 30 days ago\n\nDay 1: 2-click account setup\nDay 2: Got personal promo code\nDay 7: First €25 withdrawal\nDay 15: €150 earned\nDay 30: €847 total! 🤯\n\nThe viral bot is INSANE! 🚀\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#SuccessStory #PassiveIncome #AI #GPU #MoneyMaking #Affiliate #Growth #Profit #FinTech #Viral",
            
            "🔓 EVERYTHING IS OPEN SOURCE:\n\n✅ Viral marketing bot\n✅ VPN software\n✅ Referral tracking\n✅ 2-click account setup\n✅ Personal promo codes\n✅ €20+ withdrawals\n\nFull transparency! 👀\nCustomize everything! ⚙️\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#OpenSource #Transparency #AI #GPU #VPN #Community #Tech #Innovation #Development #Free",
            
            # 🤖 AUTOMATION FOCUS
            "🤖 AUTOMATION LEVEL: EXPERT\n\nMy VoltageGPU system runs 24/7:\n• 2-click account created ✅\n• Personal promo code active ✅\n• Viral bot finds AI communities ✅\n• Shares code automatically ✅\n• €50+ daily on autopilot! 💰\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Automation #AI #GPU #Bot #PassiveIncome #MachineLearning #FinTech #MoneyMaking #Tech #Innovation",
            
            "🌟 COMPLETE ECOSYSTEM:\n\n🖥️ Cheap GPU rentals (2-click setup)\n💰 5% referral earnings\n🤖 Viral marketing bot\n🔐 Free VPN included\n💳 Stripe withdrawals (€20+)\n📊 Real-time analytics\n\nThis is the future! 🚀\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Ecosystem #AI #GPU #VPN #FinTech #Automation #OpenSource #Innovation #Tech #Complete",
            
            # ₿ CRYPTO COMMUNITY
            "₿ CRYPTO COMMUNITY: VoltageGPU accepts crypto payments!\n\n✅ Bitcoin, Ethereum, USDT\n✅ 2-click account setup\n✅ 5% discount with my code\n✅ I earn 5% on your deposits\n✅ Perfect for mining setups\n✅ Anonymous transactions\n✅ FREE VPN included\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Crypto #Bitcoin #Ethereum #AI #GPU #Mining #Anonymous #Blockchain #FinTech #Innovation",
            
            # 👨‍💻 DEVELOPERS
            "👨‍💻 DEVELOPERS: Clone the viral bot repo and customize it!\n\n🔧 Features:\n• GitHub: Open source ✅\n• 5-minute setup ✅\n• Auto-targeting ✅\n• Performance analytics ✅\n• 2-click account creation ✅\n• Personal promo codes ✅\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Developers #OpenSource #GitHub #AI #GPU #Bot #Automation #Programming #Tech #Innovation",
            
            # 📈 SCALING STRATEGIES
            "📈 SCALING STRATEGY:\n\nWeek 1: 2-click setup + manual sharing (€50)\nWeek 2: Deploy viral bot (€200)\nWeek 3: Optimize targeting (€400)\nWeek 4: Scale to 10+ communities (€800+)\n\nThe bot does the heavy lifting! 🤖\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Scaling #Growth #AI #GPU #Bot #Strategy #PassiveIncome #Automation #FinTech #Success",
            
            # 🤯 ROI INSANE
            "🤯 INSANE ROI: €0 investment, €847 return in 30 days!\n\nHow? VoltageGPU's system:\n✅ 2-click account setup\n✅ Personal promo code\n✅ Viral bot finds AI communities\n✅ Shares code ethically\n✅ €20+ withdrawals via Stripe\n\nINFINITE ROI! 📈\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#ROI #Investment #AI #GPU #Bot #PassiveIncome #FinTech #Profit #MoneyMaking #Success",
            
            # ⚔️ VS COMPETITION
            "⚔️ VS COMPETITION:\n\nAWS: No referral program ❌\nGoogle Cloud: Complex affiliate ❌\nAzure: Corporate only ❌\n\nVoltageGPU:\n✅ 2-click setup\n✅ 5% instant earnings\n✅ Viral bot included\n✅ €20 min withdrawal\n✅ Free VPN bonus\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Competition #AWS #GoogleCloud #Azure #AI #GPU #Affiliate #Better #Innovation #Advantage",
            
            # 💬 TESTIMONIALS
            "💬 TESTIMONIAL: \"Made more with VoltageGPU referrals than my part-time job!\"\n\n✅ €1,200+ in 2 months\n✅ 10 minutes daily effort\n✅ 2-click account setup\n✅ Viral bot does everything\n✅ €20+ withdrawals\n\nJoin the revolution! 🚀\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#Testimonial #Success #AI #GPU #PassiveIncome #Revolution #MoneyMaking #FinTech #Profit #Life",
            
            # ⚡ TECH SPECS
            "⚡ TECH SPECS:\n\n🖥️ H100, A100, RTX4090 available\n💰 5% earnings on all deposits\n🤖 Open-source viral bot\n🔐 Military-grade VPN\n💳 Instant Stripe withdrawals\n📊 Real-time analytics\n⚡ 2-click setup\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#TechSpecs #H100 #A100 #RTX4090 #AI #GPU #VPN #Stripe #Analytics #Innovation",
            
            # 🔥 URGENCY
            "🔥 LAST CHANCE: VoltageGPU viral bot spots are limited!\n\nGet yours now:\n✅ 2-click account setup\n✅ Personal referral code\n✅ 5% earnings on deposits\n✅ Viral marketing bot\n✅ Free VPN access\n✅ €20+ Stripe withdrawals\n\nCode: {affiliate_code}\n{affiliate_link}\n\n#LastChance #Limited #AI #GPU #VPN #Bot #Opportunity #PassiveIncome #FinTech #Act"
        ]
        
        self.used_content_hashes = set()
    
    def generate_ultimate_viral_content(self, offer: Optional[Dict] = None) -> str:
        """Génère du contenu ultra-viral avec toutes les infos importantes"""
        
        max_attempts = 10
        
        for attempt in range(max_attempts):
            try:
                # Choisir un template aléatoire
                template = random.choice(self.viral_templates)
                
                # Générer les variables
                variables = self._generate_viral_variables(offer)
                
                # Formater le contenu
                content = template.format(**variables)
                
                # Vérifier l'unicité
                content_hash = hashlib.md5(content.encode()).hexdigest()
                if content_hash not in self.used_content_hashes:
                    self.used_content_hashes.add(content_hash)
                    
                    # Vérifier que le contenu est parfait
                    if self._validate_content(content, variables['affiliate_code']):
                        return content
                        
            except Exception as e:
                continue
        
        # Fallback si tout échoue
        return self._generate_fallback_content()
    
    def _generate_viral_variables(self, offer: Optional[Dict] = None) -> Dict:
        """Génère les variables pour les templates viraux"""
        
        # Configuration GPU
        if offer:
            gpu_count = offer.get('gpu_count', random.randint(4, 8))
            gpu_type = offer.get('gpu_type', random.choice(['H100', 'A100', 'RTX4090']))
            voltage_price = offer.get('price_per_hour', random.uniform(25, 45))
        else:
            gpu_count = random.randint(4, 8)
            gpu_type = random.choice(['H100', 'A100', 'RTX4090'])
            voltage_price = random.uniform(25, 45)
        
        # Prix AWS réalistes
        aws_prices = {
            'H100': 98.32,
            'A100': 32.77,
            'RTX4090': 24.48
        }
        
        aws_price_per_gpu = aws_prices.get(gpu_type, 30.0)
        aws_total_price = aws_price_per_gpu * gpu_count
        
        # Calculs d'économies
        savings_amount = aws_total_price - voltage_price
        monthly_savings = savings_amount * 24 * 30
        
        variables = {
            'affiliate_code': os.getenv('AFFILIATE_CODE', 'SHA-256-76360B81D39F'),
            'affiliate_link': f"https://voltagegpu.com/?ref={os.getenv('AFFILIATE_CODE', 'SHA-256-76360B81D39F')}",
            'gpu_count': gpu_count,
            'gpu_type': gpu_type,
            'price': f"{voltage_price:.2f}",
            'aws_price': f"{aws_total_price:.2f}",
            'monthly_savings': f"${monthly_savings:,.0f}",
            'location': random.choice(['Singapore', 'Mumbai', 'Frankfurt'])
        }
        
        return variables
    
    def _validate_content(self, content: str, affiliate_code: str) -> bool:
        """Valide que le contenu est parfait"""
        
        # Vérifications obligatoires
        checks = [
            affiliate_code in content,  # Code d'affiliation présent
            'https://voltagegpu.com' in content,  # Lien valide
            content.count('#') >= 3,  # Au moins 3 hashtags (réduit)
            len(content) <= 280,  # Limite Twitter
            '2-click' in content or 'personal' in content or 'viral bot' in content or '5%' in content  # Infos clés
        ]
        
        return all(checks)
    
    def _generate_fallback_content(self) -> str:
        """Génère du contenu de fallback parfait"""
        
        affiliate_code = os.getenv('AFFILIATE_CODE', 'SHA-256-76360B81D39F')
        affiliate_link = f"https://voltagegpu.com/?ref={affiliate_code}"
        
        return f"""🤯 PASSIVE INCOME HACK: Made €847 last month sharing my GPU rental code!

✅ 2-click account setup
✅ Personal promo code
✅ 5% earnings on deposits
✅ €20+ withdrawals via Stripe
✅ FREE viral bot included

Code: {affiliate_code}
{affiliate_link}

#PassiveIncome #AI #GPU #MoneyMaking #FinTech #Viral #Innovation #Tech #Automation #Success"""

    def get_content_stats(self) -> Dict:
        """Retourne les statistiques du générateur"""
        
        return {
            'total_templates': len(self.viral_templates),
            'used_content': len(self.used_content_hashes),
            'features': [
                '2-click account setup',
                'Personal promo codes',
                '5% referral earnings',
                '€20+ withdrawals via Stripe',
                'FREE viral bot included',
                'FREE VPN bonus',
                'Open source everything'
            ]
        }
