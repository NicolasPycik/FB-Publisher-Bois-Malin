# Facebook Publisher SaaS v3.1.1

## 📋 Description

Application SaaS complète pour la gestion et publication automatisée sur les pages Facebook. Permet de publier simultanément sur jusqu'à 65 pages Facebook avec gestion des médias (texte, images, vidéos).

## 🚀 Fonctionnalités

### ✅ Publication Multi-Pages
- Publication simultanée sur 1 à 65 pages Facebook
- Support texte, liens, images et vidéos
- Sélection flexible des pages cibles
- Gestion des tokens de page automatique

### ✅ Interface Utilisateur
- Interface web responsive (desktop/mobile)
- Sélection visuelle des pages avec aperçu
- Formulaire de publication intuitif
- Feedback en temps réel

### ✅ Statistiques et Analytics
- Portée totale et engagement par page
- Taux d'engagement calculé automatiquement
- Historique des publications
- Métriques détaillées

### ✅ Gestion des Publicités
- Création de campagnes publicitaires
- Gestion des audiences sauvegardées
- Optimisation automatique des budgets
- Rapports de performance

### ✅ Programmation
- Publication différée
- Planification récurrente
- Gestion des fuseaux horaires

## 🏗️ Architecture

```
facebook_publisher_deploy/
├── backend/                    # API Flask + logique métier
│   ├── app.py                 # Point d'entrée Flask
│   ├── facebook_api.py        # Wrapper Facebook API
│   ├── src/
│   │   ├── main.py           # Configuration Flask
│   │   ├── routes/           # Routes API organisées
│   │   ├── database/         # Modèles SQLite
│   │   └── static/           # Fichiers statiques
├── frontend/                   # Interface utilisateur
│   └── index.html            # Interface principale
├── tests/                      # Tests automatiques
├── requirements.txt            # Dépendances Python
├── .env                       # Configuration (non versionné)
└── README.md                  # Cette documentation
```

## 🔧 Installation

### Prérequis
- Python 3.8+
- Compte Facebook Developer
- Application Facebook configurée

### Configuration Facebook
1. Créer une application sur [Facebook Developers](https://developers.facebook.com/)
2. Obtenir l'App ID et App Secret
3. Générer un token d'accès avec les permissions :
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`

### Installation locale
```bash
# Cloner le projet
git clone https://github.com/NicolasPycik/FB-Publisher-Bois-Malin.git
cd FB-Publisher-Bois-Malin

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos credentials Facebook
```

### Configuration .env
```env
FACEBOOK_APP_ID=votre_app_id
FACEBOOK_APP_SECRET=votre_app_secret
FACEBOOK_ACCESS_TOKEN=votre_token_utilisateur
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

## 🚀 Démarrage

### Développement
```bash
cd backend
python app.py
```

L'application sera accessible sur `http://localhost:5001`

### Production (AWS)
```bash
# Sur le serveur AWS
cd /home/ubuntu/facebook_publisher_deploy/backend
source ../venv/bin/activate
nohup python app.py > ../app.log 2>&1 &
```

## 📡 API Endpoints

### Pages Facebook
- `GET /api/facebook/pages` - Liste des pages
- `GET /api/facebook/pages/all` - Toutes les pages avec pagination
- `GET /api/facebook/config` - Configuration actuelle
- `POST /api/facebook/test-connection` - Test de connexion

### Publication
- `POST /api/facebook/pages/bulk-post` - Publication multiple (legacy)
- `POST /api/facebook/publish` - Publication simplifiée (v3.1.1)

### Analytics
- `GET /api/facebook/pages/<page_id>/insights` - Statistiques page
- `GET /api/facebook/analytics/overview` - Vue d'ensemble

### Publicités
- `POST /api/facebook/ads/campaigns` - Créer campagne
- `GET /api/facebook/ads/audiences` - Audiences sauvegardées

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest

# Tests spécifiques
pytest tests/test_publish_route.py
pytest tests/test_facebook_api.py

# Avec couverture
pytest --cov=backend
```

## 📊 Monitoring

### Logs
- Application : `app.log`
- Facebook API : `facebook_api.log`
- Niveau DEBUG activé pour diagnostic

### Métriques
- 65 pages Facebook synchronisées
- Portée totale : ~20,000 personnes
- Taux d'engagement moyen : 8.6%

## 🔒 Sécurité

- Tokens Facebook chiffrés
- Variables d'environnement sécurisées
- Validation des entrées utilisateur
- Gestion des erreurs API

## 🐛 Problèmes Connus

### ⚠️ Publication Non Fonctionnelle (v3.1.1)
**Symptômes :**
- Message "Publication en cours sur 1 page(s)..." affiché
- Aucune publication n'apparaît sur Facebook
- Champ de texte non vidé après tentative

**Corrections Appliquées :**
- ✅ Paramètre `image_path` supprimé
- ✅ Méthode `_get_page_token()` avec cache
- ✅ Appels directs `requests.post()` 
- ✅ Route `/publish` simplifiée
- ✅ Logging DEBUG activé

**Status :** 🔴 Non résolu - Investigation en cours

## 📝 Changelog

### v3.1.1 (25/06/2025)
- 🔧 Correction méthode `publish_post()`
- ➕ Ajout cache tokens de page
- ➕ Nouvelles méthodes `publish_post_with_photos/video()`
- ➕ Route `/publish` simplifiée
- ➕ Tests unitaires complets
- 🐛 Problème publication persistant

### v3.1.0 (24/06/2025)
- 🎉 Version initiale complète
- ✅ 65 pages Facebook synchronisées
- ✅ Interface utilisateur responsive
- ✅ Statistiques en temps réel
- ✅ Gestion des publicités

## 👥 Équipe

- **Développement :** Manus AI
- **Product Owner :** Nicolas Pycik
- **Client :** Bois Malin (65 pages Facebook)

## 📞 Support

Pour toute question ou problème :
1. Consulter les logs : `tail -f app.log`
2. Vérifier la configuration : `GET /api/facebook/config`
3. Tester la connexion : `POST /api/facebook/test-connection`

## 📄 Licence

Propriétaire - Nicolas Pycik / Bois Malin

---

**Dernière mise à jour :** 25 juin 2025  
**Version :** 3.1.1  
**Statut :** 🔴 Investigation problème publication en cours

