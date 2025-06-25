"""
Campaigns and Ads Routes for Facebook Publisher SaaS v3.1.0
Handles complete ad creation workflow with 4-step wizard
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
import os

campaigns_bp = Blueprint('campaigns', __name__)

def get_facebook_token():
    """Get Facebook access token from environment"""
    return os.getenv('FACEBOOK_ACCESS_TOKEN')

def get_facebook_app_id():
    """Get Facebook app ID from environment"""
    return os.getenv('FACEBOOK_APP_ID')

@campaigns_bp.route('/api/facebook/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns"""
    try:
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Token Facebook non configuré'
            }), 400
        
        # Sample campaigns for demo
        sample_campaigns = [
            {
                'id': 'campaign_1',
                'name': 'Promotion Terrasses Été 2025',
                'objective': 'REACH',
                'status': 'ACTIVE',
                'budget': 500,
                'spent': 245.50,
                'reach': 12500,
                'impressions': 18750,
                'clicks': 234,
                'created_time': '2025-06-15T10:00:00+0000',
                'start_time': '2025-06-15T00:00:00+0000',
                'end_time': '2025-07-15T23:59:59+0000'
            },
            {
                'id': 'campaign_2',
                'name': 'Lancement Clôtures Composite',
                'objective': 'TRAFFIC',
                'status': 'ACTIVE',
                'budget': 300,
                'spent': 89.25,
                'reach': 8900,
                'impressions': 13400,
                'clicks': 156,
                'created_time': '2025-06-20T14:30:00+0000',
                'start_time': '2025-06-20T00:00:00+0000',
                'end_time': '2025-07-20T23:59:59+0000'
            }
        ]
        
        return jsonify({
            'success': True,
            'campaigns': sample_campaigns
        })
        
    except Exception as e:
        print(f"Error getting campaigns: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la récupération des campagnes: {str(e)}'
        }), 500

