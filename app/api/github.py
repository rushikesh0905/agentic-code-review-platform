from fastapi import APIRouter, Request

router = APIRouter(prefix="/webhooks", tags=["GitHub"])


@router.post("/github")
async def github_webhook(request: Request):
    payload = await request.json()

    event_type = request.headers.get("X-GitHub-Event")

    repository = payload.get("repository", {}).get("full_name")
    pull_request = payload.get("pull_request", {})

    return {
        "received": True,
        "event": event_type,
        "repository": repository,
        "action": payload.get("action"),
        "pull_request_number": pull_request.get("number"),
        "pull_request_title": pull_request.get("title"),
    }