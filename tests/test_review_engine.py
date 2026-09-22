from app.models.pull_request import PullRequest, PullRequestFile
from app.rules.security import (
    DangerousEvalRule,
    DebugPrintRule,
    HardcodedSecretRule,
)
from app.services.review_engine import ReviewEngine


def test_review_engine_detects_issues():
    patch = """@@ -1,2 +1,5 @@
 def login():
+    password = "secret123"
+    result = eval(user_input)
+    print(result)
"""

    file = PullRequestFile(
        path="app/auth.py",
        status="modified",
        additions=3,
        deletions=0,
        changes=3,
        patch=patch,
    )

    pr = PullRequest(
        number=1,
        title="Test PR",
        repository="example/project",
        author="developer",
        base_branch="main",
        head_branch="feature",
        files=[file],
    )

    engine = ReviewEngine(
        rules=[
            HardcodedSecretRule(),
            DangerousEvalRule(),
            DebugPrintRule(),
        ]
    )

    findings = engine.review(pr)

    assert len(findings) == 3

    titles = {finding.title for finding in findings}

    assert "Possible hardcoded secret" in titles
    assert "Use of eval()" in titles
    assert "Debug print statement" in titles