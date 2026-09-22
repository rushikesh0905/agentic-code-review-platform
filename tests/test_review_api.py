from fastapi.testclient import TestClient

from app.dependencies.common import get_pull_request_service, get_review_orchestrator
from app.main import app
from app.models.pull_request import PullRequest
from app.models.review import ReviewCategory, ReviewFinding, Severity
from app.services.orchestrator import ReviewReport


class FakePullRequestService:
    async def get_review_input(self, owner, repo, pull_number):
        return PullRequest(
            number=pull_number,
            title="Test PR",
            repository=f"{owner}/{repo}",
            author="developer",
            base_branch="main",
            head_branch="feature",
        )


class FakeOrchestrator:
    def review(self, pull_request):
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
                    source="security-agent",
                )
            ]
        )


def test_review_endpoint_returns_structured_report():
    app.dependency_overrides[get_pull_request_service] = lambda: FakePullRequestService()
    app.dependency_overrides[get_review_orchestrator] = lambda: FakeOrchestrator()

    try:
        response = TestClient(app).post("/reviews/example/project/7")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["findings"][0]["source"] == "security-agent"
    assert response.json()["findings"][0]["line_number"] == 2
