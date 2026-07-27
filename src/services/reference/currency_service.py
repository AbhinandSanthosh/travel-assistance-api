from sqlalchemy.orm import Session

from src.exceptions.currency import (
    CurrencyAlreadyExistsError,
    CurrencyNotFoundError,
)
from src.models.reference.currency import Currency
from src.repositories.reference.currency_repository import CurrencyRepository
from src.schemas.reference.currency import (
    CurrencyCreate,
    CurrencyUpdate,
)
from src.services.base_crud_service import BaseCrudService

class CurrencyService:
    """Service layer for Currency."""

    def __init__(
        self,
        currency_repository: CurrencyRepository,
    ):
        self.currency_repository = currency_repository
        self.base_crud = BaseCrudService(currency_repository)

    def create_currency(
        self,
        db: Session,
        currency_data: CurrencyCreate,
    ) -> Currency:
        """Create a new currency."""

        existing_code = self.currency_repository.get_by_code(
            db,
            currency_data.currency_code,
        )
        if existing_code:
            raise CurrencyAlreadyExistsError(
                "currency_code",
                currency_data.currency_code,
            )

        existing_name = self.currency_repository.get_by_name(
            db,
            currency_data.currency_name,
        )
        if existing_name:
            raise CurrencyAlreadyExistsError(
                "currency_name",
                currency_data.currency_name,
            )

        return self.base_crud.create(
            db=db,
            model=Currency,
            data=currency_data,
        )

    def get_currency(
        self,
        db: Session,
        currency_id: int,
    ) -> Currency:
        """Get a currency by ID."""

        currency = self.base_crud.get_by_id(
            db=db,
            obj_id=currency_id,
        )

        if not currency:
            raise CurrencyNotFoundError(currency_id)

        return currency

    def get_all_currencies(
        self,
        db: Session,
    ) -> list[Currency]:
        """Get all currencies."""

        return self.base_crud.get_all(db)

    def update_currency(
        self,
        db: Session,
        currency_id: int,
        currency_data: CurrencyUpdate,
    ) -> Currency:
        """Update a currency."""

        currency = self.base_crud.get_by_id(
            db=db,
            obj_id=currency_id,
        )

        if not currency:
            raise CurrencyNotFoundError(currency_id)

        update_data = currency_data.model_dump(
            exclude_unset=True,
        )

        if (
            "currency_code" in update_data
            and update_data["currency_code"] != currency.currency_code
        ):
            existing = self.currency_repository.get_by_code(
                db,
                update_data["currency_code"],
            )

            if existing:
                raise CurrencyAlreadyExistsError(
                    "currency_code",
                    update_data["currency_code"],
                )

        if (
            "currency_name" in update_data
            and update_data["currency_name"] != currency.currency_name
        ):
            existing = self.currency_repository.get_by_name(
                db,
                update_data["currency_name"],
            )

            if existing:
                raise CurrencyAlreadyExistsError(
                    "currency_name",
                    update_data["currency_name"],
                )

        return self.base_crud.update(
            db=db,
            obj=currency,
            data=currency_data,
        )

    def delete_currency(
        self,
        db: Session,
        currency_id: int,
    ) -> None:
        """Delete a currency."""

        currency = self.base_crud.get_by_id(
            db=db,
            obj_id=currency_id,
        )

        if not currency:
            raise CurrencyNotFoundError(currency_id)

        self.base_crud.delete(
            db=db,
            obj=currency,
        )

