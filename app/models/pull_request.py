from pydantic import BaseModel

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

    files: list[PullRequestFile] = []