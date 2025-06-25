"""
Scheduler Utility

This module provides a scheduler for handling delayed Facebook posts.

Author: Manus AI
Date: June 19, 2025
"""

import time
import threading
import logging
from datetime import datetime
from typing import List, Dict, Any, Callable

from models.post import Post
from facebook_api import FacebookAPI
from utils import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("scheduler")


class PostScheduler:
    """
    Scheduler for handling delayed Facebook posts
    """
    
    def __init__(self, facebook_api: FacebookAPI, check_interval: int = 60):
        """
        Initialize the post scheduler
        
        Args:
            facebook_api: FacebookAPI instance
            check_interval: Interval in seconds to check for due posts
        """
        self.facebook_api = facebook_api
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        self.on_post_published = None  # Callback for UI updates
        
    def start(self, on_post_published: Callable[[Post], None] = None):
        """
        Start the scheduler thread
        
        Args:
            on_post_published: Optional callback when a post is published
        """
        if self.running:
            logger.warning("Scheduler is already running")
            return
            
        self.on_post_published = on_post_published
        self.running = True
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
        logger.info("Post scheduler started")
        
    def stop(self):
        """Stop the scheduler thread"""
        if not self.running:
            logger.warning("Scheduler is not running")
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        logger.info("Post scheduler stopped")
        
    def _scheduler_loop(self):
        """Main scheduler loop that checks for due posts"""
        while self.running:
            try:
                self._check_scheduled_posts()
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                
            # Sleep for the check interval
            for _ in range(self.check_interval):
                if not self.running:
                    break
                time.sleep(1)
                
    def _check_scheduled_posts(self):
        """Check for posts that are due for publication"""
        # Load scheduled posts
        posts_data = config.load_scheduled_posts()
        posts_list = posts_data.get('posts', [])
        
        # Check if any posts are due
        now = datetime.now()
        updated = False
        
        for i, post_dict in enumerate(posts_list):
            post = Post.from_dict(post_dict)
            
            # Skip if already published or not due yet
            if post.published or not post.is_due():
                continue
                
            logger.info(f"Publishing scheduled post: {post}")
            
            # Publish the post
            try:
                # Load pages to get access tokens
                pages_data = config.load_pages()
                pages_dict = {page['id']: page for page in pages_data.get('pages', [])}
                
                # Publish to each selected page
                for page_id in post.page_ids:
                    if page_id not in pages_dict:
                        logger.warning(f"Page {page_id} not found in saved pages")
                        continue
                        
                    page_token = pages_dict[page_id].get('access_token')
                    
                    # Handle posts with images
                    if post.image_paths and len(post.image_paths) > 0:
                        # Upload each image
                        photo_ids = []
                        for image_path in post.image_paths:
                            try:
                                photo_response = self.facebook_api.upload_photo(
                                    page_id=page_id,
                                    photo_path=image_path,
                                    published=False,
                                    page_access_token=page_token
                                )
                                photo_ids.append(photo_response.get('id'))
                            except Exception as e:
                                logger.error(f"Error uploading photo {image_path}: {str(e)}")
                                
                        # Publish post with photos
                        if photo_ids:
                            response = self.facebook_api.publish_post_with_photos(
                                page_id=page_id,
                                message=post.message,
                                photo_ids=photo_ids,
                                page_access_token=page_token
                            )
                            post.post_id = response.get('id')
                    else:
                        # Publish text/link post
                        response = self.facebook_api.publish_post(
                            page_id=page_id,
                            message=post.message,
                            link=post.link,
                            page_access_token=page_token
                        )
                        post.post_id = response.get('id')
                
                # Mark as published
                post.published = True
                posts_list[i] = post.to_dict()
                updated = True
                
                # Call the callback if provided
                if self.on_post_published:
                    self.on_post_published(post)
                    
            except Exception as e:
                logger.error(f"Error publishing scheduled post: {str(e)}")
        
        # Save updated posts
        if updated:
            posts_data['posts'] = posts_list
            config.save_scheduled_posts(posts_data)
            
    def add_scheduled_post(self, post: Post) -> bool:
        """
        Add a post to the scheduler
        
        Args:
            post: Post to schedule
            
        Returns:
            True if successful, False otherwise
        """
        if not post.scheduled_time:
            logger.error("Cannot schedule post without scheduled_time")
            return False
            
        # Load current scheduled posts
        posts_data = config.load_scheduled_posts()
        posts_list = posts_data.get('posts', [])
        
        # Add the new post
        posts_list.append(post.to_dict())
        posts_data['posts'] = posts_list
        
        # Save updated posts
        success = config.save_scheduled_posts(posts_data)
        if success:
            logger.info(f"Added scheduled post for {post.scheduled_time.isoformat()}")
        return success
        
    def get_scheduled_posts(self) -> List[Post]:
        """
        Get all scheduled posts
        
        Returns:
            List of Post objects
        """
        posts_data = config.load_scheduled_posts()
        return [Post.from_dict(post_dict) for post_dict in posts_data.get('posts', [])]
        
    def remove_scheduled_post(self, index: int) -> bool:
        """
        Remove a scheduled post by index
        
        Args:
            index: Index of the post to remove
            
        Returns:
            True if successful, False otherwise
        """
        # Load current scheduled posts
        posts_data = config.load_scheduled_posts()
        posts_list = posts_data.get('posts', [])
        
        # Check if index is valid
        if index < 0 or index >= len(posts_list):
            logger.error(f"Invalid post index: {index}")
            return False
            
        # Remove the post
        removed = posts_list.pop(index)
        posts_data['posts'] = posts_list
        
        # Save updated posts
        success = config.save_scheduled_posts(posts_data)
        if success:
            logger.info(f"Removed scheduled post at index {index}")
        return success
