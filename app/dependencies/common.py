from app.config import settings
from app.agents.llm import OpenAICompatibleClient
from app.agents.specialized import (
    BugReviewAgent,
    PerformanceReviewAgent,
    QualityReviewAgent,
    SecurityReviewAgent,
)
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
    agents = []
    if settings.llm_api_key:
        client = OpenAICompatibleClient(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            timeout=settings.llm_timeout,
            retries=settings.llm_retries,
        )
        agents = [
            SecurityReviewAgent(client),
            BugReviewAgent(client),
            QualityReviewAgent(client),
            PerformanceReviewAgent(client),
        ]

    return ReviewOrchestrator(
        review_engine=ReviewEngine(
            rules=[
                HardcodedSecretRule(),
                DangerousEvalRule(),
                DebugPrintRule(),
            ]
        ),
        agents=agents,
    )