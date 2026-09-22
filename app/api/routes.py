from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.common import get_app_name
from app.dependencies.common import (
    get_pull_request_service,
    get_review_orchestrator,
)
from app.services.orchestrator import ReviewOrchestrator
from app.services.pull_request import PullRequestService

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/info")
def app_info(app_name: str = Depends(get_app_name)):
    return {"app_name": app_name}


@router.post(
    "/reviews/{owner}/{repo}/{pull_number}",
    tags=["Reviews"],
)
async def review_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
    pull_request_service: PullRequestService = Depends(get_pull_request_service),
    orchestrator: ReviewOrchestrator = Depends(get_review_orchestrator),
):
    try:
        pull_request = await pull_request_service.get_review_input(
            owner,
            repo,
            pull_number,
        )
        return orchestrator.review(pull_request)
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch or review the pull request",
        ) from error