from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
from config import settings
import asyncio
import aiosqlite


# Create async engine for SQLite
engine = create_async_engine(
    settings.database_url.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=False
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class ArtifactRepository:
    """Repository class for artifact operations"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def create_artifact(self, artifact_data: dict) -> "Artifact":
        """Create a new artifact record"""
        from models import Artifact
        artifact = Artifact(**artifact_data)
        self.db.add(artifact)
        await self.db.commit()
        await self.db.refresh(artifact)
        return artifact
    
    async def get_artifact_by_id(self, artifact_id: int) -> "Artifact":
        """Get artifact by ID"""
        from models import Artifact
        from sqlalchemy import select
        result = await self.db.execute(
            select(Artifact).where(Artifact.id == artifact_id)
        )
        return result.scalar_one_or_none()
    
    async def get_artifact_by_name(self, name: str) -> "Artifact":
        """Get artifact by name"""
        from models import Artifact
        from sqlalchemy import select
        result = await self.db.execute(
            select(Artifact).where(Artifact.name == name)
        )
        return result.scalar_one_or_none()
    
    async def list_artifacts(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """List artifacts with pagination"""
        from models import Artifact
        from sqlalchemy import select, func
        offset = (page - 1) * page_size
        
        # Get total count
        count_result = await self.db.execute(select(func.count(Artifact.id)))
        total = count_result.scalar()
        
        # Get paginated results
        result = await self.db.execute(
            select(Artifact).order_by(Artifact.created_at.desc()).limit(page_size).offset(offset)
        )
        artifacts = result.scalars().all()
        
        return artifacts, total
    
    async def delete_artifact(self, artifact_id: int) -> bool:
        """Delete artifact by ID"""
        from models import Artifact
        from sqlalchemy import delete
        result = await self.db.execute(
            delete(Artifact).where(Artifact.id == artifact_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def update_artifact(self, artifact_id: int, update_data: dict) -> "Artifact":
        """Update artifact"""
        from models import Artifact
        from sqlalchemy import update
        
        await self.db.execute(
            update(Artifact).where(Artifact.id == artifact_id).values(**update_data)
        )
        await self.db.commit()
        
        return await self.get_artifact_by_id(artifact_id)
