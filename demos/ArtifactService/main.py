from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import io
import logging

from database import get_db, init_db
from services import ArtifactService
from models import ArtifactCreate, ArtifactResponse, ArtifactListResponse, UploadResponse
from config import settings
from middleware import LoggingMiddleware, ErrorHandlingMiddleware
from exceptions import ArtifactNotFoundError, StorageError, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()
    logger.info("Database initialized")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": "Artifact Service API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "artifact-service"}


@app.post("/api/v1/artifacts/upload", response_model=UploadResponse, tags=["Artifacts"])
async def upload_artifact(
    file: UploadFile = File(...),
    name: str = Form(...),
    is_public: bool = Form(False),
    metadata: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a new artifact file
    
    - **file**: The file to upload
    - **name**: Unique name for the artifact
    - **is_public**: Whether the artifact should be publicly accessible
    - **metadata**: Optional JSON metadata as string
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Create artifact data
        artifact_data = ArtifactCreate(
            name=name,
            original_filename=file.filename,
            content_type=file.content_type,
            is_public=is_public,
            metadata=metadata
        )
        
        # Upload artifact
        service = ArtifactService(db)
        artifact = await service.upload_artifact(file_content, artifact_data)
        
        return UploadResponse(
            artifact_id=artifact.id,
            message="Artifact uploaded successfully",
            download_url=artifact.download_url
        )
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/artifacts/{artifact_id}/download", tags=["Artifacts"])
async def download_artifact(
    artifact_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Download an artifact file
    
    - **artifact_id**: ID of the artifact to download
    """
    try:
        service = ArtifactService(db)
        file_content, filename, content_type = await service.download_artifact(artifact_id)
        
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Artifact not found")
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/artifacts/{artifact_id}", response_model=ArtifactResponse, tags=["Artifacts"])
async def get_artifact_info(
    artifact_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get artifact information
    
    - **artifact_id**: ID of the artifact
    """
    try:
        service = ArtifactService(db)
        artifact = await service.get_artifact_info(artifact_id)
        return artifact
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Artifact not found")
    except Exception as e:
        logger.error(f"Get artifact info failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/artifacts", response_model=ArtifactListResponse, tags=["Artifacts"])
async def list_artifacts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all artifacts with pagination
    
    - **page**: Page number (starting from 1)
    - **page_size**: Number of items per page (max 100)
    """
    try:
        service = ArtifactService(db)
        result = await service.list_artifacts(page, page_size)
        return ArtifactListResponse(**result)
        
    except Exception as e:
        logger.error(f"List artifacts failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/artifacts/{artifact_id}/url", tags=["Artifacts"])
async def get_artifact_url(
    artifact_id: int,
    expires_in: Optional[int] = Query(3600, ge=60, le=86400, description="URL expiration time in seconds"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get presigned URL for artifact access
    
    - **artifact_id**: ID of the artifact
    - **expires_in**: URL expiration time in seconds (60-86400)
    """
    try:
        service = ArtifactService(db)
        url = await service.get_artifact_url(artifact_id, expires_in)
        
        return {
            "artifact_id": artifact_id,
            "url": url,
            "expires_in": expires_in
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Artifact not found")
    except Exception as e:
        logger.error(f"Get artifact URL failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/artifacts/{artifact_id}", tags=["Artifacts"])
async def delete_artifact(
    artifact_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an artifact
    
    - **artifact_id**: ID of the artifact to delete
    """
    try:
        service = ArtifactService(db)
        success = await service.delete_artifact(artifact_id)
        
        if success:
            return {"message": "Artifact deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Artifact not found")
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Artifact not found")
    except Exception as e:
        logger.error(f"Delete artifact failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/files/{file_path:path}", tags=["Files"])
async def serve_file(
    file_path: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Serve file directly (for NFS storage)
    
    - **file_path**: Path to the file
    """
    try:
        # For NFS storage, we can serve files directly
        if settings.storage_type == "nfs":
            from storage.factory import StorageFactory
            storage_adapter = StorageFactory.create_storage_adapter("nfs")
            
            if await storage_adapter.file_exists(file_path):
                file_content = await storage_adapter.download_file(file_path)
                return StreamingResponse(
                    io.BytesIO(file_content),
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f"inline; filename={file_path.split('/')[-1]}"}
                )
            else:
                raise HTTPException(status_code=404, detail="File not found")
        else:
            raise HTTPException(status_code=404, detail="Direct file serving not available for this storage type")
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Serve file failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
