from fastapi import APIRouter, Depends, status

from src.api.dependencies.data_collection import (
    get_ai_extraction_service,
)
from src.models.data_collection.ai_extraction import (
    AIExtraction,
)
from src.schemas.data_collection.ai_extraction import (
    AIExtractionCreate,
    AIExtractionResponse,
    AIExtractionUpdate,
)
from src.services.data_collection.ai_extraction import (
    AIExtractionService,
)

router = APIRouter(
    prefix="/ai-extractions",
    tags=["AI Extractions"],
)


@router.post(
    "/",
    response_model=AIExtractionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ai_extraction(
    data: AIExtractionCreate,
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> AIExtraction:
    return await service.create_ai_extraction(data)


@router.get(
    "/",
    response_model=list[AIExtractionResponse],
)
async def get_ai_extractions(
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> list[AIExtraction]:
    return await service.get_ai_extractions()


@router.get(
    "/{extraction_id}",
    response_model=AIExtractionResponse,
)
async def get_ai_extraction(
    extraction_id: int,
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> AIExtraction:
    return await service.get_ai_extraction(
        extraction_id,
    )


@router.put(
    "/{extraction_id}",
    response_model=AIExtractionResponse,
)
async def update_ai_extraction(
    extraction_id: int,
    data: AIExtractionUpdate,
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> AIExtraction:
    return await service.update_ai_extraction(
        extraction_id,
        data,
    )


@router.delete(
    "/{extraction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ai_extraction(
    extraction_id: int,
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> None:
    await service.delete_ai_extraction(
        extraction_id,
    )