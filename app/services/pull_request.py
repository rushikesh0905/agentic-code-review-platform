from app.clients.github import GitHubClient


class PullRequestService:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    async def get_review_input(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> dict:
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

        return {
            "pull_request": pull_request,
            "files": files,
        }