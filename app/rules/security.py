import re

from app.models.pull_request import PullRequestFile
from app.models.review import ReviewCategory, ReviewFinding, Severity
from app.rules.base import ReviewRule


class HardcodedSecretRule(ReviewRule):
    PATTERN = re.compile(
        r"(password|passwd|secret|api_key|apikey|token)\s*=\s*[\"'][^\"']+[\"']",
        re.IGNORECASE,
    )

    def check(
        self,
        file: PullRequestFile,
    ) -> list[ReviewFinding]:
        findings = []

        if not file.patch:
            return findings

        for hunk in file.parsed_diff():
            line_number = hunk["new_start"]

            for change in hunk["changes"]:
                if change["type"] == "added":
                    content = change["content"]

                    if self.PATTERN.search(content):
                        findings.append(
                            ReviewFinding(
                                file_path=file.path,
                                line_number=line_number,
                                severity=Severity.HIGH,
                                category=ReviewCategory.SECURITY,
                                title="Possible hardcoded secret",
                                description=(
                                    "A credential-like value appears to be "
                                    "hardcoded in the source code."
                                ),
                                suggestion=(
                                    "Use environment variables or a "
                                    "dedicated secret manager."
                                ),
                                confidence=0.90,
                            )
                        )

                if change["type"] in ("added", "context"):
                    line_number += 1

        return findings


class DangerousEvalRule(ReviewRule):
    def check(
        self,
        file: PullRequestFile,
    ) -> list[ReviewFinding]:
        findings = []

        if not file.patch:
            return findings

        for hunk in file.parsed_diff():
            line_number = hunk["new_start"]

            for change in hunk["changes"]:
                if change["type"] == "added":
                    content = change["content"]

                    if "eval(" in content:
                        findings.append(
                            ReviewFinding(
                                file_path=file.path,
                                line_number=line_number,
                                severity=Severity.HIGH,
                                category=ReviewCategory.SECURITY,
                                title="Use of eval()",
                                description=(
                                    "eval() can execute dynamically supplied "
                                    "Python code and may introduce security risks."
                                ),
                                suggestion=(
                                    "Avoid eval() and use a safer, "
                                    "explicit parsing approach."
                                ),
                                confidence=0.95,
                            )
                        )

                if change["type"] in ("added", "context"):
                    line_number += 1

        return findings


class DebugPrintRule(ReviewRule):
    def check(
        self,
        file: PullRequestFile,
    ) -> list[ReviewFinding]:
        findings = []

        if not file.patch:
            return findings

        for hunk in file.parsed_diff():
            line_number = hunk["new_start"]

            for change in hunk["changes"]:
                if change["type"] == "added":
                    content = change["content"].strip()

                    if content.startswith("print("):
                        findings.append(
                            ReviewFinding(
                                file_path=file.path,
                                line_number=line_number,
                                severity=Severity.LOW,
                                category=ReviewCategory.MAINTAINABILITY,
                                title="Debug print statement",
                                description=(
                                    "A print() statement was introduced "
                                    "into the code."
                                ),
                                suggestion=(
                                    "Remove the debug statement or use "
                                    "the application's logging framework."
                                ),
                                confidence=0.85,
                            )
                        )

                if change["type"] in ("added", "context"):
                    line_number += 1

        return findings