from fastapi import FastAPI

app = FastAPI(
    title="Agentic Code Review Platform",
    description="AI-powered code review platform for GitHub Pull Requests.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}