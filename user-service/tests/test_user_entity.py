from datetime import date, timedelta

import pytest

from user_service.domain.entities.user import IdentificationType, User
from user_service.domain.exceptions import InvalidUserError


def make_user(**overrides):
    data = dict(
        name="Ana Pérez",
        email="ANA@Mail.com",
        identification_type=IdentificationType.CC,
        identification_number="1001",
        birthday_date=date(1999, 5, 1),
    )
    data.update(overrides)
    return User(**data)


def test_normaliza_email():
    assert make_user().email == "ana@mail.com"


def test_nombre_vacio_falla():
    with pytest.raises(InvalidUserError):
        make_user(name="   ")


def test_fecha_de_nacimiento_futura_falla():
    with pytest.raises(InvalidUserError):
        make_user(birthday_date=date.today() + timedelta(days=1))
