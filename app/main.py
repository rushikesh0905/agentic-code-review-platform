from fastapi import FastAPI

from app.api.github import router as github_router
from app.api.routes import router

app = FastAPI(
    title="Agentic Code Review Platform",
    description="AI-powered code review platform for GitHub Pull Requests.",
    version="0.1.0",
)

app.include_router(router)
app.include_router(github_router)