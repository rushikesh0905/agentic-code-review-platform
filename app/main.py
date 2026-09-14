from fastapi import FastAPI

from app.api.routes import router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI-powered code review platform for GitHub Pull Requests.",
    version=settings.app_version,
)

app.include_router(router)