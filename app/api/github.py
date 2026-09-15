from fastapi import APIRouter, HTTPException, Request

from app.config import settings
from app.security.github import verify_github_signature

router = APIRouter(prefix="/webhooks", tags=["GitHub"])


@router.post("/github")
async def github_webhook(request: Request):
    payload = await request.body()

    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_github_signature(
        payload,
        signature,
        settings.github_webhook_secret,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature",
        )

    data = await request.json()

    event_type = request.headers.get("X-GitHub-Event")

    repository = data.get("repository", {}).get("full_name")
    pull_request = data.get("pull_request", {})

    return {
        "received": True,
        "event": event_type,
        "repository": repository,
        "action": data.get("action"),
        "pull_request_number": pull_request.get("number"),
        "pull_request_title": pull_request.get("title"),
    }