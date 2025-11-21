from fastapi import APIRouter
from src.application.search import router as search_router

router = APIRouter()

router.include_router(search_router)

