from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_user_service,
)
from src.db.session import get_db

from src.schemas.administration.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)

from src.services.administration.user import (
    UserService,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user."""
    return service.create_user(
        db,
        user_data,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_all_users(
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    """Retrieve all users."""
    return service.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Retrieve a user by ID."""
    return service.get_user(
        db,
        user_id,
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update an existing user."""
    return service.update_user(
        db=db,
        user_id=user_id,
        user_data=user_data,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
) -> Response:
    """Delete a user."""
    service.delete_user(
        db,
        user_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )