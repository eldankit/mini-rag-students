# mini-rag-students

a mini rag system to help students learn by asking on their course materials

## Project Structure

- `backend/` — FastAPI backend (Python, Poetry, Docker-ready)
- `docker-compose.yml` — Orchestrates backend (and future frontend) services

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Running the Backend with Docker Compose

From the project root, run:
```sh
docker-compose up --build
```
The FastAPI backend will be available at [http://localhost:8000](http://localhost:8000).

### Development (Backend Only)

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

## Future Plans
- Add a React frontend
- Extend Docker Compose to orchestrate both frontend and backend

---

Feel free to contribute or open issues!
