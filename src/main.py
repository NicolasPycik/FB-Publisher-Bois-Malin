"""
Facebook Publisher SaaS - Main Application
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Facebook Publisher SaaS'})

@app.route('/api/dashboard/overview')
def dashboard_overview():
    """Get dashboard overview data"""
    try:
        # Mock data for now
        data = {
            'pages_count': 65,
            'posts_today': 12,
            'total_reach': 15400,
            'engagement': 892,
            'recent_activities': [
                {'activity': 'Publication sur 5 pages', 'type': 'Post', 'status': 'Publié', 'time': 'Il y a 2h'},
                {'activity': 'Campagne "Promo Été" créée', 'type': 'Publicité', 'status': 'En attente', 'time': 'Il y a 4h'},
                {'activity': 'Boost post avec budget 20€', 'type': 'Boost', 'status': 'Actif', 'time': 'Il y a 6h'}
            ]
        }
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du chargement: {str(e)}'
        }), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """Handle settings get/save"""
    settings_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    
    if request.method == 'GET':
        # Read settings
        settings = {}
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        settings[key] = value
        
        # Return settings with secrets hidden
        return jsonify({
            'app_id': settings.get('FACEBOOK_APP_ID', ''),
            'app_secret': '***' if settings.get('FACEBOOK_APP_SECRET') else '',
            'access_token': '***' if settings.get('FACEBOOK_ACCESS_TOKEN') else '',
            'email_notifications': settings.get('EMAIL_NOTIFICATIONS', 'false').lower() == 'true',
            'auto_reports': settings.get('AUTO_REPORTS', 'false').lower() == 'true',
            'timezone': settings.get('TIMEZONE', 'Europe/Paris')
        })
    
    elif request.method == 'POST':
        # Save settings
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('app_id') or not data.get('app_secret') or not data.get('access_token'):
                return jsonify({'error': 'Tous les champs sont obligatoires'}), 400
            
            # Create .env content
            env_content = f"""# Facebook API Configuration
FACEBOOK_APP_ID={data['app_id']}
FACEBOOK_APP_SECRET={data['app_secret']}
FACEBOOK_ACCESS_TOKEN={data['access_token']}

