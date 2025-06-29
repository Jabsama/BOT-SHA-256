#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Reddit Intelligence Module - Anti-Ban & Rule Compliance System
Automatically detects subreddit rules, formats posts correctly, and avoids bans
"""

import re
import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
from dataclasses import dataclass

@dataclass
class SubredditRules:
    """Structure pour stocker les règles d'un subreddit"""
    name: str
    requires_tags: bool
    allowed_tags: List[str]
    title_format: str
    content_requirements: List[str]
    banned_keywords: List[str]
    min_karma_required: int
    account_age_required: int
    posting_frequency_limit: str
    flair_required: bool
    available_flairs: List[str]
    last_updated: datetime

class RedditIntelligence:
    """Module d'intelligence Reddit pour éviter les bans et maximiser l'engagement"""
    
    def __init__(self, data_file: str = 'data/reddit_intelligence.json'):
        self.data_file = data_file
        self.subreddit_rules = {}
        self.ban_patterns = {}
        self.successful_patterns = {}
        self.account_health = {}
        
        # Patterns de détection des règles communes
        self.rule_patterns = {
            'tags_required': [
                r'\[([A-Z])\]',
                r'tag.*required',
                r'must.*include.*tag',
                r'posts.*must.*be.*tagged'
            ],
            'no_promotion': [
                r'no.*promotion',
                r'no.*advertising',
                r'no.*spam',
                r'no.*self.*promotion'
            ],
            'minimum_effort': [
                r'low.*effort',
                r'minimum.*effort',
                r'detailed.*post',
                r'substantial.*content'
            ],
            'account_requirements': [
                r'minimum.*karma',
                r'account.*age',
                r'new.*accounts',
                r'karma.*requirement'
            ]
        }
        
        # Templates de contenu intelligent par type de subreddit
        self.content_templates = {
            'MachineLearning': {
                'tags': ['[D]', '[R]', '[N]', '[P]'],
                'title_format': '[{tag}] {title}',
                'content_style': 'academic',
                'required_elements': ['technical_context', 'specific_question', 'research_background']
            },
            'artificial': {
                'tags': ['Discussion', 'News', 'Research'],
                'title_format': '{title}',
                'content_style': 'technical',
                'required_elements': ['ai_context', 'practical_application']
            },
            'deeplearning': {
                'tags': ['[D]', '[R]', '[P]'],
                'title_format': '[{tag}] {title}',
                'content_style': 'research',
                'required_elements': ['methodology', 'results', 'implications']
            },
            'compsci': {
                'tags': [],
                'title_format': '{title}',
                'content_style': 'educational',
                'required_elements': ['problem_statement', 'solution_approach']
            }
        }
        
        self._load_intelligence_data()
        
    def _load_intelligence_data(self):
        """Charge les données d'intelligence depuis le fichier"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Charger les règles des subreddits
            for name, rule_data in data.get('subreddit_rules', {}).items():
                self.subreddit_rules[name] = SubredditRules(
                    name=rule_data['name'],
                    requires_tags=rule_data['requires_tags'],
                    allowed_tags=rule_data['allowed_tags'],
                    title_format=rule_data['title_format'],
                    content_requirements=rule_data['content_requirements'],
                    banned_keywords=rule_data['banned_keywords'],
                    min_karma_required=rule_data['min_karma_required'],
                    account_age_required=rule_data['account_age_required'],
                    posting_frequency_limit=rule_data['posting_frequency_limit'],
                    flair_required=rule_data['flair_required'],
                    available_flairs=rule_data['available_flairs'],
                    last_updated=datetime.fromisoformat(rule_data['last_updated'])
                )
                
            self.ban_patterns = data.get('ban_patterns', {})
            self.successful_patterns = data.get('successful_patterns', {})
            self.account_health = data.get('account_health', {})
            
        except (FileNotFoundError, json.JSONDecodeError):
            logging.info("🧠 Initializing new Reddit intelligence database")
            self._initialize_default_rules()
    
    def _save_intelligence_data(self):
        """Sauvegarde les données d'intelligence"""
        try:
            import os
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Convertir les règles en dictionnaire
            subreddit_rules_dict = {}
            for name, rules in self.subreddit_rules.items():
                subreddit_rules_dict[name] = {
                    'name': rules.name,
                    'requires_tags': rules.requires_tags,
                    'allowed_tags': rules.allowed_tags,
                    'title_format': rules.title_format,
                    'content_requirements': rules.content_requirements,
                    'banned_keywords': rules.banned_keywords,
                    'min_karma_required': rules.min_karma_required,
                    'account_age_required': rules.account_age_required,
                    'posting_frequency_limit': rules.posting_frequency_limit,
                    'flair_required': rules.flair_required,
                    'available_flairs': rules.available_flairs,
                    'last_updated': rules.last_updated.isoformat()
                }
            
            data = {
                'subreddit_rules': subreddit_rules_dict,
                'ban_patterns': self.ban_patterns,
                'successful_patterns': self.successful_patterns,
                'account_health': self.account_health
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"❌ Erreur sauvegarde intelligence Reddit: {e}")
    
    def _initialize_default_rules(self):
        """Initialise les règles par défaut pour les subreddits populaires"""
        default_rules = {
            'MachineLearning': SubredditRules(
                name='MachineLearning',
                requires_tags=True,
                allowed_tags=['[D]', '[R]', '[N]', '[P]'],
                title_format='[{tag}] {title}',
                content_requirements=['technical_depth', 'research_context', 'specific_question'],
                banned_keywords=['promotion', 'affiliate', 'discount', 'cheap', 'deal'],
                min_karma_required=50,
                account_age_required=30,
                posting_frequency_limit='1_per_week',
                flair_required=True,
                available_flairs=['Discussion', 'Research', 'News', 'Project'],
                last_updated=datetime.now()
            ),
            'artificial': SubredditRules(
                name='artificial',
                requires_tags=False,
                allowed_tags=[],
                title_format='{title}',
                content_requirements=['ai_context', 'thoughtful_discussion'],
                banned_keywords=['promotion', 'affiliate', 'spam'],
                min_karma_required=10,
                account_age_required=7,
                posting_frequency_limit='2_per_week',
                flair_required=False,
                available_flairs=[],
                last_updated=datetime.now()
            ),
            'deeplearning': SubredditRules(
                name='deeplearning',
                requires_tags=True,
                allowed_tags=['[D]', '[R]', '[P]', '[N]'],
                title_format='[{tag}] {title}',
                content_requirements=['technical_content', 'research_basis'],
                banned_keywords=['promotion', 'commercial', 'sale'],
                min_karma_required=25,
                account_age_required=14,
                posting_frequency_limit='1_per_week',
                flair_required=True,
                available_flairs=['Discussion', 'Research', 'Project'],
                last_updated=datetime.now()
            )
        }
        
        self.subreddit_rules.update(default_rules)
        self._save_intelligence_data()
    
    def analyze_subreddit_rules(self, reddit_client, subreddit_name: str) -> SubredditRules:
        """Analyse automatiquement les règles d'un subreddit"""
        try:
            subreddit = reddit_client.subreddit(subreddit_name)
            
            # Récupérer la description et les règles
            description = subreddit.description
            rules_text = ""
            
            try:
                rules = subreddit.rules()
                rules_text = " ".join([rule.description for rule in rules])
            except:
                pass
            
            # Analyser le texte combiné
            combined_text = f"{description} {rules_text}".lower()
            
            # Détecter les exigences de tags
            requires_tags = False
            allowed_tags = []
            
            for pattern in self.rule_patterns['tags_required']:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    requires_tags = True
                    # Extraire les tags spécifiques
                    tag_matches = re.findall(r'\[([A-Z])\]', combined_text.upper())
                    allowed_tags = [f'[{tag}]' for tag in tag_matches]
                    break
            
            # Détecter les mots-clés interdits
            banned_keywords = []
            if any(re.search(pattern, combined_text) for pattern in self.rule_patterns['no_promotion']):
                banned_keywords.extend(['promotion', 'affiliate', 'discount', 'deal', 'cheap'])
            
            # Détecter les exigences de contenu
            content_requirements = []
            if any(re.search(pattern, combined_text) for pattern in self.rule_patterns['minimum_effort']):
                content_requirements.extend(['detailed_content', 'substantial_discussion'])
            
            # Créer les règles
            rules = SubredditRules(
                name=subreddit_name,
                requires_tags=requires_tags,
                allowed_tags=allowed_tags if allowed_tags else ['[D]', '[Q]'],
                title_format='[{tag}] {title}' if requires_tags else '{title}',
                content_requirements=content_requirements,
                banned_keywords=banned_keywords,
                min_karma_required=10,  # Estimation par défaut
                account_age_required=7,
                posting_frequency_limit='1_per_week',
                flair_required=False,
                available_flairs=[],
                last_updated=datetime.now()
            )
            
            # Sauvegarder les règles apprises
            self.subreddit_rules[subreddit_name] = rules
            self._save_intelligence_data()
            
            logging.info(f"🧠 Règles analysées pour r/{subreddit_name}: Tags={requires_tags}, Mots interdits={len(banned_keywords)}")
            return rules
            
        except Exception as e:
            logging.error(f"❌ Erreur analyse r/{subreddit_name}: {e}")
            # Retourner des règles par défaut
            return SubredditRules(
                name=subreddit_name,
                requires_tags=False,
                allowed_tags=[],
                title_format='{title}',
                content_requirements=[],
                banned_keywords=['promotion', 'affiliate'],
                min_karma_required=5,
                account_age_required=3,
                posting_frequency_limit='1_per_day',
                flair_required=False,
                available_flairs=[],
                last_updated=datetime.now()
            )
    
    def generate_compliant_content(self, subreddit_name: str, base_content: str, base_title: str) -> Tuple[str, str]:
        """Génère du contenu conforme aux règles du subreddit"""
        # Obtenir les règles
        if subreddit_name not in self.subreddit_rules:
            logging.warning(f"⚠️ Règles inconnues pour r/{subreddit_name}, utilisation des règles par défaut")
            rules = SubredditRules(
                name=subreddit_name,
                requires_tags=False,
                allowed_tags=[],
                title_format='{title}',
                content_requirements=[],
                banned_keywords=['promotion', 'affiliate'],
                min_karma_required=5,
                account_age_required=3,
                posting_frequency_limit='1_per_day',
                flair_required=False,
                available_flairs=[],
                last_updated=datetime.now()
            )
        else:
            rules = self.subreddit_rules[subreddit_name]
        
        # Adapter le titre
        adapted_title = base_title
        if rules.requires_tags and rules.allowed_tags:
            # Choisir le tag le plus approprié
            if '[D]' in rules.allowed_tags:
                tag = '[D]'  # Discussion - le plus sûr
            elif '[Q]' in rules.allowed_tags:
                tag = '[Q]'  # Question
            else:
                tag = rules.allowed_tags[0]
            
            adapted_title = rules.title_format.format(tag=tag, title=base_title)
        
        # Adapter le contenu
        adapted_content = base_content
        
        # Supprimer les mots-clés interdits
        for keyword in rules.banned_keywords:
            adapted_content = re.sub(rf'\b{keyword}\b', self._get_synonym(keyword), adapted_content, flags=re.IGNORECASE)
        
        # Ajouter du contexte technique si requis
        if 'technical_depth' in rules.content_requirements:
            adapted_content = self._add_technical_context(adapted_content, subreddit_name)
        
        if 'research_context' in rules.content_requirements:
            adapted_content = self._add_research_context(adapted_content)
        
        # Ajouter une question spécifique si requis
        if 'specific_question' in rules.content_requirements:
            adapted_content = self._add_specific_question(adapted_content, subreddit_name)
        
        return adapted_title, adapted_content
    
    def _get_synonym(self, word: str) -> str:
        """Retourne un synonyme pour éviter les mots-clés interdits"""
        synonyms = {
            'promotion': 'recommendation',
            'affiliate': 'referral',
            'discount': 'savings',
            'deal': 'offer',
            'cheap': 'affordable',
            'spam': 'content'
        }
        return synonyms.get(word.lower(), word)
    
    def _add_technical_context(self, content: str, subreddit_name: str) -> str:
        """Ajoute du contexte technique approprié"""
        technical_contexts = {
            'MachineLearning': [
                "I've been working on optimizing computational resources for ML workloads and came across an interesting cost-efficiency challenge.",
                "While researching distributed training setups, I discovered some significant cost variations in GPU infrastructure.",
                "In my recent experiments with large-scale model training, I've been analyzing the economics of different compute platforms."
            ],
            'artificial': [
                "I've been exploring the intersection of AI development and infrastructure costs.",
                "While building AI applications, I've noticed significant variations in compute pricing across platforms.",
                "In my AI research, I've been investigating cost-effective approaches to GPU-intensive workloads."
            ],
            'deeplearning': [
                "During my deep learning research, I've been analyzing the computational requirements and associated costs.",
                "I've been experimenting with different GPU configurations for neural network training and noticed interesting cost patterns.",
                "While optimizing my deep learning pipeline, I discovered some significant infrastructure cost differences."
            ]
        }
        
        contexts = technical_contexts.get(subreddit_name, technical_contexts['artificial'])
        selected_context = random.choice(contexts)
        
        return f"{selected_context}\n\n{content}"
    
    def _add_research_context(self, content: str) -> str:
        """Ajoute un contexte de recherche"""
        research_contexts = [
            "Based on my analysis of current market trends in cloud computing,",
            "According to recent studies on computational cost optimization,",
            "My research into distributed computing economics has revealed that",
            "Industry reports suggest that"
        ]
        
        selected_context = random.choice(research_contexts)
        return f"{selected_context} {content.lower()}"
    
    def _add_specific_question(self, content: str, subreddit_name: str) -> str:
        """Ajoute une question spécifique pour encourager la discussion"""
        questions = {
            'MachineLearning': [
                "What has been your experience with cost optimization in ML infrastructure?",
                "How do you balance computational costs with model performance in your projects?",
                "What strategies have you found effective for reducing training costs?",
                "Have you encountered similar cost efficiency challenges in your ML work?"
            ],
            'artificial': [
                "What's your take on the current state of AI infrastructure costs?",
                "How do you approach cost optimization in your AI projects?",
                "What trends are you seeing in AI compute pricing?",
                "How do you evaluate cost-effectiveness in AI development?"
            ],
            'deeplearning': [
                "What's your experience with GPU cost optimization for deep learning?",
                "How do you handle computational costs in your research?",
                "What infrastructure strategies work best for your deep learning projects?",
                "Have you found effective ways to reduce training costs?"
            ]
        }
        
        subreddit_questions = questions.get(subreddit_name, questions['artificial'])
        selected_question = random.choice(subreddit_questions)
        
        return f"{content}\n\n{selected_question}"
    
    def check_account_health(self, account_name: str) -> Dict:
        """Vérifie la santé d'un compte Reddit"""
        if account_name not in self.account_health:
            self.account_health[account_name] = {
                'posts_this_week': 0,
                'last_post_date': None,
                'ban_risk_score': 0,
                'successful_posts': 0,
                'removed_posts': 0,
                'last_removal_reason': None,
                'subreddits_posted': []
            }
        
        return self.account_health[account_name]
    
    def record_post_result(self, account_name: str, subreddit_name: str, success: bool, removal_reason: str = None):
        """Enregistre le résultat d'un post pour l'apprentissage"""
        health = self.check_account_health(account_name)
        
        if success:
            health['successful_posts'] += 1
            health['ban_risk_score'] = max(0, health['ban_risk_score'] - 1)
            
            # Enregistrer le pattern de succès
            if subreddit_name not in self.successful_patterns:
                self.successful_patterns[subreddit_name] = []
            
        else:
            health['removed_posts'] += 1
            health['ban_risk_score'] += 2
            health['last_removal_reason'] = removal_reason
            
            # Enregistrer le pattern d'échec
            if subreddit_name not in self.ban_patterns:
                self.ban_patterns[subreddit_name] = []
            
            if removal_reason:
                self.ban_patterns[subreddit_name].append({
                    'reason': removal_reason,
                    'date': datetime.now().isoformat(),
                    'account': account_name
                })
        
        health['last_post_date'] = datetime.now().isoformat()
        if subreddit_name not in health['subreddits_posted']:
            health['subreddits_posted'].append(subreddit_name)
        
        self._save_intelligence_data()
        
        logging.info(f"📊 Post result recorded: r/{subreddit_name} - {'✅' if success else '❌'} - Risk: {health['ban_risk_score']}")
    
    def should_post_to_subreddit(self, account_name: str, subreddit_name: str) -> Tuple[bool, str]:
        """Détermine si on peut poster dans un subreddit avec ce compte"""
        health = self.check_account_health(account_name)
        
        # Vérifier le score de risque
        if health['ban_risk_score'] > 5:
            return False, f"Ban risk too high ({health['ban_risk_score']})"
        
        # Vérifier la fréquence de posting
        if health['last_post_date']:
            last_post = datetime.fromisoformat(health['last_post_date'])
            if datetime.now() - last_post < timedelta(hours=6):
                return False, "Posted too recently (< 6h)"
        
        # Vérifier les patterns d'échec récents
        if subreddit_name in self.ban_patterns:
            recent_bans = [
                ban for ban in self.ban_patterns[subreddit_name]
                if datetime.fromisoformat(ban['date']) > datetime.now() - timedelta(days=7)
            ]
            if len(recent_bans) > 2:
                return False, f"Too many recent bans in r/{subreddit_name}"
        
        return True, "Safe to post"
    
    def get_best_subreddits(self, account_name: str, limit: int = 5) -> List[str]:
        """Retourne les meilleurs subreddits pour ce compte"""
        health = self.check_account_health(account_name)
        
        # Subreddits recommandés par catégorie
        safe_subreddits = [
            'artificial', 'MachineLearning', 'deeplearning', 'compsci',
            'programming', 'learnmachinelearning', 'MLQuestions',
            'ArtificialIntelligence', 'datascience', 'statistics'
        ]
        
        # Filtrer selon la santé du compte
        available_subreddits = []
        for subreddit in safe_subreddits:
            can_post, reason = self.should_post_to_subreddit(account_name, subreddit)
            if can_post:
                available_subreddits.append(subreddit)
        
        return available_subreddits[:limit]
    
    def get_intelligence_summary(self) -> Dict:
        """Retourne un résumé de l'intelligence accumulée"""
        total_rules = len(self.subreddit_rules)
        total_accounts = len(self.account_health)
        
        # Calculer les statistiques de succès
        total_successful = sum(health['successful_posts'] for health in self.account_health.values())
        total_removed = sum(health['removed_posts'] for health in self.account_health.values())
        success_rate = total_successful / (total_successful + total_removed) if (total_successful + total_removed) > 0 else 0
        
        return {
            'subreddits_analyzed': total_rules,
            'accounts_tracked': total_accounts,
            'total_successful_posts': total_successful,
            'total_removed_posts': total_removed,
            'success_rate': success_rate,
            'ban_patterns_learned': len(self.ban_patterns),
            'successful_patterns': len(self.successful_patterns)
        }
