from sqlalchemy.orm import Session

from src.exceptions.administration.client_ip_whitelist import (
    ClientIPWhitelistNotFoundError,
    InvalidWhitelistEntryError,
)
from src.models.administration.client_ip_whitelist import (
    ClientIPWhitelist,
)
from src.repositories.administration.client_ip_whitelist import (
    ClientIPWhitelistRepository,
)
from src.schemas.administration.client_ip_whitelist import (
    ClientIPWhitelistCreate,
    ClientIPWhitelistUpdate,
)
from src.services.base_crud_service import BaseCrudService


class ClientIPWhitelistService:
    """Service for Client IP Whitelist."""

    def __init__(
        self,
        repository: ClientIPWhitelistRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_client_ip_whitelist(
        self,
        db: Session,
        whitelist_data: ClientIPWhitelistCreate,
    ) -> ClientIPWhitelist:
        """Create a client IP whitelist entry."""

        if (
            whitelist_data.ip_address is None
            and whitelist_data.cidr_range is None
        ):
            raise InvalidWhitelistEntryError()

        return self.base_crud.create(
            db=db,
            model=ClientIPWhitelist,
            data=whitelist_data,
        )

    def get_client_ip_whitelist(
        self,
        db: Session,
        whitelist_id: int,
    ) -> ClientIPWhitelist:
        """Return a client IP whitelist entry by ID."""

        whitelist = self.base_crud.get_by_id(
            db=db,
            obj_id=whitelist_id,
        )

        if whitelist is None:
            raise ClientIPWhitelistNotFoundError(
                whitelist_id,
            )

        return whitelist

    def get_all_client_ip_whitelists(
        self,
        db: Session,
    ) -> list[ClientIPWhitelist]:
        """Return all client IP whitelist entries."""

        return self.base_crud.get_all(db=db)

    def get_client_whitelist_entries(
        self,
        db: Session,
        client_id: int,
    ) -> list[ClientIPWhitelist]:
        """Return whitelist entries for an API client."""

        return self.repository.get_by_client_id(
            db=db,
            client_id=client_id,
        )

    def update_client_ip_whitelist(
        self,
        db: Session,
        whitelist_id: int,
        whitelist_data: ClientIPWhitelistUpdate,
    ) -> ClientIPWhitelist:
        """Update a client IP whitelist entry."""

        whitelist = self.get_client_ip_whitelist(
            db=db,
            whitelist_id=whitelist_id,
        )

        ip_address = (
            whitelist_data.ip_address
            if whitelist_data.ip_address is not None
            else whitelist.ip_address
        )

        cidr_range = (
            whitelist_data.cidr_range
            if whitelist_data.cidr_range is not None
            else whitelist.cidr_range
        )

        if ip_address is None and cidr_range is None:
            raise InvalidWhitelistEntryError()

        return self.base_crud.update(
            db=db,
            obj=whitelist,
            data=whitelist_data,
        )

    def delete_client_ip_whitelist(
        self,
        db: Session,
        whitelist_id: int,
    ) -> None:
        """Delete a client IP whitelist entry."""

        whitelist = self.get_client_ip_whitelist(
            db=db,
            whitelist_id=whitelist_id,
        )

        self.base_crud.delete(
            db=db,
            obj=whitelist,
        )