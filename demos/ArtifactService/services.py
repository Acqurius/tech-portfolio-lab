import os
import uuid
from datetime import datetime
from typing import Optional, BinaryIO
from sqlalchemy.ext.asyncio import AsyncSession
from database import ArtifactRepository
from storage.factory import StorageFactory
from storage.base import StorageAdapter
from models import Artifact, ArtifactCreate, ArtifactResponse
from config import settings
import logging

logger = logging.getLogger(__name__)


class ArtifactService:
    """Service class for artifact operations"""
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repository = ArtifactRepository(db_session)
        self.storage_adapter: StorageAdapter = StorageFactory.create_storage_adapter()
    
    def _generate_file_path(self, original_filename: str) -> str:
        """Generate unique file path"""
        file_extension = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y/%m/%d")
        return f"{timestamp}/{unique_id}{file_extension}"
    
    async def upload_artifact(self, 
                            file_content: bytes, 
                            artifact_data: ArtifactCreate) -> ArtifactResponse:
        """Upload artifact file and create database record"""
        try:
            # Generate unique file path
            file_path = self._generate_file_path(artifact_data.original_filename)
            
            # Upload file to storage
            storage_path = await self.storage_adapter.upload_file(
                file_content, 
                file_path, 
                artifact_data.content_type
            )
            
            # Calculate checksum
            checksum = self.storage_adapter.calculate_checksum(file_content)
            
            # Get file size
            file_size = len(file_content)
            
            # Create database record
            artifact_record = {
                "name": artifact_data.name,
                "original_filename": artifact_data.original_filename,
                "file_path": file_path,
                "file_size": file_size,
                "content_type": artifact_data.content_type,
                "checksum": checksum,
                "storage_type": settings.storage_type,
                "storage_path": storage_path,
                "is_public": artifact_data.is_public,
                "metadata_json": artifact_data.metadata if artifact_data.metadata else None
            }
            
            artifact = await self.repository.create_artifact(artifact_record)
            
            # Generate download URL
            download_url = await self.storage_adapter.get_file_url(storage_path)
            
            logger.info(f"Successfully uploaded artifact: {artifact.id}")
            
            return ArtifactResponse(
                id=artifact.id,
                name=artifact.name,
                original_filename=artifact.original_filename,
                file_size=artifact.file_size,
                content_type=artifact.content_type,
                checksum=artifact.checksum,
                storage_type=artifact.storage_type,
                is_public=artifact.is_public,
                created_at=artifact.created_at,
                updated_at=artifact.updated_at,
                download_url=download_url
            )
            
        except Exception as e:
            logger.error(f"Failed to upload artifact: {e}")
            raise
    
    async def download_artifact(self, artifact_id: int) -> tuple[bytes, str, str]:
        """Download artifact file content"""
        try:
            # Get artifact record
            artifact = await self.repository.get_artifact_by_id(artifact_id)
            if not artifact:
                raise FileNotFoundError(f"Artifact not found: {artifact_id}")
            
            # Download file content
            file_content = await self.storage_adapter.download_file(artifact.storage_path)
            
            return file_content, artifact.original_filename, artifact.content_type or "application/octet-stream"
            
        except Exception as e:
            logger.error(f"Failed to download artifact {artifact_id}: {e}")
            raise
    
    async def get_artifact_info(self, artifact_id: int) -> ArtifactResponse:
        """Get artifact information"""
        try:
            artifact = await self.repository.get_artifact_by_id(artifact_id)
            if not artifact:
                raise FileNotFoundError(f"Artifact not found: {artifact_id}")
            
            # Generate download URL
            download_url = await self.storage_adapter.get_file_url(artifact.storage_path)
            
            return ArtifactResponse(
                id=artifact.id,
                name=artifact.name,
                original_filename=artifact.original_filename,
                file_size=artifact.file_size,
                content_type=artifact.content_type,
                checksum=artifact.checksum,
                storage_type=artifact.storage_type,
                is_public=artifact.is_public,
                created_at=artifact.created_at,
                updated_at=artifact.updated_at,
                download_url=download_url
            )
            
        except Exception as e:
            logger.error(f"Failed to get artifact info {artifact_id}: {e}")
            raise
    
    async def list_artifacts(self, page: int = 1, page_size: int = 20) -> dict:
        """List artifacts with pagination"""
        try:
            artifacts, total = await self.repository.list_artifacts(page, page_size)
            
            artifact_responses = []
            for artifact in artifacts:
                download_url = await self.storage_adapter.get_file_url(artifact.storage_path)
                artifact_responses.append(ArtifactResponse(
                    id=artifact.id,
                    name=artifact.name,
                    original_filename=artifact.original_filename,
                    file_size=artifact.file_size,
                    content_type=artifact.content_type,
                    checksum=artifact.checksum,
                    storage_type=artifact.storage_type,
                    is_public=artifact.is_public,
                    created_at=artifact.created_at,
                    updated_at=artifact.updated_at,
                    download_url=download_url
                ))
            
            return {
                "artifacts": artifact_responses,
                "total": total,
                "page": page,
                "page_size": page_size
            }
            
        except Exception as e:
            logger.error(f"Failed to list artifacts: {e}")
            raise
    
    async def delete_artifact(self, artifact_id: int) -> bool:
        """Delete artifact and its file"""
        try:
            # Get artifact record
            artifact = await self.repository.get_artifact_by_id(artifact_id)
            if not artifact:
                raise FileNotFoundError(f"Artifact not found: {artifact_id}")
            
            # Delete file from storage
            await self.storage_adapter.delete_file(artifact.storage_path)
            
            # Delete database record
            success = await self.repository.delete_artifact(artifact_id)
            
            logger.info(f"Successfully deleted artifact: {artifact_id}")
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete artifact {artifact_id}: {e}")
            raise
    
    async def get_artifact_url(self, artifact_id: int, expires_in: Optional[int] = None) -> str:
        """Get presigned URL for artifact"""
        try:
            artifact = await self.repository.get_artifact_by_id(artifact_id)
            if not artifact:
                raise FileNotFoundError(f"Artifact not found: {artifact_id}")
            
            return await self.storage_adapter.get_file_url(artifact.storage_path, expires_in)
            
        except Exception as e:
            logger.error(f"Failed to get artifact URL {artifact_id}: {e}")
            raise
