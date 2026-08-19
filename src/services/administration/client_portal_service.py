import re
import secrets
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from src.core.api_key import (
    generate_api_key,
    hash_api_key,
    key_display_parts,
)
from src.core.jwt import create_access_token
from src.core.security import hash_password, verify_password
from src.enums.subscription_plan import SubscriptionPlan
from src.exceptions.administration.client_portal import (
    ClientAlreadyRegisteredError,
    ClientPortalAccountInactiveError,
    InvalidClientCredentialsError,
)
from src.models.administration.api_client import APIClient
from src.models.administration.client_ip_whitelist import (
    ClientIPWhitelist,
)
from src.repositories.administration.api_client import APIClientRepository
from src.repositories.administration.client_ip_whitelist import (
    ClientIPWhitelistRepository,
)
from src.schemas.administration.client_portal import (
    APIKeyStatusResponse,
    ClientSignupRequest,
    GeneratedAPIKeyResponse,
)


_SIGNUP_PLAN = SubscriptionPlan.STANDARD
_SIGNUP_REQUESTS_PER_MINUTE = 30



PORTAL_TOKEN_TYPE = "client_portal"  

_SLUG_RE = re.compile(r"[^A-Z0-9]+")


class ClientPortalService:
    """Signup / login / API-key lifecycle for the client self-service
    portal.
    """

    def __init__(
        self,
        repository: APIClientRepository,
        whitelist_repository: ClientIPWhitelistRepository,
    ) -> None:
        self.repository = repository
        self.whitelist_repository = whitelist_repository

    # ------------------------------------------------------------------
    # Signup / login
    # ------------------------------------------------------------------

    def signup(
        self,
        db: Session,
        payload: ClientSignupRequest,
    ) -> APIClient:
        existing = self.repository.get_by_contact_email(
            db,
            payload.contact_email,
        )

        if existing is not None:
            raise ClientAlreadyRegisteredError(
                payload.contact_email,
            )

        client = APIClient(
            client_name=payload.client_name,
            company_name=payload.company_name,
            client_code=self._generate_unique_client_code(
                db,
                payload.company_name,
            ),
            api_key=None,
            contact_name=payload.client_name,
            contact_email=payload.contact_email,
            contact_phone=payload.contact_phone,
            contact_password_hash=hash_password(
                payload.password,
            ),
            subscription_plan=_SIGNUP_PLAN,
            requests_per_minute=_SIGNUP_REQUESTS_PER_MINUTE,
            status=True,
        )

        return self.repository.create(
            db=db,
            obj=client,
        )

    def login(
        self,
        db: Session,
        contact_email: str,
        password: str,
    ) -> APIClient:
        client = self.repository.get_by_contact_email(
            db,
            contact_email,
        )

        if client is None or client.contact_password_hash is None:
            raise InvalidClientCredentialsError()

        if not verify_password(
            password,
            client.contact_password_hash,
        ):
            raise InvalidClientCredentialsError()

        if not client.status:
            raise ClientPortalAccountInactiveError()

        return client

    def issue_portal_token(
        self,
        client: APIClient,
    ) -> tuple[str, int]:
        return create_access_token(
            subject=str(client.id),
            extra_claims={
                "type": PORTAL_TOKEN_TYPE,
                "contact_email": client.contact_email,
            },
        )

    # ------------------------------------------------------------------
    # API key lifecycle
    # ------------------------------------------------------------------

    def generate_api_key(
        self,
        db: Session,
        client: APIClient,
        client_ip: str | None = None,
    ) -> GeneratedAPIKeyResponse:
        """Issue a new live API key.

        The plaintext API key is returned only once.

        The IP address used to generate the API key is automatically
        added to the client's IP whitelist if it is not already present.
        """

        plain_key = generate_api_key()
        prefix, last_four = key_display_parts(plain_key)
        now = datetime.now(UTC)

        # --------------------------------------------------------------
        # 1. Store API key hash
        # --------------------------------------------------------------

        client.api_key_hash = hash_api_key(plain_key)
        client.api_key_prefix = prefix
        client.api_key_last_four = last_four
        client.api_key_created_at = now
        client.api_key_revoked_at = None

        self.repository.save(
            db=db,
            obj=client,
        )

        # --------------------------------------------------------------
        # 2. Automatically whitelist the IP that generated the key
        # --------------------------------------------------------------

        if client_ip:
            existing_entries = (
                self.whitelist_repository.get_by_client_id(
                    db=db,
                    client_id=client.id,
                )
            )

            matching_entry = next(
                (
                    entry
                    for entry in existing_entries
                    if entry.ip_address == client_ip
                    and entry.active
                ),
                None,
            )

            if matching_entry is None:
                whitelist_entry = ClientIPWhitelist(
                    client_id=client.id,
                    ip_address=client_ip,
                    cidr_range=None,
                    description=(
                        "Automatically added during "
                        "API key generation"
                    ),
                    is_primary=len(existing_entries) == 0,
                    active=True,
                )

                self.whitelist_repository.create(
                    db=db,
                    obj=whitelist_entry,
                )

        # --------------------------------------------------------------
        # 3. Return plaintext API key once
        # --------------------------------------------------------------

        return GeneratedAPIKeyResponse(
            api_key=plain_key,
            prefix=prefix,
            last_four=last_four,
            created_at=now,
        )

    def revoke_api_key(
        self,
        db: Session,
        client: APIClient,
    ) -> None:
        """Revoke the client's current API key."""

        client.api_key_revoked_at = datetime.now(UTC)
        client.api_key_hash = None

        self.repository.save(
            db=db,
            obj=client,
        )

    def get_api_key_status(
        self,
        client: APIClient,
    ) -> APIKeyStatusResponse:
        """Return masked API key status."""

        if not client.api_key_hash:
            return APIKeyStatusResponse(
                has_active_key=False,
            )

        masked = (
            f"{client.api_key_prefix}..."
            f"{client.api_key_last_four}"
        )

        return APIKeyStatusResponse(
            has_active_key=True,
            masked_key=masked,
            created_at=client.api_key_created_at,
            revoked_at=client.api_key_revoked_at,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _generate_unique_client_code(
        self,
        db: Session,
        company_name: str,
    ) -> str:
        base = (
            _SLUG_RE.sub(
                "",
                company_name.upper(),
            )[:12]
            or "CLIENT"
        )

        for _ in range(10):
            candidate = (
                f"{base}{secrets.token_hex(3).upper()}"
            )

            if (
                self.repository.get_by_client_code(
                    db,
                    candidate,
                )
                is None
            ):
                return candidate

        raise RuntimeError(
            "Could not generate a unique client_code."
        )