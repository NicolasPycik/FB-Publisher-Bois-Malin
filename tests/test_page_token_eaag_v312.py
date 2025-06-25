"""
Test unitaire pour vérifier l'utilisation des Page Access Tokens EAAG v3.1.2

Ce test vérifie que l'application utilise correctement les Page Access Tokens
qui commencent par "EAAG" au lieu du User Access Token pour les publications.

Author: Manus AI
Date: June 25, 2025
Version: v3.1.2
"""

import pytest
import unittest.mock as mock
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from facebook_api import FacebookAPI, FacebookAPIError

class TestPageTokenEAAG:
    """Tests pour vérifier l'utilisation des Page Access Tokens EAAG"""
    
    @pytest.fixture
    def mock_facebook_api(self):
        """Fixture pour créer une instance FacebookAPI mockée"""
        with mock.patch.dict(os.environ, {
            'FACEBOOK_APP_ID': 'test_app_id',
            'FACEBOOK_APP_SECRET': 'test_app_secret',
            'FACEBOOK_ACCESS_TOKEN': 'EAABwzLixnjYBO1234567890'  # User token
        }):
            api = FacebookAPI()
            return api
    
    def test_page_token_starts_with_eaag(self, mock_facebook_api):
        """
        🔍 TEST CRITIQUE: Vérifie que _get_page_token() retourne un token EAAG
        """
        # Mock de la réponse /me/accounts
        mock_response = {
            "data": [
                {
                    "id": "244376752099348",
                    "name": "Bois de Rennes",
                    "access_token": "EAAGwzLixnjYBOx4RufP..."  # Page Access Token EAAG
                },
                {
                    "id": "629558686901232", 
                    "name": "Test Page",
                    "access_token": "EAAGwzLixnjYBOy5SugQ..."  # Page Access Token EAAG
                }
            ]
        }
        
        with mock.patch.object(mock_facebook_api, '_make_request', return_value=mock_response):
            # Test pour la première page
            page_token = mock_facebook_api._get_page_token("244376752099348")
            
            # 🎯 ASSERTION CRITIQUE: Le token doit commencer par EAAG
            assert page_token.startswith("EAAG"), f"❌ Page token should start with 'EAAG', got: {page_token[:10]}..."
            assert page_token == "EAAGwzLixnjYBOx4RufP...", f"❌ Unexpected page token: {page_token}"
            
            # Test pour la deuxième page
            page_token_2 = mock_facebook_api._get_page_token("629558686901232")
            assert page_token_2.startswith("EAAG"), f"❌ Page token should start with 'EAAG', got: {page_token_2[:10]}..."
    
    def test_publish_post_uses_page_token_eaag(self, mock_facebook_api):
        """
        🔍 TEST CRITIQUE: Vérifie que publish_post() utilise le Page Access Token EAAG
        """
        # Mock de la réponse /me/accounts
        mock_accounts_response = {
            "data": [
                {
                    "id": "244376752099348",
                    "access_token": "EAAGwzLixnjYBOx4RufPABCDEF123456"  # Page Access Token EAAG
                }
            ]
        }
        
        # Mock de la réponse de publication
        mock_publish_response = {
            "id": "244376752099348_122198332112256786"
        }
        
        # Variable pour capturer le token utilisé
        captured_token = None
        
        def mock_make_request(method, endpoint, params=None, data=None, files=None, access_token=None, max_retries=3):
            nonlocal captured_token
            
            if endpoint == "/me/accounts":
                return mock_accounts_response
            elif endpoint == "/244376752099348/feed":
                # 🎯 CAPTURE DU TOKEN UTILISÉ
                captured_token = access_token
                return mock_publish_response
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        with mock.patch.object(mock_facebook_api, '_make_request', side_effect=mock_make_request):
            # Exécuter la publication
            result = mock_facebook_api.publish_post(
                page_id="244376752099348",
                message="🔍 TEST v3.1.2 - Vérification Page Token EAAG"
            )
            
            # 🎯 ASSERTIONS CRITIQUES
            assert result == "244376752099348_122198332112256786", f"❌ Unexpected post ID: {result}"
            assert captured_token is not None, "❌ No access token was captured"
            assert captured_token.startswith("EAAG"), f"❌ Token should start with 'EAAG', got: {captured_token[:10]}..."
            assert captured_token == "EAAGwzLixnjYBOx4RufPABCDEF123456", f"❌ Wrong token used: {captured_token}"
    
    def test_publish_post_with_photos_uses_page_token_eaag(self, mock_facebook_api):
        """
        🔍 TEST CRITIQUE: Vérifie que publish_post_with_photos() utilise le Page Access Token EAAG
        """
        # Mock de la réponse /me/accounts
        mock_accounts_response = {
            "data": [
                {
                    "id": "244376752099348",
                    "access_token": "EAAGwzLixnjYBOx4RufPXYZ789"  # Page Access Token EAAG
                }
            ]
        }
        
        # Mock des réponses d'upload de photos
        mock_photo_response = {"id": "photo_123456"}
        mock_publish_response = {"id": "244376752099348_post_with_photos"}
        
        # Variables pour capturer les tokens utilisés
        captured_tokens = []
        
        def mock_make_request(method, endpoint, params=None, data=None, files=None, access_token=None, max_retries=3):
            nonlocal captured_tokens
            
            if endpoint == "/me/accounts":
                return mock_accounts_response
            elif endpoint == "/244376752099348/photos":
                # 🎯 CAPTURE DU TOKEN POUR UPLOAD PHOTO
                captured_tokens.append(("photo_upload", access_token))
                return mock_photo_response
            elif endpoint == "/244376752099348/feed":
                # 🎯 CAPTURE DU TOKEN POUR PUBLICATION
                captured_tokens.append(("post_publish", access_token))
                return mock_publish_response
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        # Mock de open() pour les fichiers
        mock_file = mock.mock_open(read_data=b"fake image data")
        
        with mock.patch.object(mock_facebook_api, '_make_request', side_effect=mock_make_request), \
             mock.patch('builtins.open', mock_file):
            
            # Exécuter la publication avec photos
            result = mock_facebook_api.publish_post_with_photos(
                page_id="244376752099348",
                message="🔍 TEST v3.1.2 - Photos avec Page Token EAAG",
                files=["/fake/path/image.jpg"]
            )
            
            # 🎯 ASSERTIONS CRITIQUES
            assert result == "244376752099348_post_with_photos", f"❌ Unexpected post ID: {result}"
            assert len(captured_tokens) == 2, f"❌ Expected 2 token captures, got: {len(captured_tokens)}"
            
            # Vérifier que tous les tokens utilisés sont des Page Access Tokens EAAG
            for operation, token in captured_tokens:
                assert token is not None, f"❌ No token captured for {operation}"
                assert token.startswith("EAAG"), f"❌ Token for {operation} should start with 'EAAG', got: {token[:10]}..."
                assert token == "EAAGwzLixnjYBOx4RufPXYZ789", f"❌ Wrong token for {operation}: {token}"
    
    def test_publish_post_with_video_uses_page_token_eaag(self, mock_facebook_api):
        """
        🔍 TEST CRITIQUE: Vérifie que publish_post_with_video() utilise le Page Access Token EAAG
        """
        # Mock de la réponse /me/accounts
        mock_accounts_response = {
            "data": [
                {
                    "id": "244376752099348",
                    "access_token": "EAAGwzLixnjYBOx4RufPVIDEO999"  # Page Access Token EAAG
                }
            ]
        }
        
        # Mock de la réponse d'upload vidéo
        mock_video_response = {"id": "244376752099348_video_123456"}
        
        # Variable pour capturer le token utilisé
        captured_token = None
        
        def mock_make_request(method, endpoint, params=None, data=None, files=None, access_token=None, max_retries=3):
            nonlocal captured_token
            
            if endpoint == "/me/accounts":
                return mock_accounts_response
            elif endpoint == "/244376752099348/videos":
                # 🎯 CAPTURE DU TOKEN POUR UPLOAD VIDÉO
                captured_token = access_token
                return mock_video_response
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        # Mock de open() pour le fichier vidéo
        mock_file = mock.mock_open(read_data=b"fake video data")
        
        with mock.patch.object(mock_facebook_api, '_make_request', side_effect=mock_make_request), \
             mock.patch('builtins.open', mock_file):
            
            # Exécuter la publication avec vidéo
            result = mock_facebook_api.publish_post_with_video(
                page_id="244376752099348",
                video_path="/fake/path/video.mp4",
                message="🔍 TEST v3.1.2 - Vidéo avec Page Token EAAG"
            )
            
            # 🎯 ASSERTIONS CRITIQUES
            assert result == "244376752099348_video_123456", f"❌ Unexpected video ID: {result}"
            assert captured_token is not None, "❌ No access token was captured"
            assert captured_token.startswith("EAAG"), f"❌ Token should start with 'EAAG', got: {captured_token[:10]}..."
            assert captured_token == "EAAGwzLixnjYBOx4RufPVIDEO999", f"❌ Wrong token used: {captured_token}"
    
    def test_user_token_vs_page_token_difference(self, mock_facebook_api):
        """
        🔍 TEST CRITIQUE: Vérifie que l'API distingue bien User Token vs Page Token
        """
        # Le User Access Token (depuis .env)
        user_token = mock_facebook_api.access_token
        assert user_token.startswith("EAAB"), f"❌ User token should start with 'EAAB', got: {user_token[:10]}..."
        
        # Mock de la réponse /me/accounts avec Page Access Tokens
        mock_accounts_response = {
            "data": [
                {
                    "id": "244376752099348",
                    "access_token": "EAAGwzLixnjYBOx4RufPDIFF123"  # Page Access Token EAAG
                }
            ]
        }
        
        with mock.patch.object(mock_facebook_api, '_make_request', return_value=mock_accounts_response):
            page_token = mock_facebook_api._get_page_token("244376752099348")
            
            # 🎯 ASSERTIONS CRITIQUES
            assert user_token != page_token, "❌ User token and page token should be different"
            assert user_token.startswith("EAAB"), f"❌ User token should start with 'EAAB': {user_token[:10]}..."
            assert page_token.startswith("EAAG"), f"❌ Page token should start with 'EAAG': {page_token[:10]}..."
    
    def test_page_token_cache_functionality(self, mock_facebook_api):
        """
        🔍 TEST: Vérifie que le cache des Page Access Tokens fonctionne correctement
        """
        # Mock de la réponse /me/accounts
        mock_accounts_response = {
            "data": [
                {
                    "id": "244376752099348",
                    "access_token": "EAAGwzLixnjYBOx4RufPCACHE123"
                },
                {
                    "id": "629558686901232",
                    "access_token": "EAAGwzLixnjYBOx4RufPCACHE456"
                }
            ]
        }
        
        call_count = 0
        def mock_make_request(method, endpoint, params=None, data=None, files=None, access_token=None, max_retries=3):
            nonlocal call_count
            if endpoint == "/me/accounts":
                call_count += 1
                return mock_accounts_response
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")
        
        with mock.patch.object(mock_facebook_api, '_make_request', side_effect=mock_make_request):
            # Premier appel - doit faire l'appel API
            token1 = mock_facebook_api._get_page_token("244376752099348")
            assert call_count == 1, "❌ First call should trigger API request"
            assert token1 == "EAAGwzLixnjYBOx4RufPCACHE123"
            
            # Deuxième appel pour la même page - doit utiliser le cache
            token2 = mock_facebook_api._get_page_token("244376752099348")
            assert call_count == 1, "❌ Second call should use cache, not trigger API request"
            assert token2 == token1, "❌ Cached token should be the same"
            
            # Appel pour une autre page - doit utiliser le cache existant
            token3 = mock_facebook_api._get_page_token("629558686901232")
            assert call_count == 1, "❌ Third call should use existing cache"
            assert token3 == "EAAGwzLixnjYBOx4RufPCACHE456"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

