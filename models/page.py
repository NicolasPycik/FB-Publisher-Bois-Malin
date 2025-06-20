"""
Facebook Page Model

This module defines the Page class for representing Facebook pages.

Author: Manus AI
Date: June 19, 2025
"""

from typing import Optional, Dict, Any


class Page:
    """
    Represents a Facebook page with its properties and access token
    """
    
    def __init__(self, page_id: str, name: str, access_token: str):
        """
        Initialize a Facebook page
        
        Args:
            page_id: Facebook page ID
            name: Page name
            access_token: Page-specific access token
        """
        self.id = page_id
        self.name = name
        self.access_token = access_token
        
    @classmethod
    def from_api_response(cls, response_data: Dict[str, Any]) -> 'Page':
        """
        Create a Page object from API response data
        
        Args:
            response_data: Dictionary containing page data from API
            
        Returns:
            Page object
        """
        return cls(
            page_id=response_data.get('id', ''),
            name=response_data.get('name', ''),
            access_token=response_data.get('access_token', '')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Page object to dictionary for serialization
        
        Returns:
            Dictionary representation of the page
        """
        return {
            'id': self.id,
            'name': self.name,
            'access_token': self.access_token
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Page':
        """
        Create a Page object from dictionary data
        
        Args:
            data: Dictionary containing page data
            
        Returns:
            Page object
        """
        return cls(
            page_id=data.get('id', ''),
            name=data.get('name', ''),
            access_token=data.get('access_token', '')
        )
    
    def __str__(self) -> str:
        """String representation of the page"""
        return f"Page(id={self.id}, name={self.name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the page"""
        return f"Page(id={self.id}, name={self.name}, access_token=***)"
