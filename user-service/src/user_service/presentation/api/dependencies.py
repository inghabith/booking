"""Composition root: el único lugar que decide qué adaptador concreto se usa."""
from fastapi import Depends

from user_service.application.use_cases.create_user import CreateUser
from user_service.application.use_cases.get_user import GetUser
from user_service.application.use_cases.list_users import ListUsers
from user_service.domain.repositories.user_repository import UserRepository
from user_service.infrastructure.database.session import get_session
from user_service.infrastructure.persistence.repositories.sqlmodel_user_repository import (
    SQLModelUserRepository,
)


# scope="function": el commit se ejecuta ANTES de enviar la respuesta.
def get_user_repository(session=Depends(get_session, scope="function")) -> UserRepository:
    return SQLModelUserRepository(session)


def get_create_user(repository=Depends(get_user_repository)) -> CreateUser:
    return CreateUser(repository)


def get_get_user(repository=Depends(get_user_repository)) -> GetUser:
    return GetUser(repository)


def get_list_users(repository=Depends(get_user_repository)) -> ListUsers:
    return ListUsers(repository)
