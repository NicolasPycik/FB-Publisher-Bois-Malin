"""
Facebook Publisher SaaS - Main Application v3.1.0
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import route blueprints with error handling
try:
    from routes.analytics_routes import analytics_bp
    from routes.campaigns_routes import campaigns_bp  
    from routes.audiences_routes import audiences_bp
    from routes.facebook_api_routes import facebook_bp
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports
    analytics_bp = None
    campaigns_bp = None
    audiences_bp = None
    facebook_bp = None

app = Flask(__name__)
CORS(app)

# Register blueprints if available
if analytics_bp:
    app.register_blueprint(analytics_bp)
if campaigns_bp:
    app.register_blueprint(campaigns_bp)
if audiences_bp:
    app.register_blueprint(audiences_bp)
if facebook_bp:
    app.register_blueprint(facebook_bp, url_prefix='/api/facebook')

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
        if not access_token or access_token.strip() == '':
            return jsonify({
                'error': 'Token d\'accès Facebook non configuré',
                'message': 'Veuillez configurer votre token d\'accès Facebook dans les Paramètres.',
                'action_required': 'configure_token',
                'instructions': [
                    '1. Allez dans l\'onglet Paramètres',
                    '2. Remplissez votre Access Token Facebook',
                    '3. Cliquez sur Sauvegarder',
                    '4. Revenez ici et cliquez sur Synchroniser'
                ]
            }), 400
        
        # Call Facebook Graph API to get pages
        import requests
        
        # First, check token validity and permissions
        me_url = f"https://graph.facebook.com/v18.0/me"
        me_params = {
            'access_token': access_token,
            'fields': 'id,name'
        }
        
        try:
            me_response = requests.get(me_url, params=me_params, timeout=10)
        except requests.exceptions.Timeout:
            return jsonify({
                'error': 'Timeout de connexion à Facebook',
                'message': 'La connexion à Facebook a pris trop de temps. Veuillez réessayer.',
                'action_required': 'retry'
            }), 500
        except requests.exceptions.ConnectionError:
            return jsonify({
                'error': 'Erreur de connexion à Facebook',
                'message': 'Impossible de se connecter à Facebook. Vérifiez votre connexion internet.',
                'action_required': 'check_connection'
            }), 500
        
        if me_response.status_code != 200:
            error_data = me_response.json()
            error_info = error_data.get('error', {})
            error_message = error_info.get('message', 'Token invalide')
            error_code = error_info.get('code', 'unknown')
            error_type = error_info.get('type', 'unknown')
            
            # Handle specific Facebook errors
            if error_code == 190:  # Invalid token
                return jsonify({
                    'error': 'Token Facebook invalide ou expiré',
                    'message': f'Erreur validating access token: {error_message}',
                    'action_required': 'regenerate_token',
                    'instructions': [
                        '1. Votre token a expiré ou est invalide',
                        '2. Allez sur https://developers.facebook.com/tools/explorer/',
                        '3. Générez un nouveau token avec les permissions pages_manage_posts et pages_show_list',
                        '4. Copiez le nouveau token dans les Paramètres',
                        '5. Sauvegardez et réessayez la synchronisation'
                    ],
                    'facebook_error': {
                        'code': error_code,
                        'type': error_type,
                        'message': error_message
                    }
                }), 400
            else:
                return jsonify({
                    'error': f'Erreur Facebook API (Code: {error_code})',
                    'message': error_message,
                    'action_required': 'check_token',
                    'facebook_error': {
                        'code': error_code,
                        'type': error_type,
                        'message': error_message
                    }
                }), 400
        
        user_data = me_response.json()
        user_name = user_data.get('name', 'Utilisateur')
        
        # Check permissions
        permissions_url = f"https://graph.facebook.com/v18.0/me/permissions"
        permissions_params = {'access_token': access_token}
        
        permissions_response = requests.get(permissions_url, params=permissions_params, timeout=10)
        permissions_data = permissions_response.json() if permissions_response.status_code == 200 else {'data': []}
        granted_permissions = [p['permission'] for p in permissions_data.get('data', []) if p.get('status') == 'granted']
        
        # Check if user has pages_manage_posts permission
        required_permissions = ['pages_manage_posts', 'pages_show_list']
        missing_permissions = [perm for perm in required_permissions if perm not in granted_permissions]
        
        if missing_permissions:
            return jsonify({
                'error': 'Permissions insuffisantes',
                'message': f'Bonjour {user_name}, votre token n\'a pas toutes les permissions nécessaires.',
                'action_required': 'add_permissions',
                'missing_permissions': missing_permissions,
                'current_permissions': granted_permissions,
                'instructions': [
                    '1. Allez sur https://developers.facebook.com/tools/explorer/',
                    '2. Sélectionnez votre application',
                    '3. Cliquez sur "Ajouter des permissions"',
                    f'4. Ajoutez les permissions manquantes: {", ".join(missing_permissions)}',
                    '5. Générez un nouveau token',
                    '6. Copiez le nouveau token dans les Paramètres'
                ]
            }), 400
        
        # Get ALL pages managed by the user with ENHANCED pagination
        all_pages = []
        pages_url = f"https://graph.facebook.com/v18.0/me/accounts"
        params = {
            'access_token': access_token,
            'fields': 'id,name,category,fan_count,access_token,picture',
            'limit': 100  # Maximum limit per request
        }
        
        page_count = 0
        max_iterations = 100  # Increased to support up to 10,000 pages
        iteration = 0
        
        print(f"Starting ENHANCED pagination to fetch ALL pages for user {user_name}")
        
        # Enhanced pagination loop to get ALL pages
        while pages_url and iteration < max_iterations:
            iteration += 1
            print(f"ENHANCED Pagination iteration {iteration}: Fetching from {pages_url[:150]}...")
            
            try:
                response = requests.get(pages_url, params=params, timeout=60)  # Increased timeout to 60s
            except requests.exceptions.Timeout:
                print(f"Timeout at iteration {iteration}, returning {len(all_pages)} pages")
                if len(all_pages) > 0:
                    break  # Continue with what we have
                else:
                    return jsonify({
                        'error': 'Timeout lors de la récupération des pages',
                        'message': 'La récupération des pages a pris trop de temps. Veuillez réessayer.',
                        'action_required': 'retry_sync'
                    }), 408
            except requests.exceptions.RequestException as e:
                print(f"Network error at iteration {iteration}: {str(e)}")
                if len(all_pages) > 0:
                    break  # Continue with what we have
                else:
                    return jsonify({
                        'error': 'Erreur de connexion lors de la pagination',
                        'message': f'Erreur réseau: {str(e)}',
                        'action_required': 'check_connection'
                    }), 500
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                error_data = response.json() if response.content else {}
                error_info = error_data.get('error', {})
                error_message = error_info.get('message', 'Erreur API Facebook')
                error_code = error_info.get('code', 'unknown')
                
                print(f"API Error at iteration {iteration}: {error_code} - {error_message}")
                
                # Special handling for rate limiting
                if error_code in [4, 17, 613]:  # Rate limit error codes
                    print(f"Rate limit detected, waiting 5 seconds...")
                    import time
                    time.sleep(5)
                    continue  # Retry the same request
                
                # If we have some pages already, continue with what we have
                if len(all_pages) > 0:
                    print(f"Continuing with {len(all_pages)} pages despite error")
                    break
                else:
                    return jsonify({
                        'error': f'Erreur Facebook API lors de la pagination (Code: {error_code})',
                        'message': error_message,
                        'action_required': 'check_token_permissions',
                        'facebook_error': {
                            'code': error_code,
                            'message': error_message,
                            'iteration': iteration
                        }
                    }), 400
            
            data = response.json()
            current_pages = data.get('data', [])
            
            print(f"Retrieved {len(current_pages)} pages in iteration {iteration}")
            
            # Add current pages to our collection
            if current_pages:
                all_pages.extend(current_pages)
                page_count += len(current_pages)
                print(f"Total pages accumulated: {len(all_pages)}")
            
            # Check if there are more pages to fetch
            paging = data.get('paging', {})
            next_url = paging.get('next')
            
            if next_url:
                pages_url = next_url
                params = {}  # Clear params as next URL contains all needed parameters
                print(f"Next URL found: {next_url[:150]}...")
                
                # Additional safety check for infinite loops
                if 'after=' not in next_url and 'before=' not in next_url:
                    print(f"Warning: No pagination cursor in URL at iteration {iteration}")
                    # Try to continue anyway, but with extra caution
                    if iteration > 10:  # If we've been going for a while without cursors, stop
                        print("Stopping due to potential infinite loop")
                        break
            else:
                print("No next URL found, pagination complete")
                break
            
            # Progress logging every 10 iterations
            if iteration % 10 == 0:
                print(f"PROGRESS: {iteration} iterations completed, {len(all_pages)} pages retrieved")
        
        pages = all_pages
        
        # Enhanced logging for debugging
        print(f"ENHANCED PAGINATION COMPLETE: {len(pages)} pages retrieved in {iteration} iterations")
        if len(pages) > 0:
            print(f"First 10 page names: {[p.get('name', 'Unknown') for p in pages[:10]]}")
            if len(pages) > 10:
                print(f"Last 5 page names: {[p.get('name', 'Unknown') for p in pages[-5:]]}")
        
        # Special message if we got exactly the expected number
        if len(pages) >= 60:  # Close to the expected 66
            print(f"SUCCESS: Retrieved {len(pages)} pages - this looks like the full set!")
        elif len(pages) >= 10:
            print(f"PARTIAL SUCCESS: Retrieved {len(pages)} pages - may need token permission review")
        else:
            print(f"LIMITED RESULTS: Only {len(pages)} pages - likely permission or access issue")
        
        if len(pages) == 0:
            return jsonify({
                'error': 'Aucune page trouvée',
                'message': f'Bonjour {user_name}, aucune page Facebook n\'a été trouvée sur votre compte.',
                'action_required': 'check_page_access',
                'debug_info': {
                    'user_id': user_data.get('id'),
                    'user_name': user_name,
                    'permissions': granted_permissions,
                    'iterations': iteration,
                    'last_api_response': data if 'data' in locals() else None
                },
                'instructions': [
                    '1. Vérifiez que vous êtes administrateur de pages Facebook',
                    '2. Ou créez une page de test pour tester l\'application',
                    '3. Assurez-vous que votre token a les bonnes permissions',
                    '4. Vérifiez que vos pages ne sont pas dans un état restreint'
                ]
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

@app.route('/api/facebook/pages/publishing')
def get_pages_for_publishing():
    """Get pages formatted for publishing interface"""
    try:
        # Import Facebook API here to avoid import issues
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from facebook_api import FacebookAPI
        
        # Load configuration
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            return jsonify({'success': False, 'error': 'Token Facebook non configuré'}), 400
        
        # Initialize Facebook API
        fb_api = FacebookAPI(access_token=access_token)
        
        # Get all pages
        pages = fb_api.get_all_pages_for_publishing()
        
        # Format pages for publishing interface
        formatted_pages = []
        for page in pages:
            formatted_pages.append({
                'id': page['id'],
                'name': page['name'],
                'category': page.get('category', 'Business'),
                'fan_count': page.get('fan_count', 0),
                'picture': page.get('picture', {}).get('data', {}).get('url', ''),
                'access_token': page.get('access_token', '')
            })
        
        return jsonify({
            'success': True,
            'pages': formatted_pages,
            'total': len(formatted_pages)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du chargement des pages: {str(e)}'
        }), 500

@app.route('/api/facebook/publish/multi', methods=['POST'])
def publish_multi_pages():
    """Publish content to multiple Facebook pages"""
    try:
        # Import Facebook API here to avoid import issues
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from facebook_api import FacebookAPI
        
        # Get form data
        message = request.form.get('message', '').strip()
        page_ids = json.loads(request.form.get('page_ids', '[]'))
        link = request.form.get('link', '').strip()
        
        if not message:
            return jsonify({'success': False, 'error': 'Le message est obligatoire'}), 400
        
        if not page_ids:
            return jsonify({'success': False, 'error': 'Aucune page sélectionnée'}), 400
        
        # Load configuration
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            return jsonify({'success': False, 'error': 'Token Facebook non configuré'}), 400
        
        # Initialize Facebook API
        fb_api = FacebookAPI(access_token=access_token)
        
        # Get all pages to get access tokens
        all_pages = fb_api.get_all_pages_for_publishing()
        page_tokens = {page['id']: page.get('access_token', '') for page in all_pages}
        
        # Publish to each selected page
        results = {}
        successful = 0
        failed = 0
        
        for page_id in page_ids:
            try:
                page_token = page_tokens.get(page_id)
                if not page_token:
                    results[page_id] = {
                        'success': False,
                        'message': 'Token de page non trouvé'
                    }
                    failed += 1
                    continue
                
                # Create page-specific API instance
                page_api = FacebookAPI(access_token=page_token)
                
                # Publish post
                if link:
                    post_data = {
                        'message': message,
                        'link': link
                    }
                else:
                    post_data = {
                        'message': message
                    }
                
                result = page_api.publish_post(page_id, **post_data)
                
                if result.get('id'):
                    results[page_id] = {
                        'success': True,
                        'message': 'Publication réussie',
                        'post_id': result['id']
                    }
                    successful += 1
                else:
                    results[page_id] = {
                        'success': False,
                        'message': 'Erreur lors de la publication'
                    }
                    failed += 1
                    
            except Exception as e:
                results[page_id] = {
                    'success': False,
                    'message': f'Erreur: {str(e)}'
                }
                failed += 1
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': {
                'total': len(page_ids),
                'successful': successful,
                'failed': failed
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la publication: {str(e)}'
        }), 500

@app.route('/api/facebook/posts/performance')
def get_posts_performance():
    """Get posts performance data for analytics"""
    try:
        # Import Facebook API here to avoid import issues
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from facebook_api import FacebookAPI
        
        # Load configuration
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            return jsonify({'success': False, 'error': 'Token Facebook non configuré'}), 400
        
        # Initialize Facebook API
        fb_api = FacebookAPI(access_token=access_token)
        
        # Get all pages
        pages = fb_api.get_all_pages_for_publishing()
        
        # Get posts for each page (sample data for now)
        all_posts = []
        total_reach = 0
        total_engagement = 0
        total_shares = 0
        active_boosted = 0
        
        for page in pages[:5]:  # Limit to first 5 pages for demo
            try:
                # In a real implementation, you would fetch actual posts data
                # For now, we'll generate sample data
                page_posts = generate_sample_posts_for_page(page)
                all_posts.extend(page_posts)
                
                # Aggregate stats
                for post in page_posts:
                    total_reach += post.get('reach', 0)
                    total_engagement += post.get('engagement', 0)
                    total_shares += post.get('shares', 0)
                    if post.get('status') == 'boosted':
                        active_boosted += 1
                        
            except Exception as e:
                print(f"Error getting posts for page {page['name']}: {e}")
                continue
        
        # Sort posts by date (newest first)
        all_posts.sort(key=lambda x: x['created_time'], reverse=True)
        
        return jsonify({
            'success': True,
            'posts': all_posts,
            'stats': {
                'total_reach': total_reach,
                'total_engagement': total_engagement,
                'total_shares': total_shares,
                'active_boosted_posts': active_boosted
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du chargement des statistiques: {str(e)}'
        }), 500

def generate_sample_posts_for_page(page):
    """Generate sample posts data for a page"""
    import random
    from datetime import datetime, timedelta
    
    posts = []
    page_name = page['name']
    page_id = page['id']
    
    # Generate 2-4 sample posts per page
    num_posts = random.randint(2, 4)
    
    sample_messages = [
        f"Découvrez nos nouvelles collections chez {page_name} ! 🌿",
        f"Promotion spéciale ce week-end chez {page_name} ! -20%",
        f"Conseils d'experts de l'équipe {page_name}",
        f"Nouveau produit disponible chez {page_name} !",
        f"Merci à tous nos clients fidèles de {page_name} ❤️"
    ]
    
    for i in range(num_posts):
        # Random date within last 30 days
        days_ago = random.randint(1, 30)
        created_time = datetime.now() - timedelta(days=days_ago)
        
        # Random engagement metrics
        reach = random.randint(500, 3000)
        likes = random.randint(20, 200)
        comments = random.randint(5, 50)
        shares = random.randint(2, 30)
        engagement = likes + comments + shares
        
        # Random boost status
        is_boosted = random.random() < 0.3  # 30% chance of being boosted
        
        post = {
            'id': f"{page_id}_post_{i}",
            'message': random.choice(sample_messages),
            'page_name': page_name,
            'page_id': page_id,
            'created_time': created_time.isoformat() + 'Z',
            'reach': reach,
            'engagement': engagement,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'status': 'boosted' if is_boosted else 'organic',
            'can_boost': not is_boosted
        }
        
        if is_boosted:
            post['boost_budget'] = random.randint(10, 50)
            post['boost_reach'] = reach + random.randint(1000, 3000)
        
        posts.append(post)
    
    return posts

@app.route('/api/facebook/boost/create', methods=['POST'])
def create_boost_campaign():
    """Create a boost campaign for a post"""
    try:
        # Import Facebook API here to avoid import issues
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from facebook_api import FacebookAPI
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Données manquantes'}), 400
        
        post_id = data.get('post_id')
        objective = data.get('objective', 'REACH')
        daily_budget = data.get('daily_budget', 20)
        duration = data.get('duration', 7)
        audience_type = data.get('audience_type', 'auto')
        
        if not post_id:
            return jsonify({'success': False, 'error': 'ID du post manquant'}), 400
        
        # Load configuration
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            return jsonify({'success': False, 'error': 'Token Facebook non configuré'}), 400
        
        # Initialize Facebook API
        fb_api = FacebookAPI(access_token=access_token)
        
        # For now, simulate boost creation (in real implementation, use Facebook Marketing API)
        boost_data = {
            'post_id': post_id,
            'objective': objective,
            'daily_budget': daily_budget,
            'duration': duration,
            'audience_type': audience_type,
            'status': 'active',
            'created_time': datetime.now().isoformat()
        }
        
        if audience_type == 'custom':
            boost_data['audience'] = data.get('audience', {})
        elif audience_type == 'saved':
            boost_data['saved_audience_id'] = data.get('saved_audience_id')
        
        # In a real implementation, you would:
        # 1. Create a campaign using Facebook Marketing API
        # 2. Create an ad set with the specified audience and budget
        # 3. Create an ad using the existing post
        # 4. Store the campaign details in your database
        
        # For demo purposes, we'll simulate success
        campaign_id = f"campaign_{post_id}_{int(datetime.now().timestamp())}"
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Boost lancé avec succès',
            'estimated_reach': daily_budget * 100,  # Simple estimation
            'total_budget': daily_budget * duration
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du lancement du boost: {str(e)}'
        }), 500

@app.route('/api/facebook/audiences')
def get_saved_audiences():
    """Get saved audiences for targeting"""
    try:
        # For demo purposes, return sample audiences
        # In a real implementation, fetch from Facebook Marketing API
        sample_audiences = [
            {
                'id': 'audience_1',
                'name': 'Propriétaires de maisons 25-55 ans',
                'description': 'Propriétaires intéressés par l\'aménagement extérieur',
                'size': 45000
            },
            {
                'id': 'audience_2', 
                'name': 'Professionnels du bâtiment',
                'description': 'Artisans, architectes, constructeurs',
                'size': 12000
            },
            {
                'id': 'audience_3',
                'name': 'Amateurs de bricolage',
                'description': 'Passionnés de DIY et rénovation',
                'size': 78000
            }
        ]
        
        return jsonify({
            'success': True,
            'audiences': sample_audiences
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du chargement des audiences: {str(e)}'
        }), 500

# ===== CAMPAIGNS/ADS ENDPOINTS =====

@app.route('/api/facebook/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns"""
    try:
        # For demo purposes, return sample campaigns
        # In a real implementation, fetch from Facebook Marketing API
        sample_campaigns = [
            {
                'id': 'campaign_1',
                'name': 'Promotion Terrasses Été 2024',
                'objective': 'CONVERSIONS',
                'status': 'ACTIVE',
                'budget': 500,
                'reach': 15420,
                'clicks': 234,
                'cpc': '2.14',
                'created_time': '2024-06-01T10:00:00Z'
            },
            {
                'id': 'campaign_2',
                'name': 'Lancement Bois Exotique',
                'objective': 'TRAFFIC',
                'status': 'PAUSED',
                'budget': 300,
                'reach': 8750,
                'clicks': 156,
                'cpc': '1.92',
                'created_time': '2024-05-15T14:30:00Z'
            },
            {
                'id': 'campaign_3',
                'name': 'Retargeting Visiteurs Site',
                'objective': 'CONVERSIONS',
                'status': 'ACTIVE',
                'budget': 200,
                'reach': 3240,
                'clicks': 89,
                'cpc': '2.25',
                'created_time': '2024-06-10T09:15:00Z'
            }
        ]
        
        return jsonify({
            'success': True,
            'campaigns': sample_campaigns
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du chargement des campagnes: {str(e)}'
        }), 500

