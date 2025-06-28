# Guide de Développement - Facebook Publisher SaaS

**Version :** v3.1.1  
**Date :** 25 juin 2025  
**Auteur :** Manus AI

## 🎯 Introduction

Ce guide s'adresse aux développeurs souhaitant comprendre, maintenir ou étendre l'application Facebook Publisher SaaS. Il couvre l'architecture technique, les conventions de code, les processus de développement et les bonnes pratiques.

## 🏗️ Architecture Technique

### Vue d'ensemble

L'application suit une architecture MVC (Model-View-Controller) avec séparation claire entre le frontend et le backend :

```
Frontend (HTML/JS) ↔ API REST ↔ Backend (Flask) ↔ Facebook Graph API
                                      ↓
                                 SQLite Database
```

### Stack Technologique

**Backend :**
- **Python 3.11** : Langage principal
- **Flask 2.3+** : Framework web
- **SQLite** : Base de données
- **Requests** : Client HTTP pour API Facebook
- **Pytest** : Framework de tests

**Frontend :**
- **HTML5/CSS3** : Structure et style
- **JavaScript ES6+** : Logique côté client
- **Fetch API** : Communication avec le backend
- **Responsive Design** : Compatible mobile/desktop

**APIs Externes :**
- **Facebook Graph API** : Publication et gestion des pages
- **Facebook Marketing API** : Publicités et audiences

## 📁 Structure du Projet

```
facebook_publisher_deploy/
├── backend/                    # Backend Flask
│   ├── facebook_api.py        # Wrapper API Facebook
│   ├── app.py                 # Application Flask principale
│   ├── main.py                # Point d'entrée
│   ├── wsgi.py                # Configuration WSGI
│   └── src/
│       ├── __init__.py
│       ├── main.py            # Configuration alternative
│       ├── models/            # Modèles de données
│       │   └── user.py
│       ├── routes/            # Routes API
│       │   ├── facebook_api_routes.py
│       │   ├── analytics_routes.py
│       │   ├── campaigns_routes.py
│       │   ├── audiences_routes.py
│       │   ├── dashboard.py
│       │   └── user.py
│       ├── static/            # Fichiers statiques
│       │   ├── index.html
│       │   └── index_mobile.html
│       └── database/          # Base de données
│           └── app.db
├── frontend/                  # Frontend standalone
│   ├── index.html
│   └── index_mobile.html
├── tests/                     # Tests automatisés
│   ├── test_facebook_api.py
│   ├── test_publish_route.py
│   ├── test_saas_v3.py
│   ├── test_v31_complete.py
│   ├── test_ads.py
│   └── test_ads_workflow.py
├── requirements.txt           # Dépendances Python
├── .env                      # Variables d'environnement
├── .env.example              # Exemple de configuration
├── .gitignore               # Fichiers ignorés par Git
└── README.md                # Documentation principale
```

## 🔧 Configuration de l'Environnement de Développement

### Installation Locale

```bash
# Cloner le dépôt
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
# Éditer .env avec vos tokens Facebook
```

### Configuration Facebook Developer

1. **Créer une application Facebook** :
   - Aller sur https://developers.facebook.com/
   - Créer une nouvelle application
   - Ajouter le produit "Facebook Login"

2. **Configurer les permissions** :
   - `pages_manage_posts` : Publication sur les pages
   - `pages_show_list` : Liste des pages gérées
   - `pages_read_engagement` : Lecture des statistiques
   - `ads_management` : Gestion des publicités

3. **Obtenir les tokens** :
   - App ID et App Secret dans les paramètres de base
   - User Access Token via Graph API Explorer
   - Page Access Tokens générés automatiquement

### Variables d'Environnement

Fichier `.env` requis :

```bash
# Facebook API
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_user_access_token

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=DEBUG

# Database (optionnel)
DATABASE_URL=sqlite:///app.db
```

## 🧩 Composants Principaux

### 1. FacebookAPI Class (`facebook_api.py`)

Wrapper principal pour l'API Facebook Graph :

```python
class FacebookAPI:
    def __init__(self, app_id: str, app_secret: str, access_token: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.BASE_URL = "https://graph.facebook.com/v18.0"
        self._page_token_cache = {}
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Méthode générique pour les appels API"""
        
    def get_user_pages(self) -> List[Dict]:
        """Récupère toutes les pages gérées par l'utilisateur"""
        
    def publish_post(self, page_id: str, message: str, link: Optional[str] = None) -> str:
        """Publie un post texte/lien sur une page"""
        
    def publish_post_with_photos(self, page_id: str, message: str, files: List[str]) -> str:
        """Publie un post avec photos"""
        
    def get_page_insights(self, page_id: str, metrics: List[str]) -> Dict:
        """Récupère les statistiques d'une page"""
```

