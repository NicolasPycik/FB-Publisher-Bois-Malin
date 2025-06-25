# Guide d'Installation Rapide - Facebook Publisher Bois Malin

## Prérequis
- Python 3.11 ou plus récent
- Compte développeur Facebook
- Application Facebook configurée

## Installation

1. **Extraire l'application**
   ```bash
   # Extraire le fichier zip dans un dossier de votre choix
   cd /chemin/vers/facebook_automation
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement**
   ```bash
   # Copier le fichier d'exemple
   cp .env.example .env
   
   # Éditer le fichier .env avec vos informations Facebook
   # APP_ID=votre_app_id
   # APP_SECRET=votre_app_secret
   # USER_ACCESS_TOKEN=votre_token
   ```

4. **Tester l'installation**
   ```bash
   python test_app.py
   ```

5. **Lancer l'application**
   ```bash
   python main.py
   ```

## Configuration Facebook

1. Créer une application sur https://developers.facebook.com/
2. Ajouter les produits "Facebook Login" et "Marketing API"
3. Configurer les permissions : `pages_manage_posts`, `pages_read_engagement`, `ads_management`
4. Générer un token d'accès depuis l'Explorateur d'API

## Première Utilisation

1. Aller dans l'onglet "Paramètres"
2. Cliquer sur "Actualiser la liste des pages Facebook"
3. Vérifier que vos pages apparaissent correctement
4. Commencer à publier depuis l'onglet "Publication"

## Support

- Consulter README.pdf pour la documentation complète
- Vérifier les logs dans facebook_api.log en cas de problème
- Utiliser le script test_app.py pour diagnostiquer les problèmes

