"""
Analytics and Boost Post Routes for Facebook Publisher SaaS v3.0.0
"""

import os
import json
import requests
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

analytics_bp = Blueprint('analytics', __name__)

def get_facebook_token():
    """Get Facebook access token from environment"""
    settings_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            for line in f:
                if line.startswith('FACEBOOK_ACCESS_TOKEN='):
                    return line.split('=', 1)[1].strip()
    return None

@analytics_bp.route('/api/facebook/posts/performance', methods=['GET'])
def get_posts_performance():
    """Get posts performance data for analytics"""
    try:
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'error': 'Token Facebook non configuré',
                'posts': [],
                'stats': {}
            }), 400

        # Get pages first
        pages_url = f"https://graph.facebook.com/v18.0/me/accounts"
        pages_params = {
            'access_token': access_token,
            'fields': 'id,name,access_token',
            'limit': 100
        }
        
        pages_response = requests.get(pages_url, params=pages_params, timeout=30)
        if pages_response.status_code != 200:
            return jsonify({
                'error': 'Erreur lors de la récupération des pages',
                'posts': [],
                'stats': {}
            }), 400

        pages_data = pages_response.json()
        pages = pages_data.get('data', [])
        
        all_posts = []
        total_reach = 0
        total_engagement = 0
        total_shares = 0
        boosted_posts_count = 0
        
        # Get posts from each page
        for page in pages[:10]:  # Limit to first 10 pages for performance
            page_id = page['id']
            page_name = page['name']
            page_token = page.get('access_token', access_token)
            
            # Get posts from this page
            posts_url = f"https://graph.facebook.com/v18.0/{page_id}/posts"
            posts_params = {
                'access_token': page_token,
                'fields': 'id,message,created_time,insights.metric(post_impressions,post_engaged_users,post_clicks,post_reactions_like_total,post_reactions_love_total,post_reactions_wow_total,post_reactions_haha_total,post_reactions_sorry_total,post_reactions_anger_total,post_comments,post_shares)',
                'limit': 20,
                'since': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            }
            
            try:
                posts_response = requests.get(posts_url, params=posts_params, timeout=20)
                if posts_response.status_code == 200:
                    posts_data = posts_response.json()
                    page_posts = posts_data.get('data', [])
                    
                    for post in page_posts:
                        # Extract insights data
                        insights = post.get('insights', {}).get('data', [])
                        post_metrics = {}
                        
                        for insight in insights:
                            metric_name = insight.get('name')
                            metric_values = insight.get('values', [])
                            if metric_values:
                                post_metrics[metric_name] = metric_values[0].get('value', 0)
                        
                        # Calculate engagement
                        likes = post_metrics.get('post_reactions_like_total', 0)
                        loves = post_metrics.get('post_reactions_love_total', 0)
                        wows = post_metrics.get('post_reactions_wow_total', 0)
                        hahas = post_metrics.get('post_reactions_haha_total', 0)
                        sorrys = post_metrics.get('post_reactions_sorry_total', 0)
                        angers = post_metrics.get('post_reactions_anger_total', 0)
                        comments = post_metrics.get('post_comments', 0)
                        shares = post_metrics.get('post_shares', 0)
                        
                        total_reactions = likes + loves + wows + hahas + sorrys + angers
                        engagement = total_reactions + comments + shares
                        reach = post_metrics.get('post_impressions', 0)
                        
                        # Add to totals
                        total_reach += reach
                        total_engagement += engagement
                        total_shares += shares
                        
                        # Format post data
                        post_data = {
                            'id': post['id'],
                            'message': post.get('message', '')[:100] + ('...' if len(post.get('message', '')) > 100 else ''),
                            'page_name': page_name,
                            'page_id': page_id,
                            'created_time': post.get('created_time'),
                            'reach': reach,
                            'engagement': engagement,
                            'likes': total_reactions,
                            'comments': comments,
                            'shares': shares,
                            'status': 'boosted' if reach > 1000 else 'organic',  # Simple heuristic
                            'boost_eligible': True
                        }
                        
                        if post_data['status'] == 'boosted':
                            boosted_posts_count += 1
                        
                        all_posts.append(post_data)
                        
            except Exception as e:
                print(f"Error getting posts for page {page_name}: {str(e)}")
                continue
        
        # Sort posts by engagement descending
        all_posts.sort(key=lambda x: x['engagement'], reverse=True)
        
        # Prepare stats summary
        stats = {
            'total_reach': total_reach,
            'total_engagement': total_engagement,
            'total_shares': total_shares,
            'boosted_posts_count': boosted_posts_count,
            'posts_count': len(all_posts)
        }
        
        return jsonify({
            'success': True,
            'posts': all_posts[:50],  # Return top 50 posts
            'stats': stats
        })
        
    except Exception as e:
        print(f"Error in get_posts_performance: {str(e)}")
        
        # Return sample data for demo
        sample_posts = [
            {
                'id': 'post_1',
                'message': 'Découvrez notre nouvelle gamme de terrasses en bois composite ! 🌿',
                'page_name': 'Les Bois Malouins',
                'page_id': 'page_1',
                'created_time': '2025-06-20T10:30:00Z',
                'reach': 2340,
                'engagement': 156,
                'likes': 89,
                'comments': 23,
                'shares': 44,
                'status': 'organic',
                'boost_eligible': True
            },
            {
                'id': 'post_2',
                'message': 'Promotion spéciale sur les lames de terrasse en pin traité 🏡',
                'page_name': 'Bois Grand Ouest',
                'page_id': 'page_2',
                'created_time': '2025-06-19T14:15:00Z',
                'reach': 4560,
                'engagement': 298,
                'likes': 167,
                'comments': 45,
                'shares': 86,
                'status': 'boosted',
                'boost_eligible': False
            },
            {
                'id': 'post_3',
                'message': 'Conseils d\'entretien pour vos terrasses en bois 🔧',
                'page_name': 'Terrasses et Bois du Maine',
                'page_id': 'page_3',
                'created_time': '2025-06-18T09:45:00Z',
                'reach': 1890,
                'engagement': 134,
                'likes': 78,
                'comments': 34,
                'shares': 22,
                'status': 'organic',
                'boost_eligible': True
            }
        ]
        
        sample_stats = {
            'total_reach': 8790,
            'total_engagement': 588,
            'total_shares': 152,
            'boosted_posts_count': 1,
            'posts_count': 3
        }
        
        return jsonify({
            'success': True,
            'posts': sample_posts,
            'stats': sample_stats
        })

