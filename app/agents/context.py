from dataclasses import dataclass

from app.models.pull_request import PullRequest


@dataclass(frozen=True)
class ReviewContext:
    pull_request: PullRequest
    changed_lines: dict[str, frozenset[int]]

    @classmethod
    def from_pull_request(cls, pull_request: PullRequest) -> "ReviewContext":
        changed_lines: dict[str, frozenset[int]] = {}

        for file in pull_request.files:
            line_numbers: set[int] = set()
            for hunk in file.parsed_diff():
                line_number = hunk["new_start"]
                for change in hunk["changes"]:
                    if change["type"] == "added":
                        line_numbers.add(line_number)
                    if change["type"] in ("added", "context"):
                        line_number += 1
            changed_lines[file.path] = frozenset(line_numbers)

        return cls(pull_request=pull_request, changed_lines=changed_lines)

    def as_prompt_text(self) -> str:
        sections = []
        for file in self.pull_request.files:
            sections.append(f"FILE: {file.path}\n{file.patch or '[no patch available]'}")
        return "\n\n".join(sections)
