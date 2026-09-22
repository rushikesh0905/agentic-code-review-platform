from app.models.pull_request import PullRequest
from app.models.review import ReviewFinding
from app.rules.base import ReviewRule


class ReviewEngine:
    def __init__(self, rules: list[ReviewRule]):
        self.rules = rules

    def review(self, pull_request: PullRequest) -> list[ReviewFinding]:
        findings = []

        for file in pull_request.files:
            for rule in self.rules:
                findings.extend(rule.check(file))

        return findings
    