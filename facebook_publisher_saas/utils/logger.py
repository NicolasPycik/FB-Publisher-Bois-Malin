"""
Logger Utility

This module provides logging functionality for the application.

Author: Manus AI
Date: June 19, 2025
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

# Default log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths
APP_LOG_FILE = os.path.join(LOG_DIR, 'app.log')
API_LOG_FILE = os.path.join(LOG_DIR, 'api.log')
SCHEDULER_LOG_FILE = os.path.join(LOG_DIR, 'scheduler.log')

# Log format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level
        
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create handlers
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=3
    )
    console_handler = logging.StreamHandler()
    
    # Set level
    file_handler.setLevel(level)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Application logger
app_logger = setup_logger('app', APP_LOG_FILE)

# API logger
api_logger = setup_logger('api', API_LOG_FILE)

# Scheduler logger
scheduler_logger = setup_logger('scheduler', SCHEDULER_LOG_FILE)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger by name
    
    Args:
        name: Logger name (app, api, scheduler, or custom)
        
    Returns:
        Logger instance
    """
    if name == 'app':
        return app_logger
    elif name == 'api':
        return api_logger
    elif name == 'scheduler':
        return scheduler_logger
    elif name:
        return logging.getLogger(name)
    else:
        return app_logger
