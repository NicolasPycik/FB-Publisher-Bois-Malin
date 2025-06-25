"""
Test unitaire pour vérifier l'utilisation correcte des Page Access Tokens
selon les corrections définitives pour résoudre le problème de publication Facebook.

Author: Manus AI
Date: June 25, 2025
"""

import pytest
import requests
from unittest.mock import Mock, patch
import sys
import os

# Ajouter le chemin du backend pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from facebook_api import FacebookAPI, FacebookAPIError


class TestPageTokenUsage:
    """Tests pour vérifier l'utilisation correcte des Page Access Tokens"""
    
    def setup_method(self):
        """Configuration pour chaque test"""
        self.api = FacebookAPI(
            app_id="test_app_id",
            app_secret="test_app_secret", 
            access_token="test_user_token"
        )
    
    def test_page_token_used_in_publish_post(self, monkeypatch):
        """Test que publish_post utilise bien le Page Access Token"""
        
        # Mock de la réponse /me/accounts pour récupérer les page tokens
        def mock_make_request(method, endpoint, params=None, access_token=None, **kwargs):
            if endpoint == "/me/accounts":
                return {
                    "data": [
                        {"id": "123456789", "access_token": "EAAG_page_token_123"},
                        {"id": "987654321", "access_token": "EAAG_page_token_987"}
                    ]
                }
            elif endpoint == "/123456789/feed":
                # Vérifier que le token de page est utilisé
                assert access_token == "EAAG_page_token_123", f"Expected page token, got {access_token}"
                return {"id": "123456789_post_id"}
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        monkeypatch.setattr(self.api, "_make_request", mock_make_request)
        
        # Test de publication
        result = self.api.publish_post("123456789", "Test message")
        
        # Vérifications
        assert result == "123456789_post_id"
        assert "123456789" in self.api._page_token_cache
        assert self.api._page_token_cache["123456789"] == "EAAG_page_token_123"
    
    def test_page_token_used_in_publish_post_with_photos(self, monkeypatch):
        """Test que publish_post_with_photos utilise bien le Page Access Token"""
        
        def mock_make_request(method, endpoint, params=None, access_token=None, files=None, data=None, **kwargs):
            if endpoint == "/me/accounts":
                return {
                    "data": [{"id": "123456789", "access_token": "EAAG_page_token_123"}]
                }
            elif endpoint == "/123456789/photos":
                assert access_token == "EAAG_page_token_123"
                return {"id": "photo_123"}
            elif endpoint == "/123456789/feed":
                assert access_token == "EAAG_page_token_123"
                return {"id": "123456789_post_with_photos"}
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        # Mock open() pour les fichiers avec context manager
        class MockFile:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return b"fake image data"
        
        monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
        monkeypatch.setattr(self.api, "_make_request", mock_make_request)
        
        # Test de publication avec photos
        result = self.api.publish_post_with_photos("123456789", "Test with photo", ["test.jpg"])
        
        assert result == "123456789_post_with_photos"
    
    def test_page_token_used_in_publish_post_with_video(self, monkeypatch):
        """Test que publish_post_with_video utilise bien le Page Access Token"""
        
        def mock_make_request(method, endpoint, params=None, access_token=None, files=None, **kwargs):
            if endpoint == "/me/accounts":
                return {
                    "data": [{"id": "123456789", "access_token": "EAAG_page_token_123"}]
                }
            elif endpoint == "/123456789/videos":
                assert access_token == "EAAG_page_token_123"
                return {"id": "video_123"}
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        # Mock open() pour les fichiers avec context manager
        class MockFile:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return b"fake video data"
        
        monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
        monkeypatch.setattr(self.api, "_make_request", mock_make_request)
        
        # Test de publication avec vidéo
        result = self.api.publish_post_with_video("123456789", "test.mp4", "Test video")
        
        assert result == "video_123"
    
    def test_page_token_cache(self, monkeypatch):
        """Test que le cache des page tokens fonctionne correctement"""
        
        call_count = 0
        
        def mock_make_request(method, endpoint, params=None, access_token=None, **kwargs):
            nonlocal call_count
            if endpoint == "/me/accounts":
                call_count += 1
                return {
                    "data": [{"id": "123456789", "access_token": "EAAG_page_token_123"}]
                }
            elif endpoint == "/123456789/feed":
                return {"id": "post_id"}
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        monkeypatch.setattr(self.api, "_make_request", mock_make_request)
        
        # Premier appel - doit récupérer le token
        self.api.publish_post("123456789", "Message 1")
        assert call_count == 1
        
        # Deuxième appel - doit utiliser le cache
        self.api.publish_post("123456789", "Message 2")
        assert call_count == 1  # Pas d'appel supplémentaire à /me/accounts
    
    def test_page_not_found_error(self, monkeypatch):
        """Test la gestion d'erreur quand une page n'est pas trouvée"""
        
        def mock_make_request(method, endpoint, params=None, access_token=None, **kwargs):
            if endpoint == "/me/accounts":
                return {
                    "data": [{"id": "123456789", "access_token": "EAAG_page_token_123"}]
                }
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        monkeypatch.setattr(self.api, "_make_request", mock_make_request)
        
        # Test avec une page qui n'existe pas
        with pytest.raises(FacebookAPIError) as exc_info:
            self.api.publish_post("999999999", "Test message")
        
        assert "Page token error" in str(exc_info.value)
    
    def test_facebook_api_error_handling(self, monkeypatch):
        """Test la gestion des erreurs de l'API Facebook"""
        
        def mock_make_request(method, endpoint, params=None, access_token=None, **kwargs):
            if endpoint == "/me/accounts":
                return {
                    "data": [{"id": "123456789", "access_token": "EAAG_page_token_123"}]
                }
            elif endpoint == "/123456789/feed":
                raise FacebookAPIError("(#200) Permissions error")
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        monkeypatch.setattr(self.api, "_make_request", mock_make_request)
        
        # Test de gestion d'erreur de permissions
        with pytest.raises(FacebookAPIError) as exc_info:
            self.api.publish_post("123456789", "Test message")
        
        assert "Publication failed" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

