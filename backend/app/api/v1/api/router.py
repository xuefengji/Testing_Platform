from fastapi import APIRouter
from app.api.v1.api import api_folders, api_endpoints

apis_router = APIRouter()
apis_router.include_router(api_endpoints.api_endpoint_router)
apis_router.include_router(api_folders.api_folders_router)
