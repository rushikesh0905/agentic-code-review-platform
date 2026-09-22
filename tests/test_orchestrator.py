from app.agents.context import ReviewContext
from app.agents.base import ReviewAgent
from app.models.pull_request import PullRequest
from app.models.review import ReviewCategory, ReviewFinding, Severity
from app.services.orchestrator import ReviewOrchestrator


class StaticAgent(ReviewAgent):
    name = "static-agent"
    role = "test agent"

    def __init__(self, findings=None, error=None):
        self.findings = findings or []
        self.error = error

    def review(self, context: ReviewContext):
        if self.error:
            raise self.error
        return self.findings


def make_pull_request():
    return PullRequest(
        number=1,
        title="Test",
        repository="example/project",
        author="developer",
        base_branch="main",
        head_branch="feature",
    )


def finding(confidence):
    return ReviewFinding(
        file_path="app/auth.py",
        line_number=2,
        severity=Severity.HIGH,
        category=ReviewCategory.SECURITY,
        title="Unsafe token handling",
        description="Token is exposed.",
        evidence="return token",
        confidence=confidence,
    )


def test_orchestrator_deduplicates_and_keeps_highest_confidence():
    report = ReviewOrchestrator(
        agents=[StaticAgent([finding(0.6)]), StaticAgent([finding(0.9)])]
    ).review(make_pull_request())

    assert len(report.findings) == 1
    assert report.findings[0].confidence == 0.9
    assert report.agent_errors == {}


def test_orchestrator_isolates_agent_failures():
    report = ReviewOrchestrator(
        agents=[StaticAgent(error=RuntimeError("provider unavailable"))]
    ).review(make_pull_request())

    assert report.findings == []
    assert report.agent_errors == {"static-agent": "provider unavailable"}