# Application Settings
EMAIL_NOTIFICATIONS={str(data.get('email_notifications', False)).lower()}
AUTO_REPORTS={str(data.get('auto_reports', False)).lower()}
TIMEZONE={data.get('timezone', 'Europe/Paris')}
DEBUG=True
LOG_LEVEL=INFO
"""
            
            # Write to .env file
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            with open(settings_file, 'w') as f:
                f.write(env_content)
            
            return jsonify({
                'success': True,
                'message': 'Paramètres sauvegardés avec succès'
            })
            
        except Exception as e:
            return jsonify({'error': f'Erreur lors de la sauvegarde: {str(e)}'}), 500

@app.route('/api/facebook/pages/sync', methods=['POST'])
def sync_facebook_pages():
    """Synchronize Facebook pages from Graph API"""
    try:
        # Read settings from .env file
        settings_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        settings = {}
        
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        settings[key] = value
        
        access_token = settings.get('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            return jsonify({'error': 'Token d\'accès Facebook non configuré'}), 400
        
        # Call Facebook Graph API to get pages
        import requests
        
        # First, check token validity and permissions
        me_url = f"https://graph.facebook.com/v18.0/me"
        me_params = {
            'access_token': access_token,
            'fields': 'id,name'
        }
        
        me_response = requests.get(me_url, params=me_params)
        if me_response.status_code != 200:
            error_data = me_response.json()
            error_message = error_data.get('error', {}).get('message', 'Token invalide')
            return jsonify({'error': f'Token Facebook invalide: {error_message}'}), 400
        
        user_data = me_response.json()
        user_name = user_data.get('name', 'Utilisateur')
        
        # Check permissions
        permissions_url = f"https://graph.facebook.com/v18.0/me/permissions"
        permissions_params = {'access_token': access_token}
        
        permissions_response = requests.get(permissions_url, params=permissions_params)
        permissions_data = permissions_response.json() if permissions_response.status_code == 200 else {'data': []}
        granted_permissions = [p['permission'] for p in permissions_data.get('data', []) if p.get('status') == 'granted']
        
        # Check if user has pages_manage_posts permission
        if 'pages_manage_posts' not in granted_permissions and 'pages_show_list' not in granted_permissions:
            return jsonify({
                'error': 'Permissions insuffisantes',
                'message': f'Bonjour {user_name}, votre token n\'a pas les permissions nécessaires pour gérer les pages.',
                'required_permissions': ['pages_manage_posts', 'pages_show_list'],
                'current_permissions': granted_permissions,
                'solution': 'Veuillez générer un nouveau token avec les permissions pages_manage_posts et pages_show_list dans l\'Explorateur d\'API Graph Facebook.'
            }), 400
        
        # Get ALL pages managed by the user with pagination
        all_pages = []
        pages_url = f"https://graph.facebook.com/v18.0/me/accounts"
        params = {
            'access_token': access_token,
            'fields': 'id,name,category,fan_count,access_token,picture',
            'limit': 100  # Maximum limit per request
        }
        
        # Pagination loop to get all pages
        while pages_url:
            response = requests.get(pages_url, params=params)
            
            if response.status_code != 200:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Erreur API Facebook')
                return jsonify({'error': f'Erreur Facebook API: {error_message}'}), 400
            
            data = response.json()
            current_pages = data.get('data', [])
            all_pages.extend(current_pages)
            
            # Check if there are more pages to fetch
            paging = data.get('paging', {})
            pages_url = paging.get('next')  # URL for next page of results
            params = {}  # Clear params for next URL as it contains all needed parameters
        
        pages = all_pages
        
        if len(pages) == 0:
            return jsonify({
                'error': 'Aucune page trouvée',
                'message': f'Bonjour {user_name}, aucune page Facebook n\'a été trouvée sur votre compte.',
                'debug_info': {
                    'user_id': user_data.get('id'),
                    'user_name': user_name,
                    'permissions': granted_permissions,
                    'api_response': data
                },
                'solution': 'Vérifiez que vous êtes administrateur de pages Facebook ou créez une page de test.'
            }), 200
        
        # Format pages data for frontend
        formatted_pages = []
        for page in pages:
            # Get recent posts count (optional)
            posts_count = 0
            last_post_time = 'Aucune publication'
            try:
                posts_url = f"https://graph.facebook.com/v18.0/{page['id']}/posts"
                posts_params = {
                    'access_token': page.get('access_token', access_token),
                    'limit': 5,
                    'fields': 'created_time,message'
                }
                posts_response = requests.get(posts_url, params=posts_params)
                if posts_response.status_code == 200:
                    posts_data = posts_response.json()
                    posts_list = posts_data.get('data', [])
                    posts_count = len(posts_list)
                    if posts_list:
                        from datetime import datetime
                        last_post = posts_list[0].get('created_time', '')
                        if last_post:
                            # Convert to readable format
                            last_post_time = 'Récemment'
            except:
                pass
            
            formatted_page = {
                'id': page['id'],
                'name': page['name'],
                'category': page.get('category', 'Page'),
                'fan_count': page.get('fan_count', 0),
                'access_token': page.get('access_token', ''),
                'picture': page.get('picture', {}).get('data', {}).get('url', ''),
                'posts_count': posts_count,
                'status': 'Connectée',
                'last_post': last_post_time
            }
            formatted_pages.append(formatted_page)
        
        # Save pages to a simple JSON file for persistence
        pages_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'facebook_pages.json')
        os.makedirs(os.path.dirname(pages_file), exist_ok=True)
        
        with open(pages_file, 'w') as f:
            json.dump(formatted_pages, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'{len(formatted_pages)} pages synchronisées avec succès pour {user_name}',
            'pages': formatted_pages,
            'user_info': {
                'name': user_name,
                'id': user_data.get('id'),
                'permissions': granted_permissions
            }
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erreur de connexion à Facebook: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la synchronisation: {str(e)}'}), 500

@app.route('/api/facebook/pages', methods=['GET'])
def get_facebook_pages():
    """Get stored Facebook pages"""
    try:
        pages_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'facebook_pages.json')
        
        if os.path.exists(pages_file):
            with open(pages_file, 'r') as f:
                pages = json.load(f)
            return jsonify({'pages': pages})
        else:
            # Return sample data if no real pages synced yet
            sample_pages = [
                {
                    'id': 'sample_1',
                    'name': 'Bois Malin Paris',
                    'category': 'Business',
                    'fan_count': 2340,
                    'status': 'Connectée',
                    'last_post': 'Il y a 2h',
                    'posts_count': 156
                },
                {
                    'id': 'sample_2', 
                    'name': 'Bois Malin Lyon',
                    'category': 'Business',
                    'fan_count': 1890,
                    'status': 'Connectée',
                    'last_post': 'Il y a 4h',
                    'posts_count': 98
                },
                {
                    'id': 'sample_3',
                    'name': 'Bois Malin Marseille', 
                    'category': 'Business',
                    'fan_count': 1567,
                    'status': 'Connectée',
                    'last_post': 'Hier',
                    'posts_count': 67
                }
            ]
            return jsonify({'pages': sample_pages})
            
    except Exception as e:
        return jsonify({'error': f'Erreur lors du chargement des pages: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

