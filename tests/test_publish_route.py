"""
Test module for publish route functionality

Tests the /api/publish endpoint with various scenarios
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from backend.src.main import create_app
from backend.facebook_api import FacebookAPI


@pytest.fixture
def app():
    """Create test app"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def mock_api():
    """Mock Facebook API"""
    api = MagicMock(spec=FacebookAPI)
    return api


def test_publish_simple(monkeypatch, client):
    """Test simple text post publication"""
    def fake_post(*_):
        return "111_222"
    
    with patch('backend.src.routes.facebook_api_routes.get_facebook_api') as mock_get_api:
        mock_api = MagicMock()
        mock_api.publish_post.return_value = "111_222"
        mock_get_api.return_value = mock_api
        
        resp = client.post("/api/facebook/publish", 
                          json={"page_ids": ["1"], "message": "hi"})
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["1"]["post_id"] == "111_222"
        assert data["1"]["status"] == "ok"


def test_publish_with_link(client):
    """Test post with link"""
    with patch('backend.src.routes.facebook_api_routes.get_facebook_api') as mock_get_api:
        mock_api = MagicMock()
        mock_api.publish_post.return_value = "222_333"
        mock_get_api.return_value = mock_api
        
        resp = client.post("/api/facebook/publish", 
                          json={
                              "page_ids": ["1"], 
                              "message": "Check this out",
                              "link": "https://example.com"
                          })
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["1"]["post_id"] == "222_333"
        mock_api.publish_post.assert_called_with("1", "Check this out", "https://example.com")


def test_publish_with_images(client):
    """Test post with images"""
    with patch('backend.src.routes.facebook_api_routes.get_facebook_api') as mock_get_api:
        mock_api = MagicMock()
        mock_api.publish_post_with_photos.return_value = "333_444"
        mock_get_api.return_value = mock_api
        
        resp = client.post("/api/facebook/publish", 
                          json={
                              "page_ids": ["1"], 
                              "message": "Photo post",
                              "images": ["/path/to/image.jpg"]
                          })
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["1"]["post_id"] == "333_444"
        mock_api.publish_post_with_photos.assert_called_with("1", "Photo post", ["/path/to/image.jpg"])


def test_publish_with_video(client):
    """Test post with video"""
    with patch('backend.src.routes.facebook_api_routes.get_facebook_api') as mock_get_api:
        mock_api = MagicMock()
        mock_api.publish_post_with_video.return_value = "444_555"
        mock_get_api.return_value = mock_api
        
        resp = client.post("/api/facebook/publish", 
                          json={
                              "page_ids": ["1"], 
                              "message": "Video post",
                              "video": "/path/to/video.mp4"
                          })
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["1"]["post_id"] == "444_555"
        mock_api.publish_post_with_video.assert_called_with("1", "/path/to/video.mp4", "Video post")


def test_publish_multiple_pages(client):
    """Test publishing to multiple pages"""
    with patch('backend.src.routes.facebook_api_routes.get_facebook_api') as mock_get_api:
        mock_api = MagicMock()
        mock_api.publish_post.side_effect = ["111_222", "333_444"]
        mock_get_api.return_value = mock_api
        
        resp = client.post("/api/facebook/publish", 
                          json={
                              "page_ids": ["1", "2"], 
                              "message": "Multi-page post"
                          })
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["1"]["post_id"] == "111_222"
        assert data["2"]["post_id"] == "333_444"
        assert len(data) == 2


def test_publish_error_handling(client):
    """Test error handling in publish"""
    with patch('backend.src.routes.facebook_api_routes.get_facebook_api') as mock_get_api:
        mock_api = MagicMock()
        mock_api.publish_post.side_effect = Exception("API Error")
        mock_get_api.return_value = mock_api
        
        resp = client.post("/api/facebook/publish", 
                          json={
                              "page_ids": ["1"], 
                              "message": "Error test"
                          })
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["1"]["status"] == "error"
        assert "API Error" in data["1"]["error"]


def test_publish_no_api(client):
    """Test when Facebook API is not configured"""
    with patch('backend.src.routes.facebook_api_routes.get_facebook_api') as mock_get_api:
        mock_get_api.return_value = None
        
        resp = client.post("/api/facebook/publish", 
                          json={
                              "page_ids": ["1"], 
                              "message": "Test"
                          })
        
        assert resp.status_code == 500
        data = resp.get_json()
        assert "Facebook API not configured" in data["error"]

