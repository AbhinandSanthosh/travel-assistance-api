from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.api_client import APIClient
from src.repositories.base_repository import BaseRepository


class APIClientRepository(BaseRepository[APIClient]):
    """Repository for API Client."""

    def __init__(self) -> None:
        super().__init__(APIClient)

    def get_by_client_code(
        self,
        db: Session,
        client_code: str,
    ) -> APIClient | None:
        """Return an API client by client code."""

        return db.scalar(
            select(APIClient).where(
                APIClient.client_code == client_code,
            )
        )

    def get_by_api_key(
        self,
        db: Session,
        api_key: str,
    ) -> APIClient | None:
        """Return an API client by API key."""

        return db.scalar(
            select(APIClient).where(
                APIClient.api_key == api_key,
            )
        )