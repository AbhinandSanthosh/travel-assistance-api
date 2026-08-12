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
        """Return an API client by legacy plaintext API key.

        Only ever matches pre-portal, seeded/demo clients -- new
        clients never populate this column. See get_by_api_key_hash
        for the current lookup path.
        """

        return db.scalar(
            select(APIClient).where(
                APIClient.api_key == api_key,
            )
        )

    def get_by_api_key_hash(
        self,
        db: Session,
        api_key_hash: str,
    ) -> APIClient | None:
        """Return an API client by hashed (SHA-256) API key."""

        return db.scalar(
            select(APIClient).where(
                APIClient.api_key_hash == api_key_hash,
            )
        )

    def get_by_contact_email(
        self,
        db: Session,
        contact_email: str,
    ) -> APIClient | None:
        """Return an API client by contact/portal-login email."""

        return db.scalar(
            select(APIClient).where(
                APIClient.contact_email == contact_email,
            )
        )