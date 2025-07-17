from fastapi import APIRouter
from app.api.file_routes import router as file_router

router = APIRouter()

@router.get("/ping")
def ping():
    return {"ping": "pong"}

# Include file routes
router.include_router(file_router) 