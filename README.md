# Facebook Publisher Bois Malin

Application web complète pour la gestion et publication de contenu sur 65 pages Facebook simultanément.

## 🚀 Fonctionnalités

### ✅ **Gestion Multi-Pages**
- **65 pages Facebook** supportées avec pagination automatique
- Affichage du nombre d'abonnés pour chaque page
- Sélection individuelle ou globale des pages
- Boutons "Sélectionner tout" / "Désélectionner tout"

### ✅ **Publication Avancée**
- Publication de texte, images et vidéos
- Aperçu des fichiers avant publication
- Support des formats : JPG, PNG, GIF, MP4, MOV, AVI
- Publication simultanée sur plusieurs pages

### ✅ **Interface Moderne**
- Design responsive et intuitif
- Navigation par onglets (Publier, Pages, Paramètres, etc.)
- Prévisualisation en temps réel
- Gestion d'erreurs complète

## 📋 Prérequis

- Python 3.8+
- Compte Facebook Developer
- Application Facebook configurée
- Token d'accès Facebook avec permissions appropriées

## 🛠️ Installation

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
cp .env.example .env
```

Éditez le fichier `.env` avec vos identifiants :
```env
FACEBOOK_APP_ID=votre_app_id
FACEBOOK_APP_SECRET=votre_app_secret
FACEBOOK_ACCESS_TOKEN=votre_access_token
SECRET_KEY=votre_secret_key_flask
```

### 4. Lancer l'application
```bash
cd src
python main.py
```

L'application sera accessible sur `http://localhost:5001`

## 🔧 Configuration Facebook

### 1. Créer une application Facebook
1. Allez sur [Facebook Developers](https://developers.facebook.com/)
2. Créez une nouvelle application
3. Ajoutez le produit "Facebook Login"
4. Configurez les permissions nécessaires

### 2. Permissions requises
- `pages_manage_posts` : Publication sur les pages
- `pages_read_engagement` : Lecture des statistiques
- `pages_show_list` : Accès à la liste des pages

### 3. Token d'accès
- Générez un token d'accès utilisateur
- Échangez-le contre un token de page pour chaque page
- L'application gère automatiquement la récupération des tokens

## 📁 Structure du Projet

```
FB-Publisher-Bois-Malin/
├── src/
│   ├── main.py                 # Application Flask principale
│   ├── routes/
│   │   ├── facebook_api_routes.py  # Routes API Facebook
│   │   ├── analytics_routes.py     # Routes analytiques
│   │   ├── campaigns_routes.py     # Routes campagnes
│   │   └── audiences_routes.py     # Routes audiences
│   ├── models/
│   │   └── user.py             # Modèles utilisateur
│   ├── static/
│   │   └── index.html          # Interface utilisateur
│   └── database/
│       └── app.db              # Base de données SQLite
├── facebook_api.py             # API Facebook avec pagination
├── requirements.txt            # Dépendances Python
├── .env.example               # Exemple de configuration
├── .gitignore                 # Fichiers à ignorer
└── README.md                  # Documentation
```

## 🎯 Utilisation

### 1. Synchronisation des Pages
1. Allez dans l'onglet "Pages"
2. Cliquez sur "Synchroniser" pour récupérer vos 65 pages
3. Vérifiez que toutes les pages sont listées avec leurs abonnés

### 2. Publication de Contenu
1. Allez dans l'onglet "Publier"
2. Rédigez votre message
3. Ajoutez des fichiers (optionnel) avec aperçu
4. Sélectionnez les pages cibles :
   - Individuellement en cochant les cases
   - Toutes en une fois avec "Sélectionner tout"
5. Cliquez sur "Publier maintenant"

### 3. Gestion des Fichiers
- **Formats supportés :** JPG, PNG, GIF, MP4, MOV, AVI
- **Aperçu automatique :** Les images et vidéos sont prévisualisées
- **Suppression :** Possibilité de retirer des fichiers avant publication

## 🔍 Fonctionnalités Techniques

### Pagination Facebook
L'application utilise la pagination automatique pour récupérer toutes les pages :
```python
def get_user_pages(self) -> List[Dict]:
    all_pages = []
    url = "/me/accounts"
    params = {
        "fields": "name,access_token,fan_count,category,picture",
        "limit": 100
    }
    
    while url:
        response = self._make_request("GET", url, params=params)
        # Gestion de la pagination avec curseur "after"
        ...
```

### Gestion Multi-Pages
Publication simultanée sur plusieurs pages avec gestion d'erreurs :
```python
@facebook_bp.route('/upload', methods=['POST'])
def upload():
    # Support des formats JSON et form-data
    # Publication sur toutes les pages sélectionnées
    # Gestion d'erreurs individuelles par page
```

## 🚨 Dépannage

### Problème : "Endpoint not found"
- Vérifiez que l'application Flask est démarrée
- Contrôlez que le blueprint est enregistré dans `main.py`

### Problème : "No pages found"
- Vérifiez vos tokens d'accès Facebook
- Assurez-vous d'avoir les permissions `pages_show_list`
- Cliquez sur "Synchroniser" dans l'onglet Pages

### Problème : "Publication failed"
- Vérifiez les permissions `pages_manage_posts`
- Contrôlez que les pages sont bien sélectionnées
- Vérifiez les logs dans la console du navigateur

## 📊 Logs et Monitoring

L'application génère des logs détaillés :
- Logs de l'API Facebook dans `src/facebook_api.log`
- Logs de l'application dans la console
- Logs de debug dans le navigateur (F12)

## 🔒 Sécurité

- **Tokens :** Stockés dans des variables d'environnement
- **HTTPS :** Recommandé pour la production
- **Permissions :** Principe du moindre privilège
- **Validation :** Validation côté serveur et client

## 🚀 Déploiement

### Déploiement Local
```bash
cd src
python main.py
```

### Déploiement AWS (Exemple)
```bash
# Configuration du serveur
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Lancement avec nohup
cd src
nohup python3 main.py > app.log 2>&1 &
```

### Variables d'Environnement Production
```env
FLASK_ENV=production
FACEBOOK_APP_ID=production_app_id
FACEBOOK_APP_SECRET=production_app_secret
FACEBOOK_ACCESS_TOKEN=production_token
SECRET_KEY=production_secret_key_très_sécurisé
```

## 📈 Améliorations Futures

- [ ] Programmation de publications
- [ ] Statistiques avancées
- [ ] Gestion des campagnes publicitaires
- [ ] API REST pour intégrations tierces
- [ ] Interface mobile native
- [ ] Support de plus de réseaux sociaux

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation Facebook Developers
- Vérifiez les logs de l'application

## 🎉 Remerciements

- Facebook Graph API pour l'intégration
- Flask pour le framework web
- Tous les contributeurs du projet

---

**Développé avec ❤️ pour Bois Malin**

