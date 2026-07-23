from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.deps import get_currency_service
from src.db.session import get_db
from src.schemas.reference.currency import (
    CurrencyCreate,
    CurrencyResponse,
    CurrencyUpdate,
)
from src.services.reference.currency_service import CurrencyService

router = APIRouter(
    prefix="/currencies",
    tags=["Currencies"],
)


@router.post(
    "",
    response_model=CurrencyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_currency(
    currency_data: CurrencyCreate,
    db: Session = Depends(get_db),
    service: CurrencyService = Depends(get_currency_service),
):
    return service.create_currency(db, currency_data)


@router.get(
    "",
    response_model=list[CurrencyResponse],
)
def get_all_currencies(
    db: Session = Depends(get_db),
    service: CurrencyService = Depends(get_currency_service),
):
    return service.get_all_currencies(db)


@router.get(
    "/{currency_id}",
    response_model=CurrencyResponse,
)
def get_currency(
    currency_id: int,
    db: Session = Depends(get_db),
    service: CurrencyService = Depends(get_currency_service),
):
    return service.get_currency(db, currency_id)


@router.put(
    "/{currency_id}",
    response_model=CurrencyResponse,
)
def update_currency(
    currency_id: int,
    currency_data: CurrencyUpdate,
    db: Session = Depends(get_db),
    service: CurrencyService = Depends(get_currency_service),
):
    return service.update_currency(
        db,
        currency_id,
        currency_data,
    )


@router.delete(
    "/{currency_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_currency(
    currency_id: int,
    db: Session = Depends(get_db),
    service: CurrencyService = Depends(get_currency_service),
):
    service.delete_currency(db, currency_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)