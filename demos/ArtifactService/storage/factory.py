from typing import Union
from .base import StorageAdapter
from .nfs_adapter import NFSStorageAdapter
from .s3_adapter import S3StorageAdapter
from config import settings
import logging

logger = logging.getLogger(__name__)


class StorageFactory:
    """Factory class for creating storage adapters"""
    
    @staticmethod
    def create_storage_adapter(storage_type: str = None) -> StorageAdapter:
        """Create storage adapter based on configuration"""
        storage_type = storage_type or settings.storage_type
        
        if storage_type.lower() == "nfs":
            logger.info("Creating NFS storage adapter")
            return NFSStorageAdapter()
        
        elif storage_type.lower() == "s3":
            logger.info("Creating S3 storage adapter")
            return S3StorageAdapter()
        
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
    
    @staticmethod
    def get_available_storage_types() -> list[str]:
        """Get list of available storage types"""
        return ["nfs", "s3"]
