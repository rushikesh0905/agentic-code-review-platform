from app.agents.base import ReviewAgent, StructuredModelClient


class SecurityReviewAgent(ReviewAgent):
    name = "security-agent"
    role = "security review agent"

    def __init__(self, client: StructuredModelClient):
        super().__init__(client)
        self.role += ". Focus on secrets, injection, authentication, authorization, and unsafe input handling."


class BugReviewAgent(ReviewAgent):
    name = "bug-agent"
    role = "bug and correctness review agent"

    def __init__(self, client: StructuredModelClient):
        super().__init__(client)
        self.role += ". Focus on incorrect behavior, edge cases, state errors, and broken control flow."


class QualityReviewAgent(ReviewAgent):
    name = "quality-agent"
    role = "code quality and maintainability review agent"

    def __init__(self, client: StructuredModelClient):
        super().__init__(client)
        self.role += ". Focus on maintainability, clarity, duplication, and inappropriate complexity."


class PerformanceReviewAgent(ReviewAgent):
    name = "performance-agent"
    role = "performance review agent"

    def __init__(self, client: StructuredModelClient):
        super().__init__(client)
        self.role += ". Focus on unnecessary work, inefficient data access, and scalability risks."
