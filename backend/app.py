#!/usr/bin/env python3
"""
Facebook Publisher SaaS v3.1.0 - Application Entry Point
Déploiement sur serveur de production
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the Flask app from main module
from main import app

if __name__ == '__main__':
    # Configuration pour production
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Démarrage Facebook Publisher SaaS v3.1.0")
    print(f"📡 Port: {port}")
    print(f"🔧 Debug: {debug}")
    print(f"🌐 URL: http://0.0.0.0:{port}")
    
    # Démarrer l'application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )

