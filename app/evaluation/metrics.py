from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationMetrics:
    true_positives: int
    false_positives: int
    false_negatives: int

    @property
    def precision(self) -> float:
        denominator = self.true_positives + self.false_positives
        return self.true_positives / denominator if denominator else 0.0

    @property
    def recall(self) -> float:
        denominator = self.true_positives + self.false_negatives
        return self.true_positives / denominator if denominator else 0.0

    @property
    def f1(self) -> float:
        if self.precision + self.recall == 0:
            return 0.0
        return 2 * self.precision * self.recall / (self.precision + self.recall)


def evaluate_findings(
    predicted: set[tuple[str, int | None, str]],
    expected: set[tuple[str, int | None, str]],
) -> EvaluationMetrics:
    true_positives = len(predicted & expected)
    return EvaluationMetrics(
        true_positives=true_positives,
        false_positives=len(predicted - expected),
        false_negatives=len(expected - predicted),
    )