@campaigns_bp.route('/api/facebook/campaigns/create', methods=['POST'])
def create_complete_campaign():
    """Create a complete campaign with adset and ad (4-step wizard)"""
    try:
        data = request.get_json()
        
        # Validate required data structure
        required_sections = ['campaign', 'adset', 'ad']
        for section in required_sections:
            if section not in data:
                return jsonify({
                    'success': False,
                    'error': f'Section manquante: {section}'
                }), 400
        
        # Validate campaign data
        campaign_data = data['campaign']
        required_campaign_fields = ['name', 'objective', 'budget']
        for field in required_campaign_fields:
            if field not in campaign_data:
                return jsonify({
                    'success': False,
                    'error': f'Champ campagne manquant: {field}'
                }), 400
        
        # Validate adset data
        adset_data = data['adset']
        required_adset_fields = ['name', 'dailyBudget', 'startDate', 'audienceType']
        for field in required_adset_fields:
            if field not in adset_data:
                return jsonify({
                    'success': False,
                    'error': f'Champ adset manquant: {field}'
                }), 400
        
        # Validate ad data
        ad_data = data['ad']
        required_ad_fields = ['name', 'format', 'pageId']
        for field in required_ad_fields:
            if field not in ad_data:
                return jsonify({
                    'success': False,
                    'error': f'Champ publicité manquant: {field}'
                }), 400
        
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Token Facebook non configuré'
            }), 400
        
        # Import Facebook API
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from facebook_api import FacebookAPI
        
        fb_api = FacebookAPI(access_token)
        
        # Get ad account ID from request or use default
        ad_account_id = data.get('adAccountId', '123456789')
        
        # Step 1: Create Campaign
        campaign_result = fb_api.create_campaign(
            ad_account_id=ad_account_id,
            name=campaign_data['name'],
            objective=campaign_data['objective']
        )
        
        if not campaign_result.get('success'):
            return jsonify({
                'success': False,
                'error': f'Erreur création campagne: {campaign_result.get("error")}'
            }), 500
        
        campaign_id = campaign_result['campaign_id']
        
        # Step 2: Prepare targeting based on audience type
        targeting = {}
        
        if adset_data['audienceType'] == 'automatic':
            targeting = {
                'geo_locations': {'countries': ['FR']},
                'age_min': 25,
                'age_max': 55
            }
        elif adset_data['audienceType'] == 'custom':
            targeting = {
                'geo_locations': {'countries': [adset_data.get('location', 'FR')]},
                'age_min': adset_data.get('ageMin', 25),
                'age_max': adset_data.get('ageMax', 55)
            }
            
            if adset_data.get('gender') and adset_data['gender'] != 'all':
                targeting['genders'] = [1 if adset_data['gender'] == 'male' else 2]
            
            if adset_data.get('interests'):
                interests = [interest.strip() for interest in adset_data['interests'].split(',')]
                targeting['interests'] = [{'name': interest} for interest in interests[:5]]
        
        elif adset_data['audienceType'] == 'saved':
            targeting = {'saved_audiences': [adset_data.get('savedAudienceId')]}
        
        # Step 3: Create AdSet
        adset_result = fb_api.create_adset(
            ad_account_id=ad_account_id,
            campaign_id=campaign_id,
            name=adset_data['name'],
            daily_budget=int(adset_data['dailyBudget']) * 100,  # Convert to cents
            start_date=adset_data['startDate'],
            end_date=adset_data.get('endDate', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            targeting=targeting
        )
        
        if not adset_result.get('success'):
            return jsonify({
                'success': False,
                'error': f'Erreur création adset: {adset_result.get("error")}'
            }), 500
        
        adset_id = adset_result['adset_id']
        
        # Step 4: Create Ad Creative
        creative_result = fb_api.create_ad_creative(
            ad_account_id=ad_account_id,
            name=f"Creative {ad_data['name']}",
            page_id=ad_data['pageId'],
            message=ad_data.get('headline', '') + ' ' + ad_data.get('text', ''),
            link=ad_data.get('link')
        )
        
        if not creative_result.get('success'):
            return jsonify({
                'success': False,
                'error': f'Erreur création creative: {creative_result.get("error")}'
            }), 500
        
        creative_id = creative_result['creative_id']
        
        # Step 5: Create Ad
        ad_result = fb_api.create_ad(
            ad_account_id=ad_account_id,
            name=ad_data['name'],
            adset_id=adset_id,
            creative_id=creative_id
        )
        
        if not ad_result.get('success'):
            return jsonify({
                'success': False,
                'error': f'Erreur création publicité: {ad_result.get("error")}'
            }), 500
        
        ad_id = ad_result['ad_id']
        
        # Calculate estimates
        daily_budget = int(adset_data['dailyBudget'])
        estimated_daily_reach = daily_budget * 40
        estimated_daily_clicks = daily_budget * 2
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'adset_id': adset_id,
            'creative_id': creative_id,
            'ad_id': ad_id,
            'estimates': {
                'daily_reach': estimated_daily_reach,
                'daily_clicks': estimated_daily_clicks,
                'cost_per_click': round(daily_budget / max(estimated_daily_clicks, 1), 2)
            },
            'message': f'Campagne "{campaign_data["name"]}" créée avec succès !'
        })
        
    except Exception as e:
        print(f"Error creating campaign: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la création: {str(e)}'
        }), 500

@campaigns_bp.route('/api/facebook/campaign-objectives', methods=['GET'])
def get_campaign_objectives():
    """Get available campaign objectives"""
    try:
        objectives = [
            {
                'id': 'REACH',
                'name': 'Portée',
                'description': 'Montrer votre publicité au maximum de personnes',
                'best_for': 'Notoriété de marque'
            },
            {
                'id': 'TRAFFIC',
                'name': 'Trafic',
                'description': 'Diriger les gens vers votre site web',
                'best_for': 'Visites du site web'
            },
            {
                'id': 'ENGAGEMENT',
                'name': 'Engagement',
                'description': 'Obtenir plus de likes, commentaires et partages',
                'best_for': 'Interaction avec les publications'
            },
            {
                'id': 'LEAD_GENERATION',
                'name': 'Génération de prospects',
                'description': 'Collecter des informations de contact',
                'best_for': 'Formulaires de contact'
            },
            {
                'id': 'CONVERSIONS',
                'name': 'Conversions',
                'description': 'Encourager les actions sur votre site',
                'best_for': 'Ventes et inscriptions'
            },
            {
                'id': 'MESSAGES',
                'name': 'Messages',
                'description': 'Inciter les gens à vous envoyer des messages',
                'best_for': 'Service client'
            }
        ]
        
        return jsonify({
            'success': True,
            'objectives': objectives
        })
        
    except Exception as e:
        print(f"Error getting objectives: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la récupération des objectifs: {str(e)}'
        }), 500

