from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RAG-based FAQ service for SmartTask documentation",
    version="1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=sorted(settings.BACKEND_CORS_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply static files mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the SmartTask FAQ",
        "documentation": "/docs",
        "api_version": settings.API_V1_STR,
    }

@app.get("/health")
async def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "service": "smart-task-faq",
            "timestamp": __import__("datetime").datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}