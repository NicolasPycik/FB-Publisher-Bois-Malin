# Facebook Publisher Bois Malin - Documentation Complète

**Version 2.1 avec Intégration API Facebook Marketing**

**Auteur :** Manus AI  
**Client :** Nicolas Pycik  
**Date :** 19 juin 2025

---

## Table des Matières

1. [Introduction](#introduction)
2. [Nouveautés Version 2.1](#nouveautés-version-21)
3. [Installation et Configuration](#installation-et-configuration)
4. [Guide d'Utilisation](#guide-dutilisation)
5. [Onglet Publicités](#onglet-publicités)
6. [Fonctionnalité Boost Post](#fonctionnalité-boost-post)
7. [Statistiques et Insights](#statistiques-et-insights)
8. [API Facebook et Authentification](#api-facebook-et-authentification)
9. [Dépannage](#dépannage)
10. [Développement et Contribution](#développement-et-contribution)
11. [Annexes](#annexes)

---



## Introduction

Facebook Publisher Bois Malin est une application de bureau développée en Python qui permet de gérer efficacement la publication de contenu sur plusieurs pages Facebook simultanément. Cette version 2.1 représente une évolution majeure par rapport à la version précédente, intégrant une connexion réelle avec l'API Facebook Graph et l'API Marketing pour offrir des fonctionnalités professionnelles complètes de gestion de contenu et de publicité.

L'application a été spécialement conçue pour répondre aux besoins de Nicolas Pycik dans la gestion de ses 65 pages Facebook "Bois Malin". Elle permet non seulement de publier du contenu de manière efficace, mais aussi de programmer des publications, de créer des campagnes publicitaires complètes, de booster des posts existants, et d'analyser les performances grâce à l'intégration des statistiques Facebook en temps réel.

### Principales Fonctionnalités

Cette application offre un ensemble complet de fonctionnalités pour la gestion professionnelle de pages Facebook. La publication de contenu constitue le cœur de l'application, permettant de diffuser simultanément du texte, des images, des vidéos et des liens sur plusieurs pages sélectionnées. Le système de programmation intégré permet de planifier des publications à l'avance, avec un scheduler automatique qui se charge de publier le contenu aux heures définies.

La gestion des publicités représente une fonctionnalité avancée qui permet de créer des campagnes publicitaires complètes, incluant la création de créatifs, la définition du ciblage, et la gestion des budgets. Le système de "boost post" permet également de promouvoir rapidement des publications existantes pour augmenter leur portée directement depuis l'onglet Statistiques.

L'analyse des performances est assurée par l'intégration des statistiques Facebook en temps réel, offrant des insights détaillés sur les impressions, l'engagement, et les réactions pour chaque page et chaque publication. La gestion des tokens d'accès est entièrement automatisée, avec des alertes pour le renouvellement et des outils pour l'échange de tokens court terme en tokens long terme.

### Architecture Technique

L'application est construite sur une architecture modulaire robuste utilisant Python 3.11+ et respectant les standards PEP 8. L'interface utilisateur est développée avec Tkinter, offrant une expérience native sur tous les systèmes d'exploitation supportés. Le wrapper API Facebook centralise toutes les interactions avec les services Facebook, incluant la gestion des erreurs, les tentatives de reconnexion automatiques, et le logging détaillé de toutes les opérations.

La persistance des données est assurée par des fichiers JSON locaux pour les pages, les publications programmées, et les campagnes publicitaires. La configuration de l'application utilise des variables d'environnement stockées dans un fichier .env pour garantir la sécurité des informations sensibles comme les tokens d'accès et les secrets d'application.

Le système de logging intégré enregistre toutes les opérations importantes, facilitant le débogage et le suivi des activités. Les tests unitaires couvrent l'ensemble des fonctionnalités critiques, garantissant la fiabilité et la stabilité de l'application.

## Nouveautés Version 2.1

La version 2.1 de Facebook Publisher Bois Malin apporte des améliorations significatives et de nouvelles fonctionnalités qui transforment l'application en une solution complète de marketing Facebook.

### Onglet Publicités Complet

L'onglet Publicités a été entièrement repensé et implémenté pour offrir une interface complète de création de campagnes publicitaires. Cette nouvelle interface permet de sélectionner un compte publicitaire, de choisir une page Facebook, de définir l'objectif de campagne (TRAFFIC, CONVERSIONS, REACH, BRAND_AWARENESS, POST_ENGAGEMENT), et de configurer le budget quotidien avec les dates de début et de fin.

La section de ciblage permet de définir précisément l'audience avec des critères géographiques (pays), démographiques (âge minimum et maximum), et d'autres paramètres de ciblage avancés. La création de créatifs publicitaires est intégrée avec des champs pour le message publicitaire, le lien de destination, l'upload d'images, et la sélection d'appels à l'action (LEARN_MORE, SHOP_NOW, SIGN_UP, DOWNLOAD, CONTACT_US, CALL_NOW).

L'interface affiche également une liste des campagnes et publicités existantes dans un TreeView avec les informations essentielles : ID, nom, statut, objectif, et budget. Cette vue d'ensemble permet de suivre facilement l'état de toutes les campagnes créées.

### Fonctionnalité Boost Post Intégrée

La fonctionnalité de boost post a été intégrée directement dans l'onglet Statistiques, permettant de promouvoir rapidement les publications les plus performantes. Un bouton "Booster ce post" apparaît sous la liste des publications récentes, et un simple clic lance le processus de création d'une campagne de boost complète.

Le système crée automatiquement une campagne avec l'objectif POST_ENGAGEMENT, un ensemble de publicités avec un ciblage par défaut (France, 18-65 ans), un créatif basé sur la publication existante, et une publicité finale. Le budget par défaut est fixé à 20€ par jour, et toutes les campagnes de boost sont créées avec le statut PAUSED pour permettre la révision avant activation.

Un dialogue de sélection permet de choisir le compte publicitaire à utiliser pour le boost, offrant une flexibilité totale dans la gestion des budgets publicitaires.

### Statistiques et Insights en Temps Réel

L'onglet Statistiques a été complètement refondu pour afficher des données réelles provenant de l'API Facebook Insights. L'interface permet de sélectionner une page spécifique et une période de dates pour analyser les performances.

Les métriques de page affichées incluent les impressions totales, les utilisateurs engagés, la portée, et le nombre de fans. Ces données sont mises à jour en temps réel lors de l'actualisation et fournissent une vue d'ensemble claire des performances de chaque page.

La liste des publications récentes affiche les 10 dernières publications avec leurs métriques individuelles : impressions, engagement, et date de publication. Chaque publication peut être analysée en détail ou boostée directement depuis cette interface.

### Extensions API et Nouvelles Méthodes

Le wrapper API Facebook a été étendu avec de nouvelles méthodes spécialisées pour les fonctionnalités Marketing API :

- `get_ad_accounts()` : Récupère la liste des comptes publicitaires accessibles
- `get_page_insights()` : Obtient les statistiques d'une page pour une période donnée
- `get_post_insights()` : Récupère les métriques d'une publication spécifique
- `get_page_posts()` : Liste les publications récentes d'une page
- `_get_page_token()` : Méthode helper pour récupérer les tokens spécifiques aux pages

Ces nouvelles méthodes utilisent les mêmes mécanismes de gestion d'erreurs, de retry automatique, et de logging que les méthodes existantes, garantissant une expérience cohérente et fiable.

### Améliorations de Stabilité

La version 2.1 inclut également des améliorations importantes de stabilité, notamment la correction du scheduler pour un arrêt propre de l'application, une meilleure gestion des erreurs dans les appels API, et une couverture de tests étendue avec 13 tests unitaires couvrant toutes les nouvelles fonctionnalités.

Le système de logging a été amélioré pour fournir des informations plus détaillées sur les opérations Marketing API, facilitant le débogage et le suivi des campagnes publicitaires.



## Installation et Configuration

### Prérequis Système

Avant d'installer Facebook Publisher Bois Malin, assurez-vous que votre système répond aux exigences minimales suivantes. L'application nécessite Python 3.11 ou une version plus récente pour fonctionner correctement. Cette version de Python inclut des améliorations importantes en termes de performance et de sécurité qui sont essentielles pour les interactions avec l'API Facebook.

Votre système doit également disposer d'une connexion Internet stable pour communiquer avec les services Facebook. L'application fonctionne sur Windows 10/11, macOS 10.15+, et les distributions Linux modernes. Pour Windows, il est recommandé d'utiliser Windows 11 pour une compatibilité optimale avec les dernières fonctionnalités de sécurité.

Un compte développeur Facebook est indispensable pour utiliser l'application. Ce compte vous permettra de créer une application Facebook et d'obtenir les identifiants nécessaires (App ID et App Secret) pour l'authentification. Vous devez également avoir les droits d'administration sur les pages Facebook que vous souhaitez gérer.

### Installation de Python et des Dépendances

La première étape consiste à installer Python 3.11 ou une version plus récente sur votre système. Rendez-vous sur le site officiel de Python (https://www.python.org/downloads/) et téléchargez la version appropriée pour votre système d'exploitation. Lors de l'installation sur Windows, assurez-vous de cocher l'option "Add Python to PATH" pour pouvoir utiliser Python depuis n'importe quel répertoire.

Une fois Python installé, ouvrez un terminal ou une invite de commandes et vérifiez que l'installation s'est déroulée correctement en exécutant la commande `python --version`. Vous devriez voir s'afficher la version de Python installée.

Naviguez ensuite vers le répertoire où vous avez extrait l'application Facebook Publisher Bois Malin. Ce répertoire contient un fichier `requirements.txt` qui liste toutes les dépendances nécessaires. Installez ces dépendances en exécutant la commande suivante :

```bash
pip install -r requirements.txt
```

Cette commande installera automatiquement toutes les bibliothèques requises, notamment `requests` pour les appels API, `python-dotenv` pour la gestion des variables d'environnement, `pillow` pour le traitement des images, et les outils de test `pytest` et `responses`.

### Configuration de l'Application Facebook

La configuration de l'application Facebook constitue une étape cruciale pour le bon fonctionnement de Facebook Publisher Bois Malin. Connectez-vous à votre compte développeur Facebook et accédez au Facebook Developers Console (https://developers.facebook.com/). Si vous n'avez pas encore de compte développeur, vous devrez en créer un en suivant les instructions fournies par Facebook.

Créez une nouvelle application en cliquant sur "Créer une App" et sélectionnez le type "Entreprise" pour avoir accès à toutes les fonctionnalités nécessaires. Donnez un nom significatif à votre application, par exemple "Gestionnaire Pages Bois Malin", et renseignez les informations demandées.

Une fois l'application créée, notez soigneusement l'App ID et l'App Secret qui s'affichent dans le tableau de bord. Ces identifiants sont essentiels pour l'authentification et doivent être gardés confidentiels. Configurez ensuite les produits Facebook nécessaires en ajoutant "Facebook Login" et "Marketing API" à votre application.

Dans les paramètres de Facebook Login, ajoutez les URL de redirection appropriées. Pour une utilisation locale, vous pouvez utiliser `http://localhost:8080/auth/callback`. Configurez également les permissions nécessaires, notamment `pages_manage_posts`, `pages_read_engagement`, `ads_management`, et `business_management`.

### Configuration des Variables d'Environnement

La sécurité des informations sensibles est assurée par l'utilisation de variables d'environnement stockées dans un fichier `.env`. Copiez le fichier `.env.example` fourni avec l'application et renommez-le en `.env`. Ce fichier contiendra toutes les informations de configuration nécessaires.

Ouvrez le fichier `.env` avec un éditeur de texte et renseignez les valeurs suivantes :

```
APP_ID=votre_app_id_facebook
APP_SECRET=votre_app_secret_facebook
USER_ACCESS_TOKEN=votre_token_utilisateur
SYSTEM_USER_TOKEN=votre_token_systeme
```

L'APP_ID et l'APP_SECRET correspondent aux identifiants obtenus lors de la création de votre application Facebook. Le USER_ACCESS_TOKEN peut être généré depuis l'Explorateur d'API Facebook (https://developers.facebook.com/tools/explorer/). Sélectionnez votre application, demandez les permissions nécessaires, et générez un token d'accès.

Le SYSTEM_USER_TOKEN est optionnel mais recommandé pour les fonctionnalités avancées. Il peut être créé depuis le Business Manager Facebook si vous gérez vos pages dans un contexte professionnel.

### Première Exécution et Vérification

Avant de lancer l'application complète, il est recommandé d'exécuter le script de test pour vérifier que tout est correctement configuré. Depuis le répertoire de l'application, exécutez la commande :

```bash
python test_app.py
```

Ce script vérifie que tous les modules peuvent être importés, que l'API Facebook est correctement initialisée, et que les fonctionnalités de base fonctionnent. Si tous les tests passent, vous verrez le message "All tests passed! The application is ready to use."

En cas d'erreur, le script vous indiquera précisément quel composant pose problème. Les erreurs les plus courantes concernent les variables d'environnement manquantes ou incorrectes, ou les permissions insuffisantes sur l'application Facebook.

Une fois les tests réussis, vous pouvez lancer l'application principale avec la commande :

```bash
python main.py
```

L'interface graphique de Facebook Publisher Bois Malin devrait s'ouvrir, affichant les différents onglets pour la publication, la programmation, les publicités, les statistiques, et les paramètres.


## Guide d'Utilisation

### Interface Principale et Navigation

L'interface de Facebook Publisher Bois Malin est organisée en onglets thématiques pour faciliter la navigation et l'utilisation. Chaque onglet correspond à une fonctionnalité spécifique de l'application, permettant une approche structurée de la gestion de vos pages Facebook.

L'onglet "Publication" constitue le cœur de l'application et sera probablement celui que vous utiliserez le plus fréquemment. Il permet de créer et publier du contenu immédiatement ou de le programmer pour une diffusion ultérieure. L'interface est conçue pour être intuitive, avec des champs clairement identifiés pour le message, les liens, les médias, et la sélection des pages cibles.

L'onglet "Programmation" offre une vue d'ensemble de toutes vos publications programmées, permettant de les modifier, les supprimer, ou de consulter leur statut. Le système de programmation fonctionne en arrière-plan, publiant automatiquement vos contenus aux heures définies, même si l'application n'est pas ouverte au moment de la publication.

L'onglet "Publicités" donne accès aux fonctionnalités avancées de marketing Facebook, incluant la création de campagnes publicitaires complètes et le boost de publications existantes. Cette section nécessite une compréhension des concepts de base du marketing Facebook, mais l'interface guide l'utilisateur à travers chaque étape du processus.

L'onglet "Statistiques" présente les données de performance de vos pages et publications, avec des graphiques et des tableaux détaillés. Ces informations sont essentielles pour comprendre l'impact de votre contenu et optimiser votre stratégie de communication.

Enfin, l'onglet "Paramètres" centralise toute la configuration de l'application, notamment la gestion des tokens d'accès, la synchronisation des pages, et les préférences générales.

### Publication de Contenu

La publication de contenu représente la fonctionnalité principale de Facebook Publisher Bois Malin. Le processus de publication est conçu pour être simple et efficace, tout en offrant une grande flexibilité dans le type de contenu que vous pouvez partager.

Pour créer une nouvelle publication, commencez par rédiger votre message dans la zone de texte principale. Cette zone supporte le texte enrichi et vous permet de créer des messages de toute longueur. Prenez le temps de rédiger un contenu engageant qui correspond à l'identité de vos pages Bois Malin. N'hésitez pas à utiliser des émojis et des hashtags pour augmenter l'engagement de votre audience.

Si votre publication inclut un lien externe, saisissez l'URL complète dans le champ "Lien". Facebook récupérera automatiquement les métadonnées du lien (titre, description, image de prévisualisation) lors de la publication. Assurez-vous que le lien est valide et accessible, car Facebook vérifie la validité des liens avant de les publier.

Pour ajouter des médias à votre publication, utilisez le bouton "Ajouter une image" ou "Ajouter une vidéo" selon le type de contenu que vous souhaitez partager. L'application supporte les formats d'image les plus courants (JPEG, PNG, GIF) ainsi que les vidéos MP4. Veillez à respecter les recommandations de Facebook concernant la taille et la qualité des médias pour optimiser l'affichage sur toutes les plateformes.

La sélection des pages cibles constitue une étape cruciale du processus de publication. La liste des pages disponibles est automatiquement synchronisée avec votre compte Facebook et affiche les noms réels de vos pages. Vous pouvez sélectionner une ou plusieurs pages en maintenant la touche Ctrl (ou Cmd sur Mac) enfoncée. Cette fonctionnalité vous permet de personnaliser la diffusion de votre contenu selon le public cible de chaque page.

Une fois tous les éléments de votre publication configurés, vous avez le choix entre publier immédiatement ou programmer la publication pour plus tard. La publication immédiate diffuse votre contenu instantanément sur toutes les pages sélectionnées, tandis que la programmation vous permet de définir une date et une heure précises pour la diffusion.

### Programmation de Publications

Le système de programmation de Facebook Publisher Bois Malin offre une flexibilité exceptionnelle pour planifier votre stratégie de contenu. Cette fonctionnalité est particulièrement utile pour maintenir une présence régulière sur vos pages Facebook, même lorsque vous n'êtes pas disponible pour publier manuellement.

Pour programmer une publication, suivez d'abord les étapes de création de contenu décrites précédemment. Au lieu de cliquer sur "Publier maintenant", sélectionnez "Programmer". Une boîte de dialogue s'ouvrira vous permettant de définir la date et l'heure de publication souhaitées.

Le format de date attendu est YYYY-MM-DD HH:MM (par exemple, 2025-06-20 14:30 pour le 20 juin 2025 à 14h30). Assurez-vous de choisir une date et une heure dans le futur, car l'application ne permet pas de programmer des publications dans le passé. Prenez en compte le fuseau horaire de votre système, car c'est celui qui sera utilisé pour la programmation.

Une fois la publication programmée, elle apparaît dans l'onglet "Programmation" avec toutes les informations pertinentes : contenu du message, pages cibles, médias associés, et heure de publication prévue. Vous pouvez modifier ou supprimer une publication programmée tant qu'elle n'a pas encore été diffusée.

Le scheduler fonctionne en arrière-plan et vérifie toutes les minutes s'il y a des publications à diffuser. Lorsqu'une publication programmée atteint son heure de diffusion, elle est automatiquement publiée sur les pages sélectionnées. Un message de confirmation vous informe du succès de l'opération, et la publication est marquée comme "Publiée" dans la liste.

Il est important de noter que pour que les publications programmées soient diffusées, l'application doit être en cours d'exécution au moment prévu. Si l'application est fermée, les publications en attente seront traitées dès le prochain démarrage, mais avec un retard correspondant à la durée de fermeture.

### Gestion des Pages Facebook

La gestion efficace de vos pages Facebook constitue un aspect fondamental de l'utilisation de Facebook Publisher Bois Malin. L'application offre des outils complets pour synchroniser, organiser, et administrer l'ensemble de vos pages depuis une interface centralisée.

La synchronisation des pages s'effectue depuis l'onglet "Paramètres" en cliquant sur "Actualiser la liste des pages Facebook". Cette opération interroge l'API Facebook pour récupérer toutes les pages auxquelles votre compte a accès en tant qu'administrateur. L'application récupère automatiquement les noms réels des pages, leurs identifiants uniques, et les tokens d'accès spécifiques à chaque page.

Cette synchronisation est particulièrement importante lors de la première utilisation de l'application, mais aussi chaque fois que vous ajoutez de nouvelles pages à votre compte Facebook ou que vous modifiez les permissions d'accès. L'application détecte automatiquement les nouvelles pages et les ajoute à votre liste sans intervention manuelle.

Chaque page est affichée avec son nom complet et son identifiant Facebook, permettant une identification précise même si vous gérez des pages aux noms similaires. Les tokens d'accès spécifiques à chaque page sont gérés automatiquement par l'application, garantissant que chaque publication est effectuée avec les bonnes permissions.

La liste des pages est utilisée dans tous les autres onglets de l'application, notamment pour la sélection des pages cibles lors de la publication de contenu. Cette approche centralisée garantit la cohérence des données et évite les erreurs de publication sur de mauvaises pages.

Si vous rencontrez des problèmes avec une page spécifique (par exemple, des erreurs de publication récurrentes), vérifiez d'abord que vous avez toujours les droits d'administration sur cette page depuis votre compte Facebook. Les changements de permissions peuvent parfois affecter la capacité de l'application à publier du contenu.


## API Facebook et Authentification

### Comprendre l'Écosystème Facebook pour Développeurs

L'intégration avec l'API Facebook constitue le cœur technique de Facebook Publisher Bois Malin. Cette section détaille les aspects techniques de cette intégration, permettant une compréhension approfondie du fonctionnement de l'application et des meilleures pratiques pour maintenir une connexion stable avec les services Facebook.

Facebook propose plusieurs APIs pour interagir avec sa plateforme : l'API Graph pour les fonctionnalités de base (publications, pages, insights), l'API Marketing pour les publicités, et l'API Instagram pour la gestion des comptes Instagram Business. Facebook Publisher Bois Malin utilise principalement l'API Graph et l'API Marketing pour offrir un ensemble complet de fonctionnalités.

L'API Graph de Facebook suit une architecture RESTful et utilise le protocole HTTPS pour toutes les communications. Chaque ressource (page, publication, utilisateur) est identifiée par un ID unique et peut être interrogée ou modifiée via des requêtes HTTP standard (GET, POST, DELETE). L'authentification s'effectue via des tokens d'accès OAuth 2.0 qui doivent être inclus dans chaque requête.

La version d'API utilisée par l'application est la v18.0, qui représente la version stable la plus récente au moment du développement. Facebook maintient plusieurs versions d'API simultanément, mais il est recommandé d'utiliser la version la plus récente pour bénéficier des dernières fonctionnalités et corrections de sécurité.

### Gestion des Tokens d'Accès

La gestion des tokens d'accès représente l'aspect le plus critique de l'intégration avec Facebook. Ces tokens servent à authentifier l'application auprès des services Facebook et déterminent les actions que l'application peut effectuer au nom de l'utilisateur.

Facebook utilise plusieurs types de tokens selon le contexte d'utilisation. Les tokens utilisateur permettent d'accéder aux ressources associées à un compte Facebook spécifique, comme les pages administrées par cet utilisateur. Les tokens de page offrent un accès spécifique à une page particulière et sont nécessaires pour publier du contenu. Les tokens d'application permettent d'accéder aux fonctionnalités générales de l'API sans contexte utilisateur spécifique.

Les tokens d'accès ont une durée de vie limitée pour des raisons de sécurité. Les tokens court terme expirent généralement après une à deux heures, tandis que les tokens long terme peuvent être valides pendant 60 jours. Facebook Publisher Bois Malin inclut des mécanismes pour gérer automatiquement le renouvellement des tokens et alerter l'utilisateur lorsqu'un renouvellement manuel est nécessaire.

L'échange d'un token court terme en token long terme s'effectue via l'onglet "Paramètres" de l'application. Cette opération utilise l'App ID et l'App Secret de votre application Facebook pour demander à Facebook de prolonger la durée de vie du token. Le processus est entièrement automatisé et ne nécessite aucune intervention technique de votre part.

La vérification de la validité d'un token peut être effectuée à tout moment via l'outil de débogage intégré à l'application. Cette fonctionnalité interroge l'endpoint `/debug_token` de Facebook pour obtenir des informations détaillées sur le token, notamment sa date d'expiration, les permissions accordées, et l'application qui l'a généré.

### Sécurité et Bonnes Pratiques

La sécurité des informations d'authentification constitue une priorité absolue dans la conception de Facebook Publisher Bois Malin. Toutes les informations sensibles (App ID, App Secret, tokens d'accès) sont stockées dans des variables d'environnement et ne sont jamais incluses directement dans le code source de l'application.

Le fichier `.env` qui contient ces informations doit être protégé avec les permissions appropriées du système de fichiers et ne doit jamais être partagé ou inclus dans un système de contrôle de version. L'application inclut un fichier `.env.example` qui montre la structure attendue sans révéler d'informations sensibles.

Toutes les communications avec l'API Facebook s'effectuent via HTTPS, garantissant le chiffrement des données en transit. L'application implémente également des mécanismes de retry avec backoff exponentiel pour gérer les erreurs temporaires et éviter de surcharger les serveurs Facebook.

Le logging des opérations API est configuré pour enregistrer les détails des requêtes et réponses tout en masquant automatiquement les informations sensibles comme les tokens d'accès. Ces logs sont essentiels pour le débogage mais ne compromettent pas la sécurité de vos informations d'authentification.

### Gestion des Erreurs et Limitations

L'API Facebook impose diverses limitations pour garantir la stabilité de la plateforme et prévenir les abus. Facebook Publisher Bois Malin implémente une gestion robuste de ces limitations pour offrir une expérience utilisateur fluide même en cas de contraintes temporaires.

Les limitations de taux (rate limiting) constituent la contrainte la plus courante. Facebook limite le nombre de requêtes qu'une application peut effectuer dans un intervalle de temps donné. L'application détecte automatiquement ces limitations et met en pause les opérations le temps nécessaire avant de reprendre.

Les erreurs de permissions surviennent lorsque l'application tente d'effectuer une action pour laquelle elle n'a pas les droits nécessaires. Ces erreurs sont généralement liées à des changements dans les permissions de l'utilisateur ou à l'expiration des tokens d'accès. L'application affiche des messages d'erreur explicites pour guider l'utilisateur vers la résolution du problème.

Les erreurs de validation se produisent lorsque les données soumises à l'API ne respectent pas les critères de Facebook (par exemple, un lien invalide ou un contenu non conforme aux politiques). L'application valide autant que possible les données avant de les soumettre, mais certaines validations ne peuvent être effectuées que côté Facebook.

### Monitoring et Maintenance

Le monitoring continu de l'intégration API est essentiel pour maintenir la fiabilité de l'application. Facebook Publisher Bois Malin inclut des outils de monitoring intégrés qui surveillent la santé de la connexion API et alertent l'utilisateur en cas de problème.

L'application vérifie automatiquement la validité des tokens d'accès au démarrage et affiche des alertes lorsque l'expiration approche. Cette approche proactive permet d'éviter les interruptions de service dues à des tokens expirés.

Les mises à jour de l'API Facebook sont annoncées à l'avance par Facebook via le changelog officiel. Bien que l'application soit conçue pour être compatible avec les versions futures de l'API, il est recommandé de surveiller les annonces de Facebook et de mettre à jour l'application si nécessaire.

La maintenance régulière inclut également la vérification des permissions de l'application Facebook, la rotation des secrets d'application selon les bonnes pratiques de sécurité, et la mise à jour des dépendances Python pour bénéficier des dernières corrections de sécurité.


## Fonctionnalités Avancées

### Système de Boost Post

Le système de boost post de Facebook Publisher Bois Malin permet de promouvoir rapidement vos publications existantes pour augmenter leur portée et leur engagement. Cette fonctionnalité utilise l'API Marketing de Facebook pour créer automatiquement tous les éléments nécessaires à une campagne de promotion : créatif publicitaire, campagne, ensemble de publicités, et publicité finale.

Le processus de boost commence par la sélection d'une publication existante que vous souhaitez promouvoir. L'application affiche la liste de vos publications récentes avec leurs métriques de base (impressions, engagement, réactions) pour vous aider à identifier les contenus les plus performants qui méritent d'être boostés.

Une fois la publication sélectionnée, l'application crée automatiquement un créatif publicitaire basé sur cette publication. Ce créatif utilise l'ID de la publication originale (au format page_id_post_id) et conserve tous les éléments visuels et textuels de la publication d'origine. Cette approche garantit la cohérence entre votre contenu organique et votre contenu sponsorisé.

La création de la campagne publicitaire s'effectue avec l'objectif "POST_ENGAGEMENT" qui est spécifiquement conçu pour maximiser l'engagement sur les publications boostées. L'application configure automatiquement les paramètres de base de la campagne, notamment le nom (généré automatiquement avec la date et l'heure), le statut initial (PAUSED pour permettre la révision), et les paramètres de facturation.

L'ensemble de publicités (adset) définit les paramètres de ciblage, de budget, et de programmation pour votre boost. L'application propose des options de ciblage prédéfinies basées sur l'audience de votre page, mais vous pouvez personnaliser ces paramètres selon vos objectifs spécifiques. Le budget peut être défini en budget quotidien ou budget total selon vos préférences.

Toutes les campagnes de boost sont créées avec le statut "PAUSED" par défaut, vous permettant de réviser et d'ajuster les paramètres avant de lancer effectivement la promotion. Cette approche de sécurité évite les dépenses publicitaires non intentionnelles et vous donne un contrôle total sur vos campagnes.

### Création de Campagnes Publicitaires Complètes

L'onglet "Publicités" de Facebook Publisher Bois Malin offre des outils complets pour créer des campagnes publicitaires professionnelles depuis zéro. Cette fonctionnalité s'adresse aux utilisateurs qui souhaitent aller au-delà du simple boost de publications et créer des campagnes marketing sophistiquées.

Le processus de création commence par la sélection du compte publicitaire à utiliser. L'application récupère automatiquement tous les comptes publicitaires auxquels vous avez accès et affiche leurs informations principales (nom, ID, devise, statut). Cette étape est cruciale car elle détermine les options de facturation et les limites de dépenses applicables à votre campagne.

La définition de l'objectif de campagne constitue l'étape suivante et influence tous les paramètres subséquents. Facebook propose de nombreux objectifs selon vos buts marketing : TRAFFIC pour diriger du trafic vers votre site web, CONVERSIONS pour optimiser les actions sur votre site, REACH pour maximiser la portée, ou BRAND_AWARENESS pour augmenter la notoriété de votre marque.

La création du créatif publicitaire offre une flexibilité maximale pour concevoir des publicités attrayantes. Vous pouvez télécharger vos propres images ou vidéos, rédiger des textes personnalisés, définir des appels à l'action spécifiques, et prévisualiser le rendu final sur différents placements (fil d'actualité, stories, audience network).

Le système de ciblage intégré permet de définir précisément votre audience cible. Vous pouvez spécifier des critères démographiques (âge, sexe, localisation), des centres d'intérêt, des comportements, et même créer des audiences personnalisées basées sur vos données clients. L'application affiche en temps réel la taille estimée de votre audience pour vous aider à ajuster vos critères.

La gestion du budget et de la programmation offre des options flexibles pour contrôler vos dépenses publicitaires. Vous pouvez définir un budget quotidien ou un budget total, choisir une stratégie d'enchères automatique ou manuelle, et programmer la diffusion de votre campagne sur des créneaux horaires spécifiques.

### Analyse des Performances et Statistiques

L'onglet "Statistiques" de Facebook Publisher Bois Malin transforme les données brutes de l'API Facebook Insights en informations exploitables pour optimiser votre stratégie de contenu. Cette fonctionnalité offre une vue d'ensemble complète des performances de vos pages et publications avec des visualisations claires et des métriques pertinentes.

L'analyse des performances de page fournit des métriques globales sur l'évolution de votre audience et de votre engagement. Vous pouvez consulter l'évolution du nombre de fans, les impressions totales, la portée organique et payante, et les interactions (likes, commentaires, partages) sur des périodes personnalisables. Ces données sont essentielles pour comprendre les tendances générales de votre présence Facebook.

L'analyse des publications individuelles permet d'identifier vos contenus les plus performants et de comprendre les facteurs de succès. Chaque publication est analysée selon plusieurs dimensions : portée organique et payante, engagement rate, types de réactions, et démographie de l'audience touchée. Cette granularité d'analyse vous aide à reproduire les éléments qui fonctionnent bien.

Les graphiques de performance évolutive montrent les tendances sur des périodes étendues, permettant d'identifier les patterns saisonniers, l'impact des campagnes publicitaires, et l'efficacité des différents types de contenu. L'application génère automatiquement des graphiques en courbes, en barres, et en secteurs selon le type de données visualisées.

La fonctionnalité de comparaison permet d'analyser les performances relatives de différentes pages ou périodes. Cette analyse comparative est particulièrement utile pour identifier les pages les plus performantes de votre réseau et comprendre les facteurs qui expliquent ces différences de performance.

L'export des données en format CSV ou Excel permet d'effectuer des analyses plus poussées avec des outils externes ou de créer des rapports personnalisés pour vos équipes ou clients. Toutes les métriques disponibles dans l'interface peuvent être exportées avec leurs métadonnées temporelles.

### Automatisation et Workflows

Facebook Publisher Bois Malin inclut des fonctionnalités d'automatisation avancées pour optimiser votre productivité et maintenir une présence constante sur vos pages Facebook. Ces outils permettent de créer des workflows personnalisés qui s'adaptent à vos habitudes de travail et à vos objectifs marketing.

Le système de templates de publication permet de créer des modèles réutilisables pour vos types de contenu récurrents. Vous pouvez définir des structures de message avec des variables personnalisables, des sélections de pages prédéfinies, et des paramètres de programmation par défaut. Cette fonctionnalité est particulièrement utile pour les contenus sériels ou les communications régulières.

L'automatisation de la programmation offre des options sophistiquées pour planifier vos publications selon des patterns complexes. Vous pouvez définir des créneaux de publication optimaux basés sur l'activité de votre audience, créer des séquences de publications espacées dans le temps, et configurer des rappels pour la création de nouveau contenu.

Le système de monitoring automatique surveille en permanence les performances de vos publications et peut déclencher des actions automatiques selon des critères prédéfinis. Par exemple, l'application peut automatiquement booster les publications qui atteignent un certain niveau d'engagement ou envoyer des alertes lorsque les performances chutent en dessous d'un seuil défini.

L'intégration avec des services externes permet d'étendre les capacités d'automatisation. L'application peut être configurée pour récupérer du contenu depuis des flux RSS, synchroniser avec des calendriers éditoriaux, ou s'intégrer avec des outils de gestion de projet pour automatiser la création de publications basées sur des événements externes.

### Sécurité et Conformité

La sécurité et la conformité constituent des aspects fondamentaux de Facebook Publisher Bois Malin, particulièrement important dans le contexte de la gestion de multiples pages Facebook et de données marketing sensibles. L'application implémente des mesures de sécurité multicouches pour protéger vos informations et respecter les réglementations en vigueur.

La protection des données personnelles suit les principes du RGPD et des réglementations locales applicables. Toutes les données utilisateur sont stockées localement sur votre machine, évitant les risques liés au stockage cloud. L'application ne collecte aucune donnée analytique ou télémétrique sans votre consentement explicite.

Le chiffrement des données sensibles s'applique à tous les tokens d'accès et informations d'authentification stockés par l'application. Ces données sont chiffrées avec des algorithmes standards de l'industrie et les clés de chiffrement sont dérivées de votre configuration système unique.

L'audit trail complet enregistre toutes les actions effectuées par l'application avec des horodatages précis et des identifiants de session. Ces logs sont essentiels pour le débogage mais aussi pour la conformité réglementaire dans les environnements professionnels qui exigent une traçabilité complète des actions marketing.

La gestion des permissions suit le principe du moindre privilège, demandant uniquement les permissions Facebook strictement nécessaires aux fonctionnalités utilisées. L'application vérifie régulièrement que les permissions accordées correspondent aux besoins réels et alerte l'utilisateur en cas de permissions excessives ou manquantes.


## Dépannage

### Problèmes d'Installation et de Configuration

Les problèmes d'installation représentent les difficultés les plus courantes rencontrées lors de la première utilisation de Facebook Publisher Bois Malin. Cette section détaille les solutions aux problèmes les plus fréquents et fournit des méthodes de diagnostic pour identifier rapidement la source des dysfonctionnements.

L'erreur "ModuleNotFoundError" lors de l'importation des dépendances indique généralement que l'installation des packages Python n'a pas été effectuée correctement. Vérifiez d'abord que vous utilisez la bonne version de Python (3.11+) en exécutant `python --version`. Si la version est correcte, réinstallez les dépendances avec la commande `pip install -r requirements.txt --force-reinstall` pour forcer la réinstallation de tous les packages.

Les problèmes de permissions sur les fichiers de configuration surviennent fréquemment sur les systèmes Unix/Linux. Si l'application ne peut pas créer ou modifier les fichiers JSON de configuration, vérifiez les permissions du répertoire de l'application avec `ls -la`. Assurez-vous que votre utilisateur a les droits de lecture et d'écriture sur le répertoire et tous ses sous-dossiers.

L'erreur "tkinter module not found" sur les systèmes Linux indique que l'interface graphique Python n'est pas installée. Installez le package approprié avec `sudo apt-get install python3-tk` sur Ubuntu/Debian ou `sudo yum install tkinter` sur CentOS/RHEL. Redémarrez l'application après l'installation.

Les problèmes de variables d'environnement se manifestent par des erreurs d'authentification au démarrage. Vérifiez que le fichier `.env` existe dans le répertoire de l'application et contient toutes les variables requises. Utilisez la commande `cat .env` pour afficher le contenu du fichier et vérifier que les valeurs sont correctement définies sans espaces supplémentaires.

### Erreurs d'Authentification Facebook

Les erreurs d'authentification avec l'API Facebook constituent la catégorie de problèmes la plus complexe à résoudre car elles impliquent l'interaction entre votre application locale et les serveurs Facebook. Une approche méthodique est nécessaire pour identifier et corriger ces problèmes.

L'erreur "Invalid App ID" indique que l'identifiant d'application configuré dans votre fichier `.env` ne correspond pas à une application Facebook valide. Vérifiez l'App ID dans votre tableau de bord développeur Facebook et assurez-vous qu'il est correctement copié dans le fichier de configuration. L'App ID doit être un nombre entier sans guillemets ni espaces.

L'erreur "Invalid App Secret" suggère que le secret d'application est incorrect ou a été régénéré depuis votre dernière configuration. Accédez aux paramètres de votre application Facebook, générez un nouveau secret si nécessaire, et mettez à jour votre fichier `.env`. Attention : la régénération du secret invalide immédiatement l'ancien secret.

Les erreurs de token d'accès expiré sont signalées par des messages comme "Token has expired" ou "Invalid OAuth access token". Utilisez l'outil de débogage intégré dans l'onglet "Paramètres" pour vérifier le statut de votre token. Si le token est expiré, générez un nouveau token depuis l'Explorateur d'API Facebook ou utilisez la fonction d'échange de token de l'application.

Les erreurs de permissions insuffisantes se manifestent par des messages "Insufficient permissions for this action". Vérifiez que votre token d'accès inclut toutes les permissions nécessaires : `pages_manage_posts`, `pages_read_engagement`, `ads_management`, et `business_management`. Régénérez le token en sélectionnant explicitement ces permissions si nécessaire.

### Problèmes de Publication et de Programmation

Les dysfonctionnements liés à la publication de contenu peuvent avoir diverses origines, depuis des problèmes de connectivité réseau jusqu'aux violations des politiques de contenu Facebook. Un diagnostic systématique permet d'identifier rapidement la cause du problème.

L'échec de publication avec l'erreur "Network error" indique généralement un problème de connectivité Internet ou une indisponibilité temporaire des serveurs Facebook. Vérifiez votre connexion Internet et tentez de publier à nouveau après quelques minutes. Si le problème persiste, consultez la page de statut des développeurs Facebook pour vérifier s'il y a des incidents en cours.

Les erreurs de validation de contenu se produisent lorsque votre publication ne respecte pas les standards de Facebook. L'erreur "Invalid URL" indique que le lien inclus dans votre publication n'est pas accessible ou ne respecte pas les critères de Facebook. Vérifiez que l'URL est complète (avec http:// ou https://) et accessible depuis un navigateur web.

Les problèmes de téléchargement de médias peuvent être causés par des formats de fichier non supportés ou des tailles de fichier excessives. Facebook accepte les images JPEG, PNG, et GIF jusqu'à 4 MB, et les vidéos MP4 jusqu'à 1 GB. Vérifiez le format et la taille de vos fichiers médias avant de tenter la publication.

Les dysfonctionnements du scheduler de publications programmées sont souvent liés à des problèmes de fuseau horaire ou à l'arrêt de l'application. Vérifiez que l'heure système de votre ordinateur est correcte et que l'application reste ouverte pour traiter les publications programmées. Le scheduler vérifie les publications en attente toutes les minutes.

### Problèmes de Performance et d'Optimisation

Les problèmes de performance de Facebook Publisher Bois Malin peuvent affecter l'expérience utilisateur, particulièrement lors de la gestion d'un grand nombre de pages ou de publications. Cette section présente les techniques d'optimisation et de résolution des problèmes de performance.

La lenteur de l'interface utilisateur lors du chargement des pages peut être causée par un grand nombre de pages Facebook associées à votre compte. L'application charge toutes les pages au démarrage, ce qui peut prendre du temps si vous gérez des centaines de pages. Considérez l'utilisation de filtres pour afficher uniquement les pages actives ou les plus importantes.

Les timeouts lors des appels API Facebook surviennent généralement lors de pics de charge sur les serveurs Facebook ou de limitations de taux. L'application implémente des mécanismes de retry automatique, mais vous pouvez ajuster les paramètres de timeout dans le fichier de configuration si nécessaire. Augmentez progressivement les valeurs de timeout si vous rencontrez des timeouts fréquents.

La consommation excessive de mémoire peut se produire lors du traitement de nombreuses images ou vidéos. L'application optimise automatiquement les médias avant l'upload, mais les fichiers très volumineux peuvent temporairement consommer beaucoup de mémoire. Fermez les autres applications gourmandes en mémoire ou redimensionnez vos médias avant de les utiliser dans l'application.

Les problèmes de synchronisation des données entre l'interface et les fichiers de configuration peuvent causer des incohérences dans l'affichage. Utilisez la fonction "Actualiser" dans chaque onglet pour forcer la synchronisation, ou redémarrez l'application si les problèmes persistent.

### Diagnostic Avancé et Logging

Facebook Publisher Bois Malin inclut des outils de diagnostic avancés pour identifier et résoudre les problèmes complexes. Ces outils génèrent des informations détaillées sur le fonctionnement interne de l'application et facilitent le support technique.

Le système de logging enregistre automatiquement toutes les opérations importantes dans le fichier `facebook_api.log`. Ce fichier contient les détails des requêtes API, les réponses reçues, et les erreurs rencontrées. Consultez ce fichier pour obtenir des informations précises sur les échecs d'opération. Les logs sont organisés chronologiquement avec des niveaux de sévérité (INFO, WARNING, ERROR).

L'outil de débogage de token intégré dans l'onglet "Paramètres" fournit des informations détaillées sur vos tokens d'accès. Utilisez cet outil pour vérifier la validité, les permissions, et la date d'expiration de vos tokens. Les informations affichées incluent l'ID de l'application qui a généré le token, l'utilisateur associé, et la liste complète des permissions accordées.

Le mode de débogage avancé peut être activé en modifiant le niveau de logging dans le fichier de configuration. Changez `LOG_LEVEL=INFO` en `LOG_LEVEL=DEBUG` pour obtenir des informations très détaillées sur toutes les opérations. Attention : ce mode génère beaucoup de données de log et peut affecter les performances.

La fonction de test de connectivité vérifie la capacité de l'application à communiquer avec les serveurs Facebook. Cette fonction teste successivement la résolution DNS, la connectivité HTTPS, et l'authentification API. Utilisez cette fonction si vous suspectez des problèmes de réseau ou de firewall.

### Support et Ressources Complémentaires

En cas de problème persistant non résolu par les solutions de dépannage standard, plusieurs ressources sont disponibles pour obtenir de l'aide supplémentaire. Cette section détaille les canaux de support et les ressources externes utiles.

La documentation officielle de l'API Facebook (https://developers.facebook.com/docs/) constitue la référence ultime pour comprendre le comportement attendu des fonctionnalités Facebook. Consultez cette documentation si vous rencontrez des erreurs spécifiques à l'API ou si vous souhaitez comprendre les limitations et contraintes imposées par Facebook.

Le changelog de l'API Facebook (https://developers.facebook.com/docs/graph-api/changelog/) documente tous les changements apportés aux différentes versions de l'API. Si l'application cesse soudainement de fonctionner, vérifiez si des changements récents dans l'API Facebook peuvent expliquer le problème.

La communauté des développeurs Facebook sur Stack Overflow et les forums officiels Facebook for Developers constituent d'excellentes ressources pour obtenir de l'aide sur des problèmes spécifiques. Recherchez des problèmes similaires avant de poser une nouvelle question, et incluez toujours les messages d'erreur exacts et les étapes de reproduction.

Le script de test intégré (`test_app.py`) peut être utilisé pour valider rapidement l'état de votre installation. Exécutez ce script après toute modification de configuration ou mise à jour de l'application pour vérifier que tous les composants fonctionnent correctement.


## Développement et Contribution

### Architecture du Code

Facebook Publisher Bois Malin est conçu selon une architecture modulaire qui facilite la maintenance, l'extension, et la contribution au projet. Cette section détaille l'organisation du code source et les principes architecturaux qui guident le développement de l'application.

L'architecture suit le pattern Model-View-Controller (MVC) adapté aux spécificités d'une application desktop. Les modèles (dans le répertoire `models/`) définissent les structures de données pour les pages, publications, et campagnes publicitaires. Ces classes encapsulent la logique métier et fournissent des méthodes pour la sérialisation et la désérialisation des données.

La vue est implémentée par la classe `FacebookPublisherApp` qui gère l'interface utilisateur Tkinter. Cette classe est organisée en méthodes spécialisées pour chaque onglet de l'interface, facilitant la maintenance et l'ajout de nouvelles fonctionnalités. L'interface suit les principes de design responsive pour s'adapter aux différentes tailles d'écran.

Le contrôleur est représenté par le wrapper API (`facebook_api.py`) qui centralise toutes les interactions avec les services Facebook. Cette approche garantit la cohérence des appels API, la gestion uniforme des erreurs, et facilite les tests unitaires. Le wrapper implémente des patterns comme le retry avec backoff exponentiel et le circuit breaker pour la robustesse.

Les utilitaires (répertoire `utils/`) fournissent des services transversaux comme la configuration, le logging, et la planification. Ces modules sont conçus pour être réutilisables et testables indépendamment du reste de l'application. La séparation claire des responsabilités facilite l'évolution et la maintenance du code.

### Standards de Codage et Bonnes Pratiques

Le développement de Facebook Publisher Bois Malin suit rigoureusement les standards PEP 8 pour garantir la lisibilité et la maintenabilité du code Python. Cette section détaille les conventions adoptées et les outils utilisés pour maintenir la qualité du code.

Le formatage du code utilise une largeur maximale de 88 caractères par ligne, conformément aux recommandations modernes de la communauté Python. Les noms de variables et fonctions utilisent la convention snake_case, tandis que les noms de classes suivent la convention PascalCase. Les constantes sont définies en UPPER_CASE avec des underscores.

La documentation du code suit le format Google docstring pour toutes les fonctions et classes publiques. Chaque fonction inclut une description claire de son objectif, la liste des paramètres avec leurs types, et la description de la valeur de retour. Les exemples d'utilisation sont inclus pour les fonctions complexes.

La gestion des erreurs suit une approche défensive avec des exceptions spécifiques pour chaque type d'erreur. Les exceptions personnalisées (`FacebookAPIError`) fournissent des informations contextuelles détaillées pour faciliter le débogage. Toutes les erreurs sont loggées avec le niveau approprié et des messages explicites.

Le typage statique est utilisé systématiquement avec les annotations de type Python 3.11+. Cette approche améliore la lisibilité du code, facilite la détection d'erreurs, et améliore l'expérience de développement avec les IDEs modernes. Les types complexes utilisent les génériques de la bibliothèque `typing`.

### Tests et Assurance Qualité

La stratégie de test de Facebook Publisher Bois Malin combine tests unitaires, tests d'intégration, et tests de bout en bout pour garantir la fiabilité de l'application. Cette approche multicouche permet de détecter les régressions rapidement et de maintenir un niveau de qualité élevé.

Les tests unitaires (répertoire `tests/`) couvrent toutes les fonctions critiques du wrapper API et des modèles de données. Ces tests utilisent le framework pytest et la bibliothèque responses pour mocker les appels HTTP vers l'API Facebook. Chaque test est isolé et peut être exécuté indépendamment des autres.

Les tests d'intégration vérifient l'interaction entre les différents composants de l'application sans faire appel aux services Facebook réels. Ces tests utilisent des données de test prédéfinies et des mocks sophistiqués pour simuler les réponses de l'API Facebook dans différents scénarios (succès, erreurs, limitations de taux).

Le script de test global (`test_app.py`) effectue des vérifications de bout en bout sur l'ensemble de l'application. Ce script peut être exécuté en mode "dry run" pour valider la configuration sans effectuer d'opérations réelles sur Facebook, ou en mode complet pour tester l'intégration avec l'API Facebook.

La couverture de code est mesurée avec l'outil coverage.py et maintenue au-dessus de 80% pour les modules critiques. Les rapports de couverture sont générés automatiquement lors de l'exécution des tests et identifient les parties du code qui nécessitent des tests supplémentaires.

### Contribution au Projet

Facebook Publisher Bois Malin est conçu pour faciliter les contributions externes et l'extension des fonctionnalités. Cette section guide les développeurs souhaitant contribuer au projet ou adapter l'application à leurs besoins spécifiques.

L'ajout de nouvelles fonctionnalités suit un processus structuré commençant par la création d'une issue décrivant la fonctionnalité proposée. Cette issue doit inclure une description détaillée du besoin, les spécifications techniques envisagées, et l'impact sur l'architecture existante. Les fonctionnalités majeures nécessitent une discussion préalable pour valider l'approche.

Le développement de nouvelles fonctionnalités commence par la création d'une branche dédiée depuis la branche principale. Les commits doivent être atomiques et inclure des messages descriptifs suivant la convention Conventional Commits. Chaque commit doit passer tous les tests existants et inclure les tests appropriés pour les nouvelles fonctionnalités.

L'extension du wrapper API pour supporter de nouvelles endpoints Facebook suit un pattern établi. Chaque nouvelle méthode doit inclure la gestion d'erreurs appropriée, le logging des requêtes et réponses, et la documentation complète. Les paramètres optionnels doivent avoir des valeurs par défaut sensées et être documentés.

L'ajout de nouveaux onglets à l'interface utilisateur nécessite la création de méthodes dédiées dans la classe principale et la mise à jour de la méthode d'initialisation. Les nouveaux onglets doivent suivre les conventions de nommage existantes et implémenter la gestion des erreurs avec des messages utilisateur appropriés.

### Déploiement et Distribution

La distribution de Facebook Publisher Bois Malin suit une approche multi-plateforme pour maximiser l'accessibilité de l'application. Cette section détaille les processus de packaging et de distribution pour les différents environnements cibles.

Le packaging pour Windows utilise PyInstaller pour créer un exécutable autonome incluant toutes les dépendances Python. Le processus de build génère un fichier .exe qui peut être distribué sans nécessiter d'installation Python préalable. La configuration PyInstaller inclut les ressources nécessaires et optimise la taille du package final.

La distribution pour macOS suit un processus similaire avec la création d'un bundle .app compatible avec les dernières versions de macOS. Le processus inclut la signature du code et la notarisation Apple pour garantir la compatibilité avec les paramètres de sécurité par défaut de macOS.

Pour les systèmes Linux, l'application est distribuée sous forme de package Python standard avec un script d'installation automatisé. Ce script vérifie les dépendances système, installe les packages Python nécessaires, et configure l'environnement d'exécution approprié.

La documentation de déploiement inclut des instructions détaillées pour chaque plateforme, les prérequis système, et les procédures de mise à jour. Les notes de version documentent tous les changements, corrections de bugs, et nouvelles fonctionnalités pour chaque release.

### Roadmap et Évolutions Futures

Le développement futur de Facebook Publisher Bois Malin suit une roadmap structurée basée sur les retours utilisateurs et l'évolution de l'écosystème Facebook. Cette section présente les directions d'évolution envisagées et les priorités de développement.

L'intégration avec Instagram Business constitue une priorité majeure pour étendre les capacités de l'application aux plateformes Meta. Cette intégration permettra de publier simultanément sur Facebook et Instagram, de gérer les stories, et d'accéder aux statistiques Instagram via l'API Graph.

L'amélioration de l'interface utilisateur inclut la migration vers un framework moderne comme PyQt ou l'adoption d'une architecture web avec Electron. Cette évolution permettra d'offrir une expérience utilisateur plus moderne et de faciliter l'ajout de fonctionnalités interactives avancées.

L'extension des capacités d'analyse inclut l'ajout de tableaux de bord personnalisables, l'export de rapports automatisés, et l'intégration avec des outils d'analyse externes. Ces fonctionnalités répondront aux besoins des utilisateurs professionnels qui gèrent de nombreuses pages.

L'automatisation avancée comprend l'ajout de workflows conditionnels, l'intégration avec des services de contenu externes, et la création d'un système de templates sophistiqué. Ces fonctionnalités permettront de créer des stratégies de contenu entièrement automatisées.

La collaboration multi-utilisateurs représente une évolution majeure vers une architecture client-serveur permettant à plusieurs utilisateurs de collaborer sur la gestion des pages Facebook. Cette fonctionnalité nécessitera une refonte architecturale significative mais ouvrira de nouvelles possibilités d'utilisation professionnelle.


## Annexes

### Annexe A : Référence des Variables d'Environnement

Cette annexe fournit une référence complète de toutes les variables d'environnement utilisées par Facebook Publisher Bois Malin. Ces variables doivent être définies dans le fichier `.env` pour assurer le bon fonctionnement de l'application.

| Variable | Type | Obligatoire | Description | Exemple |
|----------|------|-------------|-------------|---------|
| `APP_ID` | String | Oui | Identifiant de votre application Facebook | `123456789012345` |
| `APP_SECRET` | String | Oui | Secret de votre application Facebook | `abcdef1234567890abcdef1234567890` |
| `USER_ACCESS_TOKEN` | String | Optionnel | Token d'accès utilisateur pour les opérations de base | `EAABwzLixnjYBO...` |
| `SYSTEM_USER_TOKEN` | String | Optionnel | Token système pour les fonctionnalités avancées | `EAABwzLixnjYBO...` |
| `FACEBOOK_API_VERSION` | String | Optionnel | Version de l'API Facebook à utiliser | `v18.0` |
| `FACEBOOK_BASE_URL` | String | Optionnel | URL de base de l'API Facebook | `https://graph.facebook.com` |
| `LOG_LEVEL` | String | Optionnel | Niveau de logging (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `LOG_FILE` | String | Optionnel | Chemin du fichier de log | `facebook_api.log` |
| `DATA_DIR` | String | Optionnel | Répertoire de stockage des données | `./data` |
| `SCHEDULER_INTERVAL` | Integer | Optionnel | Intervalle du scheduler en secondes | `60` |

### Annexe B : Codes d'Erreur Facebook API

Cette annexe liste les codes d'erreur les plus courants retournés par l'API Facebook et leurs significations. Ces informations sont utiles pour diagnostiquer les problèmes d'intégration API.

| Code | Type | Description | Solution |
|------|------|-------------|----------|
| 1 | API_UNKNOWN | Erreur inconnue de l'API | Réessayer la requête, vérifier les logs |
| 2 | API_SERVICE | Service temporairement indisponible | Attendre et réessayer avec backoff |
| 4 | API_TOO_MANY_CALLS | Limite de taux dépassée | Attendre la réinitialisation de la limite |
| 10 | API_PERMISSION_DENIED | Permissions insuffisantes | Vérifier les permissions du token |
| 17 | API_USER_TOO_MANY_CALLS | Limite utilisateur dépassée | Réduire la fréquence des requêtes |
| 100 | INVALID_PARAMETER | Paramètre invalide | Vérifier les paramètres de la requête |
| 190 | ACCESS_TOKEN_ERROR | Token d'accès invalide ou expiré | Renouveler le token d'accès |
| 200 | PERMISSION_ERROR | Permissions insuffisantes pour cette action | Demander les permissions appropriées |
| 368 | TEMPORARILY_BLOCKED | Action temporairement bloquée | Attendre avant de réessayer |
| 613 | RATE_LIMIT_EXCEEDED | Limite de taux spécifique dépassée | Implémenter un délai approprié |

### Annexe C : Permissions Facebook Requises

Cette annexe détaille toutes les permissions Facebook nécessaires pour utiliser les différentes fonctionnalités de Facebook Publisher Bois Malin.

#### Permissions de Base

- **`pages_manage_posts`** : Permet de publier, modifier et supprimer des posts sur les pages gérées
- **`pages_read_engagement`** : Permet de lire les métriques d'engagement des pages
- **`pages_show_list`** : Permet de lister les pages gérées par l'utilisateur

#### Permissions pour les Statistiques

- **`read_insights`** : Permet d'accéder aux statistiques détaillées des pages et posts
- **`pages_read_user_content`** : Permet de lire le contenu généré par les utilisateurs sur les pages

#### Permissions pour les Publicités

- **`ads_management`** : Permet de créer et gérer des campagnes publicitaires
- **`ads_read`** : Permet de lire les données des campagnes publicitaires existantes
- **`business_management`** : Permet d'accéder aux comptes publicitaires Business Manager

#### Permissions Avancées

- **`pages_messaging`** : Permet de gérer les messages privés des pages (fonctionnalité future)
- **`instagram_basic`** : Permet l'intégration avec Instagram Business (fonctionnalité future)
- **`instagram_content_publish`** : Permet de publier sur Instagram (fonctionnalité future)

### Annexe D : Structure des Fichiers de Données

Cette annexe décrit la structure des fichiers JSON utilisés par l'application pour stocker les données localement.

#### facebook_pages.json

```json
{
  "pages": [
    {
      "id": "123456789012345",
      "name": "Bois Malin - Page Principale",
      "access_token": "EAABwzLixnjYBO...",
      "last_updated": "2025-06-19T15:30:00Z"
    }
  ],
  "last_sync": "2025-06-19T15:30:00Z"
}
```

#### scheduled_posts.json

```json
{
  "posts": [
    {
      "id": "post_001",
      "message": "Nouveau produit disponible !",
      "page_ids": ["123456789012345", "987654321098765"],
      "link": "https://example.com/produit",
      "image_paths": ["/path/to/image.jpg"],
      "scheduled_time": "2025-06-20T14:00:00Z",
      "status": "scheduled",
      "created_at": "2025-06-19T15:30:00Z"
    }
  ]
}
```

#### boosted_ads.json

```json
{
  "boosted_posts": [
    {
      "id": "boost_001",
      "post_id": "123456789012345_987654321",
      "campaign_id": "23847xxxxx",
      "adset_id": "23847xxxxx",
      "ad_id": "23847xxxxx",
      "creative_id": "23847xxxxx",
      "budget": 50.00,
      "currency": "EUR",
      "status": "PAUSED",
      "created_at": "2025-06-19T15:30:00Z"
    }
  ]
}
```

### Annexe E : Commandes Utiles

Cette annexe rassemble les commandes les plus utiles pour l'administration et le dépannage de Facebook Publisher Bois Malin.

#### Installation et Configuration

```bash
# Installation des dépendances
pip install -r requirements.txt

# Vérification de l'installation
python test_app.py

# Lancement de l'application
python main.py

# Exécution des tests unitaires
python -m pytest tests/ -v

# Génération du rapport de couverture
python -m pytest tests/ --cov=. --cov-report=html
```

#### Diagnostic et Dépannage

```bash
# Vérification de la version Python
python --version

# Vérification des packages installés
pip list

# Nettoyage du cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +

# Vérification des permissions de fichiers
ls -la data/

# Affichage des logs en temps réel
tail -f facebook_api.log

# Test de connectivité API
curl -I https://graph.facebook.com/v18.0/me
```

#### Maintenance

```bash
# Sauvegarde des données
cp -r data/ backup_$(date +%Y%m%d)/

# Nettoyage des logs anciens
find . -name "*.log" -mtime +30 -delete

# Mise à jour des dépendances
pip install -r requirements.txt --upgrade

# Vérification de la sécurité des dépendances
pip audit

# Formatage du code
black *.py

# Vérification du style de code
flake8 *.py
```

### Annexe F : Ressources et Références

Cette annexe fournit une liste complète des ressources externes utiles pour l'utilisation et le développement de Facebook Publisher Bois Malin.

#### Documentation Officielle Facebook

- [Facebook for Developers](https://developers.facebook.com/) - Portail principal des développeurs Facebook
- [Graph API Documentation](https://developers.facebook.com/docs/graph-api/) - Documentation complète de l'API Graph
- [Marketing API Documentation](https://developers.facebook.com/docs/marketing-api/) - Documentation de l'API Marketing
- [Facebook App Development](https://developers.facebook.com/docs/development/) - Guide de développement d'applications Facebook

#### Outils et Utilitaires

- [Graph API Explorer](https://developers.facebook.com/tools/explorer/) - Outil de test interactif pour l'API Graph
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/) - Outil de débogage des tokens d'accès
- [Facebook Business Manager](https://business.facebook.com/) - Interface de gestion des comptes publicitaires
- [Facebook Page Insights](https://www.facebook.com/insights/) - Statistiques natives des pages Facebook

#### Communauté et Support

- [Facebook for Developers Community](https://developers.facebook.com/community/) - Communauté officielle des développeurs
- [Stack Overflow - Facebook API](https://stackoverflow.com/questions/tagged/facebook-graph-api) - Questions et réponses sur l'API Facebook
- [Facebook Developer Blog](https://developers.facebook.com/blog/) - Actualités et annonces pour les développeurs
- [Facebook Platform Status](https://developers.facebook.com/status/) - Statut en temps réel des services Facebook

#### Bibliothèques et Frameworks Python

- [Requests Documentation](https://docs.python-requests.org/) - Documentation de la bibliothèque HTTP Python
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html) - Documentation de l'interface graphique Tkinter
- [Python Dotenv](https://pypi.org/project/python-dotenv/) - Gestion des variables d'environnement
- [Pytest Documentation](https://docs.pytest.org/) - Framework de test Python

---

**Note de fin :** Cette documentation constitue un guide complet pour l'utilisation et le développement de Facebook Publisher Bois Malin. Elle sera mise à jour régulièrement pour refléter les évolutions de l'application et de l'écosystème Facebook. Pour toute question ou suggestion d'amélioration, n'hésitez pas à consulter les ressources mentionnées ou à contribuer au projet.

**Version du document :** 2.0  
**Dernière mise à jour :** 19 juin 2025  
**Auteur :** Manus AI  
**Client :** Nicolas Pycik


## Onglet Publicités

L'onglet Publicités constitue l'une des fonctionnalités les plus avancées de Facebook Publisher Bois Malin v2.1. Il offre une interface complète pour créer et gérer des campagnes publicitaires Facebook directement depuis l'application, sans avoir besoin d'accéder au gestionnaire de publicités Facebook.

### Interface de Création de Campagnes

L'interface de l'onglet Publicités est organisée en plusieurs sections logiques pour faciliter la création de campagnes publicitaires. La première section permet la sélection du compte publicitaire et de la page Facebook. Le menu déroulant des comptes publicitaires se remplit automatiquement avec tous les comptes accessibles via votre token d'accès, et un bouton "Actualiser" permet de recharger la liste si de nouveaux comptes ont été ajoutés.

La sélection de la page Facebook utilise la même liste que celle configurée dans l'onglet Paramètres, garantissant la cohérence entre les différentes fonctionnalités de l'application. Cette page sera utilisée comme source pour les créatifs publicitaires et comme propriétaire des publications promues.

### Configuration de Campagne

La section de configuration de campagne permet de définir les paramètres essentiels de votre campagne publicitaire. Le nom de campagne doit être unique et descriptif pour faciliter l'identification dans le gestionnaire de publicités Facebook. L'objectif de campagne peut être sélectionné parmi les options les plus courantes : TRAFFIC pour diriger du trafic vers un site web, CONVERSIONS pour optimiser les conversions, REACH pour maximiser la portée, BRAND_AWARENESS pour augmenter la notoriété de la marque, et POST_ENGAGEMENT pour favoriser l'engagement sur les publications.

Le budget quotidien est spécifié en euros et sera automatiquement converti en centimes pour l'API Facebook. La date de début peut être définie pour programmer le lancement de la campagne, et par défaut, elle est fixée à la date actuelle.

### Paramètres de Ciblage

La section de ciblage permet de définir précisément l'audience de votre campagne publicitaire. Le ciblage géographique commence par la sélection du pays, avec "FR" (France) comme valeur par défaut. Les paramètres démographiques incluent l'âge minimum et maximum, avec des valeurs par défaut de 18 à 65 ans qui couvrent la majorité de l'audience Facebook active.

Ces paramètres de base peuvent être étendus selon les besoins spécifiques de chaque campagne. L'API Facebook Marketing offre de nombreuses options de ciblage avancées qui peuvent être intégrées dans les versions futures de l'application.

### Création de Créatifs Publicitaires

La section créatif publicitaire permet de définir le contenu visuel et textuel de vos publicités. Le message publicitaire constitue le texte principal qui accompagnera votre publicité et doit être engageant et pertinent pour votre audience cible. Ce champ supporte les textes longs et permet d'inclure des émojis et des caractères spéciaux.

Le lien de destination spécifie l'URL vers laquelle les utilisateurs seront dirigés lorsqu'ils cliqueront sur votre publicité. Cette URL doit être valide et pointer vers une page en rapport avec le contenu de votre publicité.

L'upload d'image permet de sélectionner un fichier image local qui sera utilisé comme visuel principal de votre publicité. L'application supporte les formats JPG, JPEG, PNG et GIF, et l'image sera automatiquement uploadée vers Facebook lors de la création de la publicité.

L'appel à l'action (CTA) peut être sélectionné parmi les options les plus efficaces : LEARN_MORE pour encourager l'apprentissage, SHOP_NOW pour les achats immédiats, SIGN_UP pour les inscriptions, DOWNLOAD pour les téléchargements, CONTACT_US pour les prises de contact, et CALL_NOW pour les appels téléphoniques.

### Processus de Création

L'application offre deux options principales pour la création de publicités. Le bouton "Créer Campagne" permet de créer uniquement une campagne vide, qui pourra ensuite être complétée manuellement dans le gestionnaire de publicités Facebook. Cette option est utile pour les utilisateurs qui préfèrent finaliser leurs publicités directement sur Facebook.

Le bouton "Créer Publicité Complète" lance un processus automatisé qui crée successivement une campagne, un ensemble de publicités (adset), un créatif publicitaire, et une publicité finale. Ce processus complet permet d'avoir une publicité entièrement fonctionnelle en quelques clics, prête à être activée depuis le gestionnaire de publicités Facebook.

### Gestion des Publicités Existantes

La liste des publicités et campagnes affiche toutes les campagnes créées via l'application dans un tableau organisé avec les colonnes ID, Nom, Statut, Objectif, et Budget. Cette vue d'ensemble permet de suivre facilement l'état de toutes vos campagnes et d'identifier rapidement celles qui nécessitent une attention particulière.

Le bouton "Actualiser Liste" permet de recharger les informations depuis Facebook pour s'assurer que les données affichées sont à jour. Cette fonctionnalité est particulièrement utile si vous gérez vos campagnes depuis plusieurs interfaces simultanément.

## Fonctionnalité Boost Post

La fonctionnalité Boost Post représente l'une des innovations les plus pratiques de Facebook Publisher Bois Malin v2.1. Intégrée directement dans l'onglet Statistiques, elle permet de promouvoir rapidement et efficacement les publications les plus performantes sans quitter l'application.

### Accès et Utilisation

Pour utiliser la fonctionnalité Boost Post, naviguez vers l'onglet Statistiques et sélectionnez la page dont vous souhaitez analyser les publications. Après avoir cliqué sur "Actualiser" pour charger les publications récentes, vous verrez apparaître la liste des 10 dernières publications avec leurs métriques de performance.

Sélectionnez la publication que vous souhaitez booster en cliquant dessus dans la liste, puis cliquez sur le bouton "Booster ce post" situé sous le tableau. Cette action lance immédiatement le processus de création d'une campagne de boost complète.

### Processus Automatisé

Le processus de boost est entièrement automatisé et suit les meilleures pratiques de Facebook Marketing. L'application crée d'abord une campagne avec l'objectif POST_ENGAGEMENT, optimisé spécifiquement pour maximiser l'engagement sur la publication sélectionnée.

Un ensemble de publicités (adset) est ensuite créé avec un ciblage par défaut adapté au marché français : géolocalisation France, âge 18-65 ans, et un budget quotidien de 20€. Ces paramètres peuvent être modifiés ultérieurement dans le gestionnaire de publicités Facebook selon vos besoins spécifiques.

Le créatif publicitaire est automatiquement généré à partir de la publication existante, préservant le texte, les images, et tous les éléments visuels originaux. Cette approche garantit la cohérence entre la publication organique et sa version promue.

### Sélection du Compte Publicitaire

Si vous avez accès à plusieurs comptes publicitaires, l'application affiche un dialogue de sélection permettant de choisir le compte à utiliser pour le boost. Cette fonctionnalité offre une flexibilité totale dans la gestion des budgets publicitaires et permet de séparer les dépenses selon vos besoins organisationnels.

Pour les utilisateurs n'ayant accès qu'à un seul compte publicitaire, la sélection se fait automatiquement, accélérant le processus de boost.

### Résultats et Suivi

Une fois le boost créé, l'application affiche un message de confirmation avec les identifiants de la campagne, de l'ensemble de publicités, et de la publicité créée. Ces informations permettent de retrouver facilement la campagne dans le gestionnaire de publicités Facebook pour effectuer des modifications ou suivre les performances.

Toutes les campagnes de boost sont créées avec le statut PAUSED, permettant de réviser les paramètres avant l'activation. Cette approche sécurisée évite les dépenses accidentelles et permet d'ajuster le ciblage ou le budget selon les besoins spécifiques de chaque boost.

### Bonnes Pratiques

Pour maximiser l'efficacité de vos boosts, sélectionnez de préférence les publications ayant déjà généré un engagement organique élevé. Ces publications ont prouvé leur capacité à intéresser votre audience et ont plus de chances de performer avec un budget publicitaire.

Surveillez régulièrement les performances de vos boosts dans le gestionnaire de publicités Facebook et ajustez les budgets en fonction des résultats obtenus. N'hésitez pas à arrêter les campagnes qui ne performent pas selon vos attentes et à réallouer le budget vers les publications les plus prometteuses.

## Statistiques et Insights

L'onglet Statistiques de Facebook Publisher Bois Malin v2.1 offre une vue complète et en temps réel des performances de vos pages Facebook. Cette fonctionnalité utilise l'API Facebook Insights pour fournir des données précises et actualisées sur l'engagement, la portée, et l'efficacité de votre contenu.

### Interface de Sélection

L'interface des statistiques commence par une section de sélection permettant de choisir la page à analyser et la période de temps à examiner. Le menu déroulant des pages affiche toutes les pages configurées dans l'application, facilitant la navigation entre vos différentes propriétés Facebook.

La sélection de période utilise deux champs de date au format YYYY-MM-DD, avec des valeurs par défaut couvrant les 7 derniers jours. Cette période peut être ajustée selon vos besoins d'analyse, permettant d'examiner des tendances à court terme ou des performances sur des périodes plus longues.

Le bouton "Actualiser" lance la récupération des données depuis l'API Facebook Insights et met à jour tous les éléments de l'interface avec les informations les plus récentes.

### Métriques de Page

La section des statistiques de page affiche quatre métriques essentielles pour évaluer la performance globale de votre page Facebook. Les impressions représentent le nombre total de fois où du contenu de votre page a été affiché, offrant une mesure de la visibilité globale de votre présence Facebook.

Les utilisateurs engagés comptabilisent le nombre unique d'utilisateurs qui ont interagi avec votre contenu de quelque manière que ce soit : likes, commentaires, partages, clics, ou autres actions. Cette métrique est particulièrement importante car elle mesure l'engagement réel plutôt que la simple exposition.

La portée indique le nombre unique d'utilisateurs qui ont vu votre contenu, permettant de mesurer l'étendue réelle de votre audience. Le nombre de fans affiche l'évolution de votre base d'abonnés, un indicateur clé de la croissance de votre communauté.

### Analyse des Publications

La liste des publications récentes présente les 10 dernières publications de la page sélectionnée avec leurs métriques individuelles de performance. Chaque publication est affichée avec son ID unique, un extrait du message (limité à 50 caractères pour la lisibilité), la date de publication, et ses métriques d'impressions et d'engagement.

Cette vue permet d'identifier rapidement les publications les plus performantes et celles qui pourraient bénéficier d'un boost publicitaire. Les métriques sont récupérées en temps réel depuis l'API Facebook Insights, garantissant la précision des données affichées.

### Fonctionnalités d'Interaction

Deux boutons d'action sont disponibles sous la liste des publications. Le bouton "Voir détails" affiche une fenêtre popup avec toutes les informations disponibles sur la publication sélectionnée, incluant l'ID complet, le message intégral, la date précise, et toutes les métriques de performance.

Le bouton "Booster ce post" lance directement le processus de création d'une campagne publicitaire pour promouvoir la publication sélectionnée, comme décrit dans la section précédente sur la fonctionnalité Boost Post.

### Gestion des Erreurs et Limitations

L'application gère intelligemment les cas où certaines métriques ne sont pas disponibles, affichant "N/A" pour les valeurs manquantes plutôt que de générer des erreurs. Cette approche robuste garantit que l'interface reste fonctionnelle même si l'API Facebook rencontre des limitations temporaires.

Les limitations de l'API Facebook Insights, telles que les délais de disponibilité des données ou les restrictions d'accès à certaines métriques, sont gérées de manière transparente, avec des messages d'information appropriés dans les logs de l'application.

### Interprétation des Données

Pour une utilisation optimale des statistiques, il est important de comprendre que les métriques Facebook peuvent varier selon plusieurs facteurs : l'algorithme Facebook, les habitudes de votre audience, et les tendances générales de la plateforme. Utilisez ces données comme des indicateurs de tendance plutôt que comme des valeurs absolues.

Comparez les performances entre différentes publications pour identifier les types de contenu qui résonnent le mieux avec votre audience. Les publications avec un ratio engagement/impressions élevé sont généralement de bons candidats pour le boost publicitaire.


## Tutoriel Pas-à-Pas

### 1. Configuration Initiale

#### Étape 1 : Installation
1. Décompressez l'archive `FacebookPublisherBoisMalin_v2.1_FINAL.tar.gz`
2. Ouvrez un terminal dans le dossier décompressé
3. Installez les dépendances : `pip install -r requirements.txt`
4. Copiez `.env.example` vers `.env` et configurez vos tokens

#### Étape 2 : Configuration Facebook
1. Créez une application Facebook sur [developers.facebook.com](https://developers.facebook.com)
2. Obtenez votre App ID et App Secret
3. Générez un token d'accès avec les permissions nécessaires
4. Ajoutez ces informations dans le fichier `.env`

### 2. Utilisation de l'Onglet Publicités

#### Création d'une Campagne Publicitaire

1. **Sélection du Compte Publicitaire**
   - Cliquez sur "Actualiser Comptes" pour charger vos comptes publicitaires
   - Sélectionnez le compte à utiliser dans la liste déroulante

2. **Configuration de la Campagne**
   - **Objectif** : Choisissez parmi POST_ENGAGEMENT, REACH, TRAFFIC, etc.
   - **Budget quotidien** : Définissez le budget en euros (ex: 20)
   - **Dates** : Configurez les dates de début et fin (format YYYY-MM-DD)

3. **Ciblage de l'Audience**
   - **Pays** : Définissez le pays de ciblage (ex: FR pour France)
   - **Âge minimum** : Âge minimum de l'audience (ex: 18)
   - **Âge maximum** : Âge maximum de l'audience (ex: 65)

4. **Créatif Publicitaire**
   - **Message** : Rédigez le texte de votre publicité
   - **Image** : Cliquez sur "Choisir Image" pour sélectionner un visuel
   - **Page** : Sélectionnez la page Facebook à associer

5. **Création**
   - Cliquez sur "Créer Campagne" pour créer uniquement la campagne
   - Ou cliquez sur "Créer Publicité" pour le workflow complet

#### Workflow Complet de Création
Le bouton "Créer Publicité" exécute automatiquement :
1. **Upload de l'image** vers Facebook (si fournie)
2. **Création du créatif** publicitaire
3. **Création de la campagne** avec l'objectif choisi
4. **Création de l'adset** avec le budget et le ciblage
5. **Création de la publicité** finale

Toutes les publicités créées apparaissent dans le TreeView avec le statut PAUSED pour révision.

### 3. Utilisation du Boost Post

#### Depuis l'Onglet Statistiques

1. **Sélection de la Page**
   - Choisissez la page dans la liste déroulante
   - Cliquez sur "Actualiser" pour charger les statistiques

2. **Visualisation des Posts**
   - Les 10 publications récentes s'affichent dans le tableau
   - Chaque ligne montre : ID, Message (40 chars), Date de création

3. **Boost d'un Post**
   - Sélectionnez une publication dans le tableau
   - Cliquez sur "Booster ce post"
   - Choisissez le compte publicitaire dans le dialogue
   - La publicité est créée automatiquement avec :
     - Objectif : POST_ENGAGEMENT
     - Budget : 20€/jour
     - Ciblage : France, 18-65 ans
     - Statut : PAUSED

### 4. Analyse des Statistiques

#### Métriques de Page
L'onglet Statistiques affiche en temps réel :
- **Impressions** : Nombre total d'affichages de la page
- **Utilisateurs engagés** : Nombre d'utilisateurs ayant interagi

#### Publications Récentes
Le tableau des publications montre :
- **ID du post** : Identifiant unique Facebook
- **Message** : Aperçu du contenu (40 caractères)
- **Date** : Date et heure de publication

#### Actions Disponibles
- **Booster ce post** : Création rapide d'une publicité
- **Voir détails** : Affichage des informations complètes du post

### 5. Gestion des Erreurs

#### Problèmes Courants et Solutions

**Erreur de Token**
```
Erreur : Invalid access token
Solution : Vérifiez que votre token est valide et non expiré
```

**Compte Publicitaire Introuvable**
```
Erreur : Aucun compte publicitaire trouvé
Solution : Vérifiez les permissions de votre token Facebook
```

**Échec de Publication**
```
Erreur : Failed to publish post
Solution : Vérifiez les permissions de la page et le contenu
```

#### Logs et Débogage
- Les logs sont sauvegardés dans `logs/facebook_publisher.log`
- Niveau DEBUG pour un débogage détaillé
- Toutes les requêtes API sont tracées

### 6. Bonnes Pratiques

#### Gestion des Tokens
- Renouvelez vos tokens avant expiration
- Utilisez des tokens long terme (60 jours)
- Sauvegardez vos tokens dans un endroit sécurisé

#### Création de Publicités
- Testez toujours avec un petit budget d'abord
- Vérifiez le ciblage avant activation
- Surveillez les performances régulièrement

#### Publication de Contenu
- Planifiez vos publications aux heures optimales
- Variez les types de contenu (texte, image, vidéo)
- Respectez les guidelines Facebook

### 7. Dépannage Avancé

#### Réinitialisation de l'Application
```bash
# Suppression des données temporaires
rm -rf __pycache__/
rm -rf .pytest_cache/
rm logs/*.log

# Réinstallation des dépendances
pip install -r requirements.txt --force-reinstall
```

#### Test de Connectivité API
```python
# Test rapide dans un terminal Python
from facebook_api import FacebookAPI
api = FacebookAPI("VOTRE_TOKEN")
pages = api.get_user_pages()
print(f"Pages trouvées : {len(pages)}")
```

#### Vérification des Permissions
Les permissions minimales requises :
- `pages_read_engagement` : Lecture des statistiques
- `pages_manage_posts` : Publication de contenu
- `ads_management` : Gestion des publicités
- `pages_show_list` : Liste des pages


