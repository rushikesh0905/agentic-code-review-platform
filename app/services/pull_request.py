from app.clients.github import GitHubClient
from app.models.pull_request import PullRequest, PullRequestFile


class PullRequestService:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    async def get_review_input(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> PullRequest:
        pull_request = await self.github_client.get_pull_request(
            owner,
            repo,
            pull_number,
        )

        files = await self.github_client.get_pull_request_files(
            owner,
            repo,
            pull_number,
        )

        return PullRequest(
            number=pull_request["number"],
            title=pull_request["title"],
            description=pull_request.get("body"),
            repository=pull_request["base"]["repo"]["full_name"],
            author=pull_request["user"]["login"],
            base_branch=pull_request["base"]["ref"],
            head_branch=pull_request["head"]["ref"],
            files=[
                PullRequestFile(
                    path=file["filename"],
                    status=file["status"],
                    additions=file["additions"],
                    deletions=file["deletions"],
                    changes=file["changes"],
                    patch=file.get("patch"),
                )
                for file in files
            ],
        )