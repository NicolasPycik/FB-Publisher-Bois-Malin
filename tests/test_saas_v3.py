"""
Tests unitaires pour Facebook Publisher SaaS v3.0.0
"""

import unittest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from routes.analytics_routes import analytics_bp
from routes.campaigns_routes import campaigns_bp
from routes.audiences_routes import audiences_bp, AUDIENCES_STORAGE

class TestFacebookPublisherSaaS(unittest.TestCase):
    """Test suite for Facebook Publisher SaaS"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Clear audiences storage for clean tests
        global AUDIENCES_STORAGE
        AUDIENCES_STORAGE.clear()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('status') == 'healthy')
        self.assertTrue(data.get('service') == 'Facebook Publisher SaaS')
    
    def test_dashboard_overview(self):
        """Test dashboard overview endpoint"""
        response = self.client.get('/api/dashboard/overview')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('data', data)
        
        overview_data = data['data']
        self.assertIn('pages_count', overview_data)
        self.assertIn('posts_today', overview_data)
        self.assertIn('total_reach', overview_data)
        self.assertIn('engagement', overview_data)
        self.assertIn('recent_activities', overview_data)

class TestAnalyticsRoutes(unittest.TestCase):
    """Test analytics and boost post functionality"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_get_posts_performance(self):
        """Test getting posts performance data"""
        response = self.client.get('/api/facebook/posts/performance')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('posts', data)
        self.assertIn('stats', data)
    
    @patch('routes.analytics_routes.get_facebook_token')
    def test_boost_post_success(self, mock_token):
        """Test successful post boost"""
        mock_token.return_value = 'test_token'
        
        boost_data = {
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
        self.assertIn('estimated_reach', data)
    
    def test_boost_post_missing_token(self):
        """Test boost post without Facebook token"""
        boost_data = {
            'objective': 'REACH',
            'budget': 20,
            'duration': 7,
            'audience_type': 'automatic'
        }
        
        response = self.client.post('/api/facebook/posts/test_post/boost',
                                  data=json.dumps(boost_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success'))
        self.assertIn('error', data)
    
    def test_boost_post_invalid_data(self):
        """Test boost post with invalid data"""
        boost_data = {
            'objective': 'INVALID',
            'budget': -5,  # Invalid budget
            'duration': 0   # Invalid duration
        }
        
        response = self.client.post('/api/facebook/posts/test_post/boost',
                                  data=json.dumps(boost_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success'))

class TestCampaignsRoutes(unittest.TestCase):
    """Test campaigns and ads functionality"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_get_campaigns(self):
        """Test getting campaigns list"""
        response = self.client.get('/api/facebook/campaigns')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('campaigns', data)
        
        # Check sample campaigns structure
        campaigns = data['campaigns']
        if campaigns:
            campaign = campaigns[0]
            required_fields = ['id', 'name', 'objective', 'status', 'budget']
            for field in required_fields:
                self.assertIn(field, campaign)
    
    @patch('routes.campaigns_routes.get_facebook_token')
    @patch('routes.campaigns_routes.get_facebook_app_id')
    def test_create_campaign_success(self, mock_app_id, mock_token):
        """Test successful campaign creation"""
        mock_token.return_value = 'test_token'
        mock_app_id.return_value = 'test_app_id'
        
        campaign_data = {
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
                'pageId': 'test_page',
                'headline': 'Test Headline',
                'text': 'Test text',
                'description': 'Test description',
                'callToAction': 'LEARN_MORE'
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
    
    def test_create_campaign_missing_data(self):
        """Test campaign creation with missing data"""
        incomplete_data = {
            'campaign': {
                'name': 'Test Campaign'
                # Missing objective and budget
            }
        }
        
        response = self.client.post('/api/facebook/campaigns/create',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_campaign_objectives(self):
        """Test getting campaign objectives"""
        response = self.client.get('/api/facebook/campaign-objectives')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('objectives', data)
        
        objectives = data['objectives']
        self.assertGreater(len(objectives), 0)
        
        # Check objective structure
        objective = objectives[0]
        required_fields = ['id', 'name', 'description', 'best_for']
        for field in required_fields:
            self.assertIn(field, objective)
    
    def test_get_ad_formats(self):
        """Test getting ad formats"""
        response = self.client.get('/api/facebook/ad-formats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('formats', data)
        
        formats = data['formats']
        self.assertGreater(len(formats), 0)
        
        # Check format structure
        format_item = formats[0]
        required_fields = ['id', 'name', 'description', 'specs']
        for field in required_fields:
            self.assertIn(field, format_item)

class TestAudiencesRoutes(unittest.TestCase):
    """Test audiences CRUD functionality"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Clear audiences storage
        global AUDIENCES_STORAGE
        AUDIENCES_STORAGE.clear()
    
    def test_get_audiences_empty(self):
        """Test getting audiences when none exist"""
        response = self.client.get('/api/facebook/audiences')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('audiences', data)
        self.assertEqual(data['total'], 3)  # Sample audiences are loaded
    
    def test_create_audience_success(self):
        """Test successful audience creation"""
        audience_data = {
            'name': 'Test Audience',
            'description': 'Test audience description',
            'type': 'custom',
            'targeting': {
                'geo_locations': {'countries': ['FR']},
                'age_min': 25,
                'age_max': 55,
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
        """Test audience creation with missing required fields"""
        incomplete_data = {
            'name': 'Test Audience'
            # Missing description, type, targeting
        }
        
        response = self.client.post('/api/facebook/audiences',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_audience_by_id(self):
        """Test getting specific audience by ID"""
        # First create an audience
        audience_data = {
            'name': 'Test Audience',
            'description': 'Test description',
            'type': 'custom',
            'targeting': {
                'geo_locations': {'countries': ['FR']},
                'age_min': 25,
                'age_max': 55
            }
        }
        
        create_response = self.client.post('/api/facebook/audiences',
                                         data=json.dumps(audience_data),
                                         content_type='application/json')
        
        create_data = json.loads(create_response.data)
        audience_id = create_data['audience']['id']
        
        # Now get the audience
        response = self.client.get(f'/api/facebook/audiences/{audience_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('audience', data)
        self.assertEqual(data['audience']['id'], audience_id)
    
    def test_get_nonexistent_audience(self):
        """Test getting non-existent audience"""
        response = self.client.get('/api/facebook/audiences/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_update_audience(self):
        """Test updating an audience"""
        # First create an audience
        audience_data = {
            'name': 'Original Name',
            'description': 'Original description',
            'type': 'custom',
            'targeting': {
                'geo_locations': {'countries': ['FR']},
                'age_min': 25,
                'age_max': 55
            }
        }
        
        create_response = self.client.post('/api/facebook/audiences',
                                         data=json.dumps(audience_data),
                                         content_type='application/json')
        
        create_data = json.loads(create_response.data)
        audience_id = create_data['audience']['id']
        
        # Update the audience
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
        """Test deleting an audience"""
        # First create an audience
        audience_data = {
            'name': 'To Delete',
            'description': 'Will be deleted',
            'type': 'custom',
            'targeting': {
                'geo_locations': {'countries': ['FR']},
                'age_min': 25,
                'age_max': 55
            }
        }
        
        create_response = self.client.post('/api/facebook/audiences',
                                         data=json.dumps(audience_data),
                                         content_type='application/json')
        
        create_data = json.loads(create_response.data)
        audience_id = create_data['audience']['id']
        
        # Delete the audience
        response = self.client.delete(f'/api/facebook/audiences/{audience_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        
        # Verify it's deleted
        get_response = self.client.get(f'/api/facebook/audiences/{audience_id}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_duplicate_audience(self):
        """Test duplicating an audience"""
        # First create an audience
        audience_data = {
            'name': 'Original',
            'description': 'Original description',
            'type': 'custom',
            'targeting': {
                'geo_locations': {'countries': ['FR']},
                'age_min': 25,
                'age_max': 55
            }
        }
        
        create_response = self.client.post('/api/facebook/audiences',
                                         data=json.dumps(audience_data),
                                         content_type='application/json')
        
        create_data = json.loads(create_response.data)
        audience_id = create_data['audience']['id']
        
        # Duplicate the audience
        response = self.client.post(f'/api/facebook/audiences/{audience_id}/duplicate')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('audience', data)
        
        duplicate = data['audience']
        self.assertNotEqual(duplicate['id'], audience_id)
        self.assertTrue(duplicate['name'].endswith('(Copie)'))
    
    def test_estimate_audience_size(self):
        """Test audience size estimation"""
        targeting_data = {
            'targeting': {
                'geo_locations': {'countries': ['FR']},
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
        self.assertIn('size', estimate)
        self.assertIn('reach_potential', estimate)
        self.assertIn('recommendations', estimate)
        self.assertIn('cost_estimate', estimate)
    
    def test_search_interests(self):
        """Test interest search functionality"""
        response = self.client.get('/api/facebook/audiences/interests/search?q=brico')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
        self.assertIn('interests', data)
        
        interests = data['interests']
        self.assertGreater(len(interests), 0)
        
        # Check that results contain the search term
        for interest in interests:
            self.assertTrue('brico' in interest['name'].lower() or 'brico' in interest['id'].lower())
    
    def test_search_interests_short_query(self):
        """Test interest search with too short query"""
        response = self.client.get('/api/facebook/audiences/interests/search?q=a')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_calculate_audience_size(self):
        """Test audience size calculation"""
        from routes.audiences_routes import calculate_audience_size
        
        # Test custom audience
        targeting = {
            'geo_locations': {'countries': ['FR']},
            'age_min': 25,
            'age_max': 55,
            'interests': ['Bricolage', 'Jardinage']
        }
        
        size = calculate_audience_size(targeting, 'custom')
        self.assertIsInstance(size, int)
        self.assertGreater(size, 1000)
        self.assertLess(size, 10000000)
        
        # Test lookalike audience
        lookalike_size = calculate_audience_size({}, 'lookalike')
        self.assertEqual(lookalike_size, 28000)
    
    def test_generate_audience_recommendations(self):
        """Test audience recommendations generation"""
        from routes.audiences_routes import generate_audience_recommendations
        
        # Test small audience
        small_targeting = {
            'age_min': 25,
            'age_max': 30,
            'interests': ['Very', 'Specific', 'Interests', 'List', 'Too', 'Long']
        }
        
        recommendations = generate_audience_recommendations(small_targeting, 3000)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Check for warning about small audience
        warning_found = any(rec['type'] == 'warning' for rec in recommendations)
        self.assertTrue(warning_found)

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestFacebookPublisherSaaS,
        TestAnalyticsRoutes,
        TestCampaignsRoutes,
        TestAudiencesRoutes,
        TestUtilityFunctions
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"RÉSUMÉ DES TESTS")
    print(f"{'='*60}")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.failures:
        print(f"\nÉCHECS:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\nERREURS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
    
    print(f"{'='*60}")
    
    # Exit with appropriate code
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)

