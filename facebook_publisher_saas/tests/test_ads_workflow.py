"""
Tests for the complete Marketing API workflow according to specifications
"""
import responses
import pytest
from facebook_api import FacebookAPI

class TestMarketingAPIWorkflow:
    """Test complete ad workflow according to specifications"""
    
    @responses.activate
    def test_create_ad_workflow(self):
        """Test the complete ad workflow: creative → campaign → adset → ad"""
        api = FacebookAPI("TEST_TOKEN")
        
        # Mock ad creative
        responses.add(
            responses.POST, 
            "https://graph.facebook.com/v18.0/act_123/adcreatives",
            json={"id": "111"}, 
            status=200
        )
        
        # Mock campaign
        responses.add(
            responses.POST, 
            "https://graph.facebook.com/v18.0/act_123/campaigns",
            json={"id": "222"}, 
            status=200
        )
        
        # Mock adset
        responses.add(
            responses.POST, 
            "https://graph.facebook.com/v18.0/act_123/adsets",
            json={"id": "333"}, 
            status=200
        )
        
        # Mock ad
        responses.add(
            responses.POST, 
            "https://graph.facebook.com/v18.0/act_123/ads",
            json={"id": "444"}, 
            status=200
        )

        # Execute workflow
        creative = api.create_ad_creative("123", "999_888")
        camp = api.create_campaign("123", "test", "POST_ENGAGEMENT")
        adset = api.create_ad_set(
            "123", 
            "Test AdSet",
            camp["id"], 
            daily_budget=500,
            targeting={"geo_locations": {"countries": ["FR"]}}
        )
        ad = api.create_ad("123", "test", adset["id"], creative["id"])

        # Verify results
        assert creative["id"] == "111"
        assert camp["id"] == "222"
        assert adset["id"] == "333"
        assert ad["id"] == "444"

    @responses.activate
    def test_get_ad_accounts(self):
        """Test get_ad_accounts method"""
        api = FacebookAPI("TEST_TOKEN")
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/me/adaccounts",
            json={
                "data": [
                    {"id": "act_123", "name": "Test Account 1"},
                    {"id": "act_456", "name": "Test Account 2"}
                ]
            },
            status=200
        )
        
        accounts = api.get_ad_accounts()
        
        assert len(accounts) == 2
        assert accounts[0]["id"] == "act_123"
        assert accounts[1]["name"] == "Test Account 2"

    @responses.activate
    def test_get_page_insights(self):
        """Test get_page_insights method"""
        api = FacebookAPI("TEST_TOKEN")
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/123/insights",
            json={
                "data": [
                    {
                        "name": "page_impressions",
                        "values": [{"value": 1000}]
                    },
                    {
                        "name": "page_engaged_users", 
                        "values": [{"value": 150}]
                    }
                ]
            },
            status=200
        )
        
        insights = api.get_page_insights("123", 1640995200, 1641081600)
        
        assert len(insights["data"]) == 2
        assert insights["data"][0]["name"] == "page_impressions"
        assert insights["data"][0]["values"][0]["value"] == 1000
        assert insights["data"][1]["name"] == "page_engaged_users"
        assert insights["data"][1]["values"][0]["value"] == 150

    @responses.activate
    def test_get_recent_posts(self):
        """Test get_recent_posts method"""
        api = FacebookAPI("TEST_TOKEN")
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/123/feed",
            json={
                "data": [
                    {
                        "id": "123_456",
                        "message": "Test post 1",
                        "created_time": "2025-01-01T12:00:00+0000"
                    },
                    {
                        "id": "123_789", 
                        "message": "Test post 2",
                        "created_time": "2025-01-01T11:00:00+0000"
                    }
                ]
            },
            status=200
        )
        
        posts = api.get_recent_posts("123", limit=10)
        
        assert len(posts) == 2
        assert posts[0]["id"] == "123_456"
        assert posts[0]["message"] == "Test post 1"
        assert posts[1]["id"] == "123_789"

    @responses.activate
    def test_boost_post_workflow(self):
        """Test complete boost post workflow"""
        api = FacebookAPI("TEST_TOKEN")
        
        # Mock creative creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123/adcreatives",
            json={"id": "creative_111"},
            status=200
        )
        
        # Mock campaign creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123/campaigns", 
            json={"id": "campaign_222"},
            status=200
        )
        
        # Mock adset creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123/adsets",
            json={"id": "adset_333"},
            status=200
        )
        
        # Mock ad creation
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/act_123/ads",
            json={"id": "ad_444"},
            status=200
        )
        
        # Execute boost workflow
        post_id = "123_456"
        
        creative = api.create_ad_creative("123", post_id)
        campaign = api.create_campaign("123", f"Boost {post_id}", "POST_ENGAGEMENT")
        adset = api.create_ad_set(
            "123",
            f"Boost AdSet {post_id}",
            campaign["id"],
            daily_budget=2000,  # 20€ in cents
            targeting={"geo_locations": {"countries": ["FR"]}, "age_min": 18, "age_max": 65}
        )
        ad = api.create_ad("123", f"Boost {post_id}", adset["id"], creative["id"])
        
        # Verify boost workflow
        assert creative["id"] == "creative_111"
        assert campaign["id"] == "campaign_222"
        assert adset["id"] == "adset_333"
        assert ad["id"] == "ad_444"

    @responses.activate
    def test_api_error_handling(self):
        """Test API error handling"""
        api = FacebookAPI("TEST_TOKEN")
        
        responses.add(
            responses.GET,
            "https://graph.facebook.com/v18.0/me/adaccounts",
            json={"error": {"message": "Invalid access token"}},
            status=400
        )
        
        with pytest.raises(Exception):
            api.get_ad_accounts()

    @responses.activate
    def test_upload_photo_workflow(self):
        """Test photo upload for ads"""
        api = FacebookAPI("TEST_TOKEN")
        
        responses.add(
            responses.POST,
            "https://graph.facebook.com/v18.0/123/photos",
            json={"id": "photo_555"},
            status=200
        )
        
        # Mock file for testing
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            tmp_file.write(b"fake image data")
            tmp_file_path = tmp_file.name
        
        try:
            photo = api.upload_photo("123", tmp_file_path)
            assert photo["id"] == "photo_555"
        finally:
            os.unlink(tmp_file_path)

