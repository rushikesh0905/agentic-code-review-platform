from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ReviewCategory(str, Enum):
    BUG = "bug"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    MAINTAINABILITY = "maintainability"


class ReviewFinding(BaseModel):
    file_path: str
    line_number: int | None = None

    severity: Severity
    category: ReviewCategory

    title: str
    description: str
    evidence: str | None = None

    suggestion: str | None = None

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    source: str = "deterministic"