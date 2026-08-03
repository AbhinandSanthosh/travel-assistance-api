from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.data_collection import (
    get_ai_extraction_service,
)
from src.db.session import get_db
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
def create_ai_extraction(
    data: AIExtractionCreate,
    db: Session = Depends(get_db),
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> AIExtraction:
    return service.create_ai_extraction(
        db=db,
        data=data,
    )


@router.get(
    "/",
    response_model=list[AIExtractionResponse],
)
def get_ai_extractions(
    db: Session = Depends(get_db),
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> list[AIExtraction]:
    return service.get_ai_extractions(
        db=db,
    )


@router.get(
    "/{extraction_id}",
    response_model=AIExtractionResponse,
)
def get_ai_extraction(
    extraction_id: int,
    db: Session = Depends(get_db),
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> AIExtraction:
    return service.get_ai_extraction(
        db=db,
        extraction_id=extraction_id,
    )


@router.put(
    "/{extraction_id}",
    response_model=AIExtractionResponse,
)
def update_ai_extraction(
    extraction_id: int,
    data: AIExtractionUpdate,
    db: Session = Depends(get_db),
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> AIExtraction:
    return service.update_ai_extraction(
        db=db,
        extraction_id=extraction_id,
        data=data,
    )


@router.delete(
    "/{extraction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ai_extraction(
    extraction_id: int,
    db: Session = Depends(get_db),
    service: AIExtractionService = Depends(
        get_ai_extraction_service,
    ),
) -> None:
    service.delete_ai_extraction(
        db=db,
        extraction_id=extraction_id,
    )