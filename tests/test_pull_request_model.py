from app.models.pull_request import PullRequest, PullRequestFile


def test_pull_request_model():
    file = PullRequestFile(
        path="app/auth.py",
        status="modified",
        additions=10,
        deletions=3,
        changes=13,
        patch="@@ -1 +1 @@",
    )

    pr = PullRequest(
        number=42,
        title="Add authentication",
        description="Implement authentication",
        repository="example/project",
        author="developer",
        base_branch="main",
        head_branch="feature/auth",
        files=[file],
    )

    assert pr.number == 42
    assert pr.title == "Add authentication"
    assert pr.files[0].path == "app/auth.py"
    assert pr.files[0].additions == 10