from fastapi import FastAPI

from backend.config.settings import settings


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the AI-powered SOC Copilot",
    version=settings.app_version
)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