**Méthodes principales :**
- `_get_page_token()` : Cache et récupération des tokens de page
- `_make_request()` : Wrapper générique pour les appels API
- `publish_post()` : Publication de contenu texte/lien
- `publish_post_with_photos()` : Publication avec images
- `get_page_insights()` : Récupération des statistiques

### 2. Routes API (`src/routes/`)

#### Facebook API Routes (`facebook_api_routes.py`)

```python
from flask import Blueprint, request, jsonify

facebook_bp = Blueprint('facebook', __name__)

@facebook_bp.route('/pages', methods=['GET'])
def get_pages():
    """Récupère la liste des pages Facebook"""
    
@facebook_bp.route('/pages/bulk-post', methods=['POST'])
def bulk_publish():
    """Publication sur plusieurs pages simultanément"""
    
@facebook_bp.route('/publish', methods=['POST'])
def publish():
    """Publication simple sur une page"""
    
@facebook_bp.route('/config', methods=['GET', 'POST'])
def config():
    """Configuration des tokens Facebook"""
```

#### Analytics Routes (`analytics_routes.py`)

```python
@analytics_bp.route('/overview', methods=['GET'])
def overview():
    """Vue d'ensemble des statistiques"""
    
@analytics_bp.route('/pages', methods=['GET'])
def pages_analytics():
    """Statistiques détaillées par page"""
```

### 3. Frontend JavaScript

#### Fonction de Publication (`index.html`)

```javascript
async function publierContenu() {
    const selectedPages = getSelectedPages();
    const message = document.getElementById('postContent').value;
    const link = document.getElementById('postLink').value;
    
    if (!selectedPages.length || !message.trim()) {
        alert('Veuillez sélectionner au moins une page et saisir un message.');
        return;
    }
    
    try {
        const response = await fetch('/api/facebook/pages/bulk-post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                page_ids: selectedPages,
                message: message,
                link: link || null
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Gestion du succès
            showSuccessMessage(result);
            clearForm();
        } else {
            // Gestion des erreurs
            showErrorMessage(result.error);
        }
    } catch (error) {
        console.error('Erreur:', error);
        showErrorMessage('Erreur de connexion au serveur');
    }
}
```

## 🧪 Tests et Qualité

### Structure des Tests

```
tests/
├── test_facebook_api.py      # Tests du wrapper API Facebook
├── test_publish_route.py     # Tests des routes de publication
├── test_saas_v3.py          # Tests généraux de l'application
├── test_v31_complete.py     # Tests complets v3.1
├── test_ads.py              # Tests des fonctionnalités publicitaires
└── test_ads_workflow.py     # Tests des workflows publicitaires
```

### Exécution des Tests

```bash
# Tous les tests
python -m pytest tests/ -v

# Tests spécifiques
python -m pytest tests/test_facebook_api.py -v

# Tests avec couverture
python -m pytest tests/ --cov=backend --cov-report=html

# Tests en mode debug
python -m pytest tests/ -v -s --tb=short
```

### Exemple de Test

```python
import pytest
from backend.facebook_api import FacebookAPI

class TestFacebookAPI:
    def setup_method(self):
        self.api = FacebookAPI(
            app_id="test_app_id",
            app_secret="test_app_secret",
            access_token="test_token"
        )
    
    def test_publish_post_success(self, mocker):
        # Mock de la requête HTTP
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"id": "123456789"}
        mock_response.raise_for_status.return_value = None
        
        mocker.patch('requests.post', return_value=mock_response)
        
        # Test de la méthode
        result = self.api.publish_post("page_id", "Test message")
        
        assert result == "123456789"
```

### Conventions de Tests

1. **Nommage** : `test_[fonction]_[scenario]`
2. **Structure** : Arrange, Act, Assert
3. **Mocking** : Utiliser `pytest-mock` pour les appels externes
4. **Fixtures** : Réutiliser les configurations communes
5. **Couverture** : Viser 80%+ de couverture de code

## 🔍 Debugging et Logging

### Configuration des Logs

```python
import logging

# Configuration dans app.py
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Utilisation des Logs

```python
# Dans facebook_api.py
def publish_post(self, page_id: str, message: str, link: Optional[str] = None) -> str:
    logger.info(f"Publishing post to page {page_id}")
    logger.debug(f"Post content: {message[:50]}...")
    
    try:
        # ... logique de publication
        logger.info(f"Post published successfully: {post_id}")
        return post_id
    except Exception as e:
        logger.error(f"Failed to publish post: {e}")
        raise
