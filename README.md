# mini-rag-students

a mini rag system to help students learn by asking on their course materials

## Project Structure

- `backend/` — FastAPI backend (Python, Poetry, Docker-ready)
- `frontend/` — React frontend with i18n support (JavaScript, Create React App, Docker-ready)
- `docker-compose.yml` — Orchestrates both frontend and backend services

## How it Works

- **Upload**: Students upload course materials (PDF, DOCX, PPTX, TXT)
- **Processing**: Backend extracts text, chunks it, and generates vector embeddings
- **Storage**: Files are stored in MinIO (object storage); embeddings in ChromaDB (vector DB)
- **Search**: Students ask questions in English or Hebrew; the system performs cross-language semantic search and returns relevant content

## Features

### 🌍 Internationalization (i18n)
- **Multi-language Support**: English and Hebrew
- **RTL Layout**: Automatic right-to-left layout for Hebrew
- **Language Switcher**: Easy toggle between languages in the header
- **Auto-detection**: Detects browser language preference
- **Persistence**: Remembers language choice in localStorage

### 🎨 Modern UI
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Glassmorphism Effects**: Modern glass-like UI elements
- **Gradient Backgrounds**: Beautiful visual design
- **Smooth Animations**: Hover effects and transitions

### 🔧 Technical Features
- **MinIO Object Storage**: All uploaded files are stored in MinIO for scalability and reliability
- **ChromaDB Vector Database**: All document embeddings are stored in ChromaDB for fast semantic search
- **Document Processing Pipeline**: Supports PDF, DOCX, PPTX, and TXT; extracts, chunks, and embeds text
- **Multilingual Semantic Search**: Search in English or Hebrew and retrieve relevant content in either language
- **Cross-language Retrieval**: Ask in one language, find answers in another
- **Real-time Status**: Live backend connection indicator with automatic health checks
- **API Integration**: Seamless communication between frontend and backend
- **CORS Configuration**: Properly configured for cross-origin requests
- **Docker Ready**: Full containerization for easy deployment
- **Development Mode**: Hot reload for both frontend and backend

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Running the Full Stack with Docker Compose

From the project root, run:
```sh
docker-compose up --build
```

This will start both services:
- **Frontend**: Available at [http://localhost:3000](http://localhost:3000)
- **Backend**: Available at [http://localhost:8000](http://localhost:8000)

The frontend will automatically connect to the backend and display the connection status.

### Development Setup

#### Backend Development
1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Install dependencies (requires [Poetry](https://python-poetry.org/)):
   ```sh
   poetry install
   ```
3. Run the development server:
   ```sh
   poetry run uvicorn app.main:app --reload
   ```

#### Frontend Development
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install --legacy-peer-deps
   ```
3. Start the development server:
   ```sh
   npm start
   ```

## Language Support

### Available Languages
- **English (en)**: Default language
- **Hebrew (he)**: Full RTL support with Hebrew translations

### Adding New Languages
1. Create a new translation file in `frontend/src/locales/` (e.g., `fr.json`)
2. Add the language to the i18n configuration in `frontend/src/i18n.js`
3. Update the LanguageSwitcher component to include the new language

### Translation Structure
```json
{
  "header": {
    "title": "🎓 Mini RAG System",
    "subtitle": "Learn smarter with AI-powered course material assistance"
  },
  "status": {
    "title": "System Status",
    "connected": "Connected",
    "disconnected": "Disconnected"
  }
}
```

## Documentation

- **[Complete Documentation](DOCUMENTATION.md)** - Comprehensive system documentation
- **[API Quick Reference](API_QUICK_REFERENCE.md)** - Fast API endpoint reference
- **[Changelog](CHANGELOG.md)** - Version history and changes

## API Endpoints

- `GET /` - Welcome message
- `GET /api/ping` - Health check endpoint
- `POST /api/files/upload` - Upload and process files (PDF, DOCX, PPTX, TXT)
- `GET /api/files/list` - List all uploaded files
- `GET /api/files/download/{file_id}` - Download file directly by file ID
- `DELETE /api/files/files/{file_id}` - Delete file from storage by file ID
- `GET /api/files/collection-info` - Get vector database collection info
- `GET /api/files/documents` - List vectorized documents
- `POST /api/files/search` - Semantic search across documents (cross-language)
- `DELETE /api/files/documents/{doc_id}` - Delete document from vector database by document ID

## Docker Configuration

### Backend Dockerfile
- Python 3.11 with Poetry
- FastAPI with Uvicorn
- Production-ready configuration
- MinIO and ChromaDB integration

### Frontend Dockerfile
- Node.js 18 with multi-stage build
- Nginx for production serving
- API proxy configuration

### Docker Compose
- Network isolation between services
- Environment variable configuration
- Health checks and restart policies
- MinIO and ChromaDB as microservices

## Future Enhancements

- Chat interface for Q&A
- Study analytics dashboard
- User authentication
- Additional language support (Arabic, Spanish, etc.)

## Troubleshooting

### Common Issues

1. **TypeScript Version Conflicts**: Use `--legacy-peer-deps` when installing frontend dependencies
2. **Port Conflicts**: Ensure ports 3000 and 8000 are available
3. **Docker Build Issues**: Clear Docker cache with `docker system prune -a`

### Backend Connection Issues

**Problem**: Frontend shows "Backend: Disconnected" even when backend is running

**Solution**: This was a common issue where the frontend was trying to connect to the Docker service name instead of localhost. The fix has been implemented:

1. **Frontend URL Configuration**: The React app now uses `http://localhost:8000` for browser requests
2. **CORS Configuration**: Backend includes proper CORS middleware to allow frontend requests
3. **Health Check**: Frontend automatically checks backend status on load

**If you still see connection issues**:
1. Ensure both containers are running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Test backend directly: `curl http://localhost:8000/api/ping`
4. Rebuild containers: `docker-compose down && docker-compose up --build`

### Development Tips

- Use `npm install --legacy-peer-deps` for frontend dependency installation
- The frontend automatically connects to the backend on localhost:8000
- Language preferences are saved in browser localStorage
- RTL layout automatically activates for Hebrew
- Backend connection status is displayed in real-time on the frontend

---

Feel free to contribute or open issues!
