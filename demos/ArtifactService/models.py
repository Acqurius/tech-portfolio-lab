from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

Base = declarative_base()


class Artifact(Base):
    __tablename__ = "artifacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=True)
    checksum = Column(String(64), nullable=True)  # SHA256 hash
    storage_type = Column(String(20), nullable=False)  # nfs, s3
    storage_path = Column(String(500), nullable=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    metadata_json = Column(Text, nullable=True)  # Additional metadata as JSON


# Pydantic models for API
class ArtifactCreate(BaseModel):
    name: str
    original_filename: str
    content_type: Optional[str] = None
    is_public: bool = False
    metadata: Optional[str] = None  # Store as JSON string


class ArtifactResponse(BaseModel):
    id: int
    name: str
    original_filename: str
    file_size: int
    content_type: Optional[str]
    checksum: Optional[str]
    storage_type: str
    is_public: bool
    created_at: datetime
    updated_at: Optional[datetime]
    download_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class ArtifactListResponse(BaseModel):
    artifacts: list[ArtifactResponse]
    total: int
    page: int
    page_size: int


class UploadResponse(BaseModel):
    artifact_id: int
    message: str
    download_url: Optional[str] = None
