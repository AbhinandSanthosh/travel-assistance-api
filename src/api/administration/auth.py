from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.auth import get_current_user
from src.core.jwt import create_access_token
from src.core.security import verify_password
from src.db.session import get_db
from src.exceptions.administration.auth import (
    InactiveUserError,
    InvalidCredentialsError,
)
from src.models.administration.user import User
from src.repositories.administration.user import UserRepository
from src.schemas.administration.auth import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Admin Auth"],
)

_user_repository = UserRepository()


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Admin/Compliance Officer login (JWT)",
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """Authenticate an administrative user (username/email + password)
    and issue a short-lived JWT for accessing the Admin APIs.

    API clients (airlines, booking platforms, etc.) do NOT use this
    endpoint -- they authenticate to /autocheck with an X-API-Key.
    """

    user = _user_repository.get_by_username(db, payload.username)
    if user is None:
        user = _user_repository.get_by_email(db, payload.username)

    if user is None or not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise InvalidCredentialsError()

    if not user.status:
        raise InactiveUserError()

    token, expires_in = create_access_token(
        subject=str(user.id),
        extra_claims={
            "username": user.username,
            "role_id": user.role_id,
        },
    )

    return LoginResponse(access_token=token, expires_in=expires_in)


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated admin user",
)
def read_current_user(
    user: User = Depends(get_current_user),
) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role_id=user.role_id,
        role_name=user.role.role_name,
    )
