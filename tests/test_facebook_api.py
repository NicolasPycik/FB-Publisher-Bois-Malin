"""
Tests for Facebook API wrapper

This module contains unit tests for the Facebook API wrapper.

Author: Manus AI
Date: June 19, 2025
"""

import unittest
import json
from unittest.mock import patch, MagicMock
import responses
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from facebook_api import FacebookAPI, FacebookAPIError


class TestFacebookAPI(unittest.TestCase):
    """Test cases for FacebookAPI class"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'APP_ID': 'test_app_id',
            'APP_SECRET': 'test_app_secret',
            'SYSTEM_USER_TOKEN': 'test_token'
        })
        self.env_patcher.start()
        
        # Create API instance
        self.api = FacebookAPI()
        
        # Base URL for API calls
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    @responses.activate
    def test_get_user_pages(self):
        """Test get_user_pages method"""
        # Mock API response
        mock_response = {
            "data": [
                {
                    "name": "Test Page 1",
                    "id": "123456789",
                    "access_token": "page_token_1"
                },
                {
                    "name": "Test Page 2",
                    "id": "987654321",
                    "access_token": "page_token_2"
                }
            ]
        }
        
        # Register mock response
        responses.add(
            responses.GET,
            f"{self.base_url}/me/accounts",
            json=mock_response,
            status=200
        )
        
        # Call method
        result = self.api.get_user_pages()
        
        # Verify result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Test Page 1")
        self.assertEqual(result[1]["id"], "987654321")
    
    @responses.activate
    def test_publish_post(self):
        """Test publish_post method"""
        # Mock API response
        mock_response = {
            "id": "123456789_987654321"
        }
        
        # Register mock response
        responses.add(
            responses.POST,
            f"{self.base_url}/test_page_id/feed",
            json=mock_response,
            status=200
        )
        
        # Call method
        result = self.api.publish_post(
            page_id="test_page_id",
            message="Test message",
            link="https://example.com",
            page_access_token="test_page_token"
        )
        
        # Verify result
        self.assertEqual(result["id"], "123456789_987654321")
    
    @responses.activate
    def test_upload_photo(self):
        """Test upload_photo method"""
        # Mock API response
        mock_response = {
            "id": "photo_123456789"
        }
        
        # Register mock response
        responses.add(
            responses.POST,
            f"{self.base_url}/test_page_id/photos",
            json=mock_response,
            status=200
        )
        
        # Create a temporary test file
        with open("test_photo.jpg", "w") as f:
            f.write("test photo content")
        
        try:
            # Call method with test file
            with patch("builtins.open", unittest.mock.mock_open(read_data="test photo content")):
                result = self.api.upload_photo(
                    page_id="test_page_id",
                    photo_path="test_photo.jpg",
                    caption="Test caption",
                    published=False,
                    page_access_token="test_page_token"
                )
            
            # Verify result
            self.assertEqual(result["id"], "photo_123456789")
        finally:
            # Clean up test file
            if os.path.exists("test_photo.jpg"):
                os.remove("test_photo.jpg")
    
    @responses.activate
    def test_debug_token(self):
        """Test debug_token method"""
        # Mock API response
        mock_response = {
            "data": {
                "app_id": "test_app_id",
                "is_valid": True,
                "expires_at": 1719158400,  # Example timestamp
                "scopes": ["pages_show_list", "pages_read_engagement"]
            }
        }
        
        # Register mock response
        responses.add(
            responses.GET,
            f"{self.base_url}/debug_token",
            json=mock_response,
            status=200
        )
        
        # Call method
        result = self.api.debug_token("test_input_token")
        
        # Verify result
        self.assertTrue(result["data"]["is_valid"])
        self.assertEqual(result["data"]["app_id"], "test_app_id")
    
    @responses.activate
    def test_api_error_handling(self):
        """Test error handling in API calls"""
        # Mock error response
        mock_error_response = {
            "error": {
                "message": "Invalid OAuth access token.",
                "type": "OAuthException",
                "code": 190,
                "error_subcode": 1234
            }
        }
        
        # Register mock response
        responses.add(
            responses.GET,
            f"{self.base_url}/me/accounts",
            json=mock_error_response,
            status=400
        )
        
        # Call method and expect exception
        with self.assertRaises(FacebookAPIError) as context:
            self.api.get_user_pages()
        
        # Verify exception details
        self.assertEqual(context.exception.message, "Invalid OAuth access token.")
        self.assertEqual(context.exception.error_code, 190)
        self.assertEqual(context.exception.error_subcode, 1234)
    
    @responses.activate
    def test_retry_on_server_error(self):
        """Test retry mechanism on server errors"""
        # Register first response (error)
        responses.add(
            responses.GET,
            f"{self.base_url}/me/accounts",
            json={"error": {"message": "Internal server error"}},
            status=500
        )
        
        # Register second response (success)
        mock_success_response = {
            "data": [
                {
                    "name": "Test Page",
                    "id": "123456789",
                    "access_token": "page_token"
                }
            ]
        }
        responses.add(
            responses.GET,
            f"{self.base_url}/me/accounts",
            json=mock_success_response,
            status=200
        )
        
        # Patch sleep to avoid waiting in tests
        with patch('time.sleep'):
            # Call method
            result = self.api.get_user_pages()
        
        # Verify result (should be from second response)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Page")


if __name__ == '__main__':
    unittest.main()
