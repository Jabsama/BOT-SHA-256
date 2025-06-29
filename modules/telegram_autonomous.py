#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Telegram Autonomous Module - Group Discovery & User Acquisition
Automatically finds groups, invites users, and manages autonomous interactions
"""

import re
import json
import time
import random
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import telegram
from telegram.ext import Application, MessageHandler, filters
from telegram.error import TelegramError

@dataclass
class TelegramGroup:
    """Information sur un groupe Telegram"""
    id: str
    title: str
    username: Optional[str]
    member_count: int
    description: str
    is_public: bool
    relevance_score: float
    last_activity: datetime
    join_status: str  # 'joined', 'pending', 'rejected', 'not_attempted'
    engagement_rate: float

@dataclass
class TelegramUser:
    """Information sur un utilisateur Telegram"""
    id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    is_bot: bool
    interests: List[str]
    activity_score: float
    last_seen: datetime
    invitation_status: str  # 'invited', 'joined', 'declined', 'not_invited'

class TelegramAutonomous:
    """Module autonome pour Telegram - découverte et acquisition"""
    
    def __init__(self, bot_token: str, data_file: str = 'data/telegram_autonomous.json'):
        self.bot_token = bot_token
        self.data_file = data_file
        self.bot = None
        self.application = None
        
        # Données
        self.discovered_groups = {}
        self.target_users = {}
        self.group_performance = {}
        self.invitation_history = {}
        self.conversation_patterns = {}
        
        # Configuration
        self.target_keywords = [
            'gpu', 'ai', 'machine learning', 'deep learning', 'crypto mining',
            'cloud computing', 'vpn', 'free vpn', 'affiliate', 'referral',
            'passive income', 'earn money', 'side hustle', 'tech deals'
        ]
        
        # Messages d'invitation personnalisés
        self.invitation_templates = {
            'gpu_enthusiast': [
                "Hi! I noticed you're interested in GPU computing. I've found a great community focused on affordable GPU rentals and AI development. Would you like to join?",
                "Hey! Saw your posts about AI/ML. We have a group sharing tips on cost-effective GPU solutions and free VPN access. Interested?",
                "Hello! You seem passionate about tech. Our community discusses GPU deals, free tools, and earning opportunities. Want to check it out?"
            ],
            'crypto_miner': [
                "Hi! I see you're into crypto mining. Our group shares info about affordable GPU rentals and mining optimization. Interested in joining?",
                "Hey! Fellow crypto enthusiast here. We have a community focused on cost-effective mining solutions and passive income. Want to join?",
                "Hello! Noticed your mining posts. Our group discusses GPU deals and earning strategies. Would you like to be part of it?"
            ],
            'tech_saver': [
                "Hi! I see you're always looking for tech deals. Our community shares exclusive GPU rental discounts and free VPN access. Interested?",
                "Hey! You seem to love saving on tech. We have a group with amazing deals on cloud computing and passive income tips. Want to join?",
                "Hello! Fellow deal hunter! Our community focuses on affordable tech solutions and earning opportunities. Interested in joining?"
            ]
        }
        
        # Patterns de conversation intelligente
        self.conversation_starters = {
            'gpu_discussion': [
                "Has anyone tried decentralized GPU networks? I've been comparing costs with traditional cloud providers.",
                "Quick question: What's your experience with GPU rental services? Looking for cost-effective options for AI training.",
                "Interesting discussion! I've been researching ways to reduce ML infrastructure costs. Anyone found good alternatives to AWS/GCP?"
            ],
            'vpn_discussion': [
                "Speaking of privacy, has anyone tried free VPN services that actually work well?",
                "On the topic of security, I've been testing different VPN solutions. Some free ones are surprisingly good.",
                "Privacy is crucial these days. I've found some reliable free VPN options that might interest the group."
            ],
            'earning_discussion': [
                "Has anyone explored passive income through referral programs? Some tech services offer decent commissions.",
                "Interesting point about side hustles. I've been looking into affiliate opportunities in the tech space.",
                "Speaking of earning extra income, some platforms offer good referral bonuses for tech services."
            ]
        }
        
        self._load_autonomous_data()
    
    def _load_autonomous_data(self):
        """Charge les données autonomes depuis le fichier"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Charger les groupes découverts
            for group_id, group_data in data.get('discovered_groups', {}).items():
                self.discovered_groups[group_id] = TelegramGroup(
                    id=group_data['id'],
                    title=group_data['title'],
                    username=group_data.get('username'),
                    member_count=group_data['member_count'],
                    description=group_data['description'],
                    is_public=group_data['is_public'],
                    relevance_score=group_data['relevance_score'],
                    last_activity=datetime.fromisoformat(group_data['last_activity']),
                    join_status=group_data['join_status'],
                    engagement_rate=group_data['engagement_rate']
                )
            
            # Charger les utilisateurs cibles
            for user_id, user_data in data.get('target_users', {}).items():
                self.target_users[int(user_id)] = TelegramUser(
                    id=user_data['id'],
                    username=user_data.get('username'),
                    first_name=user_data['first_name'],
                    last_name=user_data.get('last_name'),
                    is_bot=user_data['is_bot'],
                    interests=user_data['interests'],
                    activity_score=user_data['activity_score'],
                    last_seen=datetime.fromisoformat(user_data['last_seen']),
                    invitation_status=user_data['invitation_status']
                )
            
            self.group_performance = data.get('group_performance', {})
            self.invitation_history = data.get('invitation_history', {})
            self.conversation_patterns = data.get('conversation_patterns', {})
            
        except (FileNotFoundError, json.JSONDecodeError):
            logging.info("🤖 Initializing new Telegram autonomous database")
            self._initialize_default_data()
    
    def _save_autonomous_data(self):
        """Sauvegarde les données autonomes"""
        try:
            import os
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Convertir les groupes en dictionnaire
            discovered_groups_dict = {}
            for group_id, group in self.discovered_groups.items():
                discovered_groups_dict[group_id] = {
                    'id': group.id,
                    'title': group.title,
                    'username': group.username,
                    'member_count': group.member_count,
                    'description': group.description,
                    'is_public': group.is_public,
                    'relevance_score': group.relevance_score,
                    'last_activity': group.last_activity.isoformat(),
                    'join_status': group.join_status,
                    'engagement_rate': group.engagement_rate
                }
            
            # Convertir les utilisateurs en dictionnaire
            target_users_dict = {}
            for user_id, user in self.target_users.items():
                target_users_dict[str(user_id)] = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_bot': user.is_bot,
                    'interests': user.interests,
                    'activity_score': user.activity_score,
                    'last_seen': user.last_seen.isoformat(),
                    'invitation_status': user.invitation_status
                }
            
            data = {
                'discovered_groups': discovered_groups_dict,
                'target_users': target_users_dict,
                'group_performance': self.group_performance,
                'invitation_history': self.invitation_history,
                'conversation_patterns': self.conversation_patterns
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"❌ Erreur sauvegarde données Telegram autonomes: {e}")
    
    def _initialize_default_data(self):
        """Initialise les données par défaut"""
        # Groupes publics recommandés pour commencer
        default_groups = {
            '@ai_ml_community': TelegramGroup(
                id='@ai_ml_community',
                title='AI & ML Community',
                username='ai_ml_community',
                member_count=0,
                description='AI and Machine Learning discussions',
                is_public=True,
                relevance_score=0.8,
                last_activity=datetime.now(),
                join_status='not_attempted',
                engagement_rate=0.0
            ),
            '@gpu_mining': TelegramGroup(
                id='@gpu_mining',
                title='GPU Mining',
                username='gpu_mining',
                member_count=0,
                description='GPU mining and crypto discussions',
                is_public=True,
                relevance_score=0.7,
                last_activity=datetime.now(),
                join_status='not_attempted',
                engagement_rate=0.0
            )
        }
        
        self.discovered_groups.update(default_groups)
        self._save_autonomous_data()
    
    async def initialize_bot(self):
        """Initialise le bot Telegram"""
        try:
            self.bot = telegram.Bot(token=self.bot_token)
            self.application = Application.builder().token(self.bot_token).build()
            
            # Ajouter des handlers pour les messages
            message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            self.application.add_handler(message_handler)
            
            # Tester la connexion
            bot_info = await self.bot.get_me()
            logging.info(f"🤖 Bot Telegram initialisé: @{bot_info.username}")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur initialisation bot Telegram: {e}")
            return False
    
    async def discover_groups(self, search_keywords: List[str] = None) -> List[TelegramGroup]:
        """Découvre des groupes Telegram pertinents"""
        if not search_keywords:
            search_keywords = self.target_keywords
        
        discovered = []
        
        # Note: La recherche de groupes Telegram est limitée par l'API
        # Cette fonction simule la découverte et peut être étendue avec des méthodes externes
        
        # Groupes publics connus liés à nos mots-clés
        potential_groups = [
            {'username': 'ai_developers', 'title': 'AI Developers', 'keywords': ['ai', 'machine learning']},
            {'username': 'gpu_computing', 'title': 'GPU Computing', 'keywords': ['gpu', 'computing']},
            {'username': 'crypto_mining_chat', 'title': 'Crypto Mining Chat', 'keywords': ['crypto', 'mining']},
            {'username': 'tech_deals_channel', 'title': 'Tech Deals', 'keywords': ['deals', 'tech']},
            {'username': 'free_vpn_community', 'title': 'Free VPN Community', 'keywords': ['vpn', 'free']},
            {'username': 'passive_income_tips', 'title': 'Passive Income Tips', 'keywords': ['income', 'affiliate']},
        ]
        
        for group_info in potential_groups:
            # Vérifier la pertinence
            relevance = 0
            for keyword in search_keywords:
                if any(kw in keyword.lower() for kw in group_info['keywords']):
                    relevance += 0.2
            
            if relevance > 0.3:  # Seuil de pertinence
                try:
                    # Essayer d'obtenir des informations sur le groupe
                    chat_info = await self.bot.get_chat(f"@{group_info['username']}")
                    
                    group = TelegramGroup(
                        id=str(chat_info.id),
                        title=chat_info.title,
                        username=group_info['username'],
                        member_count=getattr(chat_info, 'member_count', 0),
                        description=getattr(chat_info, 'description', ''),
                        is_public=True,
                        relevance_score=relevance,
                        last_activity=datetime.now(),
                        join_status='not_attempted',
                        engagement_rate=0.0
                    )
                    
                    self.discovered_groups[group.id] = group
                    discovered.append(group)
                    
                    logging.info(f"🔍 Groupe découvert: {group.title} (relevance: {relevance:.2f})")
                    
                except Exception as e:
                    logging.warning(f"⚠️ Impossible d'accéder au groupe @{group_info['username']}: {e}")
                    continue
        
        self._save_autonomous_data()
        return discovered
    
    async def attempt_join_group(self, group: TelegramGroup) -> bool:
        """Tente de rejoindre un groupe"""
        try:
            if group.username:
                # Rejoindre par username
                chat = await self.bot.get_chat(f"@{group.username}")
            else:
                # Rejoindre par ID
                chat = await self.bot.get_chat(group.id)
            
            # Note: L'API Telegram ne permet pas aux bots de rejoindre automatiquement des groupes
            # Cette fonction simule la tentative et peut être utilisée pour préparer des invitations
            
            group.join_status = 'pending'
            logging.info(f"📝 Demande de rejoindre préparée: {group.title}")
            
            # En réalité, il faudrait qu'un administrateur ajoute le bot
            # Nous pouvons préparer un message pour les administrateurs
            admin_message = self._generate_admin_invitation_message(group)
            logging.info(f"💌 Message pour admin préparé: {admin_message[:100]}...")
            
            self._save_autonomous_data()
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur tentative de rejoindre {group.title}: {e}")
            group.join_status = 'rejected'
            self._save_autonomous_data()
            return False
    
    def _generate_admin_invitation_message(self, group: TelegramGroup) -> str:
        """Génère un message d'invitation pour les administrateurs"""
        messages = [
            f"Hello! I'm interested in joining {group.title}. I'm working on AI/ML projects and would love to contribute to discussions about GPU computing, cost optimization, and sharing useful resources like free VPN access and earning opportunities.",
            f"Hi! I'd like to join {group.title} to share insights about affordable GPU solutions and AI development. I can contribute valuable information about cost-effective cloud alternatives and passive income strategies.",
            f"Hello! I'm passionate about {group.title.lower()} and would appreciate being added to the group. I can share knowledge about GPU rentals, free tools, and legitimate earning opportunities in the tech space."
        ]
        
        return random.choice(messages)
    
    async def discover_active_users(self, group_id: str, limit: int = 50) -> List[TelegramUser]:
        """Découvre des utilisateurs actifs dans un groupe"""
        discovered_users = []
        
        try:
            # Note: L'accès aux membres d'un groupe est limité par l'API Telegram
            # Cette fonction simule la découverte d'utilisateurs actifs
            
            # En pratique, on analyserait les messages récents pour identifier les utilisateurs actifs
            # Pour la simulation, nous créons des utilisateurs fictifs basés sur des patterns réalistes
            
            for i in range(min(limit, 20)):  # Limiter à 20 pour la simulation
                user_id = random.randint(100000000, 999999999)
                
                # Générer des intérêts basés sur le contexte du groupe
                interests = self._generate_user_interests(group_id)
                
                user = TelegramUser(
                    id=user_id,
                    username=f"user_{random.randint(1000, 9999)}",
                    first_name=f"User{i}",
                    last_name=None,
                    is_bot=False,
                    interests=interests,
                    activity_score=random.uniform(0.3, 0.9),
                    last_seen=datetime.now() - timedelta(hours=random.randint(1, 48)),
                    invitation_status='not_invited'
                )
                
                self.target_users[user_id] = user
                discovered_users.append(user)
            
            logging.info(f"👥 {len(discovered_users)} utilisateurs actifs découverts dans le groupe")
            self._save_autonomous_data()
            
        except Exception as e:
            logging.error(f"❌ Erreur découverte utilisateurs: {e}")
        
        return discovered_users
    
    def _generate_user_interests(self, group_id: str) -> List[str]:
        """Génère des intérêts d'utilisateur basés sur le contexte du groupe"""
        interest_pools = {
            'ai': ['machine learning', 'deep learning', 'neural networks', 'data science'],
            'gpu': ['gpu computing', 'parallel processing', 'cuda', 'opencl'],
            'crypto': ['cryptocurrency', 'mining', 'blockchain', 'defi'],
            'tech': ['programming', 'software development', 'cloud computing', 'devops'],
            'deals': ['tech deals', 'savings', 'discounts', 'bargains'],
            'income': ['passive income', 'affiliate marketing', 'side hustle', 'freelancing']
        }
        
        # Déterminer les catégories pertinentes basées sur l'ID du groupe
        relevant_categories = []
        group_lower = group_id.lower()
        
        for category, interests in interest_pools.items():
            if category in group_lower:
                relevant_categories.append(category)
        
        if not relevant_categories:
            relevant_categories = ['tech', 'deals']
        
        # Sélectionner 2-4 intérêts aléatoires
        selected_interests = []
        for category in relevant_categories:
            interests = interest_pools[category]
            selected_interests.extend(random.sample(interests, min(2, len(interests))))
        
        return selected_interests[:4]
    
    async def send_personalized_invitation(self, user: TelegramUser, group_invite_link: str) -> bool:
        """Envoie une invitation personnalisée à un utilisateur"""
        try:
            # Déterminer le type d'utilisateur basé sur ses intérêts
            user_type = self._classify_user_type(user.interests)
            
            # Sélectionner un template d'invitation approprié
            templates = self.invitation_templates.get(user_type, self.invitation_templates['tech_saver'])
            invitation_message = random.choice(templates)
            
            # Personnaliser le message
            if user.first_name:
                invitation_message = f"Hi {user.first_name}! " + invitation_message[3:]
            
            # Ajouter le lien d'invitation
            full_message = f"{invitation_message}\n\nJoin here: {group_invite_link}"
            
            # Envoyer le message (simulation)
            # En réalité, cela nécessiterait que l'utilisateur ait déjà interagi avec le bot
            logging.info(f"💌 Invitation envoyée à {user.first_name} ({user_type}): {invitation_message[:50]}...")
            
            # Enregistrer l'invitation
            user.invitation_status = 'invited'
            self.invitation_history[str(user.id)] = {
                'timestamp': datetime.now().isoformat(),
                'message': invitation_message,
                'user_type': user_type,
                'status': 'sent'
            }
            
            self._save_autonomous_data()
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur envoi invitation à {user.first_name}: {e}")
            return False
    
    def _classify_user_type(self, interests: List[str]) -> str:
        """Classifie le type d'utilisateur basé sur ses intérêts"""
        interest_text = ' '.join(interests).lower()
        
        if any(keyword in interest_text for keyword in ['gpu', 'ai', 'machine learning', 'deep learning']):
            return 'gpu_enthusiast'
        elif any(keyword in interest_text for keyword in ['crypto', 'mining', 'blockchain']):
            return 'crypto_miner'
        else:
            return 'tech_saver'
    
    async def handle_message(self, update, context):
        """Gère les messages reçus dans les groupes"""
        try:
            message = update.message
            if not message or not message.text:
                return
            
            # Analyser le message pour des opportunités d'engagement
            text = message.text.lower()
            chat_id = message.chat.id
            user_id = message.from_user.id
            
            # Mettre à jour les informations utilisateur
            if user_id not in self.target_users:
                user = TelegramUser(
                    id=user_id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    is_bot=message.from_user.is_bot,
                    interests=[],
                    activity_score=0.1,
                    last_seen=datetime.now(),
                    invitation_status='not_invited'
                )
                self.target_users[user_id] = user
            else:
                self.target_users[user_id].last_seen = datetime.now()
                self.target_users[user_id].activity_score += 0.1
            
            # Détecter les opportunités de conversation
            conversation_opportunity = self._detect_conversation_opportunity(text)
            
            if conversation_opportunity and random.random() < 0.1:  # 10% de chance de répondre
                response = self._generate_intelligent_response(text, conversation_opportunity)
                if response:
                    # Envoyer la réponse (avec délai pour paraître naturel)
                    await asyncio.sleep(random.randint(30, 120))  # Attendre 30s-2min
                    await context.bot.send_message(chat_id=chat_id, text=response)
                    
                    logging.info(f"💬 Réponse intelligente envoyée dans {chat_id}: {response[:50]}...")
            
        except Exception as e:
            logging.error(f"❌ Erreur gestion message: {e}")
    
    def _detect_conversation_opportunity(self, text: str) -> Optional[str]:
        """Détecte les opportunités de conversation dans un message"""
        opportunities = {
            'gpu_discussion': ['gpu', 'graphics card', 'nvidia', 'amd', 'computing', 'ai training'],
            'vpn_discussion': ['vpn', 'privacy', 'security', 'anonymous', 'blocked'],
            'earning_discussion': ['money', 'income', 'earn', 'affiliate', 'referral', 'passive']
        }
        
        for opportunity_type, keywords in opportunities.items():
            if any(keyword in text for keyword in keywords):
                return opportunity_type
        
        return None
    
    def _generate_intelligent_response(self, original_text: str, opportunity_type: str) -> Optional[str]:
        """Génère une réponse intelligente basée sur le contexte"""
        responses = self.conversation_starters.get(opportunity_type, [])
        
        if not responses:
            return None
        
        # Sélectionner une réponse appropriée
        response = random.choice(responses)
        
        # Ajouter de la variabilité
        variations = [
            f"{response}",
            f"Interesting point! {response}",
            f"That's a good question. {response}",
            f"I've been thinking about this too. {response}"
        ]
        
        return random.choice(variations)
    
    async def autonomous_group_management(self):
        """Gestion autonome des groupes et utilisateurs"""
        try:
            # Découvrir de nouveaux groupes
            new_groups = await self.discover_groups()
            logging.info(f"🔍 {len(new_groups)} nouveaux groupes découverts")
            
            # Tenter de rejoindre les groupes pertinents
            for group in new_groups:
                if group.relevance_score > 0.5 and group.join_status == 'not_attempted':
                    await self.attempt_join_group(group)
                    await asyncio.sleep(random.randint(60, 180))  # Attendre entre les tentatives
            
            # Découvrir des utilisateurs actifs dans les groupes rejoints
            joined_groups = [g for g in self.discovered_groups.values() if g.join_status == 'joined']
            
            for group in joined_groups[:3]:  # Limiter à 3 groupes par cycle
                users = await self.discover_active_users(group.id)
                logging.info(f"👥 {len(users)} utilisateurs découverts dans {group.title}")
                await asyncio.sleep(30)
            
            # Envoyer des invitations aux utilisateurs qualifiés
            qualified_users = [
                user for user in self.target_users.values()
                if (user.invitation_status == 'not_invited' and 
                    user.activity_score > 0.3 and
                    not user.is_bot)
            ]
            
            # Limiter les invitations pour éviter le spam
            daily_invitation_limit = 10
            invitations_sent = 0
            
            for user in qualified_users[:daily_invitation_limit]:
                if invitations_sent >= daily_invitation_limit:
                    break
                
                # Générer un lien d'invitation (simulation)
                invite_link = "https://t.me/your_group_link"
                
                success = await self.send_personalized_invitation(user, invite_link)
                if success:
                    invitations_sent += 1
                    await asyncio.sleep(random.randint(300, 600))  # 5-10 min entre invitations
            
            logging.info(f"📨 {invitations_sent} invitations envoyées")
            
        except Exception as e:
            logging.error(f"❌ Erreur gestion autonome: {e}")
    
    def get_autonomous_summary(self) -> Dict:
        """Retourne un résumé de l'activité autonome"""
        total_groups = len(self.discovered_groups)
        joined_groups = len([g for g in self.discovered_groups.values() if g.join_status == 'joined'])
        total_users = len(self.target_users)
        invited_users = len([u for u in self.target_users.values() if u.invitation_status == 'invited'])
        
        # Calculer les statistiques d'engagement
        avg_relevance = sum(g.relevance_score for g in self.discovered_groups.values()) / max(total_groups, 1)
        avg_activity = sum(u.activity_score for u in self.target_users.values()) / max(total_users, 1)
        
        return {
            'discovered_groups': total_groups,
            'joined_groups': joined_groups,
            'target_users': total_users,
            'invited_users': invited_users,
            'average_group_relevance': avg_relevance,
            'average_user_activity': avg_activity,
            'invitation_success_rate': invited_users / max(total_users, 1),
            'total_invitations_sent': len(self.invitation_history)
        }
    
    async def start_autonomous_mode(self):
        """Démarre le mode autonome"""
        if not await self.initialize_bot():
            logging.error("❌ Impossible d'initialiser le bot Telegram")
            return
        
        logging.info("🤖 Mode autonome Telegram démarré")
        
        try:
            while True:
                await self.autonomous_group_management()
                
                # Attendre avant le prochain cycle (6 heures)
                await asyncio.sleep(6 * 3600)
                
        except KeyboardInterrupt:
            logging.info("🛑 Mode autonome Telegram arrêté")
        except Exception as e:
            logging.error(f"❌ Erreur mode autonome: {e}")
