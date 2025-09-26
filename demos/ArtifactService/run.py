#!/usr/bin/env python3
"""
Artifact Service Startup Script
"""

import uvicorn
import logging
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting Artifact Service on {settings.api_host}:{settings.api_port}")
    logger.info(f"Storage type: {settings.storage_type}")
    logger.info(f"API documentation available at: http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
