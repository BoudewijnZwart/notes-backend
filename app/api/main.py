from fastapi import APIRouter

from app.api.routes import folders, notes, tags, users

api_router = APIRouter()

api_router.include_router(notes.router)
api_router.include_router(folders.router)
api_router.include_router(tags.router)
api_router.include_router(users.router)
