import pytest

from app.services.pull_request import PullRequestService


class FakeGitHubClient:
    async def get_pull_request(self, owner, repo, pull_number):
        return {
            "number": pull_number,
            "title": "Add login",
            "body": "Review authentication changes",
            "user": {"login": "developer"},
            "base": {
                "ref": "main",
                "repo": {"full_name": f"{owner}/{repo}"},
            },
            "head": {"ref": "feature/login"},
        }

    async def get_pull_request_files(self, owner, repo, pull_number):
        return [
            {
                "filename": "app/auth.py",
                "status": "modified",
                "additions": 1,
                "deletions": 0,
                "changes": 1,
                "patch": "@@ -1,1 +1,2 @@\n def login():\n+    return True",
            }
        ]


@pytest.mark.anyio
async def test_pull_request_service_builds_domain_model():
    service = PullRequestService(FakeGitHubClient())

    pull_request = await service.get_review_input("example", "project", 7)

    assert pull_request.repository == "example/project"
    assert pull_request.number == 7
    assert pull_request.files[0].path == "app/auth.py"
    assert pull_request.files[0].patch.endswith("return True")