```

### Outils de Debug

1. **Flask Debug Mode** : `FLASK_DEBUG=True`
2. **Logs détaillés** : `LOG_LEVEL=DEBUG`
3. **Profiling** : Flask-Profiler pour les performances
4. **Monitoring** : Logs structurés pour le monitoring

## 📊 Bonnes Pratiques

### Code Style

1. **PEP 8** : Respect des conventions Python
2. **Type Hints** : Utilisation des annotations de type
3. **Docstrings** : Documentation des fonctions
4. **Nommage** : Noms explicites et cohérents

```python
def publish_post(self, page_id: str, message: str, link: Optional[str] = None) -> str:
    """
    Publie un post texte/lien sur une page Facebook.
    
    Args:
        page_id: ID de la page Facebook
        message: Contenu du message
        link: Lien optionnel à inclure
        
    Returns:
        ID du post créé
        
    Raises:
        FacebookAPIError: En cas d'erreur API
    """
```

### Gestion d'Erreurs

1. **Exceptions spécifiques** : Créer des classes d'exception personnalisées
2. **Logging des erreurs** : Toujours logger les erreurs avec contexte
3. **Retry logic** : Implémenter des tentatives pour les erreurs temporaires
4. **Validation des données** : Valider les entrées utilisateur

```python
class FacebookAPIError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        super().__init__(message)
        self.error_code = error_code

def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise FacebookAPIError(f"Request failed after {max_retries} attempts: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Sécurité

1. **Variables d'environnement** : Jamais de secrets dans le code
2. **Validation des entrées** : Sanitiser toutes les données utilisateur
3. **HTTPS** : Utiliser HTTPS en production
4. **Rate limiting** : Implémenter des limites de requêtes

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@facebook_bp.route('/pages/bulk-post', methods=['POST'])
@limiter.limit("10 per minute")
def bulk_publish():
    # ... logique de publication
```

## 🚀 Processus de Développement

### Workflow Git

1. **Branches** :
   - `main` : Version stable de production
   - `develop` : Branche de développement
   - `feature/nom-feature` : Nouvelles fonctionnalités
   - `hotfix/nom-fix` : Corrections urgentes

2. **Commits** :
   - Messages descriptifs
   - Commits atomiques
   - Référence aux issues

```bash
# Exemple de workflow
git checkout develop
git pull origin develop
git checkout -b feature/improve-error-handling
# ... développement
git add .
git commit -m "feat: improve error handling in publish_post method"
git push origin feature/improve-error-handling
# ... Pull Request
```

### Déploiement

1. **Tests** : Tous les tests doivent passer
2. **Review** : Code review obligatoire
3. **Staging** : Test en environnement de staging
4. **Production** : Déploiement avec rollback possible

```bash
# Script de déploiement
#!/bin/bash
echo "Déploiement en cours..."
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/
sudo systemctl restart facebook-publisher
echo "Déploiement terminé"
```

## 🔧 Extensions et Améliorations

### Fonctionnalités Futures

1. **Planification de posts** : Scheduling avec Celery
2. **Analytics avancés** : Graphiques et rapports
3. **Multi-tenant** : Support de plusieurs clients
4. **API REST complète** : Documentation OpenAPI
5. **Interface mobile** : Application mobile native

### Architecture Évolutive

```python
# Structure modulaire recommandée
app/
├── api/                    # API REST
│   ├── v1/                # Version 1 de l'API
│   └── v2/                # Version 2 de l'API
├── core/                  # Logique métier
│   ├── facebook/          # Services Facebook
│   ├── analytics/         # Services d'analyse
│   └── scheduling/        # Services de planification
├── models/                # Modèles de données
├── services/              # Services externes
└── utils/                 # Utilitaires
```

## 📚 Ressources et Documentation

### APIs Facebook

- **Graph API** : https://developers.facebook.com/docs/graph-api/
- **Marketing API** : https://developers.facebook.com/docs/marketing-api/
- **Webhooks** : https://developers.facebook.com/docs/graph-api/webhooks/

### Outils de Développement

- **Graph API Explorer** : Test des requêtes API
- **Facebook Debugger** : Debug des liens et contenus
- **Access Token Debugger** : Validation des tokens

### Documentation Technique

- **Flask** : https://flask.palletsprojects.com/
- **Requests** : https://docs.python-requests.org/
- **Pytest** : https://docs.pytest.org/

## 🎯 Conclusion

Ce guide fournit une base solide pour le développement et la maintenance de l'application Facebook Publisher SaaS. L'architecture modulaire et les bonnes pratiques implémentées permettent une évolution et une maintenance efficaces du code.

**Points clés à retenir :**
- Architecture séparée frontend/backend
- Gestion d'erreurs robuste
- Tests automatisés complets
- Logging détaillé pour le debugging
- Sécurité et bonnes pratiques

---

**Document généré par Manus AI le 25 juin 2025**  
**Projet : Facebook Publisher SaaS v3.1.1 - Bois Malin**

