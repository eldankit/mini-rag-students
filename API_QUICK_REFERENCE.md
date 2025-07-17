# API Quick Reference Guide

## Base URL
```
http://localhost:8000
```

## Health & Status

### Check Health
```bash
curl http://localhost:8000/health
```
**Response**: `{"status":"healthy","service":"mini-rag-system"}`

### Ping
```bash
curl http://localhost:8000/api/ping
```
**Response**: `{"ping":"pong"}`

## File Management

### Upload File
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/api/files/upload
```
**Response**:
```json
{
  "filename": "uuid.pdf",
  "original_filename": "document.pdf",
  "file_size": 12345,
  "content_type": "application/pdf",
  "uploaded_at": "2025-07-17T19:21:17.847992",
  "chunks_created": 2,
  "vector_ids": ["uuid1", "uuid2"]
}
```

### List Files
```bash
curl http://localhost:8000/api/files/list
```
**Response**:
```json
[
  {
    "filename": "uuid.pdf",
    "original_filename": "document.pdf",
    "size": 12345,
    "last_modified": "2025-07-17T19:21:17.862000+00:00",
    "content_type": "application/pdf"
  }
]
```

### Download File
```bash
curl -O -J http://localhost:8000/api/files/download/uuid.pdf
```
**Response**: File content with proper headers

### Delete File
```bash
curl -X DELETE http://localhost:8000/api/files/files/uuid.pdf
```
**Response**: `{"message":"File uuid.pdf deleted successfully"}`

## Vector Database Operations

### Get Collection Info
```bash
curl http://localhost:8000/api/files/collection-info
```
**Response**:
```json
{
  "collection_name": "documents",
  "document_count": 13,
  "created_at": "2025-07-17T19:21:33.451235"
}
```

### List Documents
```bash
curl "http://localhost:8000/api/files/documents?limit=10"
```
**Response**:
```json
[
  {
    "id": "uuid",
    "text": "document chunk text...",
    "metadata": {
      "filename": "file.ext",
      "chunk_index": 0
    }
  }
]
```

### Search Documents
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "search term", "n_results": 5}' \
  http://localhost:8000/api/files/search
```
**Response**:
```json
{
  "query": "search term",
  "results": [
    {
      "text": "document chunk text",
      "metadata": {
        "filename": "file.ext",
        "original_filename": "original.ext",
        "chunk_index": 0,
        "content_type": "application/pdf"
      },
      "distance": 0.123,
      "id": "uuid"
    }
  ],
  "total_results": 1
}
```

### Delete Documents
```bash
curl -X DELETE -H "Content-Type: application/json" \
  -d '{"document_ids": ["uuid1", "uuid2"]}' \
  http://localhost:8000/api/files/documents
```
**Response**:
```json
{
  "deleted_count": 2,
  "message": "Successfully deleted 2 documents"
}
```

## Search Examples

### English Search
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "American Civil War", "n_results": 3}' \
  http://localhost:8000/api/files/search
```

### Hebrew Search
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "מלחמת האזרחים האמריקאית", "n_results": 3}' \
  http://localhost:8000/api/files/search
```

### Mixed Language Search
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "Chelsea צלסי", "n_results": 3}' \
  http://localhost:8000/api/files/search
```

## File Format Support

### Supported Extensions
- `.txt` - Text files
- `.pdf` - PDF documents
- `.docx` - Word documents
- `.pptx` - PowerPoint presentations

### Content Types
- `text/plain` - Text files
- `application/pdf` - PDF files
- `application/octet-stream` - Word/PowerPoint files

## Error Responses

### File Not Found (404)
```json
{
  "detail": "File filename.ext not found"
}
```

### Invalid File Type (400)
```json
{
  "detail": "File type 'exe' not allowed. Allowed types: ['pdf', 'docx', 'pptx', 'txt']"
}
```

### File Too Large (400)
```json
{
  "detail": "File too large. Maximum size: 50MB"
}
```

### Server Error (500)
```json
{
  "detail": "Upload failed: error message"
}
```

## Testing Commands

### Complete Workflow Test
```bash
# 1. Upload a file
curl -X POST -F "file=@test.pdf" http://localhost:8000/api/files/upload

# 2. List files
curl http://localhost:8000/api/files/list

# 3. Search for content
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "test content", "n_results": 5}' \
  http://localhost:8000/api/files/search

# 4. Download file
curl -O -J http://localhost:8000/api/files/download/uuid.pdf

# 5. Delete file
curl -X DELETE http://localhost:8000/api/files/files/uuid.pdf
```

### Performance Test
```bash
# Test search performance
time curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "test", "n_results": 10}' \
  http://localhost:8000/api/files/search
```

## Browser Access

### Interactive API Documentation
```
http://localhost:8000/docs
```

### Alternative Documentation
```
http://localhost:8000/redoc
```

### MinIO Console
```
http://localhost:9001
```
**Credentials**: minioadmin / minioadmin123

---

**Note**: Replace `uuid` with actual file IDs returned from the API responses. 