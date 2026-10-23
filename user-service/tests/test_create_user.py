from datetime import date

import pytest

from tests.fakes import InMemoryUserRepository
from user_service.application.dtos import CreateUserCommand
from user_service.application.use_cases.create_user import CreateUser
from user_service.domain.entities.user import IdentificationType
from user_service.domain.exceptions import UserAlreadyExistsError


def command(**overrides):
    data = dict(
        name="Ana",
        email="ana@mail.com",
        identification_type=IdentificationType.CC,
        identification_number="1001",
        birthday_date=date(1999, 5, 1),
    )
    data.update(overrides)
    return CreateUserCommand(**data)


def test_crea_usuario():
    repo = InMemoryUserRepository()
    user = CreateUser(repo).execute(command())
    assert repo.get_by_id(user.id) is user


def test_email_duplicado_falla():
    repo = InMemoryUserRepository()
    CreateUser(repo).execute(command())
    with pytest.raises(UserAlreadyExistsError):
        CreateUser(repo).execute(command(identification_number="2002"))


def test_identificacion_duplicada_falla():
    repo = InMemoryUserRepository()
    CreateUser(repo).execute(command())
    with pytest.raises(UserAlreadyExistsError):
        CreateUser(repo).execute(command(email="otra@mail.com"))
