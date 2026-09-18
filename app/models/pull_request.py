from pydantic import BaseModel


class PullRequestFile(BaseModel):
    path: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: str | None = None


class PullRequest(BaseModel):
    number: int
    title: str
    description: str | None = None

    repository: str
    author: str

    base_branch: str
    head_branch: str

    files: list[PullRequestFile] = []