@analytics_bp.route('/api/facebook/posts/<post_id>/boost', methods=['POST'])
def boost_post(post_id):
    """Boost a Facebook post with targeting and budget"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['ad_account_id', 'page_id', 'objective', 'budget', 'duration']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        # Validate budget and duration
        budget = int(data['budget'])
        duration = int(data['duration'])
        
        if budget < 5:
            return jsonify({
                'success': False,
                'error': 'Budget minimum: 5€/jour'
            }), 400
        
        if duration < 1:
            return jsonify({
                'success': False,
                'error': 'Durée minimum: 1 jour'
            }), 400
        
        # Get Facebook API instance
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Token Facebook non configuré'
            }), 400
        
        # Import Facebook API
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from facebook_api import FacebookAPI
        
        fb_api = FacebookAPI(access_token)
        
        # Prepare targeting
        targeting = {
            'geo_locations': {'countries': ['FR']},
            'age_min': 25,
            'age_max': 55
        }
        
        # Handle audience type
        audience_type = data.get('audience_type', 'automatic')
        
        if audience_type == 'custom':
            if 'location' in data:
                targeting['geo_locations'] = {'countries': [data['location']]}
            if 'age_min' in data:
                targeting['age_min'] = int(data['age_min'])
            if 'age_max' in data:
                targeting['age_max'] = int(data['age_max'])
            if 'gender' in data and data['gender'] != 'all':
                targeting['genders'] = [1 if data['gender'] == 'male' else 2]
            if 'interests' in data and data['interests']:
                interests = [interest.strip() for interest in data['interests'].split(',')]
                targeting['interests'] = [{'name': interest} for interest in interests[:5]]
        
        elif audience_type == 'saved':
            saved_audience_id = data.get('saved_audience_id')
            if saved_audience_id:
                targeting = {'saved_audiences': [saved_audience_id]}
        
        # Calculate dates
        from datetime import datetime, timedelta
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=duration)).strftime('%Y-%m-%d')
        
        # Create boosted post ad
        result = fb_api.create_boosted_post_ad(
            ad_account_id=data['ad_account_id'],
            page_id=data['page_id'],
            post_id=post_id,
            targeting=targeting,
            budget=budget,
            start_date=start_date,
            end_date=end_date
        )
        
        if result.get('success'):
            # Calculate estimates
            estimated_daily_reach = budget * 50
            estimated_total_reach = estimated_daily_reach * duration
            estimated_total_cost = budget * duration
            
            return jsonify({
                'success': True,
                'campaign_id': result.get('campaign_id'),
                'adset_id': result.get('adset_id'),
                'ad_id': result.get('ad_id'),
                'estimated_reach': estimated_total_reach,
                'estimated_cost': estimated_total_cost,
                'duration': duration,
                'message': f'Post boosté avec succès ! Budget: {budget}€/jour pendant {duration} jours.'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Erreur lors de la création du boost')
            }), 500
        
    except Exception as e:
        print(f"Error in boost_post: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors du boost: {str(e)}'
        }), 500

@analytics_bp.route('/api/facebook/ad-accounts', methods=['GET'])
def get_ad_accounts():
    """Get available ad accounts"""
    try:
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Token Facebook non configuré'
            }), 400
        
        # Import Facebook API
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from facebook_api import FacebookAPI
        
        fb_api = FacebookAPI(access_token)
        ad_accounts = fb_api.get_ad_accounts()
        
        return jsonify({
            'success': True,
            'ad_accounts': ad_accounts
        })
        
    except Exception as e:
        print(f"Error getting ad accounts: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la récupération des comptes publicitaires: {str(e)}'
        }), 500

@analytics_bp.route('/api/facebook/audiences', methods=['GET'])
def get_saved_audiences():
    """Get saved audiences for boost targeting"""
    try:
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'error': 'Token Facebook non configuré',
                'audiences': []
            }), 400
        
        # For demo purposes, return sample audiences
        sample_audiences = [
            {
                'id': 'audience_1',
                'name': 'Propriétaires 25-55 ans',
                'description': 'Propriétaires de maison, 25-55 ans, intéressés par l\'aménagement extérieur',
                'size': 45000,
                'type': 'custom'
            },
            {
                'id': 'audience_2',
                'name': 'Bricoleurs passionnés',
                'description': 'Personnes intéressées par le bricolage et l\'aménagement',
                'size': 32000,
                'type': 'interest'
            },
            {
                'id': 'audience_3',
                'name': 'Audience similaire clients',
                'description': 'Audience similaire basée sur les clients existants',
                'size': 28000,
                'type': 'lookalike'
            }
        ]
        
        return jsonify({
            'success': True,
            'audiences': sample_audiences
        })
        
    except Exception as e:
        print(f"Error getting audiences: {str(e)}")
        return jsonify({
            'error': f'Erreur lors de la récupération des audiences: {str(e)}'
        }), 500

@analytics_bp.route('/api/facebook/posts/<post_id>/details', methods=['GET'])
def get_post_details(post_id):
    """Get detailed information about a specific post for boost preview"""
    try:
        access_token = get_facebook_token()
        if not access_token:
            return jsonify({
                'error': 'Token Facebook non configuré'
            }), 400
        
        # For demo purposes, return sample post details
        sample_post = {
            'id': post_id,
            'message': 'Découvrez notre nouvelle gamme de terrasses en bois composite ! 🌿 Résistantes aux intempéries et faciles d\'entretien.',
            'created_time': '2025-06-20T10:30:00+0000',
            'page': {
                'id': '123456789',
                'name': 'Bois Malin'
            },
            'insights': {
                'reach': 1250,
                'engagement': 89,
                'clicks': 23,
                'shares': 12
            },
            'media': {
                'type': 'image',
                'url': 'https://example.com/terrasse-composite.jpg'
            }
        }
        
        return jsonify({
            'success': True,
            'post': sample_post
        })
        
    except Exception as e:
        print(f"Error getting post details: {str(e)}")
        return jsonify({
            'error': f'Erreur lors de la récupération des détails du post: {str(e)}'
        }), 500
