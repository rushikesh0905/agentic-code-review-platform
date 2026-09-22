from pydantic import BaseModel, Field

from app.parsers.diff import parse_patch


class PullRequestFile(BaseModel):
    path: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: str | None = None

    def parsed_diff(self) -> list[dict]:
        if not self.patch:
            return []

        return parse_patch(self.patch)


class PullRequest(BaseModel):
    number: int
    title: str
    description: str | None = None

    repository: str
    author: str

    base_branch: str
    head_branch: str
    head_sha: str | None = None

    files: list[PullRequestFile] = Field(default_factory=list)