"""
Facebook API Routes for SaaS Platform

This module provides REST API endpoints for Facebook operations
including page management, post publishing, and advertising campaigns.
"""

from flask import Blueprint, request, jsonify, current_app
import json
import os
from datetime import datetime
from facebook_api import FacebookAPI, FacebookAPIError

facebook_bp = Blueprint('facebook', __name__)

# Initialize Facebook API
fb_api = None

def get_facebook_api():
    """Get or initialize Facebook API instance"""
    global fb_api
    if fb_api is None:
        try:
            fb_api = FacebookAPI()
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Facebook API: {e}")
            return None
    return fb_api

@facebook_bp.route('/pages', methods=['GET'])
def get_pages():
    """Get user's Facebook pages"""
    try:
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        pages = api.get_user_pages()
        return jsonify({
            'success': True,
            'pages': pages
        })
    except FacebookAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting pages: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/pages/<page_id>/posts', methods=['POST'])
def publish_post(page_id):
    """Publish a post to a Facebook page"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        # Extract post data
        message = data.get('message', '')
        link = data.get('link')
        image_path = data.get('image_path')
        
        # Publish the post
        result = api.publish_post(
            page_id=page_id,
            message=message,
            link=link,
            image_path=image_path
        )
        
        return jsonify({
            'success': True,
            'post_id': result.get('id'),
            'message': 'Post published successfully'
        })
        
    except FacebookAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error publishing post: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/pages/bulk-post', methods=['POST'])
def bulk_publish():
    """Publish a post to multiple Facebook pages"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        page_ids = data.get('page_ids', [])
        message = data.get('message', '')
        link = data.get('link')
        image_path = data.get('image_path')
        
        if not page_ids:
            return jsonify({'error': 'No pages selected'}), 400
        
        results = []
        errors = []
        
        for page_id in page_ids:
            try:
                result = api.publish_post(
                    page_id=page_id,
                    message=message,
                    link=link,
                    image_path=image_path
                )
                results.append({
                    'page_id': page_id,
                    'post_id': result.get('id'),
                    'success': True
                })
            except Exception as e:
                errors.append({
                    'page_id': page_id,
                    'error': str(e)
                })
        
        return jsonify({
            'success': len(errors) == 0,
            'results': results,
            'errors': errors,
            'total_pages': len(page_ids),
            'successful_posts': len(results),
            'failed_posts': len(errors)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in bulk publish: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/pages/<page_id>/insights', methods=['GET'])
def get_page_insights(page_id):
    """Get insights for a Facebook page"""
    try:
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        # Get query parameters
        period = request.args.get('period', 'day')
        since = request.args.get('since')
        until = request.args.get('until')
        
        insights = api.get_page_insights(
            page_id=page_id,
            period=period,
            since=since,
            until=until
        )
        
        return jsonify({
            'success': True,
            'insights': insights
        })
        
    except FacebookAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting insights: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/pages/<page_id>/posts', methods=['GET'])
def get_page_posts(page_id):
    """Get recent posts for a Facebook page"""
    try:
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        limit = request.args.get('limit', 10, type=int)
        posts = api.get_recent_posts(page_id=page_id, limit=limit)
        
        return jsonify({
            'success': True,
            'posts': posts
        })
        
    except FacebookAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting posts: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/ad-accounts', methods=['GET'])
def get_ad_accounts():
    """Get user's Facebook ad accounts"""
    try:
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        ad_accounts = api.get_ad_accounts()
        return jsonify({
            'success': True,
            'ad_accounts': ad_accounts
        })
        
    except FacebookAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error getting ad accounts: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/campaigns', methods=['POST'])
def create_campaign():
    """Create a Facebook advertising campaign"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        # Extract campaign data
        ad_account_id = data.get('ad_account_id')
        name = data.get('name')
        objective = data.get('objective', 'REACH')
        status = data.get('status', 'PAUSED')
        
        if not ad_account_id or not name:
            return jsonify({'error': 'Missing required fields'}), 400
        
        campaign = api.create_campaign(
            ad_account_id=ad_account_id,
            name=name,
            objective=objective,
            status=status
        )
        
        return jsonify({
            'success': True,
            'campaign': campaign
        })
        
    except FacebookAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating campaign: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/posts/<post_id>/boost', methods=['POST'])
def boost_post(post_id):
    """Boost a Facebook post"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        api = get_facebook_api()
        if not api:
            return jsonify({'error': 'Facebook API not configured'}), 500
        
        ad_account_id = data.get('ad_account_id')
        budget = data.get('budget', 20)  # Default 20€
        
        if not ad_account_id:
            return jsonify({'error': 'Ad account ID required'}), 400
        
        result = api.create_boosted_post_ad(
            ad_account_id=ad_account_id,
            post_id=post_id,
            budget=budget
        )
        
        return jsonify({
            'success': True,
            'boost_result': result
        })
        
    except FacebookAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error boosting post: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@facebook_bp.route('/config', methods=['GET'])
def get_config():
    """Get Facebook API configuration status"""
    try:
        api = get_facebook_api()
        if not api:
            return jsonify({
                'configured': False,
                'error': 'Facebook API not configured'
            })
        
        # Test API connection
        try:
            api.get_user_pages()
            return jsonify({
                'configured': True,
                'status': 'connected'
            })
        except:
            return jsonify({
                'configured': False,
                'error': 'Invalid credentials or connection failed'
            })
            
    except Exception as e:
        return jsonify({
            'configured': False,
            'error': str(e)
        })

@facebook_bp.route('/config', methods=['POST'])
def update_config():
    """Update Facebook API configuration"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        app_id = data.get('app_id')
        app_secret = data.get('app_secret')
        access_token = data.get('access_token')
        
        if not all([app_id, app_secret, access_token]):
            return jsonify({'error': 'Missing required credentials'}), 400
        
        # Update environment variables
        os.environ['FACEBOOK_APP_ID'] = app_id
        os.environ['FACEBOOK_APP_SECRET'] = app_secret
        os.environ['FACEBOOK_ACCESS_TOKEN'] = access_token
        
        # Reinitialize API
        global fb_api
        fb_api = None
        api = get_facebook_api()
        
        if api:
            return jsonify({
                'success': True,
                'message': 'Configuration updated successfully'
            })
        else:
            return jsonify({'error': 'Failed to initialize API with new credentials'}), 400
            
    except Exception as e:
        current_app.logger.error(f"Error updating config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

