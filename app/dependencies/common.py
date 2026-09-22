from app.config import settings
from app.clients.github import GitHubClient
from app.rules.security import (
    DangerousEvalRule,
    DebugPrintRule,
    HardcodedSecretRule,
)
from app.services.orchestrator import ReviewOrchestrator
from app.services.pull_request import PullRequestService
from app.services.review_engine import ReviewEngine


def get_app_name() -> str:
    return settings.app_name


def get_pull_request_service() -> PullRequestService:
    return PullRequestService(GitHubClient())


def get_review_orchestrator() -> ReviewOrchestrator:
    return ReviewOrchestrator(
        review_engine=ReviewEngine(
            rules=[
                HardcodedSecretRule(),
                DangerousEvalRule(),
                DebugPrintRule(),
            ]
        )
    )