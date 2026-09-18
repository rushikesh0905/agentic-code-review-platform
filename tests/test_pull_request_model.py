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


def test_pull_request_file_parses_patch():
    file = PullRequestFile(
        path="app/auth.py",
        status="modified",
        additions=2,
        deletions=1,
        changes=3,
        patch="""@@ -10,3 +10,4 @@
 def login():
-    password = "1234"
+    password = get_password()
+    validate_password(password)
""",
    )

    diff = file.parsed_diff()

    assert len(diff) == 1
    assert diff[0]["old_start"] == 10
    assert diff[0]["new_start"] == 10
    assert diff[0]["changes"][1]["type"] == "removed"
    assert diff[0]["changes"][2]["type"] == "added"