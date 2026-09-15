import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


client = TestClient(app)


def create_signature(payload: bytes, secret: str) -> str:
    digest = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return f"sha256={digest}"


def test_github_webhook_rejects_invalid_signature():
    response = client.post(
        "/webhooks/github",
        json={"action": "opened"},
        headers={
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": "sha256=invalid",
        },
    )

    assert response.status_code == 401


def test_github_webhook_accepts_valid_signature():
    payload = {
        "action": "opened",
        "repository": {
            "full_name": "example/my-repository",
        },
        "pull_request": {
            "number": 42,
            "title": "Add authentication",
        },
    }

    body = json.dumps(payload).encode()

    signature = create_signature(
        body,
        settings.github_webhook_secret,
    )

    response = client.post(
        "/webhooks/github",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": signature,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["event"] == "pull_request"
    assert data["repository"] == "example/my-repository"
    assert data["pull_request_number"] == 42