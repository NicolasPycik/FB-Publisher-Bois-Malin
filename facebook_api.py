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
        self.app_id = app_id or os.getenv("APP_ID")
        self.app_secret = app_secret or os.getenv("APP_SECRET")
        self.access_token = access_token or os.getenv("SYSTEM_USER_TOKEN")
        
        if not self.app_id or not self.app_secret:
            logger.error("Missing APP_ID or APP_SECRET in environment variables")
            raise ValueError("Missing APP_ID or APP_SECRET in environment variables")
        
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
    
    def publish_post(self, page_id: str, message: str, link: Optional[str] = None, 
                    page_access_token: Optional[str] = None) -> Dict:
        """
        Publish a text/link post to a Facebook page
        
        Args:
            page_id: ID of the Facebook page
            message: Post message text
            link: Optional link to include
            page_access_token: Page-specific access token
            
        Returns:
            API response with post ID
        """
        params = {"message": message}
        if link:
            params["link"] = link
            
        return self._make_request(
            "POST",
            f"/{page_id}/feed",
            data=params,
            access_token=page_access_token
        )
    
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

