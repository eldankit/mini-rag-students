import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime
from app.core.config import settings


class VectorService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.collection_name = settings.chromadb_collection_name
        self.tenant = getattr(settings, 'chromadb_tenant', 'default_tenant')
        self.database = getattr(settings, 'chromadb_database', 'default_database')
    
    def _ensure_client(self):
        """Ensure client is initialized"""
        if self.client is None:
            # Use explicit settings to force v2 API
            chroma_settings = ChromaSettings(
                chroma_api_impl="rest",
                chroma_server_host=settings.chromadb_host,
                chroma_server_http_port=settings.chromadb_port,
                allow_reset=True,
                anonymized_telemetry=False
            )
            
            self.client = chromadb.HttpClient(
                host=settings.chromadb_host,
                port=settings.chromadb_port,
                settings=chroma_settings
            )
    
    def _get_or_create_collection(self):
        """
        Get existing collection or create a new one
        """
        self._ensure_client()
        try:
            # Try to get existing collection
            collection = self.client.get_collection(self.collection_name)
            print(f"Using existing collection: {self.collection_name}")
        except Exception:
            # Create new collection if it doesn't exist
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Document embeddings for RAG system"}
            )
            print(f"Created new collection: {self.collection_name}")
        
        return collection
    
    def _ensure_collection(self):
        """Ensure collection is initialized"""
        if self.collection is None:
            self.collection = self._get_or_create_collection()
    
    async def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Add documents to the vector database
        
        Args:
            documents: List of dicts with keys: 'text', 'metadata', 'filename'
        
        Returns:
            List of document IDs
        """
        self._ensure_collection()
        try:
            texts = [doc['text'] for doc in documents]
            metadatas = [doc['metadata'] for doc in documents]
            ids = [str(uuid.uuid4()) for _ in documents]
            
            # Add documents to collection
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Added {len(documents)} documents to vector database")
            return ids
            
        except Exception as e:
            print(f"Error adding documents to vector database: {str(e)}")
            raise Exception(f"Failed to add documents: {str(e)}")
    
    async def search_documents(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            n_results: Number of results to return
        
        Returns:
            List of similar documents with metadata
        """
        self._ensure_collection()
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'text': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else None,
                        'id': results['ids'][0][i] if results['ids'] and results['ids'][0] else None
                    })
            
            return documents
            
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            raise Exception(f"Failed to search documents: {str(e)}")
    
    async def delete_documents(self, document_ids: List[str]) -> bool:
        """
        Delete documents by their IDs
        
        Args:
            document_ids: List of document IDs to delete
        
        Returns:
            True if successful
        """
        self._ensure_collection()
        try:
            self.collection.delete(ids=document_ids)
            print(f"Deleted {len(document_ids)} documents from vector database")
            return True
            
        except Exception as e:
            print(f"Error deleting documents: {str(e)}")
            raise Exception(f"Failed to delete documents: {str(e)}")
    
    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection
        
        Returns:
            Dictionary with collection information
        """
        self._ensure_collection()
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "created_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting collection info: {str(e)}")
            raise Exception(f"Failed to get collection info: {str(e)}")
    
    async def list_documents(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List documents in the collection
        
        Args:
            limit: Maximum number of documents to return
        
        Returns:
            List of documents with metadata
        """
        self._ensure_collection()
        try:
            results = self.collection.get(limit=limit)
            
            documents = []
            if results['documents']:
                for i, doc in enumerate(results['documents']):
                    documents.append({
                        'id': results['ids'][i],
                        'text': doc[:200] + "..." if len(doc) > 200 else doc,  # Truncate long text
                        'metadata': results['metadatas'][i] if results['metadatas'] else {}
                    })
            
            return documents
            
        except Exception as e:
            print(f"Error listing documents: {str(e)}")
            raise Exception(f"Failed to list documents: {str(e)}")


# Create a singleton instance
vector_service = VectorService() 