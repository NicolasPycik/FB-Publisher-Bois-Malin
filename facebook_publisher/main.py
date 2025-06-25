#!/usr/bin/env python3
"""
Main launcher for Facebook Publisher Bois Malin

This script launches the Facebook Publisher application with proper
environment setup and error handling.

Usage:
    python main.py              # Launch GUI application
    python main.py --help       # Show help
    python main.py --test       # Test API connection
"""

import sys
import os
import argparse
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from FacebookPublisherBoisMalin import FacebookPublisherApp
    from facebook_api import FacebookAPI, test_api_connection
    from utils.logger import setup_logging, get_logger
    from utils.config import get_config
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def test_connection():
    """Test Facebook API connection"""
    print("Testing Facebook API connection...")
    
    config = get_config()
    token = config.get_facebook_token()
    
    if not token:
        print("❌ No Facebook access token found!")
        print("Please set FACEBOOK_ACCESS_TOKEN in .env file or environment variable")
        return False
    
    if test_api_connection(token):
        print("✅ Facebook API connection successful!")
        return True
    else:
        print("❌ Facebook API connection failed!")
        print("Please check your access token and internet connection")
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Facebook Publisher Bois Malin - Manage your Facebook pages and ads"
    )
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Test Facebook API connection"
    )
    parser.add_argument(
        "--log-level", 
        default="INFO", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = get_logger(__name__)
    
    logger.info("Starting Facebook Publisher Bois Malin")
    
    if args.test:
        # Test mode
        success = test_connection()
        sys.exit(0 if success else 1)
    
    try:
        # Launch GUI application
        app = FacebookPublisherApp()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"❌ Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
