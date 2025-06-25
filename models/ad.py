"""
Ad Model

This module defines the Ad class for representing Facebook ads and related entities.

Author: Manus AI
Date: June 19, 2025
"""

from typing import Optional, Dict, Any, List
from datetime import datetime


class AdCreative:
    """
    Represents a Facebook ad creative
    """
    
    def __init__(self, 
                 creative_id: str,
                 name: Optional[str] = None,
                 object_story_id: Optional[str] = None):
        """
        Initialize an AdCreative object
        
        Args:
            creative_id: Facebook creative ID
            name: Optional creative name
            object_story_id: Optional object story ID (for boosted posts)
        """
        self.creative_id = creative_id
        self.name = name
        self.object_story_id = object_story_id
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert AdCreative object to dictionary for serialization
        
        Returns:
            Dictionary representation of the creative
        """
        return {
            'creative_id': self.creative_id,
            'name': self.name,
            'object_story_id': self.object_story_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AdCreative':
        """
        Create an AdCreative object from dictionary data
        
        Args:
            data: Dictionary containing creative data
            
        Returns:
            AdCreative object
        """
        return cls(
            creative_id=data.get('creative_id', ''),
            name=data.get('name'),
            object_story_id=data.get('object_story_id')
        )


class Campaign:
    """
    Represents a Facebook ad campaign
    """
    
    def __init__(self,
                 campaign_id: str,
                 name: str,
                 objective: str,
                 status: str):
        """
        Initialize a Campaign object
        
        Args:
            campaign_id: Facebook campaign ID
            name: Campaign name
            objective: Campaign objective (e.g., POST_ENGAGEMENT, TRAFFIC)
            status: Campaign status (e.g., ACTIVE, PAUSED)
        """
        self.campaign_id = campaign_id
        self.name = name
        self.objective = objective
        self.status = status
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Campaign object to dictionary for serialization
        
        Returns:
            Dictionary representation of the campaign
        """
        return {
            'campaign_id': self.campaign_id,
            'name': self.name,
            'objective': self.objective,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Campaign':
        """
        Create a Campaign object from dictionary data
        
        Args:
            data: Dictionary containing campaign data
            
        Returns:
            Campaign object
        """
        return cls(
            campaign_id=data.get('campaign_id', ''),
            name=data.get('name', ''),
            objective=data.get('objective', ''),
            status=data.get('status', '')
        )


class AdSet:
    """
    Represents a Facebook ad set
    """
    
    def __init__(self,
                 adset_id: str,
                 name: str,
                 campaign_id: str,
                 daily_budget: int,
                 targeting: Dict[str, Any],
                 status: str,
                 start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None):
        """
        Initialize an AdSet object
        
        Args:
            adset_id: Facebook ad set ID
            name: Ad set name
            campaign_id: Parent campaign ID
            daily_budget: Daily budget in cents
            targeting: Targeting specification
            status: Ad set status (e.g., ACTIVE, PAUSED)
            start_time: Optional start time
            end_time: Optional end time
        """
        self.adset_id = adset_id
        self.name = name
        self.campaign_id = campaign_id
        self.daily_budget = daily_budget
        self.targeting = targeting
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert AdSet object to dictionary for serialization
        
        Returns:
            Dictionary representation of the ad set
        """
        return {
            'adset_id': self.adset_id,
            'name': self.name,
            'campaign_id': self.campaign_id,
            'daily_budget': self.daily_budget,
            'targeting': self.targeting,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AdSet':
        """
        Create an AdSet object from dictionary data
        
        Args:
            data: Dictionary containing ad set data
            
        Returns:
            AdSet object
        """
        start_time = None
        if data.get('start_time'):
            try:
                start_time = datetime.fromisoformat(data['start_time'])
            except (ValueError, TypeError):
                start_time = None
                
        end_time = None
        if data.get('end_time'):
            try:
                end_time = datetime.fromisoformat(data['end_time'])
            except (ValueError, TypeError):
                end_time = None
                
        return cls(
            adset_id=data.get('adset_id', ''),
            name=data.get('name', ''),
            campaign_id=data.get('campaign_id', ''),
            daily_budget=data.get('daily_budget', 0),
            targeting=data.get('targeting', {}),
            status=data.get('status', ''),
            start_time=start_time,
            end_time=end_time
        )


class Ad:
    """
    Represents a Facebook ad
    """
    
    def __init__(self,
                 ad_id: str,
                 name: str,
                 adset_id: str,
                 creative_id: str,
                 status: str):
        """
        Initialize an Ad object
        
        Args:
            ad_id: Facebook ad ID
            name: Ad name
            adset_id: Parent ad set ID
            creative_id: Ad creative ID
            status: Ad status (e.g., ACTIVE, PAUSED)
        """
        self.ad_id = ad_id
        self.name = name
        self.adset_id = adset_id
        self.creative_id = creative_id
        self.status = status
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Ad object to dictionary for serialization
        
        Returns:
            Dictionary representation of the ad
        """
        return {
            'ad_id': self.ad_id,
            'name': self.name,
            'adset_id': self.adset_id,
            'creative_id': self.creative_id,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ad':
        """
        Create an Ad object from dictionary data
        
        Args:
            data: Dictionary containing ad data
            
        Returns:
            Ad object
        """
        return cls(
            ad_id=data.get('ad_id', ''),
            name=data.get('name', ''),
            adset_id=data.get('adset_id', ''),
            creative_id=data.get('creative_id', ''),
            status=data.get('status', '')
        )


class BoostedPost:
    """
    Represents a boosted Facebook post with associated ad entities
    """
    
    def __init__(self,
                 post_id: str,
                 page_id: str,
                 creative: AdCreative,
                 campaign: Campaign,
                 adset: AdSet,
                 ad: Ad):
        """
        Initialize a BoostedPost object
        
        Args:
            post_id: Facebook post ID
            page_id: Facebook page ID
            creative: Ad creative object
            campaign: Campaign object
            adset: AdSet object
            ad: Ad object
        """
        self.post_id = post_id
        self.page_id = page_id
        self.creative = creative
        self.campaign = campaign
        self.adset = adset
        self.ad = ad
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert BoostedPost object to dictionary for serialization
        
        Returns:
            Dictionary representation of the boosted post
        """
        return {
            'post_id': self.post_id,
            'page_id': self.page_id,
            'creative': self.creative.to_dict(),
            'campaign': self.campaign.to_dict(),
            'adset': self.adset.to_dict(),
            'ad': self.ad.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoostedPost':
        """
        Create a BoostedPost object from dictionary data
        
        Args:
            data: Dictionary containing boosted post data
            
        Returns:
            BoostedPost object
        """
        return cls(
            post_id=data.get('post_id', ''),
            page_id=data.get('page_id', ''),
            creative=AdCreative.from_dict(data.get('creative', {})),
            campaign=Campaign.from_dict(data.get('campaign', {})),
            adset=AdSet.from_dict(data.get('adset', {})),
            ad=Ad.from_dict(data.get('ad', {}))
        )
