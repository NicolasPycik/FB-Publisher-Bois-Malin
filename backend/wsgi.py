#!/usr/bin/env python3
"""
WSGI Configuration for Facebook Publisher SaaS v3.1.0
Production deployment configuration
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the Flask app
from main import app

# WSGI application
application = app

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5001)

