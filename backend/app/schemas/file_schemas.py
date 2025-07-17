from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    uploaded_at: str
    chunks_created: int
    vector_ids: List[str]


class FileInfo(BaseModel):
    """Model for file information"""
    filename: str
    original_filename: str
    size: int
    last_modified: str
    content_type: Optional[str] = None


class SearchRequest(BaseModel):
    """Request model for document search"""
    query: str
    n_results: int = 5


class SearchResult(BaseModel):
    """Model for search results"""
    text: str
    metadata: Dict[str, Any]
    distance: Optional[float] = None
    id: Optional[str] = None


class SearchResponse(BaseModel):
    """Response model for search"""
    query: str
    results: List[SearchResult]
    total_results: int


class VectorDocument(BaseModel):
    """Model for vector database documents"""
    id: str
    text: str
    metadata: Dict[str, Any]


class CollectionInfo(BaseModel):
    """Model for collection information"""
    collection_name: str
    document_count: int
    created_at: str


class DeleteRequest(BaseModel):
    """Request model for deleting documents"""
    document_ids: List[str]


class DeleteResponse(BaseModel):
    """Response model for deletion"""
    deleted_count: int
    message: str 