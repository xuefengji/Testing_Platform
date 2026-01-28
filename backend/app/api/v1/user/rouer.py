from fastapi import APIRouter
from app.api.v1.user import auth

user_routers = APIRouter()
user_routers.include_router(auth.auth_router)

