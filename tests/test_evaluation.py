from app.evaluation.metrics import evaluate_findings


def test_evaluation_metrics_calculate_precision_recall_and_f1():
    expected = {
        ("app/auth.py", 10, "security"),
        ("app/db.py", 4, "bug"),
    }
    predicted = {
        ("app/auth.py", 10, "security"),
        ("app/logging.py", 3, "maintainability"),
    }

    metrics = evaluate_findings(predicted, expected)

    assert metrics.true_positives == 1
    assert metrics.false_positives == 1
    assert metrics.false_negatives == 1
    assert metrics.precision == 0.5
    assert metrics.recall == 0.5
    assert metrics.f1 == 0.5


def test_empty_evaluation_has_zero_scores():
    metrics = evaluate_findings(set(), set())

    assert metrics.precision == 0.0
    assert metrics.recall == 0.0
    assert metrics.f1 == 0.0