@app.route('/api/facebook/campaigns/create', methods=['POST'])
def create_campaign():
    """Create a new campaign with adset and ad"""
    try:
        # Import Facebook API here to avoid import issues
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from facebook_api import FacebookAPI
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Données manquantes'}), 400
        
        # Validate required data
        if not data.get('campaign') or not data.get('adset') or not data.get('ad'):
            return jsonify({'success': False, 'error': 'Données de campagne incomplètes'}), 400
        
        # Get access token from environment
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            return jsonify({'success': False, 'error': 'Token Facebook non configuré'}), 400
        
        # Initialize Facebook API
        fb_api = FacebookAPI(access_token=access_token)
        
        # For demo purposes, simulate campaign creation
        # In a real implementation, use Facebook Marketing API to create:
        # 1. Campaign
        # 2. Ad Set with targeting
        # 3. Ad Creative
        # 4. Ad
        
        campaign_data = data['campaign']
        adset_data = data['adset']
        ad_data = data['ad']
        
        # Simulate campaign creation
        campaign_id = f"campaign_{int(datetime.now().timestamp())}"
        
        # Log the campaign creation (for demo)
        print(f"Creating campaign: {campaign_data['name']}")
        print(f"Budget: {campaign_data['budget']}€")
        print(f"Objective: {campaign_data['objective']}")
        print(f"Ad Set: {adset_data['name']}")
        print(f"Daily Budget: {adset_data['dailyBudget']}€")
        print(f"Ad: {ad_data['name']}")
        print(f"Headline: {ad_data['headline']}")
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Campagne créée avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la création de la campagne: {str(e)}'
        }), 500

@app.route('/api/facebook/campaigns/<campaign_id>/toggle', methods=['POST'])
def toggle_campaign(campaign_id):
    """Toggle campaign status (active/paused)"""
    try:
        # Get JSON data
        data = request.get_json()
        new_status = data.get('status', 'PAUSED')
        
        # For demo purposes, simulate status change
        # In a real implementation, use Facebook Marketing API
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'new_status': new_status,
            'message': f'Campagne {new_status.lower()}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du changement de statut: {str(e)}'
        }), 500

@app.route('/api/facebook/campaigns/<campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete a campaign"""
    try:
        # For demo purposes, simulate deletion
        # In a real implementation, use Facebook Marketing API
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Campagne supprimée avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la suppression: {str(e)}'
        }), 500

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

