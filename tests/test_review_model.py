import pytest
from pydantic import ValidationError

from app.models.review import (
    ReviewCategory,
    ReviewFinding,
    Severity,
)


def test_review_finding():
    finding = ReviewFinding(
        file_path="auth.py",
        line_number=15,
        severity=Severity.HIGH,
        category=ReviewCategory.SECURITY,
        title="Hardcoded password",
        description="Password is stored in source code.",
        suggestion="Use a secure secret store.",
        confidence=0.96,
    )

    assert finding.file_path == "auth.py"
    assert finding.severity == Severity.HIGH
    assert finding.category == ReviewCategory.SECURITY
    assert finding.confidence == 0.96


def test_confidence_must_be_between_zero_and_one():
    with pytest.raises(ValidationError):
        ReviewFinding(
            file_path="auth.py",
            severity=Severity.HIGH,
            category=ReviewCategory.SECURITY,
            title="Test",
            description="Test",
            confidence=1.5,
        )