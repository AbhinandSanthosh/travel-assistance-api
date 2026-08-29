from sqlalchemy.orm import Session

from src.exceptions.administration.api_client import (
    APIClientAlreadyExistsError,
    APIClientNotFoundError,
)
from src.models.administration.api_client import APIClient
from src.repositories.administration.api_client import (
    APIClientRepository,
)
from src.schemas.administration.api_client import (
    APIClientCreate,
    APIClientUpdate,
)
from src.services.base_crud_service import BaseCrudService


class APIClientService:
    """Service for API Client."""

    def __init__(
        self,
        repository: APIClientRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_api_client(
        self,
        db: Session,
        client_data: APIClientCreate,
    ) -> APIClient:
        """Create an API client."""

        existing_client = self.repository.get_by_client_code(
            db=db,
            client_code=client_data.client_code,
        )

        if existing_client:
            raise APIClientAlreadyExistsError(
                client_data.client_code,
            )

        return self.base_crud.create(
            db=db,
            model=APIClient,
            data=client_data,
        )

    def get_api_client(
        self,
        db: Session,
        client_id: int,
    ) -> APIClient:
        """Return an API client by ID."""

        client = self.base_crud.get_by_id(
            db=db,
            obj_id=client_id,
        )

        if client is None:
            raise APIClientNotFoundError(client_id)

        return client

    def get_all_api_clients(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[APIClient]:
        """Return all API clients."""

        return self.base_crud.get_all(db=db, skip=skip, limit=limit)

    def update_api_client(
        self,
        db: Session,
        client_id: int,
        client_data: APIClientUpdate,
    ) -> APIClient:
        """Update an API client."""

        client = self.get_api_client(
            db=db,
            client_id=client_id,
        )

        if (
            client_data.client_code is not None
            and client_data.client_code != client.client_code
        ):
            existing_client = self.repository.get_by_client_code(
                db=db,
                client_code=client_data.client_code,
            )

            if existing_client:
                raise APIClientAlreadyExistsError(
                    client_data.client_code,
                )

        return self.base_crud.update(
            db=db,
            obj=client,
            data=client_data,
        )

    def delete_api_client(
        self,
        db: Session,
        client_id: int,
    ) -> None:
        """Delete an API client."""

        client = self.get_api_client(
            db=db,
            client_id=client_id,
        )

        self.base_crud.delete(
            db=db,
            obj=client,
        )