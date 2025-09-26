import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional
from .base import StorageAdapter
from config import settings
import logging

logger = logging.getLogger(__name__)


class S3StorageAdapter(StorageAdapter):
    """S3-compatible object storage adapter"""
    
    def __init__(self, 
                 bucket_name: str = None,
                 endpoint_url: str = None,
                 access_key_id: str = None,
                 secret_access_key: str = None,
                 region: str = None):
        
        self.bucket_name = bucket_name or settings.s3_bucket_name
        self.endpoint_url = endpoint_url or settings.s3_endpoint_url
        self.access_key_id = access_key_id or settings.s3_access_key_id
        self.secret_access_key = secret_access_key or settings.s3_secret_access_key
        self.region = region or settings.s3_region
        
        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region
        )
        
        # Ensure bucket exists
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure the S3 bucket exists"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Bucket doesn't exist, create it
                try:
                    if self.region == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.region}
                        )
                    logger.info(f"Created S3 bucket: {self.bucket_name}")
                except ClientError as create_error:
                    logger.error(f"Failed to create S3 bucket: {create_error}")
                    raise
            else:
                logger.error(f"Error checking S3 bucket: {e}")
                raise
    
    async def upload_file(self, file_content: bytes, file_path: str, content_type: Optional[str] = None) -> str:
        """Upload file to S3"""
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_path,
                Body=file_content,
                **extra_args
            )
            
            logger.info(f"Successfully uploaded file to S3: {file_path}")
            return file_path
            
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise
        except NoCredentialsError:
            logger.error("S3 credentials not found")
            raise
    
    async def download_file(self, storage_path: str) -> bytes:
        """Download file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=storage_path
            )
            return response['Body'].read()
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise FileNotFoundError(f"File not found: {storage_path}")
            logger.error(f"Failed to download file from S3: {e}")
            raise
    
    async def delete_file(self, storage_path: str) -> bool:
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=storage_path
            )
            logger.info(f"Successfully deleted file from S3: {storage_path}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            return False
    
    async def file_exists(self, storage_path: str) -> bool:
        """Check if file exists in S3"""
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=storage_path
            )
            return True
            
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            logger.error(f"Error checking file existence in S3: {e}")
            raise
    
    async def get_file_url(self, storage_path: str, expires_in: Optional[int] = None) -> str:
        """Get presigned URL for file access"""
        try:
            expires_in = expires_in or 3600  # Default 1 hour
            
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': storage_path},
                ExpiresIn=expires_in
            )
            
            return url
            
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise
    
    async def get_file_size(self, storage_path: str) -> int:
        """Get file size from S3"""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=storage_path
            )
            return response['ContentLength']
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise FileNotFoundError(f"File not found: {storage_path}")
            logger.error(f"Failed to get file size from S3: {e}")
            raise
