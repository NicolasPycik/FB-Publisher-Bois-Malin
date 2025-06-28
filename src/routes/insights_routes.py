"""
Routes Flask pour les statistiques et insights Facebook
Version 4.0.0 - Nouvelles fonctionnalités
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Ajouter le répertoire parent au path pour importer facebook_api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from facebook_api import FacebookAPI

# Créer le blueprint pour les insights
insights_bp = Blueprint('insights', __name__, url_prefix='/api/insights')

# Instance de l'API Facebook (sera initialisée dans main.py)
api = None

def init_insights_api(facebook_api_instance):
    """Initialiser l'instance API pour ce module"""
    global api
    api = facebook_api_instance

@insights_bp.route('/ad/<ad_id>', methods=['GET'])
def ad_insights(ad_id):
    """
    Récupérer les statistiques d'une publicité spécifique
    
    Paramètres URL:
    - ad_id: ID de la publicité
    
    Paramètres query optionnels:
    - date_preset: last_7d, last_30d, lifetime (défaut: lifetime)
    - fields: champs spécifiques à récupérer
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        date_preset = request.args.get('date_preset', 'lifetime')
        
        insights = api.get_insights(ad_id, level="ad", date_preset=date_preset)
        
        return jsonify({
            "success": True,
            "ad_id": ad_id,
            "date_preset": date_preset,
            "insights": insights
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des insights: {str(e)}"}), 500

@insights_bp.route('/page/<page_id>', methods=['GET'])
def page_insights(page_id):
    """
    Récupérer les statistiques d'une page Facebook
    
    Paramètres URL:
    - page_id: ID de la page Facebook
    
    Paramètres query optionnels:
    - date_preset: last_7d, last_30d, lifetime (défaut: last_7d)
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        date_preset = request.args.get('date_preset', 'last_7d')
        
        insights = api.get_insights(page_id, level="page", date_preset=date_preset)
        
        return jsonify({
            "success": True,
            "page_id": page_id,
            "date_preset": date_preset,
            "insights": insights
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des insights: {str(e)}"}), 500

@insights_bp.route('/campaign/<campaign_id>', methods=['GET'])
def campaign_insights(campaign_id):
    """
    Récupérer les statistiques d'une campagne publicitaire
    
    Paramètres URL:
    - campaign_id: ID de la campagne
    
    Paramètres query optionnels:
    - date_preset: last_7d, last_30d, lifetime (défaut: last_30d)
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        date_preset = request.args.get('date_preset', 'last_30d')
        
        insights = api.get_insights(campaign_id, level="campaign", date_preset=date_preset)
        
        return jsonify({
            "success": True,
            "campaign_id": campaign_id,
            "date_preset": date_preset,
            "insights": insights
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des insights: {str(e)}"}), 500

@insights_bp.route('/adset/<adset_id>', methods=['GET'])
def adset_insights(adset_id):
    """
    Récupérer les statistiques d'un ad set
    
    Paramètres URL:
    - adset_id: ID de l'ad set
    
    Paramètres query optionnels:
    - date_preset: last_7d, last_30d, lifetime (défaut: last_30d)
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        date_preset = request.args.get('date_preset', 'last_30d')
        
        insights = api.get_insights(adset_id, level="adset", date_preset=date_preset)
        
        return jsonify({
            "success": True,
            "adset_id": adset_id,
            "date_preset": date_preset,
            "insights": insights
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des insights: {str(e)}"}), 500

@insights_bp.route('/account/<account_id>/summary', methods=['GET'])
def account_summary(account_id):
    """
    Récupérer un résumé des statistiques pour un compte publicitaire
    
    Paramètres URL:
    - account_id: ID du compte publicitaire
    
    Paramètres query optionnels:
    - date_preset: last_7d, last_30d, lifetime (défaut: last_30d)
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        date_preset = request.args.get('date_preset', 'last_30d')
        
        # Récupérer les insights au niveau du compte
        insights = api.get_insights(f"act_{account_id}", level="account", date_preset=date_preset)
        
        return jsonify({
            "success": True,
            "account_id": account_id,
            "date_preset": date_preset,
            "summary": insights
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération du résumé: {str(e)}"}), 500

@insights_bp.route('/pages/batch', methods=['POST'])
def pages_batch_insights():
    """
    Récupérer les statistiques pour plusieurs pages en une fois
    
    Payload attendu:
    {
        "page_ids": ["page1", "page2", "page3"],
        "date_preset": "last_7d"  // optionnel
    }
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        data = request.get_json()
        
        if 'page_ids' not in data:
            return jsonify({"error": "page_ids requis"}), 400
            
        page_ids = data['page_ids']
        date_preset = data.get('date_preset', 'last_7d')
        
        results = {}
        
        for page_id in page_ids:
            try:
                insights = api.get_insights(page_id, level="page", date_preset=date_preset)
                results[page_id] = {
                    "success": True,
                    "insights": insights
                }
            except Exception as e:
                results[page_id] = {
                    "success": False,
                    "error": str(e)
                }
        
        return jsonify({
            "success": True,
            "date_preset": date_preset,
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération batch: {str(e)}"}), 500

@insights_bp.route('/ads/batch', methods=['POST'])
def ads_batch_insights():
    """
    Récupérer les statistiques pour plusieurs publicités en une fois
    
    Payload attendu:
    {
        "ad_ids": ["ad1", "ad2", "ad3"],
        "date_preset": "last_30d"  // optionnel
    }
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        data = request.get_json()
        
        if 'ad_ids' not in data:
            return jsonify({"error": "ad_ids requis"}), 400
            
        ad_ids = data['ad_ids']
        date_preset = data.get('date_preset', 'last_30d')
        
        results = {}
        
        for ad_id in ad_ids:
            try:
                insights = api.get_insights(ad_id, level="ad", date_preset=date_preset)
                results[ad_id] = {
                    "success": True,
                    "insights": insights
                }
            except Exception as e:
                results[ad_id] = {
                    "success": False,
                    "error": str(e)
                }
        
        return jsonify({
            "success": True,
            "date_preset": date_preset,
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération batch: {str(e)}"}), 500

