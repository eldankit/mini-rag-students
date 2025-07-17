from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import os
from app.schemas.file_schemas import (
    FileUploadResponse, FileInfo, SearchRequest, SearchResponse,
    VectorDocument, CollectionInfo, DeleteRequest, DeleteResponse, SearchResult
)
from app.services.storage_service import storage_service
from app.services.vector_service import vector_service
from app.services.document_service import document_service
from app.core.config import settings

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file and process it for vector storage
    """
    try:
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        if file_extension not in settings.allowed_file_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{file_extension}' not allowed. Allowed types: {settings.allowed_file_types}"
            )
        
        # Validate file size
        if file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_file_size // (1024*1024)}MB"
            )
        
        # Upload file to storage
        upload_result = await storage_service.upload_file(file)
        
        # Read file content for processing (we need to read it again since storage service consumed it)
        await file.seek(0)  # Reset file pointer
        file_content = await file.read()
        
        # Process file and create chunks
        metadata = {
            'filename': upload_result['filename'],
            'original_filename': upload_result['original_filename'],
            'content_type': upload_result['content_type'],
            'file_size': upload_result['file_size'],
            'uploaded_at': upload_result['uploaded_at']
        }
        
        chunks = await document_service.process_file(
            file_content, file_extension, metadata
        )
        
        # Add chunks to vector database
        vector_ids = await vector_service.add_documents(chunks)
        
        return FileUploadResponse(
            filename=upload_result['filename'],
            original_filename=upload_result['original_filename'],
            file_size=upload_result['file_size'],
            content_type=upload_result['content_type'],
            uploaded_at=upload_result['uploaded_at'],
            chunks_created=len(chunks),
            vector_ids=vector_ids
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/list", response_model=List[FileInfo])
async def list_files():
    """
    List all uploaded files
    """
    try:
        files = await storage_service.list_files()
        return [FileInfo(**file) for file in files]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Search for documents using semantic similarity
    """
    try:
        results = await vector_service.search_documents(
            request.query, request.n_results
        )
        
        search_results = [
            SearchResult(
                text=result['text'],
                metadata=result['metadata'],
                distance=result['distance'],
                id=result['id']
            )
            for result in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=search_results,
            total_results=len(search_results)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/documents", response_model=List[VectorDocument])
async def list_documents(limit: int = 100):
    """
    List documents in the vector database
    """
    try:
        documents = await vector_service.list_documents(limit)
        return [VectorDocument(**doc) for doc in documents]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")


@router.get("/collection-info", response_model=CollectionInfo)
async def get_collection_info():
    """
    Get information about the vector database collection
    """
    try:
        info = await vector_service.get_collection_info()
        return CollectionInfo(**info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get collection info: {str(e)}")


@router.delete("/documents", response_model=DeleteResponse)
async def delete_documents(request: DeleteRequest):
    """
    Delete documents from the vector database
    """
    try:
        success = await vector_service.delete_documents(request.document_ids)
        if success:
            return DeleteResponse(
                deleted_count=len(request.document_ids),
                message=f"Successfully deleted {len(request.document_ids)} documents"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to delete documents")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete documents: {str(e)}")


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """
    Delete a file from storage and its corresponding document chunks from vector database
    """
    try:
        # First, get the document IDs for this file from the vector database
        documents = await vector_service.list_documents(limit=1000)  # Get all documents
        file_document_ids = [
            doc['id'] for doc in documents 
            if doc.get('metadata', {}).get('filename') == filename
        ]
        
        # Delete file from storage
        success = await storage_service.delete_file(filename)
        if not success:
            raise HTTPException(status_code=404, detail=f"File {filename} not found")
        
        # Delete corresponding document chunks from vector database
        if file_document_ids:
            await vector_service.delete_documents(file_document_ids)
            return {
                "message": f"File {filename} and {len(file_document_ids)} document chunks deleted successfully"
            }
        else:
            return {"message": f"File {filename} deleted successfully (no document chunks found)"}
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")


from fastapi.responses import StreamingResponse
import io

@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a file directly
    """
    try:
        # Get file content from MinIO
        file_content = await storage_service.get_file_content(filename)
        
        # Get file metadata for content type
        try:
            head_response = storage_service.s3_client.head_object(
                Bucket=storage_service.bucket_name, 
                Key=filename
            )
            content_type = head_response.get('ContentType', 'application/octet-stream')
        except:
            content_type = 'application/octet-stream'
        
        # Create streaming response
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(file_content))
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File {filename} not found") 