from abc import ABC, abstractmethod

from app.models.pull_request import PullRequestFile
from app.models.review import ReviewFinding


class ReviewRule(ABC):
    @abstractmethod
    def check(
        self,
        file: PullRequestFile,
    ) -> list[ReviewFinding]:
        pass