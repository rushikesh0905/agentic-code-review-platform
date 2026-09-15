from fastapi import APIRouter, Depends

from app.dependencies.common import get_app_name

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/info")
def app_info(app_name: str = Depends(get_app_name)):
    return {"app_name": app_name}