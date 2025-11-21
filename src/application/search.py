from fastapi import APIRouter
from src.application.io_application.search import SearchApplicationInput
from src.domain.usecase.io_usecase.search import SearchUseCaseInput
from src.domain import search_use_case

router = APIRouter(prefix="/v1", tags=["Search"])

@router.post("/search")
async def search(request: SearchApplicationInput):
    input = SearchUseCaseInput(message=request.message)
    return await search_use_case.execute(input=input)