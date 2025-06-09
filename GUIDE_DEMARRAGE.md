# 🤖 Guide de Démarrage - VoltageGPU Bot

## 📊 **FRÉQUENCE DE PUBLICATION AUTOMATIQUE**

### ⏰ **Votre bot publiera automatiquement :**
- **Twitter** : 1 post par jour à 14h UTC (16h Paris)
- **Telegram** : 2 posts par jour à 10h et 18h UTC (12h et 20h Paris)
- **Reddit** : 1 post tous les 2 jours à 15h UTC (17h Paris)

### 📅 **Total par mois :**
- **Twitter** : 30 posts (15 GPU deals + 15 affiliation)
- **Telegram** : 60 posts (48 affiliation + 12 GPU deals)
- **Reddit** : 15 posts (rotation 6 subreddits)
- **TOTAL** : **105 posts automatiques par mois**

## 🚀 **COMMENT LANCER VOTRE BOT 24/7**

### **Option 1 : Lancement Simple (Recommandé)**
```bash
python final_optimized_bot.py
```
**⚠️ IMPORTANT** : Gardez cette fenêtre ouverte ! Si vous fermez le terminal, le bot s'arrête.

### **Option 2 : Lancement en Arrière-Plan (Windows)**
```bash
start /B python final_optimized_bot.py
```
Le bot tournera en arrière-plan même si vous fermez le terminal.

### **Option 3 : Lancement avec Logs Visibles**
```bash
python final_optimized_bot.py > bot_output.log 2>&1
```
Tous les logs seront sauvés dans `bot_output.log`.

## 📊 **VÉRIFIER QUE VOTRE BOT TOURNE**

### **Commande de Test (sans publier)**
```bash
python final_optimized_bot.py --test
```

### **Vérifier les Logs en Temps Réel**
```bash
type logs.txt
```
Ou ouvrez le fichier `logs.txt` pour voir l'activité.

## ⏰ **HORAIRES DE PUBLICATION (Heure de Paris)**

### 🐦 **Twitter**
- **14h UTC = 16h Paris** (tous les jours)
- Alternance : GPU deal → Affiliation → GPU deal...

### 📱 **Telegram**
- **10h UTC = 12h Paris** (tous les jours)
- **18h UTC = 20h Paris** (tous les jours)
- Focus : 80% affiliation, 20% GPU deals

### 🔴 **Reddit**
- **15h UTC = 17h Paris** (tous les 2 jours)
- Rotation automatique : r/MachineLearning → r/artificial → r/LocalLLaMA...

## 🔧 **STATUT ACTUEL DE VOS PLATEFORMES**

### ✅ **Configurées et Prêtes**
- **Twitter** : @GpuVoltage (clés API configurées)
- **Telegram** : @VoltageGPU (bot configuré)
- **Reddit** : RoleCold4185 (compte configuré)

### ⚠️ **Action Requise**
- **Reddit** : Ajoutez votre mot de passe dans le fichier `.env`
- Ligne à modifier : `REDDIT_PASSWORD=your_reddit_password_here`

## 🛑 **COMMENT ARRÊTER LE BOT**

### **Si lancé en mode normal :**
- Appuyez sur `Ctrl + C` dans le terminal

### **Si lancé en arrière-plan :**
```bash
taskkill /F /IM python.exe
```

## 📱 **SURVEILLANCE À DISTANCE**

### **Vérifier l'Activité**
1. Consultez vos comptes Twitter/Telegram/Reddit
2. Vérifiez le fichier `logs.txt`
3. Regardez les nouveaux posts avec votre code SHA-256-76360B81D39F

### **En Cas de Problème**
1. Vérifiez `errors.log` pour les erreurs
2. Relancez avec `python final_optimized_bot.py --test`
3. Vérifiez que vos clés API sont toujours valides

## 💰 **REVENUS ATTENDUS**

### **Avec 105 posts/mois automatiques :**
- **100+ clics** sur vos liens d'affiliation
- **20+ conversions** potentielles
- **5% commission** sur chaque vente VoltageGPU
- **Revenus passifs** sans intervention

## 🎯 **PROCHAINES ÉTAPES**

1. **Ajoutez votre mot de passe Reddit** dans `.env`
2. **Lancez le bot** : `python final_optimized_bot.py`
3. **Vérifiez les premiers posts** dans quelques heures
4. **Surveillez les logs** : `logs.txt`
5. **Profitez des revenus passifs** ! 💰

---

## ⚡ **COMMANDE FINALE POUR DÉMARRER**

```bash
python final_optimized_bot.py
```

**🎉 Votre bot publiera automatiquement 105 fois par mois avec votre code SHA-256-76360B81D39F !**
