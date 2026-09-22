from app.clients.github import GitHubClient
from app.models.pull_request import PullRequest
from app.services.orchestrator import ReviewReport


class ReviewPublisher:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    async def publish(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        pull_request: PullRequest,
        report: ReviewReport,
        *,
        dry_run: bool = False,
    ) -> dict:
        if not pull_request.head_sha:
            raise ValueError("Pull request head commit is required for publishing")

        comments = [
            {
                "path": finding.file_path,
                "line": finding.line_number,
                "side": "RIGHT",
                "body": self._format_finding(finding),
            }
            for finding in report.findings
            if finding.line_number is not None
        ]
        body = f"Agentic Code Review\n\n{len(report.findings)} finding(s) detected."

        if dry_run:
            return {"dry_run": True, "comments": comments, "body": body}

        result = await self.github_client.create_pull_request_review(
            owner,
            repo,
            pull_number,
            pull_request.head_sha,
            body,
            comments,
        )
        return {"dry_run": False, "review_id": result.get("id")}

    @staticmethod
    def _format_finding(finding) -> str:
        suggestion = f"\n\nSuggestion: {finding.suggestion}" if finding.suggestion else ""
        return f"**{finding.title}**\n\n{finding.description}\n\nEvidence: `{finding.evidence}`{suggestion}"