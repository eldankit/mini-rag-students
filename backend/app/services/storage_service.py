import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException, UploadFile
import uuid
from datetime import datetime
from typing import Optional, List
import os
from app.core.config import settings


class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=f"http://{settings.minio_endpoint}",
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
            region_name='us-east-1'  # MinIO doesn't require a specific region
        )
        self.bucket_name = settings.minio_bucket_name
    
    async def upload_file(self, file: UploadFile) -> dict:
        """
        Upload a file to MinIO storage
        """
        try:
            # Generate unique filename
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Read file content first
            file_content = await file.read()
            
            # Upload file using bytes
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=file_content,
                ContentType=file.content_type
            )
            
            return {
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_size": len(file_content),
                "content_type": file.content_type,
                "uploaded_at": datetime.utcnow().isoformat()
            }
            
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="Storage credentials not configured")
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Storage error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    async def get_file_url(self, filename: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for file download
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': filename},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    
    async def get_file_content(self, filename: str) -> bytes:
        """
        Get file content as bytes
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
            return response['Body'].read()
        except ClientError as e:
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    
    async def delete_file(self, filename: str) -> bool:
        """
        Delete a file from storage
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError as e:
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    
    async def list_files(self) -> List[dict]:
        """
        List all files in the bucket
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            files = []
            
            if 'Contents' in response:
                for obj in response['Contents']:
                    # Try to get object metadata for content type
                    try:
                        head_response = self.s3_client.head_object(Bucket=self.bucket_name, Key=obj['Key'])
                        content_type = head_response.get('ContentType', 'application/octet-stream')
                    except:
                        content_type = 'application/octet-stream'
                    
                    files.append({
                        "filename": obj['Key'],
                        "original_filename": obj['Key'],  # For now, use filename as original
                        "size": obj['Size'],
                        "last_modified": obj['LastModified'].isoformat(),
                        "content_type": content_type
                    })
            
            return files
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


# Create a singleton instance
storage_service = StorageService() 