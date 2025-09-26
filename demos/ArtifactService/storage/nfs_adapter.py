import os
import aiofiles
from pathlib import Path
from typing import Optional
from .base import StorageAdapter
from config import settings


class NFSStorageAdapter(StorageAdapter):
    """NFS/File System storage adapter"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or settings.nfs_base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _get_full_path(self, file_path: str) -> Path:
        """Get full file path"""
        return self.base_path / file_path
    
    async def upload_file(self, file_content: bytes, file_path: str, content_type: Optional[str] = None) -> str:
        """Upload file to NFS storage"""
        full_path = self._get_full_path(file_path)
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        async with aiofiles.open(full_path, 'wb') as f:
            await f.write(file_content)
        
        return file_path
    
    async def download_file(self, storage_path: str) -> bytes:
        """Download file from NFS storage"""
        full_path = self._get_full_path(storage_path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {storage_path}")
        
        async with aiofiles.open(full_path, 'rb') as f:
            return await f.read()
    
    async def delete_file(self, storage_path: str) -> bool:
        """Delete file from NFS storage"""
        full_path = self._get_full_path(storage_path)
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    
    async def file_exists(self, storage_path: str) -> bool:
        """Check if file exists in NFS storage"""
        full_path = self._get_full_path(storage_path)
        return full_path.exists()
    
    async def get_file_url(self, storage_path: str, expires_in: Optional[int] = None) -> str:
        """Get file URL (for NFS, this would be a local file path or HTTP endpoint)"""
        # For NFS, we return a relative path that can be served by the API
        return f"/api/v1/files/{storage_path}"
    
    async def get_file_size(self, storage_path: str) -> int:
        """Get file size"""
        full_path = self._get_full_path(storage_path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {storage_path}")
        
        return full_path.stat().st_size
