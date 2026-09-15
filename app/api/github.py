from fastapi import APIRouter, Request

router = APIRouter(prefix="/webhooks", tags=["GitHub"])


@router.post("/github")
async def github_webhook(request: Request):
    payload = await request.json()

    event_type = request.headers.get("X-GitHub-Event")

    return {
        "received": True,
        "event": event_type,
        "repository": payload.get("repository", {}).get("full_name"),
        "action": payload.get("action"),
    }