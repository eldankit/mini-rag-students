# mini-rag-students

a mini rag system to help students learn by asking on their course materials

## Project Structure

- `backend/` — FastAPI backend (Python, Poetry, Docker-ready)
- `frontend/` — React frontend with i18n support (JavaScript, Create React App, Docker-ready)
- `docker-compose.yml` — Orchestrates both frontend and backend services

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
- **Real-time Status**: Live backend connection indicator
- **API Integration**: Seamless communication between frontend and backend
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

## API Endpoints

- `GET /` - Welcome message
- `GET /api/ping` - Health check endpoint

## Docker Configuration

### Backend Dockerfile
- Python 3.11 with Poetry
- FastAPI with Uvicorn
- Production-ready configuration

### Frontend Dockerfile
- Node.js 18 with multi-stage build
- Nginx for production serving
- API proxy configuration

### Docker Compose
- Network isolation between services
- Environment variable configuration
- Health checks and restart policies

## Future Enhancements

- File upload functionality
- Chat interface for Q&A
- Study analytics dashboard
- User authentication
- Document processing and indexing
- Additional language support (Arabic, Spanish, etc.)

## Troubleshooting

### Common Issues

1. **TypeScript Version Conflicts**: Use `--legacy-peer-deps` when installing frontend dependencies
2. **Port Conflicts**: Ensure ports 3000 and 8000 are available
3. **Docker Build Issues**: Clear Docker cache with `docker system prune -a`

### Development Tips

- Use `npm install --legacy-peer-deps` for frontend dependency installation
- The frontend automatically connects to the backend on localhost:8000
- Language preferences are saved in browser localStorage
- RTL layout automatically activates for Hebrew

---

Feel free to contribute or open issues!
