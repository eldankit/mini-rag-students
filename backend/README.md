# Backend - Mini RAG System

A FastAPI backend for the Mini RAG System with modern Python tooling and Docker support.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **Poetry**: Dependency management and packaging
- **Docker**: Containerized deployment
- **Environment Configuration**: Flexible settings with .env support
- **Health Checks**: Built-in API endpoints for monitoring

## Tech Stack

- **Python 3.11**: Latest stable Python version
- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server for production
- **Pydantic**: Data validation and settings management
- **Poetry**: Dependency management
- **Docker**: Containerization

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Application settings
│   ├── models/                # Database models (future)
│   │   └── __init__.py
│   ├── schemas/               # Pydantic schemas (future)
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py                # FastAPI application
├── .env                       # Environment variables (not in git)
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker configuration
├── pyproject.toml             # Poetry configuration
├── poetry.lock                # Locked dependencies
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Python 3.9+ (3.11 recommended)
- [Poetry](https://python-poetry.org/docs/#installation)

### Development Setup

1. **Install Poetry** (if not already installed):
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```sh
   poetry install
   ```

3. **Set up environment variables**:
   ```sh
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the development server**:
   ```sh
   poetry run uvicorn app.main:app --reload
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# Application settings
APP_NAME=mini-rag-system
DEBUG=True

# Add more environment variables as needed
# DATABASE_URL=postgresql://user:password@localhost/dbname
# SECRET_KEY=your-secret-key-here
```

## API Endpoints

### Health Check
- `GET /` - Welcome message
- `GET /api/ping` - Health check endpoint

### Future Endpoints
- `POST /api/upload` - File upload
- `POST /api/chat` - Chat with RAG system
- `GET /api/analytics` - Study analytics

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes
- Use Pydantic models for data validation

### Adding New Endpoints

1. **Create a new route in `app/api/routes.py`**:
   ```python
   from fastapi import APIRouter
   
   router = APIRouter()
   
   @router.get("/new-endpoint")
   async def new_endpoint():
       return {"message": "New endpoint"}
   ```

2. **Register the router in `app/main.py`**:
   ```python
   from app.api.routes import router as api_router
   
   app.include_router(api_router, prefix="/api")
   ```

### Adding Dependencies

1. **Add to pyproject.toml**:
   ```toml
   [tool.poetry.dependencies]
   python = ">=3.9,<3.13"
   fastapi = "^0.111.0"
   new-dependency = "^1.0.0"
   ```

2. **Install**:
   ```sh
   poetry install
   ```

## Docker Deployment

### Build and Run
```sh
# Build the image
docker build -t mini-rag-backend .

# Run the container
docker run -p 8000:8000 mini-rag-backend
```

### Docker Compose
The backend is configured to run with the frontend using Docker Compose:
```sh
docker-compose up --build
```

### Environment Variables in Docker
Set environment variables in docker-compose.yml:
```yaml
services:
  backend:
    environment:
      - APP_NAME=mini-rag-system
      - DEBUG=False
```

## Production Deployment

### Environment Variables
- Set `DEBUG=False` in production
- Configure proper `SECRET_KEY`
- Set up database connections
- Configure CORS settings

### Security Considerations
- Use HTTPS in production
- Implement proper authentication
- Validate all input data
- Use environment variables for secrets

## Testing

### Running Tests
```sh
# Install test dependencies
poetry install --with dev

# Run tests
poetry run pytest
```

### API Testing
Use the interactive documentation at `/docs` or tools like:
- [Postman](https://www.postman.com/)
- [curl](https://curl.se/)
- [httpie](https://httpie.io/)

## Troubleshooting

### Common Issues

1. **Poetry Installation Issues**
   - Ensure Python 3.9+ is installed
   - Check Poetry installation: `poetry --version`
   - Clear Poetry cache: `poetry cache clear . --all`

2. **Port Already in Use**
   - Check if port 8000 is available: `lsof -i :8000`
   - Use different port: `uvicorn app.main:app --port 8001`

3. **Import Errors**
   - Ensure you're in the backend directory
   - Check Poetry environment: `poetry env info`
   - Reinstall dependencies: `poetry install --sync`

### Performance Tips

- Use async functions for I/O operations
- Implement proper caching strategies
- Monitor API response times
- Use connection pooling for databases

## Contributing

1. Follow the existing code structure
2. Add proper type hints
3. Include docstrings for new functions
4. Update this README for new features
5. Test your changes thoroughly

## License

MIT License - see main project README for details. 