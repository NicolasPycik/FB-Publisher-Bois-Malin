# Application Design: FacebookPublisherBoisMalin

## Vue d'ensemble

Cette documentation détaille la conception mise à jour de l'application FacebookPublisherBoisMalin, transformant une application de simulation en un outil professionnel intégré aux API Facebook pour la gestion de pages, la publication de contenu, et la création/gestion de publicités.

## Architecture

### Structure des fichiers

```
facebook_automation/
├── .env.example                # Exemple de configuration des variables d'environnement
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation principale
├── FacebookPublisherBoisMalin.py  # Application principale (interface utilisateur)
├── facebook_api.py             # Wrapper pour les appels API Facebook
├── models/                     # Modèles de données
│   ├── page.py                 # Modèle pour les pages Facebook
│   ├── post.py                 # Modèle pour les publications
│   └── ad.py                   # Modèle pour les publicités
├── utils/                      # Utilitaires
│   ├── config.py               # Gestion de la configuration
│   ├── logger.py               # Système de journalisation
│   └── scheduler.py            # Planificateur de publications
├── data/                       # Stockage local des données
│   ├── facebook_pages.json     # Pages Facebook et tokens
│   ├── scheduled_posts.json    # Publications programmées
│   └── boosted_ads.json        # Publicités créées
└── tests/                      # Tests unitaires
    ├── test_facebook_api.py    # Tests pour le wrapper API
    └── test_scheduler.py       # Tests pour le planificateur
```

### Composants principaux

1. **Interface utilisateur (FacebookPublisherBoisMalin.py)**
   - Interface Tkinter avec onglets
   - Gestion des événements utilisateur
   - Affichage des résultats et erreurs

2. **Wrapper API (facebook_api.py)**
   - Gestion des appels HTTP vers l'API Facebook
   - Authentification et gestion des tokens
   - Gestion des erreurs et retries
   - Logging des requêtes et réponses

3. **Planificateur (utils/scheduler.py)**
   - Thread en arrière-plan
   - Vérification périodique des publications programmées
   - Publication automatique au moment prévu

4. **Modèles de données**
   - Représentation des entités Facebook (pages, posts, publicités)
   - Validation des données
   - Sérialisation/désérialisation JSON

## Spécifications techniques

### Environnement

- Python 3.11+
- Tkinter pour l'interface utilisateur
- Requests pour les appels API
- Dotenv pour la gestion des variables d'environnement
- Threading pour les tâches en arrière-plan

### API Facebook

#### API Graph

1. **Authentification**
   - Utilisation de tokens d'accès de page
   - Échange de tokens courts contre tokens longs
   - Vérification de validité des tokens

2. **Gestion des pages**
   - Récupération des pages associées au compte
   - Stockage des tokens d'accès par page

3. **Publication de contenu**
   - Publication de texte, liens, images, vidéos
   - Programmation de publications
   - Récupération des statistiques

#### API Marketing

1. **Gestion des comptes publicitaires**
   - Récupération des comptes publicitaires
   - Sélection du compte actif

2. **Boost de publications**
   - Création de campagnes à partir de publications existantes
   - Paramétrage du budget et du ciblage

3. **Création de publicités**
   - Définition des objectifs, budgets, ciblages
   - Upload de médias et création de créatifs
   - Suivi des performances

### Gestion des erreurs

1. **Stratégie de retry**
   - Retry exponentiel pour les erreurs 500-599
   - Gestion des quotas et limites d'API

2. **Affichage des erreurs**
   - Messages d'erreur clairs dans l'interface
   - Journalisation détaillée pour le débogage

3. **Validation des données**
   - Vérification des entrées utilisateur
   - Validation des réponses API

## Interface utilisateur

### Onglets

1. **Publication**
   - Sélection de pages (avec noms réels)
   - Composition de messages
   - Upload de médias
   - Bouton de boost post après publication

2. **Programmation**
   - Liste des publications programmées
   - Interface de planification
   - Statut des publications (en attente/publiées)

3. **Publicités** (nouveau)
   - Sélection de compte publicitaire
   - Création de campagnes
   - Paramétrage des audiences
   - Upload de créatifs
   - Suivi des performances

4. **Statistiques**
   - Métriques de pages
   - Performances des publications
   - Visualisation des données

5. **Paramètres**
   - Gestion des tokens
   - Configuration de l'application
   - Options de journalisation

6. **À propos**
   - Informations sur l'application
   - Documentation d'aide

## Flux de travail

### Publication organique

1. L'utilisateur sélectionne une ou plusieurs pages
2. L'utilisateur compose un message et/ou ajoute des médias
3. L'application publie le contenu via l'API Graph
4. L'application affiche l'ID du post et propose de l'ouvrir dans le navigateur

### Programmation

1. L'utilisateur configure une publication future
2. L'application enregistre la configuration dans scheduled_posts.json
3. Le thread scheduler vérifie périodiquement les publications à effectuer
4. Les publications sont automatiquement publiées à l'heure prévue

### Boost de publication

1. L'utilisateur sélectionne un post existant
2. L'utilisateur configure le budget et le ciblage
3. L'application crée une campagne, un ad set et une publicité via l'API Marketing
4. L'application affiche les IDs créés et les enregistre dans boosted_ads.json

### Création de publicité

1. L'utilisateur sélectionne un compte publicitaire
2. L'utilisateur configure l'objectif, le budget, le ciblage et le créatif
3. L'application crée les entités publicitaires via l'API Marketing
4. L'application affiche les IDs créés et propose de suivre les performances

## Tests et validation

1. **Tests unitaires**
   - Tests du wrapper API avec mocks
   - Tests du planificateur
   - Tests des modèles de données

2. **Intégration continue**
   - Exécution des tests sur GitHub Actions
   - Vérification du style de code (PEP 8)

3. **Critères d'acceptation**
   - Publication réussie avec ID valide
   - Planification fonctionnelle
   - Création de publicités avec statut PAUSED
   - Gestion appropriée des erreurs

## Documentation

1. **README.md**
   - Instructions d'installation
   - Configuration de l'environnement
   - Guide d'utilisation

2. **Captures d'écran et GIF**
   - Démonstration des fonctionnalités principales
   - Workflow de publication et boost

3. **Documentation du code**
   - Docstrings pour les fonctions et classes
   - Commentaires pour les sections complexes
