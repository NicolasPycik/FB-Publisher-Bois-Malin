# Guide de Démarrage Rapide - Facebook Publisher Bois Malin v2.1

## Installation Express

### Prérequis
- Python 3.11 ou supérieur
- Compte Facebook Developer
- Application Facebook configurée

### Installation en 3 étapes

1. **Décompression et installation**
```bash
tar -xzf FacebookPublisherBoisMalin_v2.1_FINAL.tar.gz
cd facebook_automation
pip install -r requirements.txt
```

2. **Configuration**
```bash
cp .env.example .env
# Éditez .env avec vos tokens Facebook
```

3. **Lancement**
```bash
python main.py
```

## Fonctionnalités Principales

### 📝 Publication Multi-Pages
- Publication simultanée sur 65 pages
- Support texte, images, vidéos, liens
- Programmation automatique

### 📊 Publicités Complètes
- Création de campagnes publicitaires
- Ciblage avancé (pays, âge, intérêts)
- Gestion des budgets et objectifs

### 🚀 Boost Post
- Promotion rapide des publications existantes
- Sélection automatique du compte publicitaire
- Configuration optimisée (France, 18-65 ans, 20€/jour)

### 📈 Statistiques Temps Réel
- Impressions et engagement par page
- Liste des 10 publications récentes
- Insights détaillés via API Facebook

## Interface Utilisateur

### Onglet Publication
- Sélection multiple de pages
- Éditeur de texte enrichi
- Upload d'images et vidéos
- Programmation de publications

### Onglet Publicités
- Configuration de campagnes
- Sélection de comptes publicitaires
- Création de créatifs
- Suivi des publicités créées

### Onglet Statistiques
- Métriques de performance
- Publications récentes
- Bouton "Booster ce post"
- Détails des publications

### Onglet Paramètres
- Configuration des tokens
- Gestion des pages
- Paramètres de l'application

## Workflow Typique

### 1. Configuration Initiale
1. Configurez vos tokens dans `.env`
2. Lancez l'application
3. Vérifiez la connexion aux pages

### 2. Publication de Contenu
1. Sélectionnez les pages cibles
2. Rédigez votre contenu
3. Ajoutez des médias si nécessaire
4. Publiez immédiatement ou programmez

### 3. Création de Publicités
1. Accédez à l'onglet Publicités
2. Sélectionnez compte et page
3. Configurez objectif et budget
4. Définissez le ciblage
5. Créez le créatif
6. Lancez la campagne

### 4. Boost de Publications
1. Allez dans l'onglet Statistiques
2. Sélectionnez une page
3. Choisissez une publication récente
4. Cliquez sur "Booster ce post"
5. Confirmez le compte publicitaire

## Support et Dépannage

### Problèmes Fréquents

**Token expiré**
- Renouvelez votre token Facebook
- Mettez à jour le fichier `.env`

**Permissions insuffisantes**
- Vérifiez les permissions de votre app Facebook
- Assurez-vous d'avoir les droits sur les pages

**Erreur de publication**
- Vérifiez le contenu (pas de spam)
- Respectez les limites de taux Facebook

### Logs et Débogage
- Consultez `logs/facebook_publisher.log`
- Activez le mode DEBUG si nécessaire
- Contactez le support avec les logs

## Ressources

### Documentation
- README.md complet
- Guide d'installation détaillé
- Référence API Facebook

### Tests
- Suite de tests unitaires complète
- Tests d'intégration API
- Validation des workflows

### Support
- Documentation technique
- Exemples de configuration
- Guide de dépannage

---

**Version :** 2.1  
**Dernière mise à jour :** 19 juin 2025  
**Développé par :** Manus AI pour Nicolas Pycik

