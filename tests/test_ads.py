"""
Tests for the Marketing API functionality
"""
import unittest
import sys
import os
import responses
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from facebook_api import FacebookAPI, FacebookAPIError


class TestMarketingAPI(unittest.TestCase):
    """Test cases for Marketing API functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = FacebookAPI(access_token="test_token")
    
    @responses.activate
    def test_get_ad_accounts(self):
        """Test getting ad accounts"""
        # Mock response
        mock_response = {
            "data": [
                {"id": "act_123456", "name": "Test Ad Account 1"},
                {"id": "act_789012", "name": "Test Ad Account 2"}
            ]
        }
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/me/adaccounts",
            json=mock_response,
            status=200
        )
        
        # Test the method
        result = self.api.get_ad_accounts()
        
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "act_123456")
        self.assertEqual(result[0]["name"], "Test Ad Account 1")
        self.assertEqual(result[1]["id"], "act_789012")
        self.assertEqual(result[1]["name"], "Test Ad Account 2")
    
    @responses.activate
    def test_get_page_insights(self):
        """Test getting page insights"""
        # Mock response
        mock_response = {
            "data": [
                {
                    "name": "page_impressions",
                    "period": "day",
                    "values": [{"value": 1500, "end_time": "2025-06-19T07:00:00+0000"}]
                },
                {
                    "name": "page_engaged_users",
                    "period": "day", 
                    "values": [{"value": 250, "end_time": "2025-06-19T07:00:00+0000"}]
                }
            ]
        }
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/123456789/insights",
            json=mock_response,
            status=200
        )
        
        # Test the method
        result = self.api.get_page_insights("123456789", 1718755200, 1718841600)
        
        # Assertions
        self.assertIn("data", result)
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["name"], "page_impressions")
        self.assertEqual(result["data"][0]["values"][0]["value"], 1500)
        self.assertEqual(result["data"][1]["name"], "page_engaged_users")
        self.assertEqual(result["data"][1]["values"][0]["value"], 250)
    
    @responses.activate
    def test_get_post_insights(self):
        """Test getting post insights"""
        # Mock response
        mock_response = {
            "data": [
                {
                    "name": "post_impressions",
                    "period": "lifetime",
                    "values": [{"value": 850}]
                },
                {
                    "name": "post_engaged_users", 
                    "period": "lifetime",
                    "values": [{"value": 120}]
                },
                {
                    "name": "post_reactions_by_type_total",
                    "period": "lifetime",
                    "values": [{"value": {"like": 45, "love": 12, "wow": 3}}]
                }
            ]
        }
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/123456789_987654321/insights",
            json=mock_response,
            status=200
        )
        
        # Test the method
        result = self.api.get_post_insights("123456789_987654321")
        
        # Assertions
        self.assertIn("data", result)
        self.assertEqual(len(result["data"]), 3)
        self.assertEqual(result["data"][0]["name"], "post_impressions")
        self.assertEqual(result["data"][0]["values"][0]["value"], 850)
        self.assertEqual(result["data"][1]["name"], "post_engaged_users")
        self.assertEqual(result["data"][1]["values"][0]["value"], 120)
        self.assertEqual(result["data"][2]["name"], "post_reactions_by_type_total")
        self.assertEqual(result["data"][2]["values"][0]["value"]["like"], 45)
    
    @responses.activate
    def test_get_page_posts(self):
        """Test getting page posts"""
        # Mock response
        mock_response = {
            "data": [
                {
                    "id": "123456789_111111111",
                    "message": "Test post 1",
                    "created_time": "2025-06-19T10:00:00+0000",
                    "permalink_url": "https://facebook.com/123456789/posts/111111111"
                },
                {
                    "id": "123456789_222222222", 
                    "message": "Test post 2",
                    "created_time": "2025-06-18T15:30:00+0000",
                    "permalink_url": "https://facebook.com/123456789/posts/222222222"
                }
            ]
        }
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/123456789/feed",
            json=mock_response,
            status=200
        )
        
        # Test the method
        result = self.api.get_recent_posts("123456789", limit=10)
        
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "123456789_111111111")
        self.assertEqual(result[0]["message"], "Test post 1")
        self.assertEqual(result[1]["id"], "123456789_222222222")
        self.assertEqual(result[1]["message"], "Test post 2")
    
    @responses.activate
    def test_create_boosted_post_ad(self):
        """Test creating a boosted post ad (complete flow)"""
        # Mock campaign creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123456/campaigns",
            json={"id": "campaign_123"},
            status=200
        )
        
        # Mock adset creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123456/adsets",
            json={"id": "adset_456"},
            status=200
        )
        
        # Mock creative creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123456/adcreatives",
            json={"id": "creative_789"},
            status=200
        )
        
        # Mock ad creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123456/ads",
            json={"id": "ad_101112"},
            status=200
        )
        
        # Test the complete boost flow
        # 1. Create campaign (fix the double act_ prefix issue)
        campaign = self.api.create_campaign("123456", "Boost Test", "POST_ENGAGEMENT")
        self.assertEqual(campaign["id"], "campaign_123")
        
        # 2. Create adset
        targeting = {
            "geo_locations": {"countries": ["FR"]},
            "age_min": 18,
            "age_max": 65
        }
        adset = self.api.create_ad_set("123456", "Test Adset", "campaign_123", 2000, targeting=targeting)
        self.assertEqual(adset["id"], "adset_456")
        
        # 3. Create creative
        creative = self.api.create_ad_creative("123456", "123456789_987654321")
        self.assertEqual(creative["id"], "creative_789")
        
        # 4. Create ad
        ad = self.api.create_ad("123456", "Boost Ad", "adset_456", "creative_789")
        self.assertEqual(ad["id"], "ad_101112")
    
    @responses.activate
    def test_api_error_handling_marketing(self):
        """Test error handling for Marketing API calls"""
        # Mock error response
        error_response = {
            "error": {
                "message": "Invalid ad account ID",
                "type": "OAuthException",
                "code": 100
            }
        }
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/me/adaccounts",
            json=error_response,
            status=400
        )
        
        # Test that error is properly raised
        with self.assertRaises(FacebookAPIError) as context:
            self.api.get_ad_accounts()
        
        self.assertIn("Invalid ad account ID", str(context.exception))
    
    def test_get_page_token_helper(self):
        """Test the _get_page_token helper method"""
        # Mock config loading
        with patch('utils.config.load_pages') as mock_load:
            mock_load.return_value = {
                "pages": [
                    {"id": "123456789", "name": "Test Page", "access_token": "page_token_123"},
                    {"id": "987654321", "name": "Other Page", "access_token": "page_token_456"}
                ]
            }
            
            # Test getting existing page token
            token = self.api._get_page_token("123456789")
            self.assertEqual(token, "page_token_123")
            
            # Test getting non-existing page token (should fallback to system token)
            token = self.api._get_page_token("999999999")
            self.assertEqual(token, "test_token")  # Falls back to system token


if __name__ == '__main__':
    unittest.main()

