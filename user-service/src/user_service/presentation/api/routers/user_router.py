"""Router: adapta HTTP -> DTO -> caso de uso. Sin reglas de negocio ni SQL."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from user_service.application.dtos import CreateUserCommand
from user_service.application.use_cases.create_user import CreateUser
from user_service.application.use_cases.get_user import GetUser
from user_service.application.use_cases.list_users import ListUsers
from user_service.domain.entities.user import User
from user_service.presentation.api.dependencies import (
    get_create_user,
    get_get_user,
    get_list_users,
)
from user_service.presentation.api.schemas.user_schemas import (
    UserCreateRequest,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201)
def create_user(
    payload: UserCreateRequest, use_case: CreateUser = Depends(get_create_user)
) -> UserResponse:
    command = CreateUserCommand(**payload.model_dump())
    return to_response(use_case.execute(command))


@router.get("")
def list_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    use_case: ListUsers = Depends(get_list_users),
) -> list[UserResponse]:
    return [to_response(user) for user in use_case.execute(limit, offset)]


@router.get("/{user_id}")
def get_user(user_id: UUID, use_case: GetUser = Depends(get_get_user)) -> UserResponse:
    return to_response(use_case.execute(user_id))


def to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        identification_type=user.identification_type,
        identification_number=user.identification_number,
        birthday_date=user.birthday_date,
        created_at=user.created_at,
    )
