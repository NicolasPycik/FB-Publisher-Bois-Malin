"""
Post Model

This module defines the Post class for representing Facebook posts.

Author: Manus AI
Date: June 19, 2025
"""

from typing import Optional, Dict, Any, List
from datetime import datetime


class Post:
    """
    Represents a Facebook post with its properties and scheduling information
    """
    
    def __init__(self, 
                 message: str, 
                 page_ids: List[str], 
                 link: Optional[str] = None,
                 image_paths: Optional[List[str]] = None,
                 scheduled_time: Optional[datetime] = None,
                 post_id: Optional[str] = None,
                 published: bool = False):
        """
        Initialize a Facebook post
        
        Args:
            message: Post message text
            page_ids: List of page IDs to post to
            link: Optional link to include in the post
            image_paths: Optional list of image paths to upload
            scheduled_time: Optional scheduled publication time
            post_id: Optional post ID (for published posts)
            published: Whether the post has been published
        """
        self.message = message
        self.page_ids = page_ids
        self.link = link
        self.image_paths = image_paths or []
        self.scheduled_time = scheduled_time
        self.post_id = post_id
        self.published = published
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Post object to dictionary for serialization
        
        Returns:
            Dictionary representation of the post
        """
        return {
            'message': self.message,
            'page_ids': self.page_ids,
            'link': self.link,
            'image_paths': self.image_paths,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'post_id': self.post_id,
            'published': self.published
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        """
        Create a Post object from dictionary data
        
        Args:
            data: Dictionary containing post data
            
        Returns:
            Post object
        """
        scheduled_time = None
        if data.get('scheduled_time'):
            try:
                scheduled_time = datetime.fromisoformat(data['scheduled_time'])
            except (ValueError, TypeError):
                scheduled_time = None
                
        return cls(
            message=data.get('message', ''),
            page_ids=data.get('page_ids', []),
            link=data.get('link'),
            image_paths=data.get('image_paths', []),
            scheduled_time=scheduled_time,
            post_id=data.get('post_id'),
            published=data.get('published', False)
        )
    
    def is_due(self) -> bool:
        """
        Check if the post is due for publication
        
        Returns:
            True if the post is scheduled and due, False otherwise
        """
        if not self.scheduled_time or self.published:
            return False
        
        return datetime.now() >= self.scheduled_time
    
    def __str__(self) -> str:
        """String representation of the post"""
        status = "Published" if self.published else "Not published"
        if self.scheduled_time and not self.published:
            status = f"Scheduled for {self.scheduled_time.isoformat()}"
            
        return f"Post(message={self.message[:20]}..., status={status})"
