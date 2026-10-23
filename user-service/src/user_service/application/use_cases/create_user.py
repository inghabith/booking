from user_service.application.dtos import CreateUserCommand
from user_service.domain.entities.user import User
from user_service.domain.exceptions import UserAlreadyExistsError
from user_service.domain.repositories.user_repository import UserRepository


class CreateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, command: CreateUserCommand) -> User:
        # La entidad valida sus invariantes al construirse.
        user = User(
            name=command.name,
            email=command.email,
            identification_type=command.identification_type,
            identification_number=command.identification_number,
            birthday_date=command.birthday_date,
        )

        # Reglas que necesitan consultar otros usuarios: viven en el caso de uso.
        if self.user_repository.get_by_email(user.email):
            raise UserAlreadyExistsError(f"Ya existe un usuario con el email {user.email}")

        if self.user_repository.get_by_identification(
            user.identification_type, user.identification_number
        ):
            raise UserAlreadyExistsError("Ya existe un usuario con esa identificación")

        return self.user_repository.add(user)
