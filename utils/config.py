"""
Configuration Utility

This module handles configuration loading and management.

Author: Manus AI
Date: June 19, 2025
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PAGES_FILE = os.path.join(DATA_DIR, 'facebook_pages.json')
SCHEDULED_POSTS_FILE = os.path.join(DATA_DIR, 'scheduled_posts.json')
BOOSTED_ADS_FILE = os.path.join(DATA_DIR, 'boosted_ads.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable with optional default value
    
    Args:
        name: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.environ.get(name, default)


def load_json_file(file_path: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Load JSON data from file with fallback to default
    
    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or is invalid
        
    Returns:
        Loaded data or default value
    """
    if default is None:
        default = {}
        
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {file_path}: {e}")
        return default


def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """
    Save data to JSON file
    
    Args:
        file_path: Path to JSON file
        data: Data to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving {file_path}: {e}")
        return False


def load_pages() -> Dict[str, Any]:
    """
    Load Facebook pages data
    
    Returns:
        Dictionary of pages data
    """
    return load_json_file(PAGES_FILE, {'pages': []})


def save_pages(pages_data: Dict[str, Any]) -> bool:
    """
    Save Facebook pages data
    
    Args:
        pages_data: Pages data to save
        
    Returns:
        True if successful, False otherwise
    """
    return save_json_file(PAGES_FILE, pages_data)


def load_scheduled_posts() -> Dict[str, Any]:
    """
    Load scheduled posts data
    
    Returns:
        Dictionary of scheduled posts data
    """
    return load_json_file(SCHEDULED_POSTS_FILE, {'posts': []})


def save_scheduled_posts(posts_data: Dict[str, Any]) -> bool:
    """
    Save scheduled posts data
    
    Args:
        posts_data: Posts data to save
        
    Returns:
        True if successful, False otherwise
    """
    return save_json_file(SCHEDULED_POSTS_FILE, posts_data)


def load_boosted_ads() -> Dict[str, Any]:
    """
    Load boosted ads data
    
    Returns:
        Dictionary of boosted ads data
    """
    return load_json_file(BOOSTED_ADS_FILE, {'boosted_posts': []})


def save_boosted_ads(ads_data: Dict[str, Any]) -> bool:
    """
    Save boosted ads data
    
    Args:
        ads_data: Ads data to save
        
    Returns:
        True if successful, False otherwise
    """
    return save_json_file(BOOSTED_ADS_FILE, ads_data)
