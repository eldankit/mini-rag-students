# Backend - Multilingual RAG System

A FastAPI backend for a multilingual Retrieval-Augmented Generation (RAG) system with document processing, vector storage, and semantic search capabilities.

## Features

- **Multilingual Document Processing**: Support for English and Hebrew content
- **Multiple File Formats**: PDF, DOCX, PPTX, and TXT files
- **Vector Database**: ChromaDB for semantic search and document embeddings
- **Object Storage**: MinIO for scalable file storage
- **Semantic Search**: Cross-language search capabilities
- **Document Chunking**: Intelligent text segmentation for better retrieval
- **RESTful API**: Complete CRUD operations for documents and files

## Tech Stack

- **Python 3.11**: Latest stable Python version
- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server for production
- **ChromaDB**: Vector database for embeddings
- **MinIO**: Object storage for files
- **LangChain**: Document processing and chunking
- **Pydantic**: Data validation and settings management
- **Poetry**: Dependency management
- **Docker**: Containerization

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── file_routes.py      # File and document API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Application settings
│   ├── models/
│   │   └── __init__.py         # Data models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── file_schemas.py     # Pydantic schemas for API
│   ├── services/
│   │   ├── __init__.py
│   │   ├── storage_service.py  # MinIO operations
│   │   ├── vector_service.py   # ChromaDB operations
│   │   └── document_service.py # Document processing
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── Dockerfile                  # Docker configuration
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Locked dependencies
└── README.md                   # This file
```

## Getting Started

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker and Docker Compose (for MinIO and ChromaDB)

### Development Setup

1. **Install Poetry** (if not already installed):
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```sh
   poetry install
   ```

3. **Start external services** (MinIO and ChromaDB):
   ```sh
   docker-compose up -d minio chromadb
   ```

4. **Run the development server**:
   ```sh
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### Health and Status
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/ping` - API ping endpoint

### File Management
- `POST /api/files/upload` - Upload documents (PDF, DOCX, PPTX, TXT)
- `GET /api/files/list` - List all uploaded files
- `GET /api/files/download/{file_id}` - Download a file
- `DELETE /api/files/files/{file_id}` - Delete a file

### Document Search and Management
- `POST /api/files/search` - Semantic search across documents
- `GET /api/files/documents` - List processed documents
- `DELETE /api/files/documents/{doc_id}` - Delete a document
- `GET /api/files/collection-info` - Vector database statistics

## Configuration

The system uses environment variables for configuration. Key settings include:

```env
# MinIO Configuration
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=documents
MINIO_SECURE=false

# ChromaDB Configuration
CHROMADB_HOST=localhost
CHROMADB_PORT=8001
CHROMADB_COLLECTION_NAME=documents

# Application Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Document Processing

### Supported Formats
- **PDF**: Extracted using PyPDF2
- **DOCX**: Extracted using python-docx
- **PPTX**: Extracted using python-pptx
- **TXT**: Direct text processing

### Processing Pipeline
1. **File Upload**: Files are stored in MinIO
2. **Text Extraction**: Content is extracted based on file type
3. **Chunking**: Text is split into manageable chunks
4. **Embedding**: Chunks are converted to vector embeddings
5. **Storage**: Embeddings are stored in ChromaDB

### Multilingual Support
- **English**: Full support with semantic search
- **Hebrew**: Full support with right-to-left text handling
- **Mixed Content**: Documents can contain both languages
- **Cross-language Search**: Search in one language, find content in another

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout
- Document functions and classes
- Use Pydantic models for data validation

### Adding New File Types

1. **Update document service** (`app/services/document_service.py`):
   ```python
   def extract_text_from_new_format(file_path: str) -> str:
       # Add extraction logic
       pass
   ```

2. **Update file routes** to handle the new format
3. **Add tests** for the new format

### Adding New Search Features

1. **Extend vector service** (`app/services/vector_service.py`)
2. **Add new endpoints** in file routes
3. **Update schemas** as needed

## Docker Deployment

### Build and Run
```sh
# Build the image
docker build -t mini-rag-backend .

# Run the container
docker run -p 8000:8000 mini-rag-backend
```

### Docker Compose
The complete system runs with:
```sh
docker-compose up --build
```

This includes:
- Backend API (FastAPI)
- Frontend (React)
- MinIO (Object Storage)
- ChromaDB (Vector Database)

## Testing

### Manual Testing
Use the interactive documentation at `/docs` to test all endpoints:

1. **Upload Files**: Test with different file types and languages
2. **Search**: Try semantic searches in English and Hebrew
3. **File Operations**: Test download and delete operations

### API Testing Examples

```bash
# Upload a file
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"

# Search documents
curl -X POST "http://localhost:8000/api/files/search" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"query": "basketball", "limit": 5}'

# List files
curl -X GET "http://localhost:8000/api/files/list"
```

## Performance Considerations

- **Chunking Strategy**: Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` for optimal retrieval
- **Vector Search**: ChromaDB provides fast similarity search
- **File Storage**: MinIO scales horizontally for large file collections
- **Caching**: Consider implementing Redis for frequently accessed data

## Troubleshooting

### Common Issues

1. **ChromaDB Connection Issues**
   - Ensure ChromaDB is running: `docker ps | grep chromadb`
   - Check port 8001 is available
   - Verify collection exists

2. **MinIO Connection Issues**
   - Ensure MinIO is running: `docker ps | grep minio`
   - Check credentials in configuration
   - Verify bucket exists

3. **File Upload Failures**
   - Check file size limits
   - Verify supported file formats
   - Check MinIO bucket permissions

4. **Search Not Working**
   - Ensure documents are properly processed
   - Check ChromaDB collection has embeddings
   - Verify search query format

### Debug Mode
Enable debug logging by setting `DEBUG=True` in your environment.

## Production Deployment

### Security Considerations
- Use HTTPS in production
- Implement proper authentication
- Secure MinIO and ChromaDB access
- Validate all file uploads
- Set appropriate file size limits

### Scaling
- Use multiple MinIO instances for high availability
- Consider ChromaDB clustering for large datasets
- Implement load balancing for the API
- Use Redis for session management

## Contributing

1. Follow the existing code structure
2. Add proper type hints and docstrings
3. Test with multiple file types and languages
4. Update documentation for new features
5. Ensure backward compatibility

## License

MIT License - see main project README for details. 