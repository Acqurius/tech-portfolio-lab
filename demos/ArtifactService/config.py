import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "sqlite:///./artifact_service.db"
    
    # Storage Configuration
    storage_type: str = "nfs"  # Options: nfs, s3
    nfs_base_path: str = "/tmp/artifacts"
    s3_bucket_name: str = "artifact-service"
    s3_endpoint_url: str = "https://s3.amazonaws.com"
    s3_access_key_id: Optional[str] = None
    s3_secret_access_key: Optional[str] = None
    s3_region: str = "us-east-1"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Artifact Service"
    api_version: str = "1.0.0"
    api_description: str = "A RESTful API service for artifact management"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
