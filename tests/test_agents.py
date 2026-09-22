from app.agents.context import ReviewContext
from app.agents.specialized import SecurityReviewAgent
from app.models.pull_request import PullRequest, PullRequestFile


class FakeModelClient:
    def __init__(self, response):
        self.response = response
        self.system_prompt = ""
        self.user_prompt = ""

    def complete_json(self, *, system_prompt, user_prompt):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        return self.response


def make_context():
    pull_request = PullRequest(
        number=1,
        title="Add authentication",
        repository="example/project",
        author="developer",
        base_branch="main",
        head_branch="feature/auth",
        files=[
            PullRequestFile(
                path="app/auth.py",
                status="modified",
                additions=1,
                deletions=0,
                changes=1,
                patch="@@ -1,1 +1,2 @@\n def login():\n+    return token",
            )
        ],
    )
    return ReviewContext.from_pull_request(pull_request)


def test_agent_validates_structured_findings_and_source():
    client = FakeModelClient(
        {
            "findings": [
                {
                    "file_path": "app/auth.py",
                    "line_number": 2,
                    "severity": "high",
                    "category": "security",
                    "title": "Token handling needs review",
                    "description": "A token is returned directly.",
                    "evidence": "return token",
                    "confidence": 0.8,
                }
            ]
        }
    )

    findings = SecurityReviewAgent(client).review(make_context())

    assert len(findings) == 1
    assert findings[0].source == "security-agent"
    assert "FILE: app/auth.py" in client.user_prompt


def test_agent_discards_unsupported_locations_and_missing_evidence():
    client = FakeModelClient(
        {
            "findings": [
                {
                    "file_path": "app/missing.py",
                    "line_number": 2,
                    "severity": "high",
                    "category": "security",
                    "title": "Unknown file",
                    "description": "Not in the diff.",
                    "evidence": "invented",
                    "confidence": 0.8,
                },
                {
                    "file_path": "app/auth.py",
                    "line_number": 999,
                    "severity": "high",
                    "category": "security",
                    "title": "Unknown line",
                    "description": "Not in the diff.",
                    "evidence": "invented",
                    "confidence": 0.8,
                },
                {
                    "file_path": "app/auth.py",
                    "line_number": 2,
                    "severity": "high",
                    "category": "security",
                    "title": "No evidence",
                    "description": "The evidence is missing.",
                    "confidence": 0.8,
                },
            ]
        }
    )

    assert SecurityReviewAgent(client).review(make_context()) == []
