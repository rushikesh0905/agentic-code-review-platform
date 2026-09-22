from app.models.review import ReviewFinding


def aggregate_findings(findings: list[ReviewFinding]) -> list[ReviewFinding]:
    unique: dict[tuple, ReviewFinding] = {}

    for finding in findings:
        key = (
            finding.file_path,
            finding.line_number,
            finding.category,
            finding.title,
        )
        existing = unique.get(key)
        if existing is None or finding.confidence > existing.confidence:
            unique[key] = finding

    return list(unique.values())
