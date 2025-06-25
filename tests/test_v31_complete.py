"""
Tests automatiques complets pour Facebook Publisher SaaS v3.1.0
Couvre toutes les nouvelles fonctionnalités implémentées
"""

import unittest
import json
import sys
import os
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

class TestFacebookPublisherSaaSv31(unittest.TestCase):
    """Test suite complet pour Facebook Publisher SaaS v3.1.0"""
    
    def setUp(self):
        """Set up test client and temporary data directory"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create temporary directory for test data
        self.test_data_dir = tempfile.mkdtemp()
        self.original_audiences_file = None
        
        # Mock audiences file path
        import routes.audiences_routes as audiences_module
        self.original_audiences_file = audiences_module.AUDIENCES_FILE
        audiences_module.AUDIENCES_FILE = os.path.join(self.test_data_dir, 'audiences.json')
        
        # Initialize empty audiences file
        with open(audiences_module.AUDIENCES_FILE, 'w') as f:
            json.dump([], f)
    
    def tearDown(self):
        """Clean up test data"""
        if self.test_data_dir and os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        
        # Restore original audiences file path
        if self.original_audiences_file:
            import routes.audiences_routes as audiences_module
            audiences_module.AUDIENCES_FILE = self.original_audiences_file

class TestPublishMultiPages(TestFacebookPublisherSaaSv31):
    """Tests pour la publication multi-pages"""
    
    @patch('routes.facebook_api_routes.get_facebook_token')
    def test_publish_multi_pages_success(self, mock_token):
        """Test publication réussie sur plusieurs pages"""
        mock_token.return_value = 'test_token'
        
        publish_data = {
            'message': 'Test publication multi-pages',
            'link': 'https://example.com',
            'pages': ['page1', 'page2', 'page3']
        }
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {'id': 'post_123'}
            
            response = self.client.post('/api/publish',
                                      data=json.dumps(publish_data),
                                      content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data.get('success'))
            self.assertIn('results', data)
    
    def test_publish_multi_pages_missing_data(self):
        """Test publication avec données manquantes"""
        incomplete_data = {
            'message': 'Test message'
            # Missing pages
        }
        
        response = self.client.post('/api/publish',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_publish_multi_pages_empty_message(self):
        """Test publication avec message vide"""
        empty_data = {
            'message': '',
            'pages': ['page1']
        }
        
        response = self.client.post('/api/publish',
                                  data=json.dumps(empty_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

class TestBoostPostCreation(TestFacebookPublisherSaaSv31):
    """Tests pour la création de boost post"""
    
    @patch('routes.analytics_routes.get_facebook_token')
    @patch('routes.analytics_routes.FacebookAPI')
    def test_boost_post_success(self, mock_fb_api_class, mock_token):
        """Test boost post réussi"""
        mock_token.return_value = 'test_token'
        
        # Mock Facebook API instance
        mock_fb_api = MagicMock()
        mock_fb_api_class.return_value = mock_fb_api
        mock_fb_api.create_boosted_post_ad.return_value = {
            'success': True,
            'campaign_id': 'campaign_123',
            'adset_id': 'adset_123',
            'ad_id': 'ad_123'
        }
        
        boost_data = {
            'ad_account_id': 'act_123456789',
            'page_id': 'page_123',
            'objective': 'REACH',
            'budget': 20,
            'duration': 7,
            'audience_type': 'automatic'
        }
        
        response = self.client.post('/api/facebook/posts/test_post/boost',
                                  data=json.dumps(boost_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('campaign_id', data)
        self.assertIn('estimated_reach', data)
    
    def test_boost_post_missing_fields(self):
        """Test boost post avec champs manquants"""
        incomplete_data = {
            'objective': 'REACH',
            'budget': 20
            # Missing required fields
        }
        
        response = self.client.post('/api/facebook/posts/test_post/boost',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success'))
        self.assertIn('error', data)
    
    def test_boost_post_invalid_budget(self):
        """Test boost post avec budget invalide"""
        invalid_data = {
            'ad_account_id': 'act_123456789',
            'page_id': 'page_123',
            'objective': 'REACH',
            'budget': 2,  # Too low
            'duration': 7,
            'audience_type': 'automatic'
        }
        
        response = self.client.post('/api/facebook/posts/test_post/boost',
                                  data=json.dumps(invalid_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success'))
        self.assertIn('Budget minimum', data.get('error', ''))

class TestCreateAdsWithAudience(TestFacebookPublisherSaaSv31):
    """Tests pour la création de publicités avec audiences"""
    
    @patch('routes.campaigns_routes.get_facebook_token')
    @patch('routes.campaigns_routes.FacebookAPI')
    def test_create_complete_campaign_success(self, mock_fb_api_class, mock_token):
        """Test création de campagne complète réussie"""
        mock_token.return_value = 'test_token'
        
        # Mock Facebook API instance
        mock_fb_api = MagicMock()
        mock_fb_api_class.return_value = mock_fb_api
        
        # Mock successful API calls
        mock_fb_api.create_campaign.return_value = {
            'success': True,
            'campaign_id': 'campaign_123'
        }
        mock_fb_api.create_adset.return_value = {
            'success': True,
            'adset_id': 'adset_123'
        }
        mock_fb_api.create_ad_creative.return_value = {
            'success': True,
            'creative_id': 'creative_123'
        }
        mock_fb_api.create_ad.return_value = {
            'success': True,
            'ad_id': 'ad_123'
        }
        
        campaign_data = {
            'adAccountId': 'act_123456789',
            'campaign': {
                'name': 'Test Campaign',
                'objective': 'REACH',
                'budget': 500
            },
            'adset': {
                'name': 'Test Adset',
                'dailyBudget': 20,
                'startDate': '2025-06-25',
                'audienceType': 'automatic'
            },
            'ad': {
                'name': 'Test Ad',
                'format': 'single_image',
                'pageId': 'page_123',
                'headline': 'Test Headline',
                'text': 'Test text'
            }
        }
        
        response = self.client.post('/api/facebook/campaigns/create',
                                  data=json.dumps(campaign_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('campaign_id', data)
        self.assertIn('estimates', data)
    
    def test_create_campaign_missing_sections(self):
        """Test création de campagne avec sections manquantes"""
        incomplete_data = {
            'campaign': {
                'name': 'Test Campaign',
                'objective': 'REACH'
            }
            # Missing adset and ad sections
        }
        
        response = self.client.post('/api/facebook/campaigns/create',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success'))
        self.assertIn('Section manquante', data.get('error', ''))
    
    def test_get_campaign_objectives(self):
        """Test récupération des objectifs de campagne"""
        response = self.client.get('/api/facebook/campaign-objectives')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('objectives', data)
        
        objectives = data['objectives']
        self.assertGreater(len(objectives), 0)
        
        # Vérifier la structure des objectifs
        objective = objectives[0]
        required_fields = ['id', 'name', 'description', 'best_for']
        for field in required_fields:
            self.assertIn(field, objective)
    
    def test_get_ad_formats(self):
        """Test récupération des formats publicitaires"""
        response = self.client.get('/api/facebook/ad-formats')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('formats', data)
        
        formats = data['formats']
        self.assertGreater(len(formats), 0)
        
        # Vérifier la structure des formats
        format_item = formats[0]
        required_fields = ['id', 'name', 'description', 'specs']
        for field in required_fields:
            self.assertIn(field, format_item)

class TestAudienceCRUD(TestFacebookPublisherSaaSv31):
    """Tests pour le CRUD des audiences"""
    
    def test_create_audience_success(self):
        """Test création d'audience réussie"""
        audience_data = {
            'name': 'Test Audience',
            'description': 'Test audience description',
            'type': 'custom',
            'targeting': {
                'location': 'FR',
                'age_min': 25,
                'age_max': 55,
                'gender': 'all',
                'interests': ['Bricolage', 'Jardinage']
            }
        }
        
        response = self.client.post('/api/facebook/audiences',
                                  data=json.dumps(audience_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('audience', data)
        
        audience = data['audience']
        self.assertEqual(audience['name'], 'Test Audience')
        self.assertEqual(audience['type'], 'custom')
        self.assertIn('id', audience)
        self.assertIn('size', audience)
    
    def test_create_audience_missing_fields(self):
        """Test création d'audience avec champs manquants"""
        incomplete_data = {
            'name': 'Test Audience'
            # Missing required fields
        }
        
        response = self.client.post('/api/facebook/audiences',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success'))
        self.assertIn('error', data)
    
    def test_get_audiences(self):
        """Test récupération des audiences"""
        response = self.client.get('/api/facebook/audiences')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('audiences', data)
        self.assertIn('total', data)
    
    def test_update_audience(self):
        """Test mise à jour d'audience"""
        # Créer d'abord une audience
        audience_data = {
            'name': 'Original Name',
            'description': 'Original description',
            'type': 'custom',
            'targeting': {
                'location': 'FR',
                'age_min': 25,
                'age_max': 55
            }
        }
        
        create_response = self.client.post('/api/facebook/audiences',
                                         data=json.dumps(audience_data),
                                         content_type='application/json')
        
        create_data = json.loads(create_response.data)
        audience_id = create_data['audience']['id']
        
        # Mettre à jour l'audience
        update_data = {
            'name': 'Updated Name',
            'description': 'Updated description'
        }
        
        response = self.client.put(f'/api/facebook/audiences/{audience_id}',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertEqual(data['audience']['name'], 'Updated Name')
    
    def test_delete_audience(self):
        """Test suppression d'audience"""
        # Créer d'abord une audience
        audience_data = {
            'name': 'To Delete',
            'description': 'Will be deleted',
            'type': 'custom',
            'targeting': {
                'location': 'FR',
                'age_min': 25,
                'age_max': 55
            }
        }
        
        create_response = self.client.post('/api/facebook/audiences',
                                         data=json.dumps(audience_data),
                                         content_type='application/json')
        
        create_data = json.loads(create_response.data)
        audience_id = create_data['audience']['id']
        
        # Supprimer l'audience
        response = self.client.delete(f'/api/facebook/audiences/{audience_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        
        # Vérifier qu'elle est supprimée
        get_response = self.client.get(f'/api/facebook/audiences/{audience_id}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_duplicate_audience(self):
        """Test duplication d'audience"""
        # Créer d'abord une audience
        audience_data = {
            'name': 'Original',
            'description': 'Original description',
            'type': 'custom',
            'targeting': {
                'location': 'FR',
                'age_min': 25,
                'age_max': 55
            }
        }
        
        create_response = self.client.post('/api/facebook/audiences',
                                         data=json.dumps(audience_data),
                                         content_type='application/json')
        
        create_data = json.loads(create_response.data)
        audience_id = create_data['audience']['id']
        
        # Dupliquer l'audience
        response = self.client.post(f'/api/facebook/audiences/{audience_id}/duplicate')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('audience', data)
        
        duplicate = data['audience']
        self.assertNotEqual(duplicate['id'], audience_id)
        self.assertTrue(duplicate['name'].endswith('(Copie)'))
    
    def test_estimate_audience_size(self):
        """Test estimation de taille d'audience"""
        targeting_data = {
            'targeting': {
                'location': 'FR',
                'age_min': 25,
                'age_max': 55,
                'interests': ['Bricolage']
            },
            'type': 'custom'
        }
        
        response = self.client.post('/api/facebook/audiences/estimate',
                                  data=json.dumps(targeting_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('estimate', data)
        
        estimate = data['estimate']
        required_fields = ['size', 'reach_potential', 'recommendations', 'cost_estimate']
        for field in required_fields:
            self.assertIn(field, estimate)
    
    def test_search_interests(self):
        """Test recherche de centres d'intérêt"""
        response = self.client.get('/api/facebook/audiences/interests/search?q=brico')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('interests', data)
        
        interests = data['interests']
        self.assertGreater(len(interests), 0)
        
        # Vérifier que les résultats contiennent le terme recherché
        for interest in interests:
            self.assertTrue('brico' in interest['name'].lower() or 'brico' in interest['id'].lower())
    
    def test_search_interests_short_query(self):
        """Test recherche avec requête trop courte"""
        response = self.client.get('/api/facebook/audiences/interests/search?q=a')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success'))
        self.assertIn('error', data)

class TestAPIEndpoints(TestFacebookPublisherSaaSv31):
    """Tests pour les endpoints API généraux"""
    
    def test_health_check(self):
        """Test endpoint de santé"""
        response = self.client.get('/api/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('status') == 'healthy')
        self.assertTrue(data.get('service') == 'Facebook Publisher SaaS')
    
    def test_dashboard_overview(self):
        """Test endpoint vue d'ensemble du tableau de bord"""
        response = self.client.get('/api/dashboard/overview')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('data', data)
    
    @patch('routes.analytics_routes.get_facebook_token')
    def test_get_ad_accounts(self, mock_token):
        """Test récupération des comptes publicitaires"""
        mock_token.return_value = 'test_token'
        
        with patch('routes.analytics_routes.FacebookAPI') as mock_fb_api_class:
            mock_fb_api = MagicMock()
            mock_fb_api_class.return_value = mock_fb_api
            mock_fb_api.get_ad_accounts.return_value = [
                {'id': 'act_123', 'name': 'Test Account'}
            ]
            
            response = self.client.get('/api/facebook/ad-accounts')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data.get('success'))
            self.assertIn('ad_accounts', data)

class TestUtilityFunctions(TestFacebookPublisherSaaSv31):
    """Tests pour les fonctions utilitaires"""
    
    def test_calculate_audience_size(self):
        """Test calcul de taille d'audience"""
        from routes.audiences_routes import calculate_audience_size
        
        # Test audience personnalisée
        targeting = {
            'location': 'FR',
            'age_min': 25,
            'age_max': 55,
            'interests': ['Bricolage', 'Jardinage']
        }
        
        size = calculate_audience_size(targeting, 'custom')
        self.assertIsInstance(size, int)
        self.assertGreater(size, 1000)
        self.assertLess(size, 10000000)
        
        # Test audience similaire
        lookalike_size = calculate_audience_size({}, 'lookalike')
        self.assertEqual(lookalike_size, 28000)
    
    def test_generate_audience_recommendations(self):
        """Test génération de recommandations d'audience"""
        from routes.audiences_routes import generate_audience_recommendations
        
        # Test petite audience
        small_targeting = {
            'age_min': 25,
            'age_max': 30,
            'interests': ['Very', 'Specific', 'Interests']
        }
        
        recommendations = generate_audience_recommendations(small_targeting, 3000)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Vérifier qu'il y a un avertissement pour petite audience
        warning_found = any(rec['type'] == 'warning' for rec in recommendations)
        self.assertTrue(warning_found)

if __name__ == '__main__':
    # Configuration des tests
    unittest.TestLoader.sortTestMethodsUsing = None
    
    # Créer la suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter les classes de tests
    test_classes = [
        TestPublishMultiPages,
        TestBoostPostCreation,
        TestCreateAdsWithAudience,
        TestAudienceCRUD,
        TestAPIEndpoints,
        TestUtilityFunctions
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    # Afficher le résumé
    print(f"\n{'='*80}")
    print(f"RÉSUMÉ DES TESTS - Facebook Publisher SaaS v3.1.0")
    print(f"{'='*80}")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.failures:
        print(f"\nÉCHECS:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print(f"\nERREURS:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    # Calculer le pourcentage de réussite
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\nTaux de réussite: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT! Qualité de code très élevée")
    elif success_rate >= 80:
        print("✅ BIEN! Qualité de code satisfaisante")
    elif success_rate >= 70:
        print("⚠️  MOYEN! Améliorations nécessaires")
    else:
        print("❌ FAIBLE! Corrections importantes requises")
    
    print(f"{'='*80}")
    
    # Code de sortie
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)

