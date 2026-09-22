from pydantic import BaseModel, Field

from app.agents.base import ReviewAgent
from app.agents.context import ReviewContext
from app.models.pull_request import PullRequest
from app.models.review import ReviewFinding
from app.services.aggregator import aggregate_findings
from app.services.review_engine import ReviewEngine


class ReviewReport(BaseModel):
    findings: list[ReviewFinding] = Field(default_factory=list)
    agent_errors: dict[str, str] = Field(default_factory=dict)


class ReviewOrchestrator:
    def __init__(
        self,
        *,
        review_engine: ReviewEngine | None = None,
        agents: list[ReviewAgent] | None = None,
    ):
        self.review_engine = review_engine
        self.agents = agents or []

    def review(self, pull_request: PullRequest) -> ReviewReport:
        context = ReviewContext.from_pull_request(pull_request)
        findings: list[ReviewFinding] = []
        errors: dict[str, str] = {}

        if self.review_engine is not None:
            findings.extend(self.review_engine.review(pull_request))

        for agent in self.agents:
            try:
                findings.extend(agent.review(context))
            except Exception as error:
                errors[agent.name] = str(error)

        return ReviewReport(
            findings=aggregate_findings(findings),
            agent_errors=errors,
        )
