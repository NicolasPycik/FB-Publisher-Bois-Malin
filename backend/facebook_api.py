"""
Facebook API Wrapper Module

This module provides a wrapper for Facebook Graph API and Marketing API calls.
It handles authentication, error handling, retries, and logging.

Author: Manus AI
Date: June 19, 2025
"""

import os
import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("facebook_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("facebook_api")

# Load environment variables
load_dotenv()

class FacebookAPIError(Exception):
    """Custom exception for Facebook API errors"""
    def __init__(self, message: str, error_code: Optional[int] = None, error_subcode: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        self.error_subcode = error_subcode
        super().__init__(self.message)

class FacebookAPI:
    """
    Facebook API wrapper for Graph API and Marketing API
    
    Handles:
    - Authentication and token management
    - API calls with error handling and retries
    - Logging of requests and responses
    """
    
    BASE_URL = "https://graph.facebook.com/v18.0"  # Using latest stable version
    
    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None, access_token: Optional[str] = None):
        """
        Initialize the Facebook API wrapper
        
        Args:
            app_id: Facebook App ID (from .env if not provided)
            app_secret: Facebook App Secret (from .env if not provided)
            access_token: Access token (optional)
        """
        self.access_token = access_token
        self.app_id = app_id or os.getenv("FACEBOOK_APP_ID") or os.getenv("APP_ID")
        self.app_secret = app_secret or os.getenv("FACEBOOK_APP_SECRET") or os.getenv("APP_SECRET")
        
        # Initialize page token cache
        self._page_token_cache = {}
        
        # Validate required parameters
        if not self.access_token or not self.app_id or not self.app_secret:
            logger.error("Missing FACEBOOK_ACCESS_TOKEN, FACEBOOK_APP_ID or FACEBOOK_APP_SECRET in environment variables")
            raise ValueError("Missing FACEBOOK_ACCESS_TOKEN, FACEBOOK_APP_ID or FACEBOOK_APP_SECRET in environment variables")
        
        logger.info("FacebookAPI initialized")
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None, files: Optional[Dict] = None, 
                     access_token: Optional[str] = None, max_retries: int = 3) -> Dict:
        """
        Make a request to the Facebook API with retry logic
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint (without base URL)
            params: URL parameters
            data: POST data
            files: Files to upload
            access_token: Override default access token
            max_retries: Maximum number of retries for 5xx errors
            
        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        token = access_token or self.access_token
        
        # Ensure params dictionary exists
        if params is None:
            params = {}
        
        # Add access token to params if provided
        if token:
            params["access_token"] = token
        
        # Log request (without sensitive data)
        safe_params = {k: v for k, v in params.items() if k != "access_token"}
        logger.info(f"API Request: {method} {url} - Params: {safe_params}")
        
        retry_count = 0
        while True:
            try:
                if method.upper() == "GET":
                    response = requests.get(url, params=params)
                elif method.upper() == "POST":
                    response = requests.post(url, params=params, data=data, files=files)
                elif method.upper() == "DELETE":
                    response = requests.delete(url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Log response status
                logger.info(f"API Response: {response.status_code}")
                
                # Parse JSON response
                response_data = response.json()
                
                # Log full response for debugging (excluding sensitive data)
                logger.debug(f"API Response data: {json.dumps(response_data)}")
                
                # Check for API errors
                if "error" in response_data:
                    error = response_data["error"]
                    error_msg = error.get("message", "Unknown Facebook API error")
                    error_code = error.get("code")
                    error_subcode = error.get("error_subcode")
                    
                    logger.error(f"Facebook API error: {error_msg} (Code: {error_code}, Subcode: {error_subcode})")
                    
                    # Check if we should retry (server errors)
                    if 500 <= response.status_code < 600 and retry_count < max_retries:
                        retry_count += 1
                        wait_time = 2 ** retry_count  # Exponential backoff
                        logger.info(f"Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    
                    raise FacebookAPIError(error_msg, error_code, error_subcode)
                
                return response_data
                
            except requests.RequestException as e:
                logger.error(f"Request error: {str(e)}")
                
                # Retry on connection errors
                if retry_count < max_retries:
                    retry_count += 1
                    wait_time = 2 ** retry_count
                    logger.info(f"Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                
                raise FacebookAPIError(f"Request failed: {str(e)}")
    
    def _get_page_token(self, page_id: str) -> str:
        """
        Get page-specific access token with caching
        
        Args:
            page_id: Facebook page ID
            
        Returns:
            Page access token
        """
        if page_id in self._page_token_cache:
            return self._page_token_cache[page_id]
        
        resp = self._make_request("GET", "/me/accounts",
                                  params={"fields": "id,access_token", "limit": 100})
        
        for p in resp["data"]:
            self._page_token_cache[p["id"]] = p["access_token"]
        
        return self._page_token_cache.get(page_id)
    
    # Graph API Methods
    
    def get_user_pages(self) -> List[Dict]:
        """
        Get all pages managed by the user
        
        Returns:
            List of page objects with id, name, access_token
        """
        response = self._make_request(
            "GET", 
            "/me/accounts", 
            params={"fields": "name,access_token"}
        )
        
        if "data" in response:
            return response["data"]
        return []
    
    def publish_post(self, page_id: str, message: str, link: Optional[str] = None) -> str:
        """
        Publish a text/link post to a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            message: Post message text
            link: Optional link to include
            
        Returns:
            Post ID
        """
        params = {"message": message, "access_token": self._get_page_token(page_id)}
        if link:
            params["link"] = link
        
        r = requests.post(f"{self.BASE_URL}/{page_id}/feed", params=params, timeout=20)
        r.raise_for_status()
        return r.json()["id"]
    
    def publish_post_with_photos(self, page_id: str, message: str, files: List[str]) -> str:
        """
        Publish a post with photos to a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            message: Post message text
            files: List of file paths to upload
            
        Returns:
            Post ID
        """
        media_ids = []
        for path in files:
            r = requests.post(f"{self.BASE_URL}/{page_id}/photos",
                              params={"published": "false",
                                      "access_token": self._get_page_token(page_id)},
                              files={"source": open(path, "rb")})
            r.raise_for_status()
            media_ids.append({"media_fbid": r.json()["id"]})
        
        # Publish post with attached media
        params = {
            "message": message,
            "attached_media": json.dumps(media_ids),
            "access_token": self._get_page_token(page_id)
        }
        r = requests.post(f"{self.BASE_URL}/{page_id}/feed", params=params, timeout=20)
        r.raise_for_status()
        return r.json()["id"]
    
    def publish_post_with_video(self, page_id: str, video_path: str, message: str) -> str:
        """
        Publish a post with video to a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            video_path: Path to video file
            message: Post message text
            
        Returns:
            Post ID
        """
        # Upload video first
        with open(video_path, "rb") as video_file:
            r = requests.post(f"{self.BASE_URL}/{page_id}/videos",
                              params={"description": message,
                                      "access_token": self._get_page_token(page_id)},
                              files={"source": video_file})
        r.raise_for_status()
        return r.json()["id"]
    
    def upload_photo(self, page_id: str, photo_path: str, caption: Optional[str] = None, 
                    published: bool = False, page_access_token: Optional[str] = None) -> Dict:
        """
        Upload a photo to a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            photo_path: Path to the photo file
            caption: Optional photo caption
            published: Whether to publish immediately (default: False)
            page_access_token: Page-specific access token
            
        Returns:
            API response with photo ID
        """
        params = {"published": "true" if published else "false"}
        if caption:
            params["caption"] = caption
            
        with open(photo_path, "rb") as photo_file:
            files = {"source": photo_file}
            return self._make_request(
                "POST",
                f"/{page_id}/photos",
                params=params,
                files=files,
                access_token=page_access_token
            )
    
    def publish_post_with_photos(self, page_id: str, message: str, photo_ids: List[str], 
                               page_access_token: Optional[str] = None) -> Dict:
        """
        Publish a post with attached photos
        
        Args:
            page_id: ID of the Facebook page
            message: Post message text
            photo_ids: List of previously uploaded photo IDs
            page_access_token: Page-specific access token
            
        Returns:
            API response with post ID
        """
        attached_media = [{"media_fbid": photo_id} for photo_id in photo_ids]
        
        params = {
            "message": message,
            "attached_media": json.dumps(attached_media)
        }
        
        return self._make_request(
            "POST",
            f"/{page_id}/feed",
            data=params,
            access_token=page_access_token
        )
    
    def get_page_insights(self, page_id: str, metrics: List[str], since: str, until: str,
                        page_access_token: Optional[str] = None) -> Dict:
        """
        Get insights for a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            metrics: List of metrics to retrieve
            since: Start date (YYYY-MM-DD)
            until: End date (YYYY-MM-DD)
            page_access_token: Page-specific access token
            
        Returns:
            API response with insights data
        """
        params = {
            "metric": ",".join(metrics),
            "since": since,
            "until": until
        }
        
        return self._make_request(
            "GET",
            f"/{page_id}/insights",
            params=params,
            access_token=page_access_token
        )
    
    def get_post_insights(self, post_id: str, metrics: List[str], 
                        page_access_token: Optional[str] = None) -> Dict:
        """
        Get insights for a specific post
        
        Args:
            post_id: ID of the post
            metrics: List of metrics to retrieve
            page_access_token: Page-specific access token
            
        Returns:
            API response with insights data
        """
        metrics_str = ",".join(metrics)
        
        return self._make_request(
            "GET",
            f"/{post_id}",
            params={"fields": f"insights.metric({metrics_str})"},
            access_token=page_access_token
        )
    
    def debug_token(self, input_token: str) -> Dict:
        """
        Debug an access token to check validity and expiration
        
        Args:
            input_token: Token to debug
            
        Returns:
            API response with token information
        """
        app_token = f"{self.app_id}|{self.app_secret}"
        
        return self._make_request(
            "GET",
            "/debug_token",
            params={
                "input_token": input_token,
                "access_token": app_token
            }
        )
    
    def exchange_token(self, short_lived_token: str) -> Dict:
        """
        Exchange a short-lived token for a long-lived token
        
        Args:
            short_lived_token: Short-lived access token
            
        Returns:
            API response with long-lived token
        """
        return self._make_request(
            "GET",
            "/oauth/access_token",
            params={
                "grant_type": "fb_exchange_token",
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "fb_exchange_token": short_lived_token
            }
        )
    
    # Marketing API Methods
    
    def get_ad_accounts(self) -> List[Dict]:
        """
        Get all ad accounts accessible to the user
        
        Returns:
            List of ad account objects
        """
        response = self._make_request(
            "GET",
            "/me/adaccounts",
            params={"fields": "name,account_id,id"}
        )
        
        if "data" in response:
            return response["data"]
        return []
    
    def create_ad_creative(self, ad_account_id: str, object_story_id: str) -> Dict:
        """
        Create an ad creative for a boosted post
        
        Args:
            ad_account_id: ID of the ad account
            object_story_id: ID of the post to boost (format: page_id_post_id)
            
        Returns:
            API response with creative ID
        """
        return self._make_request(
            "POST",
            f"/act_{ad_account_id}/adcreatives",
            data={"object_story_id": object_story_id}
        )
    
    def create_campaign(self, ad_account_id: str, name: str, objective: str, status: str = "PAUSED") -> Dict:
        """
        Create an ad campaign
        
        Args:
            ad_account_id: ID of the ad account
            name: Campaign name
            objective: Campaign objective (e.g., POST_ENGAGEMENT, TRAFFIC)
            status: Campaign status (default: PAUSED)
            
        Returns:
            API response with campaign ID
        """
        data = {
            "name": name,
            "objective": objective,
            "status": status
        }
        
        return self._make_request(
            "POST",
            f"/act_{ad_account_id}/campaigns",
            data=data
        )
    
    def create_ad_set(self, ad_account_id: str, name: str, campaign_id: str, 
                    daily_budget: int, targeting: Dict, 
                    start_time: Optional[str] = None, end_time: Optional[str] = None,
                    status: str = "PAUSED") -> Dict:
        """
        Create an ad set
        
        Args:
            ad_account_id: ID of the ad account
            name: Ad set name
            campaign_id: Parent campaign ID
            daily_budget: Daily budget in cents
            targeting: Targeting specification
            start_time: Optional start time (ISO format)
            end_time: Optional end time (ISO format)
            status: Ad set status (default: PAUSED)
            
        Returns:
            API response with ad set ID
        """
        data = {
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget,
            "targeting": json.dumps(targeting),
            "status": status,
            "optimization_goal": "REACH"
        }
        
        if start_time:
            data["start_time"] = start_time
        if end_time:
            data["end_time"] = end_time
        
        return self._make_request(
            "POST",
            f"/act_{ad_account_id}/adsets",
            data=data
        )
    
    def create_ad(self, ad_account_id: str, name: str, adset_id: str, 
                creative_id: str, status: str = "PAUSED") -> Dict:
        """
        Create an ad
        
        Args:
            ad_account_id: ID of the ad account
            name: Ad name
            adset_id: Parent ad set ID
            creative_id: Ad creative ID
            status: Ad status (default: PAUSED)
            
        Returns:
            API response with ad ID
        """
        data = {
            "name": name,
            "adset_id": adset_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": status
        }
        
        return self._make_request(
            "POST",
            f"/act_{ad_account_id}/ads",
            data=data
        )
    
    def get_ad_insights(self, ad_id: str, fields: List[str]) -> Dict:
        """
        Get insights for a specific ad
        
        Args:
            ad_id: ID of the ad
            fields: List of fields to retrieve
            
        Returns:
            API response with insights data
        """
        return self._make_request(
            "GET",
            f"/{ad_id}/insights",
            params={"fields": ",".join(fields)}
        )

    # --- NEW: Ad Accounts -------------------------------------------------
    def get_ad_accounts(self) -> List[Dict]:
        """
        Return a list of ad accounts with id & name
        
        Returns:
            List of ad account objects with id and name
        """
        response = self._make_request(
            "GET", 
            "/me/adaccounts", 
            params={"fields": "id,name"}
        )
        return response.get("data", [])

    # --- NEW: get_page_insights ------------------------------------------
    def get_page_insights(self, page_id: str, since: int, until: int, page_access_token: Optional[str] = None) -> Dict:
        """
        Get insights for a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            since: Start timestamp (Unix timestamp)
            until: End timestamp (Unix timestamp)
            page_access_token: Page-specific access token
            
        Returns:
            API response with insights data
        """
        metrics = "page_impressions,page_engaged_users"
        params = {
            "metric": metrics,
            "since": str(since),
            "until": str(until)
        }
        
        return self._make_request(
            "GET",
            f"/{page_id}/insights",
            params=params,
            access_token=page_access_token or self._get_page_token(page_id)
        )

    # --- NEW: get_post_insights ------------------------------------------
    def get_post_insights(self, post_id: str, page_access_token: Optional[str] = None) -> Dict:
        """
        Get insights for a specific post
        
        Args:
            post_id: ID of the post
            page_access_token: Page-specific access token
            
        Returns:
            API response with insights data
        """
        metrics = "post_impressions,post_engaged_users,post_reactions_by_type_total"
        params = {"metric": metrics}
        
        return self._make_request(
            "GET",
            f"/{post_id}/insights",
            params=params,
            access_token=page_access_token
        )
    
    # --- Helper method for page tokens -----------------------------------
    def _get_page_token(self, page_id: str) -> Optional[str]:
        """
        Get the access token for a specific page
        
        Args:
            page_id: ID of the Facebook page
            
        Returns:
            Page access token or None if not found
        """
        try:
            # Load pages from config to get page tokens
            from utils import config
            pages_data = config.load_pages()
            for page in pages_data.get("pages", []):
                if page.get("id") == page_id:
                    return page.get("access_token")
        except Exception as e:
            logger.warning(f"Could not get page token for {page_id}: {e}")
        
        return self.access_token  # Fallback to system token
    
    def get_recent_posts(self, page_id: str, limit: int = 10) -> List[Dict]:
        """
        Return last *limit* posts with id, message, created_time
        
        Args:
            page_id: ID of the Facebook page
            limit: Number of posts to retrieve
            
        Returns:
            List of post objects with id, message, created_time fields
        """
        params = {
            "fields": "id,message,created_time",
            "limit": str(limit),
            "access_token": self._get_page_token(page_id)
        }
        
        response = self._make_request(
            "GET",
            f"/{page_id}/feed",
            params=params
        )
        
        return response.get("data", [])


    # --- Multi-Page Publishing Methods (v3.0.0) -------------------------
    
    def publish_to_multiple_pages(self, page_ids: List[str], message: str, 
                                 media_paths: Optional[List[str]] = None,
                                 link: Optional[str] = None) -> Dict[str, Dict]:
        """
        Publish a post to multiple Facebook pages simultaneously
        
        Args:
            page_ids: List of Facebook page IDs
            message: Post message text
            media_paths: Optional list of media file paths (images/videos)
            link: Optional link to include
            
        Returns:
            Dictionary with page_id as key and API response as value
        """
        results = {}
        
        for page_id in page_ids:
            try:
                logger.info(f"Publishing to page {page_id}")
                
                # Get page-specific access token
                page_token = self._get_page_token(page_id)
                
                if media_paths:
                    # Upload media first, then publish with media
                    media_ids = []
                    for media_path in media_paths:
                        if self._is_video_file(media_path):
                            media_response = self.upload_video(page_id, media_path, 
                                                             description=message, 
                                                             page_access_token=page_token)
                        else:
                            media_response = self.upload_photo(page_id, media_path, 
                                                             caption=message, 
                                                             published=False,
                                                             page_access_token=page_token)
                        
                        if "id" in media_response:
                            media_ids.append(media_response["id"])
                    
                    # Publish post with attached media
                    if media_ids:
                        result = self.publish_post_with_photos(page_id, message, media_ids, 
                                                             page_access_token=page_token)
                    else:
                        # Fallback to text post if media upload failed
                        result = self.publish_post(page_id, message, link, 
                                                 page_access_token=page_token)
                else:
                    # Publish text/link post
                    result = self.publish_post(page_id, message, link, 
                                             page_access_token=page_token)
                
                results[page_id] = {
                    "success": True,
                    "data": result,
                    "message": "Post published successfully"
                }
                
                logger.info(f"Successfully published to page {page_id}")
                
            except Exception as e:
                logger.error(f"Failed to publish to page {page_id}: {str(e)}")
                results[page_id] = {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to publish to page {page_id}"
                }
        
        return results
    
    def upload_video(self, page_id: str, video_path: str, title: Optional[str] = None,
                    description: Optional[str] = None, page_access_token: Optional[str] = None) -> Dict:
        """
        Upload a video to a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            video_path: Path to the video file
            title: Optional video title
            description: Optional video description
            page_access_token: Page-specific access token
            
        Returns:
            API response with video ID
        """
        params = {}
        if title:
            params["title"] = title
        if description:
            params["description"] = description
            
        with open(video_path, "rb") as video_file:
            files = {"source": video_file}
            return self._make_request(
                "POST",
                f"/{page_id}/videos",
                params=params,
                files=files,
                access_token=page_access_token
            )
    
    def _is_video_file(self, file_path: str) -> bool:
        """
        Check if a file is a video based on its extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is a video, False otherwise
        """
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
        return any(file_path.lower().endswith(ext) for ext in video_extensions)
    
    def get_all_pages_for_publishing(self) -> List[Dict]:
        """
        Get all available pages for publishing with their basic info
        
        Returns:
            List of pages with id, name, fan_count, access_token
        """
        try:
            pages = self.get_all_pages()
            return [
                {
                    "id": page["id"],
                    "name": page["name"],
                    "fan_count": page.get("fan_count", 0),
                    "access_token": page.get("access_token", ""),
                    "category": page.get("category", ""),
                    "picture": page.get("picture", {}).get("data", {}).get("url", "")
                }
                for page in pages
            ]
        except Exception as e:
            logger.error(f"Error getting pages for publishing: {str(e)}")
            return []


    
    def create_boosted_post_ad(self, ad_account_id: str, page_id: str, post_id: str,
                              targeting: dict, budget: int, start_date: str, end_date: str) -> dict:
        """
        Create a boosted post ad campaign
        
        Args:
            ad_account_id: Facebook Ad Account ID
            page_id: Facebook Page ID
            post_id: Post ID to boost
            targeting: Targeting dictionary
            budget: Daily budget in euros
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Dictionary with campaign, adset, and ad IDs
        """
        try:
            # Step 1: Create Campaign
            campaign_data = {
                'name': f"Boost Post {post_id}",
                'objective': 'POST_ENGAGEMENT',
                'status': 'ACTIVE',
                'access_token': self.access_token
            }
            
            campaign_response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/campaigns",
                data=campaign_data
            )
            campaign_id = campaign_response.get('id')
            
            # Step 2: Create Ad Creative
            creative_data = {
                'name': f"Creative for Post {post_id}",
                'object_story_id': f"{page_id}_{post_id}",
                'access_token': self.access_token
            }
            
            creative_response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/adcreatives",
                data=creative_data
            )
            creative_id = creative_response.get('id')
            
            # Step 3: Create Ad Set
            adset_data = {
                'name': f"AdSet for Post {post_id}",
                'campaign_id': campaign_id,
                'daily_budget': budget * 100,  # Convert to cents
                'start_time': f"{start_date}T00:00:00+0000",
                'end_time': f"{end_date}T23:59:59+0000",
                'targeting': json.dumps(targeting),
                'status': 'ACTIVE',
                'access_token': self.access_token
            }
            
            adset_response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/adsets",
                data=adset_data
            )
            adset_id = adset_response.get('id')
            
            # Step 4: Create Ad
            ad_data = {
                'name': f"Boost Ad for Post {post_id}",
                'adset_id': adset_id,
                'creative': json.dumps({'creative_id': creative_id}),
                'status': 'ACTIVE',
                'access_token': self.access_token
            }
            
            ad_response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/ads",
                data=ad_data
            )
            ad_id = ad_response.get('id')
            
            return {
                'campaign_id': campaign_id,
                'adset_id': adset_id,
                'creative_id': creative_id,
                'ad_id': ad_id,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error creating boosted post ad: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_saved_audience(self, ad_account_id: str, name: str, targeting_dict: dict) -> dict:
        """
        Create a saved audience
        
        Args:
            ad_account_id: Facebook Ad Account ID
            name: Audience name
            targeting_dict: Targeting parameters
            
        Returns:
            API response with audience ID
        """
        try:
            audience_data = {
                'name': name,
                'targeting': json.dumps(targeting_dict),
                'access_token': self.access_token
            }
            
            response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/saved_audiences",
                data=audience_data
            )
            
            return {
                'success': True,
                'audience_id': response.get('id'),
                'name': name
            }
            
        except Exception as e:
            logger.error(f"Error creating saved audience: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_saved_audiences(self, ad_account_id: str) -> List[Dict]:
        """
        Get all saved audiences for an ad account
        
        Args:
            ad_account_id: Facebook Ad Account ID
            
        Returns:
            List of saved audiences
        """
        try:
            response = self._make_request(
                "GET",
                f"/act_{ad_account_id}/saved_audiences",
                params={
                    "fields": "id,name,targeting,approximate_count",
                    "access_token": self.access_token
                }
            )
            
            if "data" in response:
                return response["data"]
            return []
            
        except Exception as e:
            logger.error(f"Error getting saved audiences: {str(e)}")
            return []
    
    def get_ad_accounts(self) -> List[Dict]:
        """
        Get all ad accounts accessible by the user
        
        Returns:
            List of ad account objects
        """
        try:
            response = self._make_request(
                "GET",
                "/me/adaccounts",
                params={
                    "fields": "id,name,account_status,currency",
                    "access_token": self.access_token
                }
            )
            
            if "data" in response:
                return response["data"]
            return []
            
        except Exception as e:
            logger.error(f"Error getting ad accounts: {str(e)}")
            return []
    
    def create_campaign(self, ad_account_id: str, name: str, objective: str) -> dict:
        """
        Create a new campaign
        
        Args:
            ad_account_id: Facebook Ad Account ID
            name: Campaign name
            objective: Campaign objective
            
        Returns:
            API response with campaign ID
        """
        try:
            campaign_data = {
                'name': name,
                'objective': objective,
                'status': 'PAUSED',
                'access_token': self.access_token
            }
            
            response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/campaigns",
                data=campaign_data
            )
            
            return {
                'success': True,
                'campaign_id': response.get('id')
            }
            
        except Exception as e:
            logger.error(f"Error creating campaign: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_adset(self, ad_account_id: str, campaign_id: str, name: str, 
                    daily_budget: int, start_date: str, end_date: str, targeting: dict) -> dict:
        """
        Create a new ad set
        
        Args:
            ad_account_id: Facebook Ad Account ID
            campaign_id: Campaign ID
            name: AdSet name
            daily_budget: Daily budget in cents
            start_date: Start date
            end_date: End date
            targeting: Targeting dictionary
            
        Returns:
            API response with adset ID
        """
        try:
            adset_data = {
                'name': name,
                'campaign_id': campaign_id,
                'daily_budget': daily_budget,
                'start_time': f"{start_date}T00:00:00+0000",
                'end_time': f"{end_date}T23:59:59+0000",
                'targeting': json.dumps(targeting),
                'status': 'PAUSED',
                'access_token': self.access_token
            }
            
            response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/adsets",
                data=adset_data
            )
            
            return {
                'success': True,
                'adset_id': response.get('id')
            }
            
        except Exception as e:
            logger.error(f"Error creating adset: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_ad_creative(self, ad_account_id: str, name: str, page_id: str = None, 
                          message: str = None, link: str = None, image_hash: str = None) -> dict:
        """
        Create an ad creative
        
        Args:
            ad_account_id: Facebook Ad Account ID
            name: Creative name
            page_id: Facebook Page ID
            message: Ad message
            link: Ad link
            image_hash: Image hash for creative
            
        Returns:
            API response with creative ID
        """
        try:
            creative_data = {
                'name': name,
                'access_token': self.access_token
            }
            
            if page_id and message:
                object_story_spec = {
                    'page_id': page_id,
                    'link_data': {
                        'message': message
                    }
                }
                
                if link:
                    object_story_spec['link_data']['link'] = link
                
                if image_hash:
                    object_story_spec['link_data']['image_hash'] = image_hash
                
                creative_data['object_story_spec'] = json.dumps(object_story_spec)
            
            response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/adcreatives",
                data=creative_data
            )
            
            return {
                'success': True,
                'creative_id': response.get('id')
            }
            
        except Exception as e:
            logger.error(f"Error creating ad creative: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_ad(self, ad_account_id: str, name: str, adset_id: str, creative_id: str) -> dict:
        """
        Create a new ad
        
        Args:
            ad_account_id: Facebook Ad Account ID
            name: Ad name
            adset_id: AdSet ID
            creative_id: Creative ID
            
        Returns:
            API response with ad ID
        """
        try:
            ad_data = {
                'name': name,
                'adset_id': adset_id,
                'creative': json.dumps({'creative_id': creative_id}),
                'status': 'PAUSED',
                'access_token': self.access_token
            }
            
            response = self._make_request(
                "POST",
                f"/act_{ad_account_id}/ads",
                data=ad_data
            )
            
            return {
                'success': True,
                'ad_id': response.get('id')
            }
            
        except Exception as e:
            logger.error(f"Error creating ad: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_image(self, ad_account_id: str, image_path: str) -> dict:
        """
        Upload an image for use in ads
        
        Args:
            ad_account_id: Facebook Ad Account ID
            image_path: Path to image file
            
        Returns:
            API response with image hash
        """
        try:
            with open(image_path, 'rb') as image_file:
                files = {'filename': image_file}
                data = {'access_token': self.access_token}
                
                response = requests.post(
                    f"{self.base_url}/act_{ad_account_id}/adimages",
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'images' in result:
                        image_hash = list(result['images'].keys())[0]
                        return {
                            'success': True,
                            'image_hash': image_hash
                        }
                
                return {
                    'success': False,
                    'error': 'Failed to upload image'
                }
                
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


    def get_all_pages(self) -> List[Dict]:
        """
        Get all pages managed by the user with pagination support
        
        Returns:
            List of all page objects with id, name, access_token, fan_count, etc.
        """
        try:
            all_pages = []
            url = "/me/accounts"
            params = {
                "fields": "name,access_token,fan_count,category,picture,about,website,phone,location",
                "limit": 100  # Maximum per request
            }
            
            while url:
                if url.startswith("/"):
                    # First request or relative URL
                    response = self._make_request("GET", url, params=params)
                else:
                    # Full URL from pagination
                    response = requests.get(url).json()
                
                if "data" in response:
                    all_pages.extend(response["data"])
                    logger.info(f"Récupéré {len(response['data'])} pages, total: {len(all_pages)}")
                
                # Check for next page
                if "paging" in response and "next" in response["paging"]:
                    url = response["paging"]["next"]
                    params = {}  # Parameters are already in the next URL
                else:
                    break
            
            logger.info(f"Total des pages récupérées: {len(all_pages)}")
            return all_pages
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des pages: {str(e)}")
            return []


    def publish_to_multiple_pages(self, page_ids: List[str], message: str, 
                                 media_paths: Optional[List[str]] = None, 
                                 link: Optional[str] = None) -> Dict[str, Dict]:
        """
        Publish a post to multiple Facebook pages
        
        Args:
            page_ids: List of Facebook page IDs
            message: Post message text
            media_paths: Optional list of media file paths (not used for now)
            link: Optional link to include
            
        Returns:
            Dictionary with results for each page
        """
        results = {}
        
        for page_id in page_ids:
            try:
                # Get page-specific access token
                page_token = self._get_page_token(page_id)
                if not page_token:
                    results[page_id] = {
                        'success': False,
                        'error': 'Token d\'accès de page non trouvé'
                    }
                    continue
                
                # Publish the post
                result = self.publish_post(
                    page_id=page_id,
                    message=message,
                    link=link,
                    page_access_token=page_token
                )
                
                results[page_id] = {
                    'success': True,
                    'post_id': result.get('id'),
                    'message': 'Post published successfully'
                }
                
            except Exception as e:
                results[page_id] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results

