import re


HUNK_PATTERN = re.compile(
    r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@"
)


def parse_patch(patch: str) -> list[dict]:
    lines = patch.splitlines()

    hunks = []
    current_hunk = None

    for line in lines:
        match = HUNK_PATTERN.match(line)

        if match:
            if current_hunk:
                hunks.append(current_hunk)

            old_start = int(match.group(1))
            old_count = int(match.group(2) or 1)

            new_start = int(match.group(3))
            new_count = int(match.group(4) or 1)

            current_hunk = {
                "old_start": old_start,
                "old_count": old_count,
                "new_start": new_start,
                "new_count": new_count,
                "changes": [],
            }

            continue

        if current_hunk is None:
            continue

        if line.startswith("+") and not line.startswith("+++"):
            current_hunk["changes"].append(
                {
                    "type": "added",
                    "content": line[1:],
                }
            )

        elif line.startswith("-") and not line.startswith("---"):
            current_hunk["changes"].append(
                {
                    "type": "removed",
                    "content": line[1:],
                }
            )

        elif line.startswith(" "):
            current_hunk["changes"].append(
                {
                    "type": "context",
                    "content": line[1:],
                }
            )

    if current_hunk:
        hunks.append(current_hunk)

    return hunks