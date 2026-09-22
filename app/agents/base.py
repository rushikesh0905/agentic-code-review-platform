from abc import ABC
from typing import Protocol

from pydantic import BaseModel, Field

from app.agents.context import ReviewContext
from app.models.review import ReviewFinding


class StructuredModelClient(Protocol):
    def complete_json(self, *, system_prompt: str, user_prompt: str) -> object:
        ...


class FindingBatch(BaseModel):
    findings: list[ReviewFinding] = Field(default_factory=list)


class ReviewAgent(ABC):
    name: str
    role: str

    def __init__(self, client: StructuredModelClient):
        self.client = client

    def review(self, context: ReviewContext) -> list[ReviewFinding]:
        response = self.client.complete_json(
            system_prompt=self.system_prompt(),
            user_prompt=context.as_prompt_text(),
        )
        batch = FindingBatch.model_validate(response)
        return self._validate_findings(batch.findings, context)

    def system_prompt(self) -> str:
        return (
            f"You are the {self.role}. Review only the supplied changed code. "
            "Return JSON with a findings array. Every finding must include "
            "specific evidence copied from the diff. Use null for line_number "
            "when the evidence cannot be tied to an added line. Do not invent "
            "files, lines, or code."
        )

    def _validate_findings(
        self,
        findings: list[ReviewFinding],
        context: ReviewContext,
    ) -> list[ReviewFinding]:
        validated = []
        known_files = set(context.changed_lines)

        for finding in findings:
            if finding.file_path not in known_files:
                continue
            if (
                finding.line_number is not None
                and finding.line_number not in context.changed_lines[finding.file_path]
            ):
                continue
            if not finding.evidence:
                continue
            validated.append(finding.model_copy(update={"source": self.name}))

        return validated


class AgentConfigurationError(ValueError):
    pass
