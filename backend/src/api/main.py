from fastapi import APIRouter

from src.api.routes import users, wishes

api_router = APIRouter()
api_router.include_router(users.router, tags=["users"])
api_router.include_router(wishes.router, tags=["wishes"])
