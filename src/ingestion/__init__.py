# Placeholder Python files to establish the module structure

# src/ingestion/__init__.py
"""
SaaS Analytics Platform - Python Data Ingestion Module

This package provides reusable components for extracting, transforming,
and loading data from source systems into Snowflake.
"""

__version__ = "1.0.0"
__author__ = "Analytics Engineering Team"

# src/ingestion/config.py
"""Configuration management for ingestion pipelines."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class SnowflakeConfig:
    """Snowflake connection configuration."""
    account: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
    user: str = os.getenv("SNOWFLAKE_USER", "")
    password: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    warehouse: str = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_S")
    database: str = os.getenv("SNOWFLAKE_DATABASE", "SAAS_ANALYTICS")
    schema: str = os.getenv("SNOWFLAKE_SCHEMA", "SILVER")
    role: str = os.getenv("SNOWFLAKE_ROLE", "TRANSFORMER")


@dataclass
class IngestionConfig:
    """Global ingestion configuration."""
    snowflake: SnowflakeConfig = None
    batch_size: int = int(os.getenv("INGESTION_BATCH_SIZE", "1000"))
    timeout_seconds: int = int(os.getenv("INGESTION_TIMEOUT_SECONDS", "300"))
    log_level: str = os.getenv("PYTHON_LOG_LEVEL", "INFO")
    
    def __post_init__(self):
        if self.snowflake is None:
            self.snowflake = SnowflakeConfig()


# src/ingestion/utils/logging_config.py
"""Logging configuration for ingestion pipelines."""

import logging
import sys
from typing import Optional


def setup_logging(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging for ingestion processes.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
