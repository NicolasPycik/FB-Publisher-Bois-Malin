#!/usr/bin/env python3
"""
Facebook Publisher Bois Malin - Test Script

This script tests the core functionality of the Facebook Publisher application
without requiring a GUI environment.

Usage:
    python test_app.py

Author: Manus AI
Date: June 19, 2025
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing imports...")
    
    try:
        from facebook_api import FacebookAPI, FacebookAPIError
        print("✓ facebook_api imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import facebook_api: {e}")
        return False
    
    try:
        from models.page import Page
        from models.post import Post
        from models.ad import AdCreative, Campaign, AdSet, Ad, BoostedPost
        print("✓ models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import models: {e}")
        return False
    
    try:
        from utils import config, scheduler, logger
        print("✓ utils imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utils: {e}")
        return False
    
    return True

def test_facebook_api():
    """Test Facebook API initialization"""
    print("\nTesting Facebook API...")
    
    try:
        from facebook_api import FacebookAPI
        api = FacebookAPI()
        print("✓ FacebookAPI initialized successfully")
        print(f"  App ID: {api.app_id}")
        print(f"  Has access token: {'Yes' if api.access_token else 'No'}")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize FacebookAPI: {e}")
        return False

def test_models():
    """Test model classes"""
    print("\nTesting models...")
    
    try:
        from models.page import Page
        from models.post import Post
        
        # Test Page model
        page = Page("123456", "Test Page", "test_token")
        page_dict = page.to_dict()
        page_restored = Page.from_dict(page_dict)
        assert page_restored.id == page.id
        assert page_restored.name == page.name
        print("✓ Page model works correctly")
        
        # Test Post model
        post = Post("Hello World", ["123456"])
        post_dict = post.to_dict()
        post_restored = Post.from_dict(post_dict)
        assert post_restored.message == post.message
        print("✓ Post model works correctly")
        
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_config():
    """Test configuration utilities"""
    print("\nTesting configuration...")
    
    try:
        from utils import config
        
        # Test page loading/saving
        test_pages = {"pages": [{"id": "123", "name": "Test", "access_token": "token"}]}
        config.save_pages(test_pages)
        loaded_pages = config.load_pages()
        assert "pages" in loaded_pages
        print("✓ Page configuration works")
        
        # Test scheduled posts
        test_posts = {"posts": []}
        config.save_scheduled_posts(test_posts)
        loaded_posts = config.load_scheduled_posts()
        assert "posts" in loaded_posts
        print("✓ Scheduled posts configuration works")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Facebook Publisher Bois Malin - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_facebook_api,
        test_models,
        test_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The application is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

