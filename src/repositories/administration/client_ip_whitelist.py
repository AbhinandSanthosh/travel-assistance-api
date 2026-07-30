from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.client_ip_whitelist import (
    ClientIPWhitelist,
)
from src.repositories.base_repository import BaseRepository


class ClientIPWhitelistRepository(
    BaseRepository[ClientIPWhitelist]
):
    """Repository for Client IP Whitelist."""

    def __init__(self) -> None:
        super().__init__(ClientIPWhitelist)

    def get_by_client_id(
        self,
        db: Session,
        client_id: int,
    ) -> list[ClientIPWhitelist]:
        """Return all whitelist entries for an API client."""

        return list(
            db.scalars(
                select(ClientIPWhitelist).where(
                    ClientIPWhitelist.client_id == client_id,
                )
            ).all()
        )