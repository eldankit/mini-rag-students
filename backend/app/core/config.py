from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "mini-rag-system"
    debug: bool = True
    
    # MinIO Configuration
    minio_endpoint: str = "minio:9000"  # Use Docker service name
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin123"
    minio_bucket_name: str = "documents"
    minio_secure: bool = False  # Set to True for HTTPS
    
    # ChromaDB Configuration
    chromadb_host: str = "chromadb"  # Use Docker service name
    chromadb_port: int = 8000  # Use internal port
    chromadb_collection_name: str = "documents"
    chromadb_tenant: str = "default_tenant"
    chromadb_database: str = "default_database"
    
    # File Upload Configuration
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_file_types: list = ["pdf", "docx", "pptx", "txt"]

settings = Settings() 