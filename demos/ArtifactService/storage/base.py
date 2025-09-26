from abc import ABC, abstractmethod
from typing import Optional, BinaryIO
import hashlib


class StorageAdapter(ABC):
    """Base class for storage adapters"""
    
    @abstractmethod
    async def upload_file(self, file_content: bytes, file_path: str, content_type: Optional[str] = None) -> str:
        """Upload file and return storage path"""
        pass
    
    @abstractmethod
    async def download_file(self, storage_path: str) -> bytes:
        """Download file content"""
        pass
    
    @abstractmethod
    async def delete_file(self, storage_path: str) -> bool:
        """Delete file"""
        pass
    
    @abstractmethod
    async def file_exists(self, storage_path: str) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    async def get_file_url(self, storage_path: str, expires_in: Optional[int] = None) -> str:
        """Get public URL for file access"""
        pass
    
    @abstractmethod
    async def get_file_size(self, storage_path: str) -> int:
        """Get file size in bytes"""
        pass
    
    def calculate_checksum(self, content: bytes) -> str:
        """Calculate SHA256 checksum of content"""
        return hashlib.sha256(content).hexdigest()
