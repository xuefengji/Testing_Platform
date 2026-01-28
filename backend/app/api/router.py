from fastapi import APIRouter
from app.api.v1.api import router as api_router
from app.api.v1.user import rouer as user_router

router = APIRouter(prefix="/api/v1")
router.include_router(api_router.apis_router)
router.include_router(user_router.user_routers)