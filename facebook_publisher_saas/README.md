# Facebook Publisher SaaS - Bois Malin

🚀 **Application SaaS complète pour la gestion et publication sur 65+ pages Facebook**

## 🎯 Fonctionnalités

- ✅ **Gestion de 65 pages Facebook** via Business Manager
- ✅ **Publication simultanée** sur toutes les pages
- ✅ **Programmation de posts** avec calendrier
- ✅ **Gestion des médias** (images, vidéos)
- ✅ **Statistiques et analytics** détaillées
- ✅ **Interface responsive** (mobile + desktop)
- ✅ **API REST** complète

## 🌐 Démo en Ligne

**URL de production :** https://lnh8imcd5plx.manus.space

## 🛠️ Technologies

- **Backend :** Python Flask
- **Frontend :** HTML5, CSS3, JavaScript
- **API :** Facebook Graph API v20.0
- **Base de données :** SQLite
- **Déploiement :** AWS

## 📊 Statistiques

- **65 pages Facebook** synchronisées
- **5 Business Managers** connectés
- **Support pagination** robuste
- **Gestion d'erreurs** complète

## 🚀 Installation

### Prérequis

- Python 3.11+
- Compte Facebook Developer
- App Facebook avec permissions `business_management`

### Configuration

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/facebook-publisher-saas.git
cd facebook-publisher-saas
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration environnement**
```bash
cp .env.example .env
# Éditer .env avec vos credentials Facebook
```

4. **Lancer l'application**
```bash
python src/main.py
```

## 🔧 Configuration Facebook

### Permissions requises

- `pages_show_list`
- `pages_manage_posts`
- `pages_read_engagement`
- `business_management` ⚠️ **Essentiel pour 65+ pages**

### Génération du token

1. Allez sur https://developers.facebook.com/tools/explorer/
2. Sélectionnez votre app Facebook
3. **Ajoutez la permission `business_management`**
4. Sélectionnez toutes vos pages (directes + Business Manager)
5. Générez le token
6. Configurez dans `.env`

## 📁 Structure du Projet

```
facebook_publisher_saas/
├── src/
│   ├── main.py              # Application Flask principale
│   ├── routes/              # Routes API
│   ├── models/              # Modèles de données
│   └── static/              # Interface utilisateur
├── facebook_api.py          # Wrapper API Facebook v2.2.0
├── tests/                   # Tests unitaires
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

## 🔄 API Endpoints

### Pages Facebook
- `GET /api/facebook/pages` - Liste des pages
- `POST /api/facebook/pages/sync` - Synchronisation

### Publications
- `POST /api/facebook/post` - Publier sur les pages
- `GET /api/facebook/posts` - Historique des posts

### Statistiques
- `GET /api/facebook/stats` - Analytics des pages

## 🎨 Interface Utilisateur

- **Dashboard** - Vue d'ensemble des pages et statistiques
- **Publier** - Interface de création de posts
- **Pages Facebook** - Gestion des 65 pages
- **Programmées** - Posts programmés
- **Statistiques** - Analytics détaillées

## 🔍 Fonctionnalités Avancées

### Récupération Business Manager

Le système récupère automatiquement les pages via :
- **Pages directes** du compte utilisateur
- **Business Managers** associés
- **Pages owned** et **client pages**
- **Déduplication** automatique

### Pagination Robuste

Support complet de la pagination Facebook :
- **Next URLs** et **cursors**
- **Gestion d'erreurs** gracieuse
- **Retry automatique**

## 📈 Performances

- **65 pages** synchronisées en ~30 secondes
- **API optimisée** avec mise en cache
- **Interface responsive** < 2s de chargement

## 🛡️ Sécurité

- **Variables d'environnement** pour les credentials
- **Validation** des tokens Facebook
- **Gestion d'erreurs** sécurisée
- **Logs** détaillés pour monitoring

## 📝 Changelog

### v2.2.0 (2025-06-24)
- ✅ Support Business Manager complet
- ✅ Récupération de 65 pages Facebook
- ✅ Pagination robuste améliorée
- ✅ Déploiement AWS production

### v2.1.2 (2025-06-23)
- ✅ Unification du module facebook_api
- ✅ Suppression des doublons de code
- ✅ Tests automatiques

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou support :
- **Email :** support@boismalin.com
- **Issues :** GitHub Issues
- **Documentation :** Wiki du projet

---

**Développé avec ❤️ pour Bois Malin**  
*Gestion professionnelle de 65 pages Facebook*

