# Facebook Publisher Bois Malin - Todo List

## Phase 1: Appliquer les patches au wrapper API Facebook

### Extensions du wrapper API
- [x] Ajouter get_ad_accounts() pour récupérer les comptes publicitaires
- [x] Ajouter get_page_insights() pour les statistiques de page
- [x] Ajouter get_post_insights() pour les statistiques de post
- [x] Ajouter _get_page_token() helper method

### Corrections du scheduler
- [x] Ajouter méthode stop() pour arrêt propre du thread
- [x] Modifier on_closing() pour arrêter le scheduler

## Phase 2: Implémenter l'onglet Publicités complet

### Interface utilisateur
- [x] Créer setup_ads_tab() avec sélecteurs ad account et page
- [x] Ajouter champs objectif, budget, dates, ciblage
- [x] Ajouter section créatif (message, lien, image)
- [x] Ajouter sélecteur CTA
- [x] Créer TreeView pour afficher les publicités

### Méthodes backend
- [x] Implémenter refresh_ad_accounts()
- [x] Implémenter create_campaign_flow()
- [x] Implémenter create_ad_flow()
- [x] Gérer la création complète campagne > adset > ad

## Phase 3: Ajouter la fonctionnalité Boost Post

### Interface Boost Post
- [x] Ajouter bouton "Booster ce post" dans l'onglet Statistiques
- [x] Implémenter boost_selected_post()
- [x] Créer dialogue de sélection ad account pour boost
- [x] Intégrer avec l'API Marketing pour créer boost complet

## Phase 4: Finaliser les statistiques et insights

### Statistiques réelles
- [x] Implémenter refresh_stats() avec vrais appels API
- [x] Remplir tree_recent_posts avec /feed endpoint
- [x] Afficher métriques réelles (impressions, engagement)
- [x] Gérer les périodes de dates pour les insights

## Phase 5: Compléter les tests unitaires

### Tests Marketing API
- [x] Créer tests/test_ads.py
- [x] Tester create_boosted_post_ad()
- [x] Tester get_ad_accounts()
- [x] Tester get_page_insights() et get_post_insights()

## Phase 6: Mettre à jour la documentation

### Documentation v2.1
- [x] Ajouter guide utilisation onglet Publicités
- [x] Documenter fonctionnalité Boost Post
- [x] Préciser permissions requises (ads_management)
- [x] Mettre à jour captures d'écran

## Phase 7: Livrer la version finale v2.1

### Package final
- [x] Tester l'application complète
- [x] Créer archive v2.1
- [x] Valider tous les tests
- [x] Livrer package final