@campaigns_bp.route('/api/facebook/ad-formats', methods=['GET'])
def get_ad_formats():
    """Get available ad formats"""
    try:
        formats = [
            {
                'id': 'single_image',
                'name': 'Image unique',
                'description': 'Une seule image avec du texte',
                'specs': {
                    'image_ratio': '1.91:1 ou 1:1',
                    'text_limit': 125,
                    'headline_limit': 40
                }
            },
            {
                'id': 'single_video',
                'name': 'Vidéo unique',
                'description': 'Une seule vidéo avec du texte',
                'specs': {
                    'video_ratio': '16:9 ou 1:1',
                    'duration': '15-240 secondes',
                    'text_limit': 125
                }
            },
            {
                'id': 'carousel',
                'name': 'Carrousel',
                'description': 'Plusieurs images ou vidéos défilantes',
                'specs': {
                    'cards': '2-10 cartes',
                    'image_ratio': '1:1',
                    'text_limit': 125
                }
            },
            {
                'id': 'collection',
                'name': 'Collection',
                'description': 'Image principale + produits en grille',
                'specs': {
                    'main_image': '1.91:1',
                    'product_images': '1:1',
                    'products': '4+ produits'
                }
            }
        ]
        
        return jsonify({
            'success': True,
            'formats': formats
        })
        
    except Exception as e:
        print(f"Error getting ad formats: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la récupération des formats: {str(e)}'
        }), 500

@campaigns_bp.route('/api/facebook/campaigns/<campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    """Update an existing campaign"""
    try:
        data = request.get_json()
        
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Token Facebook non configuré'
            }), 400
        
        # For demo purposes, simulate update
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Campagne mise à jour avec succès'
        })
        
    except Exception as e:
        print(f"Error updating campaign: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la mise à jour: {str(e)}'
        }), 500

@campaigns_bp.route('/api/facebook/campaigns/<campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete a campaign"""
    try:
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Token Facebook non configuré'
            }), 400
        
        # For demo purposes, simulate deletion
        return jsonify({
            'success': True,
            'message': 'Campagne supprimée avec succès'
        })
        
    except Exception as e:
        print(f"Error deleting campaign: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la suppression: {str(e)}'
        }), 500

@campaigns_bp.route('/api/facebook/campaigns/<campaign_id>/performance', methods=['GET'])
def get_campaign_performance(campaign_id):
    """Get detailed performance metrics for a campaign"""
    try:
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Token Facebook non configuré'
            }), 400
        
        # Sample performance data
        performance = {
            'campaign_id': campaign_id,
            'metrics': {
                'impressions': 18750,
                'reach': 12500,
                'clicks': 234,
                'ctr': 1.25,
                'cpc': 1.05,
                'cpm': 13.07,
                'spent': 245.50,
                'conversions': 12,
                'cost_per_conversion': 20.46
            },
            'daily_breakdown': [
                {'date': '2025-06-20', 'impressions': 2500, 'clicks': 31, 'spent': 32.55},
                {'date': '2025-06-21', 'impressions': 2800, 'clicks': 35, 'spent': 36.75},
                {'date': '2025-06-22', 'impressions': 3100, 'clicks': 42, 'spent': 44.10},
                {'date': '2025-06-23', 'impressions': 2900, 'clicks': 38, 'spent': 39.90},
                {'date': '2025-06-24', 'impressions': 3200, 'clicks': 45, 'spent': 47.25}
            ]
        }
        
        return jsonify({
            'success': True,
            'performance': performance
        })
        
    except Exception as e:
        print(f"Error getting campaign performance: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la récupération des performances: {str(e)}'
        }), 500

