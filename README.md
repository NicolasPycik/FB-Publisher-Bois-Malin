# Facebook Publisher Bois Malin

Une application web complète pour publier du contenu sur plusieurs pages Facebook simultanément. Développée spécifiquement pour les entreprises Bois Malin.

## 🚀 Fonctionnalités

### ✅ Publication Multi-Pages
- Publication simultanée sur 65+ pages Facebook
- Support des images, vidéos et audio
- Publication de texte seul
- Sélection individuelle ou groupée des pages

### ✅ Interface Web Intuitive
- Dashboard avec statistiques
- Interface responsive (desktop et mobile)
- Upload par glisser-déposer
- Prévisualisation des médias

### ✅ Gestion Avancée
- Synchronisation automatique des pages Facebook
- Gestion des tokens de page automatique
- Logs détaillés pour le debugging
- Configuration via interface web

## 🛠️ Installation

### Prérequis
- Python 3.11+
- Compte Facebook Developer
- Application Facebook configurée

### 1. Cloner le repository
```bash
git clone https://github.com/NicolasPycik/FB-Publisher-Bois-Malin.git
cd FB-Publisher-Bois-Malin
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env avec vos identifiants Facebook
nano .env
```

### 4. Lancer l'application
```bash
cd src
python main.py
```

L'application sera accessible sur `http://localhost:5001`

## 📋 Configuration Facebook

### 1. Créer une application Facebook
1. Aller sur [Facebook Developers](https://developers.facebook.com/)
2. Créer une nouvelle application
3. Ajouter le produit "Facebook Login"

### 2. Permissions requises
- `pages_read_engagement`
- `pages_manage_posts`
- `pages_show_list`

### 3. Générer un Access Token
1. Utiliser l'outil Graph API Explorer
2. Sélectionner votre application
3. Demander les permissions nécessaires
4. Générer un token longue durée

## 🏗️ Architecture

```
FB-Publisher-Bois-Malin/
├── src/
│   ├── main.py              # Point d'entrée de l'application
│   ├── routes/              # Routes Flask
│   │   ├── facebook_api_routes.py
│   │   ├── analytics_routes.py
│   │   └── campaigns_routes.py
│   ├── models/              # Modèles de données
│   ├── static/              # Fichiers statiques (HTML, CSS, JS)
│   └── database/            # Base de données SQLite
├── facebook_api.py          # API Facebook
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

## 🔧 API Endpoints

### Publication
- `POST /api/facebook/upload` - Publier du contenu avec médias
- `GET /api/facebook/pages` - Récupérer les pages Facebook

### Configuration
- `POST /api/settings` - Sauvegarder les paramètres
- `GET /api/settings` - Récupérer les paramètres

## 📊 Logs et Debugging

L'application génère des logs détaillés :
- Requêtes API Facebook
- Réponses et codes d'erreur
- Upload et traitement des fichiers
- Tokens de page utilisés

## 🚀 Déploiement AWS

L'application est optimisée pour le déploiement sur AWS EC2 :

1. Instance EC2 Ubuntu 22.04
2. Python 3.11+ pré-installé
3. Port 5001 ouvert
4. Logs dans `/home/ubuntu/app.log`

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Vérifier les logs de l'application
2. Consulter la documentation Facebook API
3. Ouvrir une issue sur GitHub

## 🎯 Statut du Projet

✅ **Version Stable** - Application entièrement fonctionnelle
- Publication multi-pages : ✅
- Upload d'images : ✅
- Upload de vidéos : ✅
- Interface web : ✅
- Déploiement AWS : ✅

---

Développé avec ❤️ pour Bois Malin

