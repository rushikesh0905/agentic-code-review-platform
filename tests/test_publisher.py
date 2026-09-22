import pytest

from app.models.pull_request import PullRequest
from app.models.review import ReviewCategory, ReviewFinding, Severity
from app.services.orchestrator import ReviewReport
from app.services.publisher import ReviewPublisher


class FakeGitHubClient:
    def __init__(self):
        self.arguments = None

    async def create_pull_request_review(self, *args):
        self.arguments = args
        return {"id": 123}


def make_pull_request():
    return PullRequest(
        number=1,
        title="Test",
        repository="example/project",
        author="developer",
        base_branch="main",
        head_branch="feature",
        head_sha="abc123",
    )


def make_report():
    return ReviewReport(
        findings=[
            ReviewFinding(
                file_path="app/auth.py",
                line_number=2,
                severity=Severity.HIGH,
                category=ReviewCategory.SECURITY,
                title="Unsafe token handling",
                description="Token is exposed.",
                evidence="return token",
                confidence=0.9,
            ),
            ReviewFinding(
                file_path="app/auth.py",
                severity=Severity.LOW,
                category=ReviewCategory.STYLE,
                title="General concern",
                description="Review manually.",
                evidence="auth module",
                confidence=0.5,
            ),
        ]
    )


@pytest.mark.anyio
async def test_publisher_dry_run_does_not_call_github():
    client = FakeGitHubClient()
    result = await ReviewPublisher(client).publish(
        "example",
        "project",
        1,
        make_pull_request(),
        make_report(),
        dry_run=True,
    )

    assert result["dry_run"] is True
    assert len(result["comments"]) == 1
    assert client.arguments is None


@pytest.mark.anyio
async def test_publisher_creates_github_review():
    client = FakeGitHubClient()
    result = await ReviewPublisher(client).publish(
        "example",
        "project",
        1,
        make_pull_request(),
        make_report(),
    )

    assert result == {"dry_run": False, "review_id": 123}
    assert client.arguments[3] == "abc123"
    assert len(client.arguments[5]) == 1
