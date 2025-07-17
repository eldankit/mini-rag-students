from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name, 
    debug=settings.debug,
    description="A RAG system with file upload, storage, and vector search capabilities"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to the {settings.app_name} FastAPI backend!",
        "version": "1.0.0",
        "features": [
            "File upload and storage",
            "Document processing and chunking", 
            "Vector database search",
            "MinIO storage integration",
            "ChromaDB vector database"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.app_name} 