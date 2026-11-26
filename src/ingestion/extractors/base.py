"""Base extractor class for data sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime


@dataclass
class ExtractionMetadata:
    """Metadata about an extraction run."""
    source_system: str
    extraction_timestamp: datetime
    record_count: int
    batch_id: str
    last_modified_date: Optional[datetime] = None


class BaseExtractor(ABC):
    """
    Abstract base class for data extractors.
    
    Provides common functionality for extracting data from various sources
    and standardizing the output format.
    """
    
    def __init__(
        self,
        source_system: str,
        logger: Optional[logging.Logger] = None,
        batch_size: int = 1000
    ):
        """
        Initialize the extractor.
        
        Args:
            source_system: Name of the source system
            logger: Logger instance
            batch_size: Number of records to fetch per batch
        """
        self.source_system = source_system
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.batch_size = batch_size
        
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to source system."""
        pass
    
    @abstractmethod
    def extract(
        self,
        query: Optional[Dict[str, Any]] = None,
        incremental: bool = False,
        last_modified_date: Optional[datetime] = None
    ) -> tuple[List[Dict[str, Any]], ExtractionMetadata]:
        """
        Extract data from source system.
        
        Args:
            query: Optional query parameters
            incremental: Whether to perform incremental extraction
            last_modified_date: Date to filter records from
            
        Returns:
            Tuple of (records, metadata)
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close connection to source system."""
        pass
    
    def validate_connection(self) -> bool:
        """
        Validate that connection to source is working.
        
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            self.connect()
            self.logger.info(f"✓ Connection to {self.source_system} successful")
            self.close()
            return True
        except Exception as e:
            self.logger.error(f"✗ Connection to {self.source_system} failed: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
