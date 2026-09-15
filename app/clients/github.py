import httpx

from app.config import settings


class GitHubClient:
    def __init__(self):
        self.base_url = settings.github_api_url

        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if settings.github_token:
            self.headers["Authorization"] = (
                f"Bearer {settings.github_token}"
            )

    async def get_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> dict:
        url = (
            f"{self.base_url}/repos/"
            f"{owner}/{repo}/pulls/{pull_number}"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=self.headers,
            )

        response.raise_for_status()

        return response.json()