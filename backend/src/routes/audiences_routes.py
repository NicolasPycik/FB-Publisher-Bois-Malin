"""
Audiences CRUD Routes for Facebook Publisher SaaS v3.1.0
Complete audience management system with JSON storage and Facebook API integration
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os
import uuid

audiences_bp = Blueprint('audiences', __name__)

# Path to audiences storage file
AUDIENCES_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'audiences.json')

def get_facebook_token():
    """Get Facebook access token from environment"""
    return os.getenv('FACEBOOK_ACCESS_TOKEN')

def load_audiences():
    """Load audiences from JSON file"""
    try:
        if os.path.exists(AUDIENCES_FILE):
            with open(AUDIENCES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading audiences: {str(e)}")
        return []

def save_audiences(audiences):
    """Save audiences to JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(AUDIENCES_FILE), exist_ok=True)
        
        with open(AUDIENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(audiences, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving audiences: {str(e)}")
        return False

def calculate_audience_size(targeting, audience_type='custom'):
    """Calculate estimated audience size based on targeting"""
    base_size = 1000000  # Base population for France
    
    if audience_type == 'lookalike':
        return 28000
    
    # Apply demographic filters
    if 'age_min' in targeting and 'age_max' in targeting:
        age_range = targeting['age_max'] - targeting['age_min']
        age_factor = min(age_range / 40, 1.0)  # Max factor for 40+ year range
        base_size *= age_factor
    
    # Apply gender filter
    if 'gender' in targeting and targeting['gender'] != 'all':
        base_size *= 0.5
    
    # Apply location filter
    if 'location' in targeting:
        location_factors = {
            'FR': 1.0,
            'BE': 0.17,
            'CH': 0.13,
            'CA': 0.56
        }
        base_size *= location_factors.get(targeting['location'], 0.1)
    
    # Apply interests filter
    if 'interests' in targeting and targeting['interests']:
        interest_count = len(targeting['interests'])
        interest_factor = max(0.1, 1.0 - (interest_count * 0.15))
        base_size *= interest_factor
    
    return max(1000, int(base_size))

def generate_audience_recommendations(targeting, estimated_size):
    """Generate recommendations for audience optimization"""
    recommendations = []
    
    if estimated_size < 10000:
        recommendations.append({
            'type': 'warning',
            'message': 'Audience trop petite (< 10k). Élargissez les critères.',
            'suggestion': 'Augmentez la tranche d\'âge ou réduisez les centres d\'intérêt'
        })
    
    if estimated_size > 500000:
        recommendations.append({
            'type': 'info',
            'message': 'Audience très large. Affinez pour de meilleurs résultats.',
            'suggestion': 'Ajoutez des centres d\'intérêt spécifiques ou réduisez la zone géographique'
        })
    
    if 'interests' in targeting and len(targeting.get('interests', [])) > 5:
        recommendations.append({
            'type': 'tip',
            'message': 'Trop de centres d\'intérêt peuvent réduire la portée.',
            'suggestion': 'Limitez à 3-5 centres d\'intérêt principaux'
        })
    
    if not recommendations:
        recommendations.append({
            'type': 'success',
            'message': 'Taille d\'audience optimale pour de bons résultats.',
            'suggestion': 'Cette audience devrait bien performer'
        })
    
    return recommendations

@audiences_bp.route('/api/facebook/audiences', methods=['GET'])
def get_audiences():
    """Get all saved audiences"""
    try:
        audiences = load_audiences()
        
        # If no audiences exist, create sample ones
        if not audiences:
            sample_audiences = [
                {
                    'id': 'audience_sample_1',
                    'name': 'Propriétaires 25-55 ans',
                    'description': 'Propriétaires de maison intéressés par l\'aménagement extérieur',
                    'type': 'custom',
                    'targeting': {
                        'location': 'FR',
                        'age_min': 25,
                        'age_max': 55,
                        'gender': 'all',
                        'interests': ['Bricolage', 'Jardinage', 'Aménagement extérieur']
                    },
                    'size': 45000,
                    'created_date': '2025-06-20T10:00:00Z',
                    'last_used': '2025-06-23T14:30:00Z'
                },
                {
                    'id': 'audience_sample_2',
                    'name': 'Bricoleurs passionnés',
                    'description': 'Personnes très actives dans le bricolage et la rénovation',
                    'type': 'custom',
                    'targeting': {
                        'location': 'FR',
                        'age_min': 30,
                        'age_max': 60,
                        'gender': 'all',
                        'interests': ['Bricolage', 'Rénovation', 'Outillage', 'Menuiserie']
                    },
                    'size': 32000,
                    'created_date': '2025-06-21T15:20:00Z',
                    'last_used': '2025-06-24T09:15:00Z'
                },
                {
                    'id': 'audience_sample_3',
                    'name': 'Audience similaire clients',
                    'description': 'Audience similaire basée sur les meilleurs clients',
                    'type': 'lookalike',
                    'targeting': {
                        'location': 'FR',
                        'source_audience': 'customers_list',
                        'similarity': 1
                    },
                    'size': 28000,
                    'created_date': '2025-06-22T11:45:00Z',
                    'last_used': '2025-06-24T16:20:00Z'
                }
            ]
            
            save_audiences(sample_audiences)
            audiences = sample_audiences
        
        return jsonify({
            'success': True,
            'audiences': audiences,
            'total': len(audiences)
        })
        
    except Exception as e:
        print(f"Error getting audiences: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la récupération des audiences: {str(e)}'
        }), 500

@audiences_bp.route('/api/facebook/audiences', methods=['POST'])
def create_audience():
    """Create a new audience"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'type', 'targeting']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        # Validate targeting data
        targeting = data['targeting']
        if data['type'] == 'custom':
            required_targeting = ['location', 'age_min', 'age_max']
            for field in required_targeting:
                if field not in targeting:
                    return jsonify({
                        'success': False,
                        'error': f'Champ de ciblage manquant: {field}'
                    }), 400
        
        # Generate unique ID
        audience_id = f"audience_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate audience size
        estimated_size = calculate_audience_size(targeting, data['type'])
        
        # Create audience object
        new_audience = {
            'id': audience_id,
            'name': data['name'],
            'description': data['description'],
            'type': data['type'],
            'targeting': targeting,
            'size': estimated_size,
            'created_date': datetime.now().isoformat() + 'Z',
            'last_used': None,
            'facebook_audience_id': None  # Will be set when created on Facebook
        }
        
        # Load existing audiences and add new one
        audiences = load_audiences()
        audiences.append(new_audience)
        
        # Save to file
        if not save_audiences(audiences):
            return jsonify({
                'success': False,
                'error': 'Erreur lors de la sauvegarde'
            }), 500
        
        # Try to create on Facebook (optional)
        access_token = get_facebook_token()
        if access_token:
            try:
                import sys
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
                from facebook_api import FacebookAPI
                
                fb_api = FacebookAPI(access_token)
                
                # Get ad account ID (you might want to make this configurable)
                ad_account_id = '123456789'  # Replace with actual ad account ID
                
                fb_result = fb_api.create_saved_audience(
                    ad_account_id=ad_account_id,
                    name=data['name'],
                    targeting_dict=targeting
                )
                
                if fb_result.get('success'):
                    new_audience['facebook_audience_id'] = fb_result.get('audience_id')
                    save_audiences(audiences)
                
            except Exception as fb_error:
                print(f"Facebook API error (non-critical): {str(fb_error)}")
        
        return jsonify({
            'success': True,
            'audience': new_audience,
            'message': f'Audience "{data["name"]}" créée avec succès'
        })
        
    except Exception as e:
        print(f"Error creating audience: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la création: {str(e)}'
        }), 500

@audiences_bp.route('/api/facebook/audiences/<audience_id>', methods=['GET'])
def get_audience(audience_id):
    """Get a specific audience by ID"""
    try:
        audiences = load_audiences()
        
        audience = next((a for a in audiences if a['id'] == audience_id), None)
        
        if not audience:
            return jsonify({
                'success': False,
                'error': 'Audience non trouvée'
            }), 404
        
        return jsonify({
            'success': True,
            'audience': audience
        })
        
    except Exception as e:
        print(f"Error getting audience: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la récupération: {str(e)}'
        }), 500

@audiences_bp.route('/api/facebook/audiences/<audience_id>', methods=['PUT'])
def update_audience(audience_id):
    """Update an existing audience"""
    try:
        data = request.get_json()
        audiences = load_audiences()
        
        audience_index = next((i for i, a in enumerate(audiences) if a['id'] == audience_id), None)
        
        if audience_index is None:
            return jsonify({
                'success': False,
                'error': 'Audience non trouvée'
            }), 404
        
        # Update audience data
        audience = audiences[audience_index]
        
        if 'name' in data:
            audience['name'] = data['name']
        if 'description' in data:
            audience['description'] = data['description']
        if 'targeting' in data:
            audience['targeting'] = data['targeting']
            # Recalculate size if targeting changed
            audience['size'] = calculate_audience_size(data['targeting'], audience['type'])
        
        audience['updated_date'] = datetime.now().isoformat() + 'Z'
        
        # Save changes
        if not save_audiences(audiences):
            return jsonify({
                'success': False,
                'error': 'Erreur lors de la sauvegarde'
            }), 500
        
        return jsonify({
            'success': True,
            'audience': audience,
            'message': f'Audience "{audience["name"]}" mise à jour avec succès'
        })
        
    except Exception as e:
        print(f"Error updating audience: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la mise à jour: {str(e)}'
        }), 500

@audiences_bp.route('/api/facebook/audiences/<audience_id>', methods=['DELETE'])
def delete_audience(audience_id):
    """Delete an audience"""
    try:
        audiences = load_audiences()
        
        audience_index = next((i for i, a in enumerate(audiences) if a['id'] == audience_id), None)
        
        if audience_index is None:
            return jsonify({
                'success': False,
                'error': 'Audience non trouvée'
            }), 404
        
        # Remove audience
        deleted_audience = audiences.pop(audience_index)
        
        # Save changes
        if not save_audiences(audiences):
            return jsonify({
                'success': False,
                'error': 'Erreur lors de la sauvegarde'
            }), 500
        
        return jsonify({
            'success': True,
            'message': f'Audience "{deleted_audience["name"]}" supprimée avec succès'
        })
        
    except Exception as e:
        print(f"Error deleting audience: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la suppression: {str(e)}'
        }), 500

@audiences_bp.route('/api/facebook/audiences/<audience_id>/duplicate', methods=['POST'])
def duplicate_audience(audience_id):
    """Duplicate an existing audience"""
    try:
        audiences = load_audiences()
        
        original_audience = next((a for a in audiences if a['id'] == audience_id), None)
        
        if not original_audience:
            return jsonify({
                'success': False,
                'error': 'Audience originale non trouvée'
            }), 404
        
        # Create duplicate
        new_audience_id = f"audience_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        duplicate_audience = {
            'id': new_audience_id,
            'name': f"{original_audience['name']} (Copie)",
            'description': f"Copie de: {original_audience['description']}",
            'type': original_audience['type'],
            'targeting': original_audience['targeting'].copy(),
            'size': original_audience['size'],
            'created_date': datetime.now().isoformat() + 'Z',
            'last_used': None,
            'facebook_audience_id': None
        }
        
        audiences.append(duplicate_audience)
        
        # Save changes
        if not save_audiences(audiences):
            return jsonify({
                'success': False,
                'error': 'Erreur lors de la sauvegarde'
            }), 500
        
        return jsonify({
            'success': True,
            'audience': duplicate_audience,
            'message': f'Audience dupliquée avec succès'
        })
        
    except Exception as e:
        print(f"Error duplicating audience: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la duplication: {str(e)}'
        }), 500

@audiences_bp.route('/api/facebook/audiences/estimate', methods=['POST'])
def estimate_audience_size():
    """Estimate audience size for given targeting"""
    try:
        data = request.get_json()
        
        if 'targeting' not in data:
            return jsonify({
                'success': False,
                'error': 'Données de ciblage manquantes'
            }), 400
        
        targeting = data['targeting']
        audience_type = data.get('type', 'custom')
        
        # Calculate size
        estimated_size = calculate_audience_size(targeting, audience_type)
        
        # Generate recommendations
        recommendations = generate_audience_recommendations(targeting, estimated_size)
        
        # Calculate cost estimates
        cost_per_thousand = 15  # Base CPM in euros
        daily_budget_suggestion = max(10, min(50, estimated_size // 1000))
        
        estimate = {
            'size': estimated_size,
            'reach_potential': 'Élevé' if estimated_size > 50000 else 'Moyen' if estimated_size > 10000 else 'Faible',
            'recommendations': recommendations,
            'cost_estimate': {
                'cpm': cost_per_thousand,
                'suggested_daily_budget': daily_budget_suggestion,
                'estimated_daily_reach': min(estimated_size, daily_budget_suggestion * 1000 // cost_per_thousand)
            }
        }
        
        return jsonify({
            'success': True,
            'estimate': estimate
        })
        
    except Exception as e:
        print(f"Error estimating audience: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de l\'estimation: {str(e)}'
        }), 500

@audiences_bp.route('/api/facebook/audiences/interests/search', methods=['GET'])
def search_interests():
    """Search for interests to use in targeting"""
    try:
        query = request.args.get('q', '').strip()
        
        if len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Requête trop courte (minimum 2 caractères)'
            }), 400
        
        # Sample interests database (in real implementation, this would query Facebook API)
        all_interests = [
            {'id': 'bricolage', 'name': 'Bricolage', 'category': 'Hobbies'},
            {'id': 'jardinage', 'name': 'Jardinage', 'category': 'Hobbies'},
            {'id': 'amenagement_exterieur', 'name': 'Aménagement extérieur', 'category': 'Home & Garden'},
            {'id': 'terrasse', 'name': 'Terrasse', 'category': 'Home & Garden'},
            {'id': 'cloture', 'name': 'Clôture', 'category': 'Home & Garden'},
            {'id': 'bois', 'name': 'Bois', 'category': 'Materials'},
            {'id': 'composite', 'name': 'Composite', 'category': 'Materials'},
            {'id': 'renovation', 'name': 'Rénovation', 'category': 'Home Improvement'},
            {'id': 'menuiserie', 'name': 'Menuiserie', 'category': 'Crafts'},
            {'id': 'outillage', 'name': 'Outillage', 'category': 'Tools'},
            {'id': 'decoration_exterieure', 'name': 'Décoration extérieure', 'category': 'Home & Garden'},
            {'id': 'piscine', 'name': 'Piscine', 'category': 'Home & Garden'},
            {'id': 'barbecue', 'name': 'Barbecue', 'category': 'Outdoor Living'},
            {'id': 'mobilier_jardin', 'name': 'Mobilier de jardin', 'category': 'Furniture'},
            {'id': 'pergola', 'name': 'Pergola', 'category': 'Home & Garden'}
        ]
        
        # Filter interests based on query
        matching_interests = [
            interest for interest in all_interests
            if query.lower() in interest['name'].lower() or query.lower() in interest['id'].lower()
        ]
        
        return jsonify({
            'success': True,
            'interests': matching_interests[:10],  # Limit to 10 results
            'query': query
        })
        
    except Exception as e:
        print(f"Error searching interests: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la recherche: {str(e)}'
        }), 500

