"""
Routes Flask pour les fonctionnalités publicitaires (Boost Post et Publicités)
Version 4.0.0 - Nouvelles fonctionnalités
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Ajouter le répertoire parent au path pour importer facebook_api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from facebook_api import FacebookAPI

# Créer le blueprint pour les publicités
ads_bp = Blueprint('ads', __name__, url_prefix='/api/ads')

# Instance de l'API Facebook (sera initialisée dans main.py)
api = None

def init_ads_api(facebook_api_instance):
    """Initialiser l'instance API pour ce module"""
    global api
    api = facebook_api_instance

@ads_bp.route('/boost', methods=['POST'])
def boost_post():
    """
    Endpoint pour booster un post existant
    
    Payload attendu:
    {
        "ad_account_id": "act_123456789",
        "page_id": "page_id",
        "post_id": "post_id",
        "name": "Nom de la campagne",
        "budget": 20,  // Budget quotidien en euros
        "start": "2025-06-29T00:00:00+0000",
        "end": "2025-07-06T23:59:59+0000",
        "targeting": {...} ou "audience_id": "saved_audience_id"
    }
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        data = request.get_json()
        
        # Validation des données requises
        required_fields = ['ad_account_id', 'page_id', 'post_id', 'name', 'budget', 'start', 'end']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Champ requis manquant: {field}"}), 400
        
        # Récupérer le targeting (soit direct soit depuis une audience sauvegardée)
        if 'targeting' in data:
            targeting = data['targeting']
        elif 'audience_id' in data:
            audience_response = api.get_saved_audience(data['ad_account_id'], data['audience_id'])
            if 'targeting' not in audience_response:
                return jsonify({"error": "Impossible de récupérer l'audience sauvegardée"}), 400
            targeting = audience_response['targeting']
        else:
            return jsonify({"error": "Targeting ou audience_id requis"}), 400
        
        # Créer la campagne
        campaign = api.create_campaign(
            data['ad_account_id'], 
            data['name'], 
            objective="POST_ENGAGEMENT"
        )
        
        if not campaign or 'id' not in campaign:
            return jsonify({"error": "Échec de création de la campagne"}), 500
        
        # Créer l'ad set
        adset = api.create_adset(
            data['ad_account_id'], 
            campaign['id'], 
            f"BoostSet-{data['name'][:20]}",
            daily_budget=int(data['budget'] * 100),  # Convertir en centimes
            start_time=data['start'], 
            end_time=data['end'], 
            targeting=targeting
        )
        
        if not adset or 'id' not in adset:
            return jsonify({"error": "Échec de création de l'ad set"}), 500
        
        # Créer le creative
        creative = api.create_ad_creative(
            data['ad_account_id'], 
            data['page_id'], 
            post_id=data['post_id']
        )
        
        if not creative or 'id' not in creative:
            return jsonify({"error": "Échec de création du creative"}), 500
        
        # Créer l'annonce
        ad = api.create_ad(
            data['ad_account_id'], 
            f"BoostAd-{data['name'][:20]}", 
            adset['id'], 
            creative['id']
        )
        
        if not ad or 'id' not in ad:
            return jsonify({"error": "Échec de création de l'annonce"}), 500
        
        return jsonify({
            "success": True,
            "campaign_id": campaign['id'],
            "adset_id": adset['id'],
            "creative_id": creative['id'],
            "ad_id": ad['id'],
            "message": "Post boosté avec succès (statut: PAUSED)"
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors du boost: {str(e)}"}), 500

@ads_bp.route('/create', methods=['POST'])
def create_ad():
    """
    Endpoint pour créer une nouvelle publicité complète
    
    Payload attendu:
    {
        "ad_account_id": "act_123456789",
        "page_id": "page_id",
        "name": "Nom de la campagne",
        "objective": "TRAFFIC",  // ou POST_ENGAGEMENT, CONVERSIONS, etc.
        "budget": 30,  // Budget quotidien en euros
        "start": "2025-06-29T00:00:00+0000",
        "end": "2025-07-06T23:59:59+0000",
        "targeting": {...} ou "audience_id": "saved_audience_id",
        "post_id": "post_id" (optionnel, pour promouvoir un post existant),
        "message": "Message de la pub" (requis si pas de post_id),
        "media_fbid": "media_hash" (requis pour pub image/vidéo sans post_id)
    }
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        data = request.get_json()
        
        # Validation des données requises
        required_fields = ['ad_account_id', 'page_id', 'name', 'budget', 'start', 'end']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Champ requis manquant: {field}"}), 400
        
        # Validation du contenu (post_id OU message+media_fbid)
        if 'post_id' not in data:
            if 'message' not in data:
                return jsonify({"error": "Message requis si pas de post_id"}), 400
            if 'media_fbid' not in data:
                return jsonify({"error": "media_fbid requis pour une publicité image/vidéo"}), 400
        
        # Récupérer le targeting
        if 'targeting' in data:
            targeting = data['targeting']
        elif 'audience_id' in data:
            audience_response = api.get_saved_audience(data['ad_account_id'], data['audience_id'])
            if 'targeting' not in audience_response:
                return jsonify({"error": "Impossible de récupérer l'audience sauvegardée"}), 400
            targeting = audience_response['targeting']
        else:
            return jsonify({"error": "Targeting ou audience_id requis"}), 400
        
        # Créer la campagne
        campaign = api.create_campaign(
            data['ad_account_id'], 
            data['name'], 
            objective=data.get('objective', 'TRAFFIC')
        )
        
        if not campaign or 'id' not in campaign:
            return jsonify({"error": "Échec de création de la campagne"}), 500
        
        # Créer l'ad set
        adset = api.create_adset(
            data['ad_account_id'], 
            campaign['id'], 
            f"AdSet-{data['name'][:20]}",
            daily_budget=int(data['budget'] * 100),  # Convertir en centimes
            start_time=data['start'], 
            end_time=data['end'], 
            targeting=targeting
        )
        
        if not adset or 'id' not in adset:
            return jsonify({"error": "Échec de création de l'ad set"}), 500
        
        # Créer le creative
        creative = api.create_ad_creative(
            data['ad_account_id'], 
            data['page_id'], 
            post_id=data.get('post_id'),
            message=data.get('message'),
            media_fbid=data.get('media_fbid')
        )
        
        if not creative or 'id' not in creative:
            return jsonify({"error": "Échec de création du creative"}), 500
        
        # Créer l'annonce
        ad = api.create_ad(
            data['ad_account_id'], 
            f"Ad-{data['name'][:20]}", 
            adset['id'], 
            creative['id']
        )
        
        if not ad or 'id' not in ad:
            return jsonify({"error": "Échec de création de l'annonce"}), 500
        
        return jsonify({
            "success": True,
            "campaign_id": campaign['id'],
            "adset_id": adset['id'],
            "creative_id": creative['id'],
            "ad_id": ad['id'],
            "message": "Publicité créée avec succès (statut: PAUSED)"
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création: {str(e)}"}), 500

@ads_bp.route('/accounts', methods=['GET'])
def get_ad_accounts():
    """
    Récupérer les comptes publicitaires de l'utilisateur
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        accounts = api.get_ad_accounts()
        return jsonify({
            "success": True,
            "accounts": accounts
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des comptes: {str(e)}"}), 500

@ads_bp.route('/upload-media', methods=['POST'])
def upload_media():
    """
    Upload d'un média (image) pour les publicités
    """
    try:
        if not api:
            return jsonify({"error": "API Facebook non initialisée"}), 500
            
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier fourni"}), 400
            
        if 'ad_account_id' not in request.form:
            return jsonify({"error": "ad_account_id requis"}), 400
            
        file = request.files['file']
        ad_account_id = request.form['ad_account_id']
        
        if file.filename == '':
            return jsonify({"error": "Aucun fichier sélectionné"}), 400
        
        # Sauvegarder temporairement le fichier
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            file.save(temp_file.name)
            
            # Upload vers Facebook
            result = api.upload_image(ad_account_id, temp_file.name)
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_file.name)
            
            if result.get('success'):
                return jsonify({
                    "success": True,
                    "media_fbid": result['image_hash']
                })
            else:
                return jsonify({"error": result.get('error', 'Échec de l\'upload')}), 500
                
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'upload: {str(e)}"}), 500

